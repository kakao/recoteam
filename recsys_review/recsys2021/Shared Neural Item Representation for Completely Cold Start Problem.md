## Shared Neural Item Representation for Completely Cold Start Problem
- Paper : https://dl.acm.org/doi/10.1145/3460231.3474228
- Authors : [[Ramin Raziperchikolaei]], [[Guannan Liang]], [[Young-joo Chung]]
- Reviewer : [[matthew.g@kakaocorp.com]]
- Topics
	- [[Practical Issues]]
	- [[Cold Start]]
	- [[Representation Learning]]
	- [[_RecSys2021]]

### Summary
- Complete item cold start 환경에서의 새로운 hybrid 모델을 제안하였습니다.
- User Interaction vector가 단순 user one-hot encoding vector보다 학습 과정에서 더 좋은 성능을 낸다는 것을 증명하였습니다.

### Approach
#### User Interaction Vector
- User Interaction Vector를 표현하는 방식에는 두 가지가 있습니다.
  1. User ID
     1. User ID에 상응하는 임베딩을 뽑아냄.
     2. embedding matrix $E^u \in \mathbb{R}^{d^u}$ 에서 $z^u_j = I^u_jE^u \in \mathbb{R}^{d^u}$를 뽑아냄.
  2. Interaction Vector
     1. $z^u_i = g^u(R_{j,:}) = \sigma(...\sigma(R_j, W^u_1)W^u_2)... W^u_L)$
- 이 중에서 (어찌보면 당연히,, ) 2번이 더 나은 결과가 나옵니다.
  - 이를 증명하는 방법으로 아래와 같은 방법들을 사용하였습니다.
    - training loss / recall이 가장 빠르고 높은 지점에서 수렴된다.
    - prob density at initialization 이 가장 normal distribution에 가깝다.
    - prob density at convergence 이 가장 normal distribution에 가깝다.
  - 이러한 점을 해석해보면 아래와 같이 정리가 가능합니다.
    - **$W^u_1 \in \mathbb{R^{n \cross p}}$  으로부터의 output은 user가 interact했던 아이템들의 임베딩의 합이다.**

#### Sharing neural Item rep with the hidden item embeddings
- Item representations from the item model을 user model에서의 hidden item embedding으로 사용하였습니다.

  $$
  \sum_{j,k\in S^+\bigcup{S^-}}{||(\vb{z}^u_j)^T\vb{z}^i_k - \vb{R}_{ij}||^2} s.t. \\
  \vb{z}^u_j = g^u(\vb{R}_{j,:}) = \sigma(...\sigma(\sigma(\vb{R}_{j,:}\vb{W}^u_1)\vb{W}^u_2)...\vb{W}^u_L)\\
  \vb{W}^u_1 = g^i(\vb{X}), \quad \vb{z}^i_k = g^i(\vb{X}_k,:)
  $$

#### Faster training with a simpler formulation
- 각 미니 배치마다 모든 아이템에 대한 $W^u_1$을 계산하는 것은 비효율적이라고 지적하였습니다.
- 그래서 한 번 구해놓은 $W^u_1$을 이용해서 각 유저가 소비한 아이템 ($p \in N_j$) 에 대해서만 $g_i$ 값을 구하는 식으로 처리하였습니다.
$$
\vb{y}_j = \vb{R}_{j,:}\vb{W}^u_1 = R_{j,:}g^i(\vb{X}) = \Sigma_{p\in N_j}g^i(\vb{X}_{p,:})
$$

#### Attention mechanism in learning uesr representations
- 유저가 소비한 **모든 아이템이 같은 가중치를 가질 필요는 없다**고 주장하였습니다.
  - user의 representation을 구할 때에 k-th item rep와 비슷한 아이템일수록 높은 attention을 주는 구조로 각 아이템 vector에 weight를 부여하였습니다.
    $$
    \sum_{j,k\in S^+\bigcup{S^-}}{||(\vb{z}^u_j)^T\vb{z}^i_k - \vb{R}_{ij}||^2} s.t. \\
    \vb{z}^u_j = g^u(\sigma(\vb{y_j})), \quad \vb{y}_j = \Sigma_{p \in N_j}\alpha_{pk}g^i(\vb{X}_{p, :}), \quad \vb{z}^i_k = g^i(\vb{X}_k,:)
    $$
  - 이 때 가중치 $\alpha_{pk}$를 주는 방식을 여러 가지로 두고 이에 대한 실험을 진행하였습니다.
    - dot product similarity
    - cosine similarity
    - general (with weight matrix)
  - 그리고 나서 attention과 같이 softmax 처리하여 $\alpha_{pk}$를 구하고 이를 weight으로 정하였습니다.

### Results
#### Dataset
- [[CiteULike]]: 사용자가 인용을 저장하고 학술 논문에 공유 할 수있는 웹 서비스입니다.
- [[Ichiba 1M]], [[Ichiba 20M]]: *Rakuten Ichiba* (일본 온라인 전자 상거래 플랫폼) interaction 데이터.

#### Result
##### Shared Item Representation
- Sharing item rep이 더 적은 iteration에서 더 나은 recall을 보여주었습니다.
- parameter 수가 많아지는 대규모 데이터셋에서 더 좋은 성능을 보여주었습니다.

##### Attention Mechanism
- Attention mechanism이 성능 향상에 도움이 되었다고 합니다.
- Attention의 경우에도 attention 계산 시에 아래와 같은 두 종류로 모델을 나누었습니다.
  - item $i_k$  그대로 사용하는 경우 (attention)
  - $i_k$는 제외하는 경우 (attention_rm_item)
- attention의 경우가 training set recall이 더 높았습니다.
- 그러나 general과 dot similarity의 경우 overfitting에 취약했던 반면, cosine similarity의 경우 Ichiba1M 데이터셋에 대해 overfitting은 적으면서도 (normalization의 효과로 보임), 가장 높은 recall을 기록하였습니다.

##### Shared Item Representation & dataset size
Sharing item rep의 경우, 데이터셋의 크기가 작을 수록 더 모델 성능에 도움을 주는 것으로 확인되었습니다. (데이터셋의 크기가 작을 수록 nonshared와 성능 차이가 더 크다.)

##### Comparison with other models
Cold-start 상황 해결을 다룬 다른 모델 (DropoutNet-WMF, ACCM, DeepMusic, CDL) 대비 [[CiteULike]] 데이터셋에서 높은 test recall을 기록하였습니다.