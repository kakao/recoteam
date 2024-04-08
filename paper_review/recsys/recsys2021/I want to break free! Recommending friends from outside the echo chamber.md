# I want to break free! Recommending friends from outside the echo chamber

- Paper : <https://dl.acm.org/doi/10.1145/3460231.3474270>
- Authors : Antonela Tommasel, Juan Manuel Rodriguez, Daniela Godoy
- Reviewer : iggy.ll
- Topics
  - [#Echo_Chambers_and_Filter_Bubbles](../../topics/Echo%20Chambers%20and%20Filter%20Bubbles.md)
  - [#RecSys2021](RecSys2021.md)

## Summary

- 논문에서 제안하는 GNN 모델에서는 사실 별로 특별히 느끼는 점이 없었습니다.
- Echo chamber로 인해 나타날 것이라 생각이 드는 현상이나 가설을 실험으로 잘 재현한다음 풀어내는데, 이게 정말 잘 된 것 같아서 공유합니다.

## Approach

### 친구 추천

유저 집합 U, 아이템 집합 I가 존재한다고 가정하자. 기존의 추천이 다루는 것은 다음과 같습니다.

1. p(r_{ui}\vert u \in U, i \in I) (연관추천)
2. \text{sim}(i \in I, j \in I) (아이템추천)

친구 추천은 p(r_{uv}|u \in U, v \in U)을 푸는 것이 목표입니다.

기존의 데이터는 주로

- 유저-아이템 인터랙션 (u, i, c) where u \in U and i \in I, and c is context w.r.t. user-item relationship.
이런 형태의 데이터가 주어지는데, 친구 추천에서는 다음과 같은 데이터가 새롭게 주어집니다.
- 유저-유저 인터랙션 (u, v, c) where u, v \in U, and c is context user-user relationship  
  그리고 기존의 (u, i, c)가 존재하지 않을 수도 있고, 추천 팀이 담당하는 서비스 중에서는 `mm에서의 친구 추천`이 친구 추천을 요구하는 영역 중 하나입니다. `친구 추천`을 다루는 추천 영역이 지금은 많지 않지만, 지금까지는 이런 문제에 그리 큰 관심이 없었던가, 기존 연관 추천/아이템 추천 문제로 캐스팅해서 풀고 있었던 것 같습니다. 친구 추천이 가진 특성을 활용해서, 연관/아이템 추천을 방법보다 더 좋은 성과를 낼 수 있다면 팀 내에서, 그리고 회사 내의 서비스에 적용할 만한 요소는 많을 것 같습니다.

### (가정) Relevancy보다 Diversity가 더 중요하다.

논문 내에서 암묵적으로 가정하고 있는 것들을 정리해보면 이렇습니다. 친구 관계 그래프에서는 일반적으로 유저들은 작은 그룹(클러스터)로 묶일 수 있고, 유저-유저 인터랙션은 대부분 이 클러스터 안에서 이뤄지고, 또한 한 클러스터 내의 유저들의 아이템 소비 패턴도 유사합니다. 이를 고려하지 않는 추천 시스템이 일반적으로 이 커뮤니티 내부에서만 추천을 만드는 경향이 있습니다. 이를테면, MF 모델을 사용한다면 (클러스터가 완벽히 분리된다고 가정한다면) 큰 interaction matrix M은 사실 다음과 같이 분해될 수 있습니다.

$$
M \simeq \begin{bmatrix}M_1 & 0 & 0 \\0 & M_2& 0 \\ 0 & 0 & M_3 \end{bmatrix}
$$

이러한 matrix에 대해 MF 모델은 사실 많은 MF 모델 여러 개를 만드는 것과 유사한 효과를 만듭니다. 또한, 클러스터 밖의 추천/유사도 비교를 힘들게 만듭니다. 따라서, 모델은 클러스터 내부의 유저와 그 유저들이 소비하는 아이템 이외의 추천을 생성하지 않으며, 이 효과는 추천 시스템이 deploy될 수록 고착화된다고 볼 수 있고, 이는 서비스/지표에 해롭습니다. 따라서 Diversity나 Novelty를 고려한 평가가 이뤄져야 한다는 것이 이 논문의 주장인 것 같습니다. 이 가정이 설득력이 있다는 생각은 들긴 하는데, 논문에서 자세한 근거를 제시하지는 않았습니다.
