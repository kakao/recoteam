# Local Factor Models for Large-Scale Inductive Recommendation

- Paper : <https://ylongqi.com/assets/pdf/yang2021local.pdf>
- Authors : [[Longqi Yang]], [[Tobias Schnabel]], [[Paul N. Bennett]], [[Susan Dumais]]
- Reviewer : [[bell.park@kakaocorp.com]]
- Topics
  - #Scalable_Performance
  - #Local_Model
  - #RecSys2021

## Summary

- User-Item co-clustering을 사용해서 Local Model의 개수를 늘릴 수 있도록 추천 모델을 디자인한 논문입니다.
- User 기준 inductive 상황에서도 모델이 추천 결과를 계산할 수 있도록, item에 대해서만 embedding 을 학습하였습니다.
- 추천 성능도 기존 local model, global model 모두에 대해서 개선이 되었습니다.
  - 그런데, 이걸 local model이라고 부를 수 있는 구조인지 의문이 들었습니다.

## Approach

### 문제 인식

- Local Model은 user subgroup에 대해서만 추천을 하는 모델을 여러개 만들어, subgroup 마다 다른 모델로 추천을 하는 방식입니다.
  - User subgroup마다 소비 취향이 다를 것이다라는 가정이 있고, 여러 선행 연구에서 괜찮은 접근임이 이미 검증되었습니다.
- User subgroup마다 모델을 만들어야 해서, 모델이 무겁다면 subgroup 개수에 제한이 생깁니다.
  - 선행 연구에서는 대부분 40-50개 수준이고 100개 정도 쓰는 모델(rGLSVD)은 파라미터가 10억개나 됩니다.
- Subgroup을 나누는 단계와 Subgroup의 추천을 계산하는 단계가 나뉘어 있고 이로 인해 inductive 상황에서 추천이 어렵습니다.
  - Subgroup을 나누는 것도 학습이 필요한데, 선행 연구 대부분이 이걸 inductive 상황에서 못하는 모델입니다. (factorization)

### 제안 모델

- 이 논문에서는 User representation을 소비한 item의 embedding으로 표현하였습니다. (Fig1에서 (b))
  - item embedding을 N-head self-attention을 돌려서 N 차원 벡터로 표현하였습니다.
- Differentiable Latent Co-Clustering에 User representation, Item representation을 넣어서 학습하였습니다. (Fig1에서 (c))
  - 이름이 거창하긴 하지만 실제로는 ReLU activation 이후, Min-Sum pooling이 전부입니다.
    - ReLU 가 negative score를 제거, 클러스터 멤버십 기능을 하게 됩니다.
- 학습은 선행 연구(VAE-CF) 따라서 Softmax loss로 학습하였습니다.
- 클러스터 개수는 512개에서 2048개까지 늘려보았다고 합니다.

![image](https://user-images.githubusercontent.com/38134957/165453119-86f76cbe-a56d-4fb5-b5eb-548e35e49394.png)

## Results

![image](https://user-images.githubusercontent.com/38134957/165453125-67be3ed8-fe00-46dd-a645-b3ec4c7b52b2.png)

- 기존 모델들 대비 성능이 소폭 좋긴한데, 큰 차이는 아닙니다.

![image](https://user-images.githubusercontent.com/38134957/165453135-058c39a8-67d8-4174-b41e-21aae392bc14.png)

- 같은 성능을 더 적은 파라미터로 만들었다는데에 의의가 있습니다.

![image](https://user-images.githubusercontent.com/38134957/165453142-8e4006b4-1db4-4b96-b07d-5927f9ac7e62.png)

- 클러스터 개수를 늘리면 당연하게도 성능이 추천 증가하게 됩니다.
