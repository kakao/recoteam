# Mini Reco <!-- omit in toc -->

## 목차 <!-- omit in toc -->

- [소개](#소개)
- [User-based Collaborative Filtering](#user-based-collaborative-filtering)
- [문제](#문제)
  - [참고 사항](#참고-사항)
- [입력 데이터](#입력-데이터)
  - [제한 사항](#제한-사항)
- [평가](#평가)
  - [예시](#예시)
- [예제 테스트 케이스](#예제-테스트-케이스)
  - [예제 입력](#예제-입력)
  - [예제 출력](#예제-출력)
  - [설명](#설명)

## 소개

이 문제의 목표는 Memory-based Collaborative Filtering 기법 중 하나인 User-based Collaborative filtering 알고리즘을 사용해 추천 시스템을 만드는 것입니다.  
아래 알고리즘을 구현하여 Task를 수행하세요.

## User-based Collaborative Filtering

The [memory-based](https://en.wikipedia.org/wiki/Collaborative_filtering#Memory-based) approach uses user rating data to compute the similarity between users or items. Typical examples of this approach are neighbourhood-based CF and item-based/user-based top-N recommendations. For example, in user based approaches, the value of ratings user u gives to item i is calculated as an aggregation of some similar users' rating of the item:

![r_{u,i} = \mathrm{aggr}_{u^\' \in U} r_{u^\', i}](https://render.githubusercontent.com/render/math?math=\color{white}\LARGE{r_{u,i}%20=%20\mathrm{aggr}_{u^\'%20\in%20U}%20r_{u^\',%20i}})

where U denotes the set of top N users that are most similar to user u who rated item i.

Some examples of the aggregation function includes:

![r_{u,i} = \frac{1}{N}\sum_{u^\' \in U}r_{u^\', i}](https://render.githubusercontent.com/render/math?math=\color{white}\LARGE{r_{u,i}%20=%20\frac{1}{N}\sum_{u^\'%20\in%20U}%20r_{u^\',%20i}})

![r_{u,i} = k\sum_{u^\' \in U}\mathrm{simil}(u,u^\')r_{u^\', i}](https://render.githubusercontent.com/render/math?math=\color{white}\LARGE{r_{u,i}%20=%20k\sum_{u^\'%20\in%20U}\mathrm{simil}(u,u^\')r_{u^\',%20i}})

where k is a normalizing factor defined as ![k = 1/\sum_{u^\' \in U}\ left|\mathrm{simil}(u,u^\prime)\right|](https://render.githubusercontent.com/render/math?math=\color{white}\Large{k%20=1/\sum_{u^\'%20\in%20U}%20\left|\mathrm{simil}(u,u^\')\right|}),  
and **(1)** ![r_{u,i} = \bar{r_u} + k\sum_{u^\' \in U}\mathrm{simil}(u,u^\')(r_{u^\', i}-\bar{r_{u^\'}})](https://render.githubusercontent.com/render/math?math=\color{white}\Large{r_{u,i}%20=%20\bar{r_u}%20%2B%20k\sum_{u^\'%20\in%20U}\mathrm{simil}(u,u^\')(r_{u^\',%20i}-\bar{r_{u^\'}})}) where ![\bar{r_{u^\'}}](https://render.githubusercontent.com/render/math?math=\color{white}\large{\bar{r_{u^\'}}}) is the average rating of user u for all the items rated by u.

The neighborhood-based algorithm calculates the similarity between two users or items, and produces a prediction for the user by taking the [weighted average](https://en.wikipedia.org/wiki/Weighted_average) of all the ratings. Similarity computation between items or users is an important part of this approach. Multiple measures, such as [Pearson correlation](https://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient) and [vector cosine](https://en.wikipedia.org/wiki/Cosine_similarity) based similarity are used for this.

The cosine similarity of two users x, y is defined as **(2)**:

![\mathrm{simil}(x,y) = \cos(\vec x,\vec y) = \frac{\vec x \cdot \vec y}{||\vec x|| \times ||\vec y||} = \frac{\sum_{i \in I_{xy}}r_{x,i}r_{y,i}}{\sqrt{\sum_{i \in I_{x}}r_{x,i}^2}\sqrt{\sum_{i \in I_{y}}r_{y,i}^2}}](https://render.githubusercontent.com/render/math?math=\color{white}\LARGE{\mathrm{simil}(x,y)%20=%20\cos(\vec%20x,\vec%20y)%20=%20\frac{\vec%20x%20\cdot%20\vec%20y}{||\vec%20x||%20\times%20||\vec%20y||}%20=%20\frac{\sum_{i%20\in%20I_{xy}}r_{x,i}r_{y,i}}{\sqrt{\sum_{i%20\in%20I_{x}}r_{x,i}^2}\sqrt{\sum_{i%20\in%20I_{y}}r_{y,i}^2}}})

where ![I_{xy}](https://render.githubusercontent.com/render/math?math=\color{white}\large{I_{xy}}) is the set of items that rated by both user x and user y.

The user based top-N recommendation algorithm uses a similarity-based vector model to identify the k most similar users to an active user. After the k most similar users are found, their corresponding user-item matrices are aggregated to identify the set of items to be recommended.

## 문제

`num_reco_users`명의 사용자를 위해 User-based Collaborative Filtering 알고리즘으로 추천 결과를 만들어야 합니다.

추천 결과를 만드는 방법은 다음과 같습니다.

1. 식 (2)를 활용하여 최근접 이웃 집합 U를 계산합니다.
    - U는 사용자와 유사도가 가장 높은 `num_sim_user_top_N`명의 최근접 이웃 사용자로 구성됩니다.
1. 식 (1)로 생성한 `num_item_rec_top_M` 개의 추천 결과를 한 줄로 출력합니다.
    - 추천 결과의 각 아이템 ID는 공백으로 구분되어야 합니다.
    - 사용자에게 추천할 수 있는 아이템은 전체 아이템 집합 I가 아닌 최근접 이웃 U가 평가한 아이템 집합 I'입니다.

### 참고 사항

문제를 해결할 때 아래 내용을 참고하시기 바랍니다.

1. 사용자가 이미 평가한 아이템은 추천 결과에 포함하지 않습니다.
1. 추천할 수 있는 아이템의 수(n)가 `num_item_rec_top_M` 보다 작은 경우, 그 n개에 대해서만 추천합니다.
1. 한 사용자가 같은 아이템을 중복해서 평가한 경우는 없습니다.
1. 데이터는 희소 행렬 데이터입니다. 그러므로 모든 사용자와 아이템 쌍에 대한 평가가 존재하는 것은 아닙니다.
1. Cosine similarity 계산이 정의되지 않는 경우에는 0으로 정의합니다.
1. 식 (1)에서 normalizing factor k 값이 정의되지 않는 경우에는 0으로 정의합니다.

## 입력 데이터

데이터는 알고리즘 구현에 필요한 변숫값과 사용자가 아이템에 평가한 점수 그리고 추천 결과를 출력할 사용자 ID로 구성됩니다.

- Line 1에는 `num_sim_user_top_N` 값이 있습니다. 평점 예측 시 사용할 최근접 이웃 사용자 수입니다.
- Line 2에는 `num_item_rec_top_M` 값이 있습니다. 사용자별로 추천해야 하는 아이템 개수입니다.
- Line 3, 4에는 각각 `num_users`, `num_items` 값이 있습니다. 해당 테스트 케이스에서 제공되는 데이터에 있는 사용자, 아이템 수입니다.
- Line 5에는 `num_rows` 값이 있습니다. 데이터로 제공될 (`user_id`, `item_id`, `rating`) triplet의 개수입니다.
- Line 6부터 `num_rows`개의 Line에는 (`user_id`, `item_id`, `rating`) triplet이 있으며 각 값은 공백으로 구분되어 있습니다.
- Line (6 + `num_rows`)에는 `num_reco_users` 값이 있습니다. 추천 결과를 만들어야 할 사용자의 수입니다.
- Line (6 + `num_rows` + 1)부터 `num_reco_users`개의 Line에는 추천 결과를 만들어야 할 사용자 ID가 있습니다.

아래는 예시입니다. _(**주의**: `//` 이하는 데이터에 대한 설명이며 실제 데이터에는 존재하지 않습니다.)_

```C
2         // num_sim_user_top_N
2         // num_item_rec_top_M
5         // num_users
10        // num_items
15        // num_rows
1 1 2.34  // 사용자 1이 아이템 1에 2.34점 부여
1 2 6.21  // 사용자 1이 아이템 2에 6.21점 부여
2 3 1.1   // 사용자 2가 아이템 3에 1.1점 부여
...
...       // Line 20 (= 5 + num_rows)
2         // num_reco_users
1         // print num_item_rec_top_M items for user 1
2         // print num_item_rec_top_M items for user 2
```

### 제한 사항

- 1 <= `num_sim_user_top_N` <= 100 (integer)
- 1 <= `num_item_rec_top_M` <= 30 (integer)
- 1 <= `num_users` <= 300 (integer)
- 1 <= `num_items` <= 70 (integer)
- 1 <= `num_rows` <= 21,000 (integer)
- 1 <= `num_reco_users` <= 100 (integer)
- 1 <= `user_id` <= 300 (integer)
- 1 <= `item_id` <= 70 (integer)
- 1.0 <= `rating` <= 10.0 (real number)

## 평가

채점은 추천 결과와 정답 데이터의 유사성으로 평가합니다.  
_(nDCG: <https://en.wikipedia.org/wiki/Discounted_cumulative_gain>)_

채점 코드에서는 정답에서 추천 결과 위치와 제출한 추천 결과 위치가 동일하면 1.0, 다르면 0.7을 부여하는 방식을 사용합니다.

간단하게 아래 2가지 특징을 참고하시기 바랍니다.

1. 정답 추천 결과와 최대한 같은 순서로 추천해야 높은 nDCG 값을 얻을 수 있습니다.  
    (이 문제의 목적은 Memory-based CF 알고리즘 로직을 정확하게 구현하는 것이지, 더 좋은 추천 결과를 생성하는 것이 아니라는 점을 유념해주시기 바랍니다.)
2. 높은 순위의 추천 결과를 틀릴수록 페널티가 큽니다.

이렇게 계산한 nDCG가 0.9를 넘으면 해당 테스트 케이스는 정답으로 채점하며, 0.9를 넘지 못하면 해당 테스트 케이스는 오답으로 채점합니다.

참고로 Python으로 작성된 nDCG 계산 코드는 아래와 같습니다.

```python
# evaluation.py
import math


def ndcg(gt, rec):
    idcg = sum([1.0 / math.log(i + 2, 2) for i in range(len(gt))])
    dcg = 0.0
    for i, r in enumerate(rec):
        if r not in gt:
            continue
        gt_index = gt.index(r)
        if i != gt_index:
            rel = 0.7
        else:
            rel = 1.0
        dcg += rel / math.log(i + 2, 2)
    ndcg = dcg / idcg

    return ndcg
```

위 코드에서 변수 `gt`는 정답 추천 결과이며, 변수 `rec`는 제출된 추천 결과를 의미합니다.

### 예시

```python
# 예시 1
>>> gt = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> rec = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> ndcg(gt, rec)
1.0
```

예시 1은 정답과 완전히 동일한 경우이며, nDCG는 1.0입니다.

```python
# 예시 2
>>> gt = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> rec = [1, 2, 3, 11, 5, 6, 7, 8, 9, 10]
>>> ndcg(gt, rec)
0.9052116356304495
```

예시 2는 네 번째 추천 결과를 틀린 경우입니다.

```python
# 예시 3
>>> gt = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> rec = [1, 2, 3, 4, 5, 6, 7, 11, 9, 10]
>>> ndcg(gt, rec)
0.9305687780632229
```

예시 3은 여덟 번째 추천 결과를 틀린 경우입니다.

네 번째 추천 결과를 틀린 예시 2보다는 여덟 번째 추천 결과를 틀린 예시 3의 nDCG가 높습니다.  
즉, 높은 순위의 추천 결과를 틀릴수록 nDCG 페널티가 큽니다.

## 예제 테스트 케이스

### 예제 입력

```text
2
2
5
10
15
1 1 1.0
1 2 2.0
1 5 1.2
2 2 1.5
2 3 3.0
3 1 2.2
3 2 6.2
3 7 1.5
4 6 1.2
4 3 1.5
4 1 3.1
4 2 4.0
5 4 8.2
5 2 6.5
5 7 8.0
2
1
2
```

### 예제 출력

```text
4 3
6 4
```

### 설명

위 입력으로부터 얻은 값들은 아래와 같습니다.

- Line 1: `num_sim_user_top_N` = 2 (집합 U는 최고 유사 사용자 2명으로 만들어야 함)
- Line 2: `num_item_rec_top_M` = 2 (사용자별 추천 결과는 2개를 만들어야 함)
- Line 3: `num_users` = 5 (평점 데이터의 사용자 수는 총 5명)
- Line 4: `num_items` = 10 (평점 데이터의 아이템 수는 총 10개)
- Line 5: `num_rows` = 15 (평점 데이터의 row 개수는 15개)
- Line 6~20: 평점 데이터의 triplet (`user_id`, `item_id`, `rating`)
- Line 21: `num_reco_users` = 2 (추천 결과를 만들어야 할 사용자 수는 2명)
- Line 22~23: 추천 결과를 만들어야 할 사용자의 ID 리스트 (`user_id`= 1, 2에 해당하는 사용자의 추천 결과를 만들어서 출력해야 함)

정리하면, 주어진 평점 데이터를 이용해서 사용자 1, 사용자 2에게 각각 추천 결과를 2개씩 만들어주면 됩니다.  
식(1)을 이용해 추천 결과를 계산할 때 사용하는 집합 U는 추천 결과를 만들어야 할 사용자와 가장 유사한 사용자 2명으로 구성합니다.

사용자 1의 경우, 최고 유사 사용자는 사용자 3, 사용자 4이고, 사용자 1과의 유사도는 각각 0.97469, 0.55279입니다.  
이렇게 구한 집합 U를 이용해서 식(1)을 계산해서 예상 평점이 가장 높은 아이템 2개를 예상 평점 순으로 내림차순 정렬해서 출력하면 됩니다.  
단, 추천 결과를 만들 때는 사용자 1이 기존에 평가한 아이템(샘플에서는 아이템 1, 아이템 2, 아이템 5)은 추천 결과에서 빠져야 하는 점을 유의해주시기 바랍니다.

위 출력 예시의 첫 번째 줄에 있는 `4 3`은 정답 소스 코드로 계산한 사용자 1의 추천 결과 1순위는 아이템 4이며, 2순위는 아이템 3이라는 뜻입니다.

사용자 1, 사용자 2의 정답 추천 결과와 제출된 추천 결과 간 nDCG 계산 후, 0.9 이상이면 정답 처리합니다.
