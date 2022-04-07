- Paper : https://dl.acm.org/doi/10.1145/3460231.3474236
- Authors : [[Minmin Chen]], [[Yuyan Wang]], [[Can Xu]], [[Ya Le]],[[ Mohit Sharma]], [[Lee Richardson]], [[Su-Lin Wu]], [[Ed Chi]]
- Reviewer : [[andrew.y@kakaocorp.com]]
- Topics
	- #Metrics_and_Evaluation 
	- #RecSys2021 

### Summary
- 강화학습 기반 추천 시스템에서 exploration이 어떤 영향을 미치는지 알아보고 user exploration을 추가하는 methodology를 소개한 논문입니다.
- Accuracy, diversity, novelty, serendipity를 측정하고, 오프라인과 온라인 실험을 통해 exploration의 영향을 분석하였습니다.

### Approach
#### 배경
논문은 REINFORCE 추천 시스템을 베이스로 사용합니다. ([참고 논문](https://arxiv.org/abs/1812.02353))
- 용어 정리
	<img src= "https://github.daumkakao.com/storage/user/7666/files/51f04286-bcd6-41c1-a632-4b85c0f36dd1" width = "300"> 
	- 유저의 히스토리 up to time t, A_t = set of item recommended at time t, a = item user interacted with, r = reward
	- u_s_t = RNN_theta(H_t) → latent user state (s_t = user state)
	- v_a = embedding of item a
- Softmax Policy over item corpus given the latent user state
	<img src= "https://github.daumkakao.com/storage/user/7666/files/31aaca00-4c6f-11ec-8542-45b56f892d67" width = "300">
	- 여기서 policy parameters θ가 밑의 수식을 (expected culumative reward) 최대화 하게 학습을 합니다.
		<img src= "https://github.daumkakao.com/storage/user/7666/files/489dec00-4c70-11ec-96c7-6e8a9daffa60" width = "400"> 
		<img src= "https://github.daumkakao.com/storage/user/7666/files/5bb0bc00-4c70-11ec-8a97-06b50252ee64" width = "300">
	- 이 학습된 softmax policy를 사용해서 time t에 set of recommendation A_t생성해서 A_t를 유저한테 추천합니다.

#### User Exploration 활성화 하는 방법
##### Entropy Regularization
policy π_θ (·|s)를 entropy가 높은 output distribution으로 유도해서 유저 관심사 밖 콘텐츠를 추천하는걸 더 활성화 시킵니다. (user exploration 활성화)
<img src= "https://github.daumkakao.com/storage/user/7666/files/42f4d600-4c71-11ec-9a58-7bd063b5b2c8" width = "250"> 
<img src= "https://github.daumkakao.com/storage/user/7666/files/ad0d7b00-4c71-11ec-9f55-3bb20ad19c56" width = "300">
- entropy는 negative reverse KL divergence of the conditional distribution π_θ (·|s) to the uniform distribution. (uniform distribution과 얼마나 비슷한지)
- entropy를 높이면 높일수록 학습된 policy는 uniform distribution이 된다. (선호도와 상관 없이 공평하게 추천된다)

##### Intrinsic Motivation and Reward Shaping
<img src= "https://github.daumkakao.com/storage/user/7666/files/7be27a00-4c74-11ec-8647-15df9765384d" width = "400">
<img src= "https://github.daumkakao.com/storage/user/7666/files/edc9d0fe-e71e-451f-bbd1-3d263377771d" width = "350">
- 위 policy 수식의 r(s,a) reward function (유저 s에게 a를 추천하는 immediate value)에서 intrinsic reward를 추가합니다.
- 유저가 소비한 아이템의 리스트가 있을때 유저가 막 소비한 아이템이 이전 아이템들이랑 많이 다르면 reward를 높게 합니다.
- multiplication인 이유는 relevance를 유지하기 위해서 (R_t^e (s_t , a_t ) = 0는 계속 0)입니다.
- 유저에게 더 좋은 user experience를 주는 surprising한 (과거 소비 아이템이랑 다른) 아이템에게 reward를 많이 줍니다.
- unknown interest는 아이템의 클러스터가 유저가 이미 소비한 클러스터가 아닌 경우를 의미합니다. (i.e. different topic, different provider)

##### Actionable Representation for Exploration
- 유저가 surprising한 아이템을 소비해서 리워드를 높게 받은 상태면, 다음에는 다르게 interact할수있게 유저 피쳐에 반영을 해야합니다.
- 따라서 유저 피쳐 (유저 히스토리)에 surprise랑 relevance를 추가합니다.
	<img src= "https://github.daumkakao.com/storage/user/7666/files/f3095164-c2ac-4d8f-b1de-b27eb69b2b38" width = "300">, i_t = 1 if topic/provider cluster different, r_t (reward) > 0 (relevance)

#### 측정 방법 
##### Accuracy
- mean average precision at K = 50 (밑의 수식에서는 j) ([참고 논문](https://www.cs.cornell.edu/people/tj/publications/yue_etal_07a.pdf))
<img src= "https://github.daumkakao.com/storage/user/7666/files/bf437de3-8b8a-491a-ae6b-db867dc4dba3" width = "450">

##### Diversity
<img src= "https://github.daumkakao.com/storage/user/7666/files/15605a80-4c7a-11ec-9698-d5cec4df3398" width = "450">
- 직관적인 수식입니다. uniform에서는 sim(i,j)는 1이니까 diversity는 0, sim(i,j)가 낮으면 낮을수록 diversity가 올라가게 됩니다.

##### Novelty
<img src= "https://github.daumkakao.com/storage/user/7666/files/45f4c400-4c7b-11ec-9c4b-5fadd921f1db" width = "350">
- I(a)= − log (# users consumed item a) + const
- globally 덜 popular 한 아이템 (모두가 좋아하지 않는 아이템)을 학습해서 추천하면 더 novel하다고 봅니다.

##### Serendipity
<img src= "https://github.daumkakao.com/storage/user/7666/files/24480c80-4c7c-11ec-8f01-88b003b80666" width = "450">
<img src= "https://github.daumkakao.com/storage/user/7666/files/2c07b100-4c7c-11ec-9cb7-29d33c0b6d89" width = "450">
- 위에 언급한 surprise + relevance를 둘다 챙기면 1, 아니면 0로 둡니다.
- 유저가 소비하는 주류 아이템이 아닌 관심있는 아이템이 있는지 quanitify 하는 metric입니다.

##### Long Term User Experience
- 결국엔 exploration이 long term user experience에는 도움이 될것인지 알려면 이거에 대한 측정 방법도 있어야 합니다.
- 논문에서는 유저가 다시 서비스를 쓰는지, 그리고 활동량이 적은 유저들이 활동량이 많은 유저로 변하는지를 보고 long term user experience를 판단합니다.

### Results
#### 오프라인 실험 결과 및 분석
![image](https://github.daumkakao.com/storage/user/7666/files/09c26300-4c7d-11ec-8988-fa5138373f7f)
- 무슨 데이터셋을 썻는지 정확히 언급은 하고 있지 않습니다. ("a billion user trajectories from a commercial recommendation platform")
- item space = most popular 10 million items in the past 48 hours on the platform
- 99% training, 1% validation

##### Entropy Regularization
- as α ↑, diversity ↑, novelty ↑ at cost of accuracy ↓ + serendipity ↓ (due to loss of relevance)

##### Intrinsic Motivation
- 위의 c를 조정 가능하지만 이 페이퍼에서는 | I_t | 를 조정하기로 하였습니다.
- baseline 대비 diversity ↑ at cost of accuracy ↓, serendipity ↑, novelty - 의 성능을 보여주었습니다.
- d = 1, 7, 365에서는 큰 차이 없었습니다.
- In the datasets, the percentage is reduced from 36% → 19% → 12% when the window size is extended from 1 → 7 → 365 days. (서프라이징 한 state-action pair %)

##### Actionable Representation
- actionable representation만으로는 baseline과 비슷해서 intrinsic motivation이랑 같이 써야합니다.
- intrinsic motivation 대비 serendipity ↑
- mean input gate activation value차이 → RNN이 surprising event때 더 큰 업데이트를 합니다. → 유의미한 차이가 있습니다.
<img src= "https://github.daumkakao.com/storage/user/7666/files/e35075ae-b7f2-4403-bf81-d30ded0ab5cb" width = "600">

#### 온라인 실험 결과 및 분석
- 오프라인 실험과 데이터 크기는 비슷합니다.
	- "a industrial recommendation platform serving billions of users", "a corpus of 10 million"
![image](https://github.daumkakao.com/storage/user/7666/files/966d2100-4c7d-11ec-8b4d-825070434287)
	- entropy regularization (red: α = 0.1, blue: α = 0.5)
	- intrinsic motivation (d = 7, topic, c = 4)
	- user enjoyment improvement 어떻게 측정 했는지 안나와있습니다.
	- α = 0.1 → α = 0.5: lower user enjoyment improvement. 따라서 diversity ↑ novelty ↑은 better user experience를 가져오지 못한다고 볼 수 있습니다.
- Figure 3b, 3c에서는 user enjoyment이 improve했고 (baseline 대비) 오프라인 분석과 합쳐서 분석하면 serendipity ↑ 이 user experience를 더 좋게 만든다고 볼 수 있습니다.
	<img src= "https://github.daumkakao.com/storage/user/7666/files/d81f8d96-a177-44e9-88b4-b1e04e78553d" width = "300">
- Returning 유저도 더 많아졌습니다.

##### Long Term User Experience
![image](https://github.daumkakao.com/storage/user/7666/files/de2cbbd2-ac08-4a15-af33-f3b280849d76)
- 시간이 지날수록 exploration의 효과 (유저가 새로운 "interest"를 찾는거)가 있었습니다.

![image](https://github.daumkakao.com/storage/user/7666/files/b0a6ff00-4c7d-11ec-91c6-4d951e4e77b6)
- 실험 시작하기 전과 후를 비교한 a user activity level transition matrix입니다.
- 저 %가 어떻게 계산되는지는 불확실합니다. (개인적으로 이해 못함)
- casual → core conversion이 많았다 주장하고 있습니다.

### Conclusion
- serendipity가 long term user experience에 좋은 영향을 준다는 것을 밝혔습니다. 따라서 long term user experience를 높히기 위해서는 exploration을 해야하고, exploration이 serendipitous recommendation을 잘 해줘야 합니다.
