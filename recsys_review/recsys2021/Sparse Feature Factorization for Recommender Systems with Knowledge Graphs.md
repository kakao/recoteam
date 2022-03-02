## Sparse Feature Factorization for Recommender Systems with Knowledge Graphs
- Paper : https://arxiv.org/abs/2107.14290
- Authors : [[Vito Walter Anelli]], [[Tommaso Di Noia]], [[Eugenio Di Sciascio]], [[Antonio Ferrara]], [[Alberto Carlo Maria Mancino]]
- Reviewer : [[bell.park@kakaocorp.com]]
- Topics
	- [[Language and Knowledge]]
	- [[Knowledge Graphs]]
	- [[_RecSys2021]]

### Summary
* 지식그래프(Knowledge Graph)와 엔트로피 기반 feature selection을 결합해서 만든 추천 모델을 제안한 논문입니다.
* 아이템 수에 따라 모델 복잡도(embedding)가 선형적으로 증가하는 기존 모델과 다르게 아이템 수가 늘어나도 모델 복잡도가 크게 증가하지 않습니다.
* nDCG는 나쁘지만(MP보다도 나쁜 케이스도 있음), diversity 측면에서 좋은 부분이 있습니다.
  * 그러나 실험 신뢰도가 낮은 편입니다. MP > MF 케이스도 있는데 저는 결과를 납득하기 어려웠습니다.

### Approach
#### 문제 인식
* 최근에 DL 기반 추천 모델들이 많이 사용되지만, 이 모델들은 아이템 수가 늘어나면 embedding 개수를 늘려야해서 모델 복잡도가 계속해서 증가하는 단점이 있습니다.
* Content-based와 접목시켜 만든 하이브리드 모델들도 아이템마다 feature를 concatenate하는 전략이 일반적이라 모델이 무거워지게 됩니다.

#### 제안 모델
* 이 논문에서는 각 아이템의 특성을 지식 그래프에서 가져오고, 아이템의 추천 점수를 특성의 추천 점수 weighted sum으로 계산하였습니다.
  * 예를 들어, 아래 그래프에서 `Rijksmuseum`의 추천 점수는 `<type, Art Museum>`, `<location, Amsterdam`, `<type, Location>`의 추천 점수의 weighted sum이 됩니다.
  * 각 특성 점수의 weight는 유저별로 다르게 적용이 되고, 정확하게는 user-feature 조합의 information gain으로 계산하였습니다.
    * information gain은 유저가 positive interaction한 아이템의 feature set을 대상으로 특정 feature를 넣었을 때와 제외했을 때의 entropy 차이를 의미합니다.
      * 예를 들어, 아래 그래프에서 모든 아이템은 다 `<type, Location>` 특성이 있어서 information gain이 0이 됩니다.
      * 대신 Pink가 고른 아이템 중 2개가 `<location, Amsterdam>`를 가지고 있어서 이 경우는 information gain이 0보다 크게 됩니다.
* 각 특성의 점수는 MF 스타일의 간단한 방식으로 계산 (user embedding dot feature embedding + user bias)하였습니다.

![Screenshot from 2022-01-25 14-24-32](https://github.daumkakao.com/storage/user/3654/files/d9ca08fc-12ee-4350-8f44-0c2b5248b47e)

### Results
![Screenshot from 2022-01-25 15-07-20](https://github.daumkakao.com/storage/user/3654/files/ac6e8bdb-8307-49a9-aea7-c6ea5271cde4)
![Screenshot from 2022-01-25 15-07-02](https://github.daumkakao.com/storage/user/3654/files/93f93d35-c8d2-4487-80e2-6e4660a46d79)
![Screenshot from 2022-01-25 15-06-46](https://github.daumkakao.com/storage/user/3654/files/4611b187-435c-46e0-9abd-74ba35de4f21)

- [[Movielens-1M]], [[Facebook Books]], [[Yahoo! Movies]]에서 평가하였습니다.
- 저자들은 괜찮은 수준이라고 얘기하긴 하지만, nDCG 차이가 많이 나는 편입니다. [[Facebook Books]]의 경우 다른 메서드도 성능이 안좋긴하지만 MP보다도 결과가 안좋았습니다. nDCG가 추천 퀄리티를 담보하진 않지만 차이가 너무나는데 contribution이라고 보기 어렵다고 생각됩니다.
