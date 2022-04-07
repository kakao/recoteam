- Paper : https://dl.acm.org/doi/10.1145/3460231.3474268
- Authors : [[Aravind Sankar]], [[Junting Wang]], [[Adit Krishnan]], [[Hari Sundaram]]
- Reviewer : [[matthew.g@kakaocorp.com]]
- Topics
	- #Language_and_Knowledge
	- #Few-Shot_Learning
	- #RecSys2021

### Summary
- Long-tail item (interaction 갯수가 작은 대다수의 아이템) 에 대해서 성능을 떨어지는 문제를 개선하고자 한 논문입니다.
- Item side information 없이 neural base recommender의 capability 만을 이용한 것이 특징입니다.

#### Contribution
- Few-shot Item Recommendation
	- 피드백이 풍부한 head item으로 base recommender를 학습한 뒤, 이를 기반으로 fine-tuning하는 컨셉입니다. 
	- Tail item의 단점인 head item과의 distribution mismatch 를 극복하고자 하였습니다.
		- 피드백이 풍부한 head item 데이터를 Meta Learning set up (support set & query set) 으로 변경하였습니다.
		- Data-rich head item에 대한 interaction으로부터 데이터를 sub-sampling하여 tail item의 피드백과 비슷한 distribution을 모사하였습니다.
- Discriminative Prototype Learning
	- Tail item이 sparse interaction을 가진다는 단점을 보완하고자 하였습니다.
	- 특정 그룹을 대표하는 벡터들을 이용하여 Base Recommender를 teacher로 삼고 Knowledge Distilation을 진행하였습니다.
- Architecture-agnostic Knowledge Transfer
	- Base recommender로 아무 NN 모델 (CF, GNN, AE 등)이나 사용 가능하다는 장점이 있습니다.

### Approach
<img width="700" alt="Screen Shot 2022-02-14 at 6 42 25 PM" src="https://github.daumkakao.com/storage/user/6543/files/8dca1f13-443b-4985-9c86-648a534b9d94">

- ProtoCF Framework
	- head item으로 Neural Recommender를 pre-train합니다.
	- tail item을 head item의 특징을 이용하여 분류할 수 있도록 Meta Learning (1) / Knowledge Distillation (2) 을 적용합니다.
	- (1) 과 (2)를 gate algorithm으로 섞어서 각 아이템을 나타내는 $e_i$를 구합니다.

#### Preliminaries
- user/item encoder의 자세한 구조는 이해하지 않아도 됩니다.

	<img width="300" alt="Screen Shot 2022-02-14 at 6 44 06 PM" src="https://github.daumkakao.com/storage/user/6543/files/af801c20-c064-4617-a2ea-3a2cf5203480">

- user/item latent feature 간의 dot product와 실제 feedback으로 손실함수를 생성합니다.

	<img width="979" alt="Screen Shot 2022-02-14 at 6 44 53 PM" src="https://github.daumkakao.com/storage/user/6543/files/cc31e819-53eb-4f69-add9-b869fefe9dc6">

- 아이템 간의 proximity (유사도) 를 구해내서 이를 knowledge distillation 단에서 사용합니다.

	<img width="956" alt="Screen Shot 2022-02-14 at 6 45 17 PM" src="https://github.daumkakao.com/storage/user/6543/files/64c4cb48-2013-4f85-ac2b-afc4488f8af5">

#### Pre-trained Neural Based Recommender
- head item 만을 이용하여 user/item encoder를 생성합니다.
- 다양한 종류의 모델을 아무거나 사용할 수 있습니다. (논문에서는 BPR, VAE, CDAE를 사용함.) 
- 대신, NN 모델이여야 합니다.
	- tail item에 대해서도 embedding을 뽑아낼 수 있도록, 또한 이후에 knowledge distillation을 이용하여 학습시킬 수 있도록 위함입니다.

#### Few-Shot Item Recommendation
meta learning 방식으로 데이터 셋을 쪼개서 학습을 진행하였습니다.

##### Task Formulation
- head item 데이터를 sub-sampling하여 tail item 과 비슷한 상황을 가진 데이터 형태로 모사하였습니다.
- 전체 head item 중 개의 아이템만 샘플링하였습니다.
- head item i에 대해서 support set, query set으로 나누어서 meta learning방식으로 학습을 진행하였습니다.

	<img width="991" alt="Screen Shot 2022-02-14 at 6 46 46 PM" src="https://github.daumkakao.com/storage/user/6543/files/972b7131-1106-42ed-82fd-a599bd08b0b0">
	
##### Item Prototype & Knowledge Distillation
- item 에 대한 representation을 mean vector of the embedded support user set S_i 로 표현하였습니다.
- 논문에서는 아이템을 소비한 유저들을 중심으로 한 clustering의 결과로 해석하였습니다.
	
	<img width="1005" alt="Screen Shot 2022-02-14 at 6 48 17 PM" src="https://github.daumkakao.com/storage/user/6543/files/1313e522-9c7e-4eac-9077-5222a028f7bb">
