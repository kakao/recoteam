- Paper : https://arxiv.org/abs/2108.01053
- Authors : [[Guillaume Salha-Galvan]], [[Romain Hennequin]], [[Benjamin Chapus]], [[Viet-Anh Tran]], [[Michalis Vazirgiannis]]
- Reviewer : [[tony.yoo@kakaocorp.com]]
- Topics
	- #Real-World_Concerns
	- #Cold_Start 
	- #Graph
	- #RecSys2021  

### Summary
- Directed graph로 정의된 item network에 대해 link prediction task을 수행한 논문입니다.
- Directed 기반의 similarity를 구하기 위해 gravity 기반의 매커니즘을 도입하여 단 방향 선호도를 예측 가능하게 만들었습니다.
- Cold item (노드 피쳐는 있으나 adjacent 정보가 isolated 된 상황)에 대해 masking과 VAE기반의 구조로 접근하여 성능 향상을 내었습니다.

### Approach

#### Gravity-Inspired similiarity
![gravity-inspired-vae-overview](https://github.daumkakao.com/storage/user/6543/files/6308a1e0-98d7-49ad-8b53-597249645747)

$$
\begin{aligned}

\hat{A}_{ij} &= \sigma \left( \log \frac{Gm_j}{\Vert z_i - z_j \Vert_2^2} \right)\\

&= \sigma \left( \underbrace{\log Gm_j}_{\text{denoted}~\tilde{m}_j} - \log\Vert z_i - z_j \Vert_2^2 \right)

\end{aligned}
$$

즉, VAE기반의 GNN를 태워 얻은 $\tilde{Z} = [Z; \tilde{M}], Z\in \mathbb{R}^{n \times d}, \tilde{M}\in \mathbb{R}^{n }$ 로 similiarity score $\hat{A}_{ij}$를 예측합니다.

#### Loss
- VAE 기반의 encoding 모델로 GNN을 사용하였습니다.
$$
q(\tilde{Z} \vert A, X) = \Pi_{i=1}^n q(\tilde{z}_i\vert A, X)
$$

$$
q(\tilde{z}_i \vert A, X) = \mathcal{N}\left( \tilde{z}_i \vert \mu_i, \text{diag}(\sigma_{i}^2)\right)
$$

$$
\begin{cases}
\mu = GNN_{\mu}(A, X) \\
\sigma = GNN_{\sigma}(A, X)
\end{cases}
$$

- $P(A)$ 를 최대화하려면 다음의 ELBO를 최대화 하면 됩니다. (jensen's inequality로 증명 가능).
$$
\mathcal{L} = \underbrace{E_{q(Z |A,X)} \left[ \log p(A|Z) \right]}_{\text{Reconstruction Loss}} − \underbrace{D_{KL}(q(Z|A,X) \Vert p(Z))}_{\text{Regularization Loss}},
$$

- Reconstruction Loss
	- $q$ 에 대한 평균을 구하기 어렵기 때문에 $A$ 가 bernoulli distribution을 따른다는 가정 하에 몬테카를로 근사를 이용해서 cross entropy 를 계산합니다.
$$
\mathcal{L}_{Reconstruction} = BCE(A, \hat{A})
$$

- Regularization Loss
	- 둘 사이의 KL divergence를 구해야하는데 $p(z)$ 를 normal distribution이라 가정하면 다음과 같이 계산됩니다.
$$
\mathcal{L}_{Regularization} = \frac{1}{2} \sum_d\sum_i^k exp(\sigma_{ii, b}^2) + \mu_{i, b} - \sigma_{ii, b} - 1
$$

#### Cold Start Similiar Items Ranking
warm item 수를 $n$, cold item 의 갯수를 $m$ 이라 하면, adjacent matrix $A \in \mathbb{R}^{(n + m) \times (n +m)}$ 에서 cold item의 row는 zero vector로 masking 됩니다.

$A$ 를 GNN 기반의 VAE 모델을 통해 다음과 같이 예측할 수 있습니다. 여기서 $\lambda$ 는 influence 와 proxmity사이의 trade off를 튜닝하는 데 사용되며 이는 popularity bias를 control하는 걸 의미합니다. 이렇게 예측된 similairity로 부터 top $k$ 개를 추천하게 됩니다.

$$
\hat{A}_{ij} = \sigma \left( \underbrace{\tilde{m}_j}_{\text{influence of j}} -\lambda \underbrace{\log \Vert z_i - z_j\Vert_2^2}_{\text{proximity of i and j}} \right)
$$

 
#### Other Methods
- [VGAE](https://arxiv.org/abs/1611.07308):
	- Undirected graph 에 대해 $\hat{A} = \sigma \left(z_i^{T}z_j\right)$ 를 통해 예측합니다. 다만, 이렇게 계산하면 symmetric 하다는 단점이 존재합니다.
- Sour-Targ GVAE:
	- Directed graph 에 대해 $\hat{A} = \sigma\left( z_i^{(s)T}z_j^{(t)}\right)$, $z^{(s)} = z[:d/2]$, $z^{(t)}=z[d/2:]$. 단, $d$는 짝수이고, 이렇게 계산하면 non-symmetric이 됩니다.

### Results
#### Dataset
- [Deezer](https://www.deezer.com/soon) 의 24,270 수의 artist 들로 구성 된 directed graph입니다.
- Node feature는 56 dimension을 가지며 다음 component들로 구성되어 있습니다.
	- Genre vector (32-dim)
	- Country vector (20-dim)
	- Mood vector (4-dim)
- Train, valid, test 는 8:1:1 로 split. Valid와 test의 경우엔 cold 노드들로 구성되어 있기 때문에 neigbor edge는 masking 되어있습니다.

#### Metric
- Recall, MAP, NDCG를 사용하였습니다.

#### Performance
![exp](https://github.daumkakao.com/storage/user/6543/files/49fece4f-a35b-4711-b3a5-8b6ed811b406)
- Gravity 매커니즘이 큰 폭으로 outperform하였습니다.
- Source.-Targ. 버전이 최근 연구에 대해 약간 우위를 보입니다. Non-symmetric 성질을 띈다는 점에 주목할 수 있습니다. Symmetric인 GAE, GVAE는 더 낮은 걸 보았을때 Non-symmetric 방법이 우수함을 의미합니다.
- Source.-Targ. 에서 VAE 가 AE보다 좋은 결과를 보였지만, Gravity 버전에서는 반대의 결과를 보였습니다. 상황에 따라 VAE vs AE의 성능이 달라지게 됩니다.

##### Mass parameter
- 정성적 분석: 왼쪽은 artist별 mass의 크기와 링크 사이를 visualization 한 결과입니다. 빨간색 노드들이 레게 아티스트들 이고, mass가 큰 것 중에 하나를 예로 들은게 레게의 유명한 아티스트 Bob Marley입니다.
- 정량적 분석: 오른쪽은 mass (아티스트들) 사이의 여러 measure (popularity, in-degree, page rank) 로 상관관계 분석을 해보았습니다. 결과를 보았을 때, mass가 높다고 measure 값들이 꼭 높은 것은 아니지만 어느정도 상관관계가 있다는것을 보여주었습니다.

<figure style="text-align: center;">
<img src="https://github.daumkakao.com/storage/user/6543/files/c6038a43-f1e3-4d02-88fa-d64499b1a1ad" style="zoom:50%;" />
<img src="./images/Pearson and Spearman correlation coefficients of masses.png" style="zoom:50%;" />
</figure>

##### Impact of attributes
- Node feature를 많이 쓸수록 성능이 향상되었습니다.
<img src="https://github.daumkakao.com/storage/user/6543/files/3db9869d-53e3-4f25-8305-d4b89d8d2b40" style="zoom:60%;" />

##### Popularity-diversity trade off
- $\lambda$ 를 높힐 수록 popular한 item의 rank 빈도가 많아지고, 줄이면 distance에 의한 계산만 하기 때문에 줄어들게 됩니다.
<img src="https://github.daumkakao.com/storage/user/6543/files/2390faca-a96d-43a1-b5c5-f8c116ac8ad7" style="zoom:50%;" />

### Conclusion
- 그래프 방법론을 이용하여 similar item 추천을 non-symetric한 상황에서 다루어 성능을 향상시킨 논문입니다.
- Cold-start 상황에서 masking, VAE 방법론등의 이점을 적용하였습니다.

#### Critical view of points:
- Cold 아이템의 경우 adjacent 정보를 masking (0으로 패딩)하면 모두 동일한 피쳐로 간주되게 됩니다.
- Cold start 상황에 대해서만 평가를 진행해보았을 때의 우위 비교가 없어 아쉬웠습니다.
- 실험에 사용된 benchmark 모델들은 비교적 최근 논문이 적어서(STAR-GCN, DEAL 빼곤 옛날 논문이라) 아쉬웠습니다.


| Model 이름 | 학회 년도 | 인용수 |
| ------------------------------------------------------------ | ---------- | ------ |
| [DropoutNet](https://www.cs.toronto.edu/~mvolkovs/nips2017_deepcf.pdf) | NIPS 2017 | 104 |
| [Graph VAE](https://arxiv.org/abs/1609.02907) | ICLR 2017 | 1,267 |
| [STAR-GCN](https://arxiv.org/abs/1905.13129) | IJCAI 2019 | 72 |
| [DEAL](https://arxiv.org/abs/2007.08053) | IJCAI 2020 | 11 |
