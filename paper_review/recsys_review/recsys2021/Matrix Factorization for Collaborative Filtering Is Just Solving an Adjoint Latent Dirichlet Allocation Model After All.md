- Paper : <https://dl.acm.org/doi/abs/10.1145/3460231.3474266>
- Authors : [[Florian Wilhelm]]
- Reviewer : [[tony.yoo@kakaocorp.com]]
- Topics
  - #Theory_and_Practice
  - #Matrix_Factorization
  - #RecSys2021

### Summary

- Matrix Factorization 문제를 Latent Dirichlet Allocation 으로 접근하여 interpretability를 향상시켰습니다.
- 추천시트템에 맞게 Bias term을 추가(기존 단점 개선)한 LDA4Rec 을 제안하여 Classic LDA 대비 성능 향상이 있었습니다.
- LDA4Rec의 rating 예측으로 MF, NMF(Non-negative MF), SNMF(Semi-NMP)의 personalized ranking 처럼 사용 할 수 있다는 걸 증명하였습니다. (증명 관점에서는 다루지 않겠습니다.)

### Approach

#### Matrix Factorization

User, item 에 대한 latent vector 에 item에 대한 bias 가 있는 MF를 벤치마킹하였습니다.
$$
\hat{x} = < \mathbf{x}_u , \mathbf{h}_i > + b_i
$$

#### LDA Approach

아래의 [Probabilistic Graph Model, PGM](https://en.wikipedia.org/wiki/Graphical_model) 을 보면, 관측되는 $i_{us}$ 를 이용하여 다른 변수들을 [EM algorithm](https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm) 을 통해 unsupervised 방법으로 학습해나가게 됩니다. (기존 모델은 [smoothed LDA](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf))

| 기존                                                         | 변형                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| <img src="/Users/kakao/Library/Application Support/typora-user-images/image-20220111110340092.png" alt="image-20220111110340092" style="zoom:50%;" /> | <img src="https://user-images.githubusercontent.com/38134957/165449976-f47ac226-be39-4389-a89a-50ecd9be470c.png" alt="LDA4Rec" style="zoom:50%;" /> |

Notation: $\boldsymbol{\varphi}_k \in \mathbb{R}^{\vert \mathcal{I} \vert}$, $\boldsymbol{\theta}_u \in \mathbb{R}^{\mathcal{\vert K \vert}}$ (보충: $\mathbf{c} \in \mathbb{R}^{\vert \mathcal{I} \vert}$)
$$
\begin{align}
\delta_i &\sim LogNormal(\mu_\delta, \sigma_\delta) \\
z_{us} &\sim Categorical(\boldsymbol{\theta}_u) \\
i_{us} &\sim p(i_{us} \vert \boldsymbol{\varphi}_{z_{us}}, \delta_i, \lambda_i) \\
p(i_{us} &\vert \boldsymbol{\varphi}_{z_{us}}, \delta_i, \lambda_i) := Categorical(\Vert \mathbf{c} \Vert_1^{-1}\mathbf{c}) \\
\mathbf{c} &= \boldsymbol{\varphi}_{z_{us}} + \lambda_u \cdot \boldsymbol{\delta}
\end{align}
$$

### Results

#### Datasets

- Split: train(90%), valid(5%), test(5%)
- The explicit feedback of these datasets was treated as implicit.

| [[Movielens-1M,]] [[MoiveLens-100K]] | [[Goodbooks]] |
| - | - |
| 1 million movie ratings across 6,040 users and 3,706 movies<br />100 thousand interactions across 610 users and 9,724 movies | 6 million interactions across 53,425 users and 10,001 books |

**Note**: LDA4Rec의 evaluation 과정에서 rating 예측을 item 하나씩 해야하기 때문에 유저당 10000개씩만 샘플링 하여 측정하였습니다.

> The bottleneck of LDA4Rec is the prediction of the personalized rankings for which we need a high number of samples per user to compute a stable ranking. Thus for each user 10,000 items were sampled.

#### Performance

- [[MoiveLens-100K]] 에서 성능 향상이 있었습니다.
<img src="https://user-images.githubusercontent.com/38134957/165450153-ca5300b3-4845-448d-a49a-6fa142dff3b4.png" alt="ex1" style="zoom:67%;" />

아쉽게도 [[Goodbooks]]에서 LDA4Rec 비교가 빠져 있지만, MF가 SNMF 보다 성능 면에서는 우수했습니다.
<img src="https://user-images.githubusercontent.com/38134957/165450159-23e829f6-3b95-4950-8b02-e47a9a34c49b.png" alt="ex2" style="zoom:60%;" />

### Conclusion

- Traditional LDA 를 the popularity of items 과 conformity of user를 통합하여 성능 향상을 이끌어 내었습니다.
- MF의 personalized ranking과 NMF, SNMF, LDA4Rec의 personalized ranking으로 transformable하다는 걸 증명하였습니다.
- (MF대비) accuracy의 큰 손실 없이 interpretability를 높혔습니다.

#### Question & View

- Q. Item에 대한 user의 bias로 접근하였는데, 굳이 종속적인 방법으로 할 필요가 있을까?
- Evalutaion 이 느리다는 단점 때문에 실용면에서 떨어집니다.
- Q. Latent representation의 most_similar 값으로 추천을 하면 성능이 어떨까?
- Accuracy 손실이 적다고 했는데, 데이터 셋 향샹을 보인건 겨우 movielen-100K 뿐입니다.
- Q. MRR과 recall은 높지만, precision이 좀 떨어지는 걸로 봐서 implicit nDCG 측정이 있었다면 어땠을까?
