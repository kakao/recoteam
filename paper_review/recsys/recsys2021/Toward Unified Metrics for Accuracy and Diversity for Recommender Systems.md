# Toward Unified Metrics for Accuracy and Diversity for Recommender Systems

- Paper : <https://dl.acm.org/doi/10.1145/3460231.3474234>
- Authors : Javier Parapar, Filip Radlinski
- Reviewer : iggy.ll
- Topics
  - [#Metrics_and_Evaluation](../../topics/Metrics%20and%20Evaluation.md)
  - #Diversity
  - [#RecSys2021](RecSys2021.md)

## Summary

## Approach

### 왜 다양성이 중요한가

추천 시스템을 평가하는 방법은 대부분 Information Retrieval (IR)에서 가져왔다고 생각합니다. NDCG를 비롯한 랭킹 메트릭도 마찬가지인데, 추천 시스템에서 고민하던 요소는 대부분 IR에서 비슷하게 고민했던 것들이지만, 디테일한 부분에서 다른 점이 많이 발생합니다.

### Diversity에 대한 대한 요구

추천 시스템뿐만 아니라, IR에서도 다양성은 중요한 metric 중 하나인데, 이는 주로 Ambiguity 때문입니다. 검색 엔진이 "재규어"라는 입력을 받을 경우 자동차 브랜드와, 고양잇과 동물에 대한 문서를 모두 찾아주어야 하고, 이러한 Ambiguity가 추천 시스템에서는 유저의 취향에 대응됩니다.

유저는 대체로 여러 취향을 가지고, 추천의 결과가 한 가지 종류의 아이템으로만 이루어져 있다면 추천이 불완전하다고 생각할 것입니다. 유저가 로맨스 영화와 호러 영화를 둘 다 좋아한다고 했을 때, 로맨스 영화만 추천하는 추천 모델은 불완전한 모델입니다.

### Novelty에 대한 요구

추천은 대부분 list 형태로 주어지며, 유저는 list를 좌에서 우로, 혹은 위에서 아래로 탐색하는 경우가 일반적입니다. $N$개의 추천 아이템이 주어진 경우, $k \leq N$인 $k$을 유저가 클릭한 경우, 유저가 $1, \dots, k-1$까지 보지 않았던 이유가 분명히 존재할 것이며, 이는 rank가 $k$ 미만인 아이템이 유저가 relevant하지 않았다고 판단했기 때문일 가능성이 높으며, $i_1, i_2, \dots, i_{k-1}$는 서로 닮아 있을 가능성이 높습니다. 이를 대비해서, $k$번째 아이템은 이전의 아이템과 충분히 다른 아이템인 게 더 좋을 수도 있습니다. 즉, Novelty는 추천 시스템이 실패했을 때를 대비한 보험이라 생각할 수 있습니다.

OTT 영화 추천을 예시로 들면, 유저가 로맨스를 좋아할 것이라 판단한 후에 로맨스 영화 5개를 추천했을 때, 추천이 성공적이었다 해도 유저는 랭크 상위의 영화 1-2개 정도밖에 보지 않을 것인데, 추천에 임의로 다른 영화를 한 두개 섞는다고 하면, 이 판단이 틀렸다고 하더라도 한 번의 기회를 더 얻을 수 있을 것입니다.

### Diversity와 Novelty를 고려한 Metric $\alpha\beta$-nDCG

#### Notation

- $\alpha_\phi$: 토픽(취향이나 선호도, 이하 토픽이라 칭함)
- 유저는 topic의 집합을 선호도로 갖고 있으며 $p(\alpha_\phi \vert u)$는 유저가 그 토픽을 선호할 확률을 나타낸다.
- 아이템 또한, topic의 집합을 갖고 있으며, 이 논문에서는 아이템의 토픽은 알려져 있다고 가정한다.

특정 유저 $u$가 rank $S \in \{1, 2, \dots, n\}$에 있는 item $i$를 선호할 확률은

$$
p(R=1  \vert u, i) = 1  -  \prod_{\phi} [1  - p(\alpha_\phi  \vert u, i) p(\alpha_\phi  \vert u, S)]
$$

로 정의된다.

#### Diversity Consideration

$p(\alpha_\phi  \vert u, i)$ (Diversity Term)는 Diversity를 고려한 식이다. 기존 ndcg에서 item 단위의 hit을 고려하는 것과는 별개로, topic 단위의 hit을 반영합니다.

$p(\alpha_\phi \vert u, i)$는 그 유저가 유저의 선호도 $\alpha_\phi$를 만족하는 정도를 나타내는데, 이를 별도로 정의하는 이유는 같은 장르이더라도, 유저가 특정 아이템을 선호할 수 있고 선호하지 않을 수 있기 때문입니다. 예를 들어서, *밴드 오브 브라더스*는 좋아하지만 *오! 인천*은 그다지 좋아하지 않는 경우가 있습니다.

$$
p(\alpha_\phi  \vert u, i) = \begin{cases}
0 & \text{아이템의 장르가 다름}  \\
\alpha & \text{유저가 그 장르를 좋아하는데, 유저가 클릭하지 않은 경우}  \\
\beta & \text{유저가 그 장르를 좋아하고, 유저가 그 아이템을 클릭한 경우}  \\
\end{cases}
$$

Diversity Term은 유저가 그 아이템을 좋아하거나, 그 장르를 선호하거나에 따라 score에 대해 차등을 주는 식으로 모델링됩니다. 간단히 요약하자면, 기존 nDCG에서는 유저가 실제로 클릭한(relevant) 대해서만 추천을 준다고 가정하는 반면, 유저가 좋아하는 장르에 대한 추천에도 약간이나마 선호도를 부여합니다.

$\alpha, \beta$에 대한 정의는 논문에서 자세히 되어있지 않지만, $p(\alpha \vert u), p(\alpha \vert i)$에 따라 적절히 정의될 수 있을 것 같습니다.

### Novelty Consideration

$p(\alpha_\phi  \vert u, S)$ (Novelty Term)는 유저가 특정 위치 $S\in \{1, 2, \dots, n\}$에 존재하는 추천에 대해 얼마나 만족하는지를 나타내는 지표입니다. 이를 별도로 모델링하는 이유는, 유저가 상위 랭크 $1, 2, \dots, S-1$에서 특정 토픽 $\alpha_\phi$를 봤다면, rank $S$에서 같은 토픽 $\alpha_\phi$인 아이템을 보더라도 만족도가 그리 높지 않을 것이라는 가정을 포함하고 있습니다.

$$
  p(\alpha_\phi  \vert u, S) = p(\alpha_\phi  \vert u)  \prod_{j = 1}^S [1-p(\alpha_\phi  \vert u, i_j)]
$$

유저가 이전에 본 항목에 같은 토픽의 아이템이 많이 들어있을 경우, Novelty Term은 감소한다. 새로운 토픽의 아이템이 추천될 경우, 이 값은 증가한다. 증가폭은 유저가 그 토픽을 선호할 확률 $p(\alpha_\phi \vert u)$에 비례합니다.

### Axioms for Diverse Ranking Evaluation

논문에서 추천 리스트와, 그 추천 리스트에 대한 평가 메트릭에 관한 공리를 정의해놨는데, 논문에서 8가지 공리가 정의되어 있지만, 거칠게 요약하자면 다음과 같습니다.

1. 두 아이템의 토픽이 완전히 같다고 가정하면, 유저는 relevancy가 더 높은 아이템이 추천되는 추천 리스트를 선호한다.
2. 유저가 좋아하는 아이템이 추천 리스트에 포함될 경우, 이 아이템이 더 상위 랭크에 있는 추천 리스트가 더 하위 랭크에 있는 추천 리스트보다 선호된다.
3. 한 추천 리스트에서 같은 토픽이 너무 자주 추천되는 경우, 이 토픽이 유저가 선호하는 토픽이라 할 지라도 유저가 좋아하지 않는 토픽의 아이템을 더 선호할 수 있다.
4. 유저는 본 적 없는 아이템을, 이미 싫어하는 아이템보다 더 선호한다.

## Conclusion

- 구현 후, 오프라인 메트릭은 구현이 제대로 되어 있는 지만 확인 한 이후 온라인 평가가 실전이다 이런 느낌으로 온라인에 배포해던가, 혹은 IPS같은 방법으로 온라인 평가를 오프라인으로 가져오는 방법만 알고 있었는데, 유저 행동에 대한 합리적인 가정과 모델링을 통해 더 좋은 offline metric을 만드는 일도 좋은 방향일 수 있구나 하는 생각이 들었습니다.
- Novelty가 중요하다는 얘기만 들었었는데, 그럴 듯 한 설명을 들은 것은 처음입니다.
