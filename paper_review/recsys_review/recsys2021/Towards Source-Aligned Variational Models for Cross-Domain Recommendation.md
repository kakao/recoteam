# Towards Source-Aligned Variational Models for Cross-Domain Recommendation

- Paper : <https://dl.acm.org/doi/10.1145/3460231.3474265>
- Authors : [[Aghiles Salah]], [[Thanh Binh Tran]], [[Hady Lauw]]
- Reviewer : [[andrew.y@kakaocorp.com]]
- Topics
  - #Language_and_Knowledge
  - #Cross-Domain
  - #RecSys2021

## Summary

- Cross Domain 추천이란?
  - 기존 data sparsity로 힘든 콜드 유저의 추천을 위해 다른 서비스에서 해당 유저의 소비 이력을 쓰는 추천입니다. (예. 유저의 영화 소비 이력으로 유저한테 책 추천)
- 기존에 있던 방법은 아래와 같습니다.
  - matrix factorization jointly factorizes rating matrices from various domains with a shared user-latent space
  - transfer learning: a mapping between the source and target models or infer user representations that are domain-invariant
- 이 논문에서 제안하는 방법은 다음과 같습니다.
  - Variational AutoEncoder (VAE)를 사용하는 기법
  - VAE를 source domain에서 학습 시켜서 target domain에 preference modeling을 한다.

## Approach

### VAE?

- [참고 링크](https://towardsdatascience.com/understanding-variational-autoencoders-vaes-f70510919f73#:~:text=In%20a%20nutshell%2C%20a%20VAE,to%20generate%20some%20new%20data.)

![image](https://user-images.githubusercontent.com/38134957/165147766-409ac332-6425-456d-bb3c-c002d8ce3ba5.png)
![image](https://user-images.githubusercontent.com/38134957/165147773-912b06b2-8965-4a77-8409-c019279351cd.png)
![image](https://user-images.githubusercontent.com/38134957/165147781-c526bc79-2acb-4a98-97f4-bb862f654f36.png)

### Why VAE?

- Matrix Factorization의 limitation인 linear nature가 아닌 non-linear recommendation 모델을 써보기 위해 VAE를 사용할 수 있습니다.
  - non-linear recommendation 모델은 sparse data에 overfitting 하기 쉬운 문제는 있습니다.
- VAE가 다른 논문들에서 성능이 좋은 측면도 있습니다.

### Source Domain

- VAE의 디코더랑 상응하는 부분 (theta 학습)
<img src= "https://user-images.githubusercontent.com/38134957/165147892-55e1404c-fade-47ba-9156-20025239bce7.png" width = "450">

- VAE의 인코더랑 상응하는 부분 (phi 학습)
<img src= "https://user-images.githubusercontent.com/38134957/165147904-3c60a039-d5ce-42f8-9de9-315ef79d3506.png" width = "250">

- Evidence Lower BOund (ELBO) -> maximize:
<img src= "https://user-images.githubusercontent.com/38134957/165147946-3479fa18-9ce9-4af0-be82-de8df93315ae.png" width = "450">

- a given input x, we want to maximise the probability to have x̂ = x when we sample z from the distribution q*_x(z) and then sample x̂ from the distribution p(x|z)

- KL divergence: staying close to the prior distribution ( <img src= "https://user-images.githubusercontent.com/38134957/165147967-c1c13c7a-abdf-456c-b178-5c3c2ac55fa0.png" width = "150"> )

### Target Domain

- Rigidly Aligned VAE (RA-VAE):
<img src= "https://user-images.githubusercontent.com/38134957/165148025-3248eb3e-1d4a-4818-bc07-76bb609f7ac3.png" width = "450">
  - source domain data held fixed while training target domain data

- Softly Aligned VAE (SA-VAE):

<img src= "https://user-images.githubusercontent.com/38134957/165148041-e6fc2157-42f9-460d-9ec3-c39e0a083b5c.png" width = "250">

<img src= "https://user-images.githubusercontent.com/38134957/165148047-55caad69-19a5-4183-9d1f-b0c45d63886c.png" width = "450">

### 논문에서 쓰는 모델들 (baseline 포함)

![image](https://user-images.githubusercontent.com/38134957/165148112-f73f3f06-1b36-435c-b184-e7487a715429.png)

## Results

- [[Amazon]], [[Douban]] 데이터셋에서 실험하였습니다.
- 오프라인 실험: 10%, 20%, 30% 랜덤하게 테스트 셋으로 ndcg, recall 계산 (target domain에서 콜드 유저로 인식)
![image](https://user-images.githubusercontent.com/38134957/165148128-b304551b-8736-48e7-a162-c3cba55b6e91.png)
![image](https://user-images.githubusercontent.com/38134957/165148172-dae9a356-7f06-48d5-a120-0d340e990e05.png)
![image](https://user-images.githubusercontent.com/38134957/165148184-f53e89ab-c1d1-48b2-84d9-7f01bda0904e.png)

tldr; RA-VAE, SA-VAE가 베이스라인보다 더 성능이 좋음. baseline에서는 EMCDR이 제일 성능이 좋음.

### 모델의 성능이 유저 활동성에 따라 달라지나? (robustness of the model)

테스트 셋은 10%으로.

![image](https://user-images.githubusercontent.com/38134957/165148349-b9041eb3-ad24-4cf1-b6c3-496c4c10c397.png)

tldr; 모든 그룹에 성능 좋아지고, 30회 이하 유저 그룹들에 베이스라인보다 더 성능이 좋아졌다 한다.

## Conclusion

- VAE 기반 cross-domain 추천을 할때 모델을 어떻게 짜는지가 중요한걸 볼수 있다. (e.g. 모델 architecture에서 sparsity issue를 줄인다던지)
- 기존에 쓰인 deterministic methods과 달리 VAE를 쓴 probabilistic approach도 cross-domain 추천에 잘 쓰일수 있다.
