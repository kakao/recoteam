# Debiased Explainable Pairwise Ranking from Implicit Feedback

- Paper : <https://arxiv.org/pdf/2107.14768.pdf>
- Authors : Khalil Damak, Sami Khenissi, Olfa Nasraoui
- Reviewer : hee.yoon
- Topics
  - [#Privacy_Fairness_Bias](../../topics/Privacy,%20Fairness,%20Bias.md)
  - #Matrix_Factorization
  - #Explainable_Recommendation
  - [#RecSys2021](RecSys2021.md)

## Summary

- 기존 Bayesian Personalized Ranking(BPR) 대비하여 explainability를 늘리고 exposure bias를 잡은 논문입니다.
  - 기존 BPR 모델은 설명 불가능한 블랙박스 모델이었습니다. -> a novel explainable loss function and a corresponding Matrix Factorization-based model called Explainable Bayesian Personalized Ranking (EBPR) that generates recommendations along with item-based explanations.
  - 기존 BPR 모델은 Missing Not At Random (MNAR) 데이터 특성 때문에 exposure bias에 취약했었습니다. -> an unbiased estimator for the ideal EBPR loss.

## Approach

### BPR

- objective function:
  <img width="403" src="https://user-images.githubusercontent.com/38134957/165450622-feaf8ae5-a197-4091-b3a9-e862857ca90d.png">

### Explainable BPR

- objective function:
  <img width="412" src="https://user-images.githubusercontent.com/38134957/165450632-6b932ca6-71e3-4ca3-a561-b84e2253f4a3.png">
- E_ui+ (1 - E_ui-) 부분은 (u, i+, i-) 인스턴스의 컨트리뷰션의 비중을 정하는 역할을 합니다. Positive 아이템의 설명력이 높을수록, negative 아이템의 설명력이 낮을수록 학습 기여도가 높습니다. 결과적으로 생성된 추천결과의 상위 아이템들은 더 높은 설명력을 가질 것이라고 기대할 수 있습니다.
- For instance, in the extreme case where either the positive item is not explainable at all or the negative item is completely explainable, the update equation is zeroed out. Hence, no contribution will come from the corresponding instance to the learning. This is reasonable and desirable since the aforementioned case depicts a non explainable preference, where either the positive item is not explainable or the negative item is explainable. Either case undermines the explainability of the preference. (설명가능하지 않은 아이템을 소비한 것은 학습에 포함이 안됩니다. 아래 E_ui 정의를 참고하면, 유저가 소비한 아이템의 이웃 아이템을 유저가 소비한 이력이 없으면 학습에 포함이 안됩니다.)

- explainability matrix:
  - E_ui = items the user interacted from the neighboring items / len(neighboring items)
    - 이웃한 아이템 중에서 해당 유저와의 인터랙션이 발생한 아이템의 비중입니다.
    - similarity의 계산: 별도의 데이터가 아닌, rating 메트릭스 기반으로 cosine similarity를 계산합니다.
  - for a specific item, the more neighboring items a given user has interacted with, the higher the explainability of that item will be to this user.
  - 학습 시작 전, 미리 계산하는 방식입니다.
  - <img width="411" src="https://user-images.githubusercontent.com/38134957/165450706-8c030819-c642-48a2-95e8-a5750254812d.png">
  - <img width="405" src="https://user-images.githubusercontent.com/38134957/165450714-805f92ba-7bad-4dc8-9b31-a7513126faca.png">
  - neighborhood size
    - <img width="820" src="https://user-images.githubusercontent.com/38134957/165450725-593fe1e4-88d2-421d-b8a4-6d674286b0a3.png">

- 추천 결과 서빙시 explainability 기반으로 해석된 결과를 제공 가능합니다. (참조 논문에서 언급한 방식)
  - 참조 논문(Using Explainability for Constrained Matrix Factorization): <https://uknowledge.uky.edu/cgi/viewcontent.cgi?article=1017&context=ccs2>
  - item 기반 explainability 사용시:
    - <img width="335" src="https://user-images.githubusercontent.com/38134957/165450845-b2fdc4ab-3fc6-4aef-8d54-e2ff856df60a.png">
  - user 기반 explainability 사용시:
    - <img width="262" src="https://user-images.githubusercontent.com/38134957/165450849-6a219ded-aeb6-44a5-9748-c7d0951250c8.png">

### Unbiased Explainable BPR (UEBPR)

- objective function:
  - <img width="403" src="https://user-images.githubusercontent.com/38134957/165450866-14ebe685-15c8-4b7d-a037-a82e9c3b447a.png">
- 가정
  - <img width="80" src="https://user-images.githubusercontent.com/38134957/165450996-03f03a0a-dcbf-4cf8-a4f9-8d07f9c141a7.png">
  - Y_u,i: user 가 item 과 인터렉션을 했는지 여부 (예: 클릭 여부) = 노출이 되고, 관련성도 있다
  - O_u,i: user 에게 item 이 노출됐는지 여부
    - <img width="237" src="https://user-images.githubusercontent.com/38134957/165451006-800761c4-3242-4313-9852-ada592cb3c61.png">
  - R_u,i: user 에게 item 이 관련성이 있는지 여부
    - <img width="96" src="https://user-images.githubusercontent.com/38134957/165451017-9b05f8d7-64c6-41d4-bda4-54ddbaf219f9.png">
    - <img width="137" src="https://user-images.githubusercontent.com/38134957/165451021-f977c481-a9d7-4b7c-a321-c66e1f2409a8.png">

#### Unbiased BPR Loss (UBPR)

- objective function:
<img width="413" src="https://user-images.githubusercontent.com/38134957/165451226-1757c3d5-18f7-4f59-aa1e-fd3069474ade.png">

#### Ideal Explainable BPR

- objective function:
<img width="403" src="https://user-images.githubusercontent.com/38134957/165451231-7247f495-40f1-4227-aca3-4e2cf6ccf78b.png">

<img width="425" src="https://user-images.githubusercontent.com/38134957/165451234-6b09a4e0-09fd-4bda-a95c-a8e53b130320.png">

#### Partially Unbiased Explainable BPR (pUEBPR)

- objective function:
<img width="396" src="https://user-images.githubusercontent.com/38134957/165451247-65014171-77dc-46e2-8a9c-83919065f26e.png">

## Results

<img width="815" src="https://user-images.githubusercontent.com/38134957/165451256-5957ea77-ef9f-4b02-8e96-5045c50368ea.png">
<img width="816" src="https://user-images.githubusercontent.com/38134957/165451259-f01fdf91-f6d6-4460-9a6a-36ed018bad14.png">
