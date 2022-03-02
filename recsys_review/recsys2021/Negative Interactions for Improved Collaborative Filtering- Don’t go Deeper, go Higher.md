## Negative Interactions for Improved Collaborative Filtering: Don’t go Deeper, go Higher
- Paper : https://dl.acm.org/doi/pdf/10.1145/3460231.3474273
- Authors : [[Harald Steck]], [[Dawen Liang]]
- Reviewer : [[marv.20@kakaocorp.com]]
- Topics
	- [[Theory and Practice]]
	- [[Netflix]]
	- [[High-Order Interactions]]
	- [[_RecSys2021]]

### Summary
- Collaborative Filtering 모델에서 higher-order interaction을 어떻게 할 것인지에 대한 방법론을 새롭게 제안하고 있습니다. 
- Linear full-rank model을 통해 higher-order interaction을 넣을 수 있게 하였고, 그 결과 큰 데이터셋에서 딥러닝 기반 방법론들보다 좋은 성능을 보였습니다.

### Approach
이 논문이 다루는 모델은 SLIM -> EASE(Embarrassingly Shallow AutoEncoder) -> Pair(this paper) 순으로 발전시켰습니다. EASE와 이 논문에서 제안한 Pair만 보면 다음과 같습니다.

#### EASE 
- https://arxiv.org/abs/1905.03375
- hidden layer가 없는 autoencoder 모델입니다. 파라미터는 item-item weight matrix $B$입니다. objective는 다음과 같습니다. 이 때 X는 interaction matrix, F는 Frobenius norm을 의미합니다.
<img width="859" alt="Screen Shot 2022-02-10 at 2 52 09 PM" src="https://github.daumkakao.com/storage/user/6543/files/b678d0f8-612a-4028-aa83-f2ca787071b0">

- solution은 다음과 같습니다.
<img width="822" alt="Screen Shot 2022-02-10 at 2 52 16 PM" src="https://github.daumkakao.com/storage/user/6543/files/556b4d06-2075-4dca-8ad5-cd6754aad965">


#### Pair (this paper)
- Relation의 용어에 대한 설명은 다음과 같습니다.
	- pairwise($B_{ij}$ ) : 유저가 item i를 소비하였을 때, item j 의 선호 예측값을 의미합니다. 따라서 유저가 i랑 k를 소비 한다면, item j에 대한 선호도 예측값은 가 됩니다.  
	- triplet : $(i, k, j)$는 위 정보를 바로 반영합니다. 유저가 i, k를 소비하였을 때 item j에 대한 선호도 예측값을 의미합 니다.
- EASE 구조에 higher-order matrix를 추가한 간단한 extension입니다. EASE에서 학습하는 파라미터 은 각각의 의 미가 item i와 item j의 pairwise한 관계를 캡쳐한다고 볼수 있습니다. 따라서 유저가 i와 k 2개의 아이템을 볼 경우 이를 모델은 $B_{ij} + B_{kj}$를 통해 점수를 내게 됩니다. 이를 직접적으로 넣기 위해서, triplet relation (i, k, j)와 같은 higher order interaction을 뽑아서 넣어주었습니다. 이 때 넣을 수 있는 relation이 매우 커지는 데, 이는 등장 횟수로 잘라주었습니다.

<img width="884" alt="Screen Shot 2022-02-10 at 2 52 27 PM" src="https://github.daumkakao.com/storage/user/6543/files/75dc70a3-87a9-46ac-bc31-38fba2b74209">

- EASE 구조를 이해한다면, 옆에다가 간단한 triplet relation matrix만 추가되었다고 보시면 됩니다.

<img width="871" alt="Screen Shot 2022-02-10 at 2 52 34 PM" src="https://github.daumkakao.com/storage/user/6543/files/6fbb9677-f627-496c-8182-bd65e79dc7d7">

### Results
-  triplet ralation을 추가함에 따라, VAE관련 모델들과 유사하거나 특정 데이터셋에서는 더 좋은 성능을 보여주었습니다.

<img width="875" alt="Screen Shot 2022-02-10 at 2 52 44 PM" src="https://github.daumkakao.com/storage/user/6543/files/a6ec0ec9-b138-4b8b-bf50-d80bc5795271">

- 이 그림은 higher order interaction이 score에 어떤 역할을 하는지를 보여주는 겁니다. pairwise relation은 positive value에 치중되어 있고, triplet relation은 negative value에 치중되어 영향을 줍니다.

<img width="386" alt="Screen Shot 2022-02-10 at 2 52 51 PM" src="https://github.daumkakao.com/storage/user/6543/files/a958f0cc-9273-4fe5-bad0-7eb4aa34c19f">

### Conclusion
 - 아직까지도 단순한 user-item interaction feature를 가지고도 발전할 여지가 많습니다. 위 구조는, 기존 EASE에다가 정 말 단순하게 많이 등장하는 triplet을 넣어서 학습한 구조이기 때문에 확장이 매우 쉽습니다. 그럼에도 기존 다양한 딥러닝 기반 방식들보다 성능이 비슷하거나 더 좋다는 것은, 온라인 실험상에서의 이점까지 고려할 때 좋은 모델인 것 같습니다. 식 이 쉬운것도 좋은 것 같습니다.
-  다만 이 high-order interaction을 단순히 등장 횟수로만 자르는 건 cf의 약점인 cold-start item들에 대해 더 취약해질 것 같습니다.