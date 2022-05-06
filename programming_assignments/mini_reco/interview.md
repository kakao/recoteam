# Mini Reco 인터뷰 질문

> [▶︎ Mini Reco 문제로 돌아가기](README.md)

Mini Reco 문제로 영입을 진행하며 지원자분에게 드렸던 인터뷰 질문과 예시 답변을 모아놓았습니다.

## 질문 1

[User-based Collaborative Filtering 설명](https://github.com/kakao/recoteam/blob/master/programming_assignments/mini_reco/README.md#user-based-collaborative-filtering)의 식 (1)을 보고 추천 결과가 어떻게 생성되는지 설명해주세요.

**(1)** ![r_{u,i} = \bar{r_u} + k\sum_{u^\' \in U}\mathrm{simil}(u,u^\')(r_{u^\', i}-\bar{r_{u^\'}}) (dark)](https://render.githubusercontent.com/render/math?math=\color{white}\Large{r_{u,i}%20=%20\bar{r_u}%20%2B%20k\sum_{u^\'%20\in%20U}\mathrm{simil}(u,u^\')(r_{u^\',%20i}-\bar{r_{u^\'}})}#gh-dark-mode-only)![r_{u,i} = \bar{r_u} + k\sum_{u^\' \in U}\mathrm{simil}(u,u^\')(r_{u^\', i}-\bar{r_{u^\'}}) (light)](https://render.githubusercontent.com/render/math?math=\Large{r_{u,i}%20=%20\bar{r_u}%20%2B%20k\sum_{u^\'%20\in%20U}\mathrm{simil}(u,u^\')(r_{u^\',%20i}-\bar{r_{u^\'}})}#gh-light-mode-only)

<details>
<summary>예시 답변</summary>

- 유저의 특정 아이템에 대한 예측 평점은 아래 두 항을 더해서 구한다.
  - 우변 첫번째 항은 해당 유저의 평점 평균을 의미하고,
  - 우변 두번째 항은 유사 이웃들의 평점 편차의 가중 평균을 의미한다.

</details>

## 질문 2

[User-based Collaborative Filtering 설명](https://github.com/kakao/recoteam/blob/master/programming_assignments/mini_reco/README.md#user-based-collaborative-filtering)의 식 (1)이 다음과 같이 바뀐다면(![\bar{r_u} (dark)](https://render.githubusercontent.com/render/math?math=\color{white}\large{\bar{r_u}}#gh-dark-mode-only)![\bar{r_u} (light)](https://render.githubusercontent.com/render/math?math=\large{\bar{r_u}}#gh-light-mode-only), ![\bar{r_{u^\'}} (dark)](https://render.githubusercontent.com/render/math?math=\color{white}\large{\bar{r_{u^\'}}}#gh-dark-mode-only)![\bar{r_{u^\'}} (light)](https://render.githubusercontent.com/render/math?math=\large{\bar{r_{u^\'}}}#gh-light-mode-only) 항이 사라진다면) 추천 결과가 어떻게 달라질까요?

**(1-1)** ![r_{u,i} = k\sum_{u^\' \in U}\mathrm{simil}(u,u^\')(r_{u^\', i}) (dark)](https://render.githubusercontent.com/render/math?math=\color{white}\Large{r_{u,i}%20=%20k\sum_{u^\'%20\in%20U}\mathrm{simil}(u,u^\')(r_{u^\',%20i})}#gh-dark-mode-only)![r_{u,i} = k\sum_{u^\' \in U}\mathrm{simil}(u,u^\')(r_{u^\', i}) (light)](https://render.githubusercontent.com/render/math?math=\Large{r_{u,i}%20=%20k\sum_{u^\'%20\in%20U}\mathrm{simil}(u,u^\')(r_{u^\',%20i})}#gh-light-mode-only)

<details>
<summary>힌트</summary>

- 만약 특정 유저의 점수가 굉장히 짠 편이라면(모든 아이템에 대해서 낮은 점수를 부여한다면) 어떤 상황이 발생할까요?

</details>

<details>
<summary>예시 답변</summary>

- 식 (1)에서 (1-1)로 바뀌는 것은 bias 텀 없이 이웃들의 평점 평균으로만 해당 유저의 평점을 계산하는 것을 의미한다.
- 하지만 유저의 평점 bias가 서로 다르고 그 점이 반영되지 않는다면, 제대로 된 추천 결과(예상 평점)가 계산되지 않을 수 있다.

(극단적으로) 예를 들면, 유저 A의 평점 평균은 2점이고 유저 A의 최근접 이웃들의 평점 평균은 4.5점인 상황을 가정해보자. 유저 A의 최근접 이웃들이 특정 아이템 B에 대해서 평균 3점 정도의 평가를 내렸다고 할 때, (bias를 반영하지 않는 식 (1-1)의 경우) 최근접 이웃들의 기준으로 보았을 때 아이템 B는 비추천할만한 아이템이지만 유저 A의 평점 평균과 비교해보았을때는 추천 작품이 될 수 있다. 따라서 각 유저의 평점 bias를 반영하여 추천 결과(예상 평점)를 계산하는 것이 더 좋은 결과를 낼 수 있을 것이다.

</details>

## 질문 3

[User-based Collaborative Filtering 설명](https://github.com/kakao/recoteam/blob/master/programming_assignments/mini_reco/README.md#user-based-collaborative-filtering)의 식 (1)이 다음과 같이 바꾸려고 한다면(![\mathrm{simil}(u,u^\') (dark)](https://render.githubusercontent.com/render/math?math=\color{white}\large{\mathrm{simil}(u,u^\')}#gh-dark-mode-only)![\mathrm{simil}(u,u^\') (light)](https://render.githubusercontent.com/render/math?math=\large{\mathrm{simil}(u,u^\')}#gh-light-mode-only) 항이 사라진다면) 식을 어떻게 수정해야할까요?

**(1-2)** ![r_{u,i} = \bar{r_u} + k\sum_{u^\' \in U}(r_{u^\', i}-\bar{r_{u^\'}}) (dark)](https://render.githubusercontent.com/render/math?math=\color{white}\Large{r_{u,i}%20=%20\bar{r_u}%20%2B%20k\sum_{u^\'%20\in%20U}(r_{u^\',%20i}-\bar{r_{u^\'}})}#gh-dark-mode-only)![r_{u,i} = \bar{r_u} + k\sum_{u^\' \in U}\mathrm{simil}(u,u^\')(r_{u^\', i}-\bar{r_{u^\'}}) (light)](https://render.githubusercontent.com/render/math?math=\Large{r_{u,i}%20=%20\bar{r_u}%20%2B%20k\sum_{u^\'%20\in%20U}(r_{u^\',%20i}-\bar{r_{u^\'}})}#gh-light-mode-only)

<details>
<summary>예시 답변</summary>

- 식 (1)에서 우변의 마지막 항은 최근접 이웃이 해당 아이템에 매긴 평점의 가중 평균이었으나, 식 (1-2)에서는 가중 평균이 아닌 산술 평균으로 변경하려는 것으로 볼 수 있다.
- 따라서 ![k=\frac{1}{|U|} (dark)](https://render.githubusercontent.com/render/math?math=\color{white}\Large{k=\frac{1}{|U|}}#gh-dark-mode-only)![k=\frac{1}{|U|} (light)](https://render.githubusercontent.com/render/math?math=\Large{k=\frac{1}{|U|}}#gh-light-mode-only)로 수정하면 최근접 이웃의 평점의 산술 평균으로 계산한 추천 결과(예상 평점)를 얻을 수 있을 것이다.

</details>