- 그러나 해당 prototype만으로는 문제가 있는데,
	- 데이터가 매우 sparse해서 tail item에 대해서는 해당 값이 매우 noisy할 수 있습니다.
	- tail item에 대해서는 데이터의 분별력이 떨어지므로, 아이템 별로 거의 비슷한 값이 나올 수 있습니다.
- 추가적으로 분별 가능한 inductive bias 역할을 하는 새로운 term이 필요합니다!

##### Group Embedding
- tail item을 좀 더 분별력 있게 설명하려면 head item과의 item - item proximity를 이용할 수 있습니다.
- 그러나 아이템의 갯수가 많아지게 되면 pairwise proximity 를 직접 저장하고 불러오는 데에 한계가 생깁니다. 
- 따라서, Group Embedding 을 이용하여 item - item proximity를 저차원으로 묘사합니다.

	<img width="941" alt="Screen Shot 2022-02-14 at 6 49 10 PM" src="https://github.daumkakao.com/storage/user/6543/files/4fa414cb-2582-4cf6-982d-129e3b88e9ac">

- 직관적으로 생각해서 의 각 벡터가 아이템의 특정한 정보 (국가, 카테고리, 장소, 업종) 등을 표현한다고 생각하면 됩니다. (MMoE랑 비슷한 느낌으로 이해하면 좋을 듯.)
- Group enhanced prototype $g_i$-> $z_i$와 $p_i$를 learnable parameter를 이용하여 attention을 처리하였습니다.
	
	<img width="997" alt="Screen Shot 2022-02-14 at 6 50 01 PM" src="https://github.daumkakao.com/storage/user/6543/files/18dc9f4e-91ea-453b-9352-eb20b6e01f29">

##### Knowledge Distillation
- Base Recommender를 통해 구한 item-item proximity에 대한 정보를 $Z_M$에 심습니다.
- $R_B$을 기준으로 i와 가장 비슷한 아이템 n=10개의 아이템에 대해서
	- base recommender / group-enhanced prototype 간의 Cross Entropy를 최소화하고자 하는 것입니다.

	<img width="993" alt="Screen Shot 2022-02-14 at 6 51 23 PM" src="https://github.daumkakao.com/storage/user/6543/files/eb59c1da-a17d-4014-8d22-8351e2b8d939">

#### Final Item Embedding
- $R_B$, $Z_M$로 구한 item embedding의 gated result로 최종 item embedding $e_i$를 구할 수 있습니다.
	
	<img width="794" alt="Screen Shot 2022-02-14 at 6 52 42 PM" src="https://github.daumkakao.com/storage/user/6543/files/0ae3295c-7e70-4757-9d88-01045dbfe571">

#### Few-shot Recommender Training
- query set Q를 이용하여 query set에 속한 user와의 relevance score를 생성합니다. (by cosine similiarity)  
- 이 때 pair 는 값이 애초에 1이므로 Negative Cross Entropy를 최소화하는 방향으로 학습 진행하면 됩니다.
	<img width="952" alt="Screen Shot 2022-02-14 at 6 55 02 PM" src="https://github.daumkakao.com/storage/user/6543/files/5bbdf8f0-c25a-4445-b176-a569d90f9bf6">
- 이 때 p_F를 구하는 방법으로 두 가지 방식이 있습니다.
	- Multimodial Log-Likelihood ( 에 속하는 모든 아이템에 대한 softmax)
	- Logistic Log-Likelihood

### Results
#### Overall
- [[Epinions]], [[Yelp]], [[Weeplaces]], [[Gowalla]]에서 실험을 진행하였습니다.
- NCF Autoencoder > latent-factor models  
- ProtoCF는 SOTA를 overall item에서 앞서는 것을 확인할 수 있었습니다.

<img width="1012" alt="Screen Shot 2022-02-14 at 11 34 44 PM" src="https://github.daumkakao.com/storage/user/6543/files/e0034868-0198-4d52-b465-45a4267a628b">

#### Few-shot Recommendation Result  
- interaction 갯수가 적은 구간일수록 ProtoCF >> baseline 경향이 강해졌습니다.
- 아래 지표는 item들을 popularity 순서대로 그룹화한 것인데, interaction 갯수가 낮은 구간에서 성능 차이가 더 발생하는 것을 확인할 수 있었습니다.

<img width="1009" alt="Screen Shot 2022-02-14 at 11 35 17 PM" src="https://github.daumkakao.com/storage/user/6543/files/0099a20b-acea-4bb2-a801-c585d1024f06">

#### Ablation Study
- few-shot performance (long tail items with less than 20 interactions) 만을 기재하였습니다. 
- 모든 부분이 critical 하게 성능에 영향을 준 것은 아니나 (모델 자체가 와 의 앙상블이므로) 각 모듈이 성능 향상에 영향을 끼쳤습니다.

<img width="1010" alt="Screen Shot 2022-02-14 at 11 35 57 PM" src="https://github.daumkakao.com/storage/user/6543/files/2117dcb6-6b50-4e30-b68a-1e8b60520e26">

#### Parameter Sensitivity
- $\lambda=0.01$ 에서 제일 성능이 좋고, 이후에는 커질수록 성능이 하락하였습니다.
- $N$(task에서의 sample size)는 클수록 성능이 좋아지는 것을 확인할 수 있었습니다.
