## Towards Source-Aligned Variational Models for Cross-Domain Recommendation
- Paper : https://dl.acm.org/doi/10.1145/3460231.3474265
- Authors : [[Aghiles Salah]], [[Thanh Binh Tran]], [[Hady Lauw]]
- Reviewer : [[andrew.y@kakaocorp.com]]
- Topics
	- [[Language and Knowledge]]
	- [[Cross-Domain]]
	- [[_RecSys2021]]

### Summary
- Cross Domain 추천이란?
	- 기존 data sparsity로 힘든 콜드 유저의 추천을 위해 다른 서비스에서 해당 유저의 소비 이력을 쓰는 추천입니다. (예. 유저의 영화 소비 이력으로 유저한테 책 추천)
- 기존에 있던 방법은 아래와 같습니다.
	- matrix factorization jointly factorizes rating matrices from various domains with a shared user-latent space
	- transfer learning: a mapping between the source and target models or infer user representations that are domain-invariant
- 이 논문에서 제안하는 방법은 다음과 같습니다.
	- Variational AutoEncoder (VAE)를 사용하는 기법
	- VAE를 source domain에서 학습 시켜서 target domain에 preference modeling을 한다.

### Approach
#### VAE? 
- [참고 링크](https://towardsdatascience.com/understanding-variational-autoencoders-vaes-f70510919f73#:~:text=In%20a%20nutshell%2C%20a%20VAE,to%20generate%20some%20new%20data.)

![image](https://github.daumkakao.com/storage/user/7666/files/44d40aea-ae61-4ff4-8b12-9183cd61d42b)

![image](https://github.daumkakao.com/storage/user/7666/files/7cac0235-aed7-4e6f-87fc-1386adddeea7)

![image](https://github.daumkakao.com/storage/user/7666/files/2aa80d8f-19f0-4b26-bc4e-af889c111db7)

#### Why VAE?
- Matrix Factorization의 limitation인 linear nature가 아닌 non-linear recommendation 모델을 써보기 위해 VAE를 사용할 수 있습니다.
     - non-linear recommendation 모델은 sparse data에 overfitting 하기 쉬운 문제는 있습니다.
- VAE가 다른 논문들에서 성능이 좋은 측면도 있습니다.

#### Source Domain
- VAE의 디코더랑 상응하는 부분 (theta 학습)
<img src= "https://github.daumkakao.com/storage/user/7666/files/6c815c08-84b4-4ff2-8f52-9752461f0468" width = "450">

- VAE의 인코더랑 상응하는 부분 (phi 학습)
<img src= "https://github.daumkakao.com/storage/user/7666/files/8b6eddbb-dbd2-4044-8401-dace86fb4b51" width = "250">

- Evidence Lower BOund (ELBO) -> maximize:
<img src= "https://github.daumkakao.com/storage/user/7666/files/8b75c780-8d5e-4188-a11a-8f9d55e11f2e" width = "450">
- a given input x, we want to maximise the probability to have x̂ = x when we sample z from the distribution q*_x(z) and then sample x̂ from the distribution p(x|z)
- KL divergence: staying close to the prior distribution ( <img src= "https://github.daumkakao.com/storage/user/7666/files/3d8cc9bb-bb48-4136-a888-9d3862e72274" width = "150"> )


#### Target Domain
- Rigidly Aligned VAE (RA-VAE):
<img src= "https://github.daumkakao.com/storage/user/7666/files/409a4df8-bcbb-4571-bb0c-d569403a8f86" width = "450">
\* - source domain data held fixed while training target domain data

- Softly Aligned VAE (SA-VAE):

<img src= "https://github.daumkakao.com/storage/user/7666/files/b0bfc7de-d7e4-4240-8071-5ed124d48768" width = "250">

<img src= "https://github.daumkakao.com/storage/user/7666/files/e5c5cb88-22dc-4135-bfd3-be2e98f64641" width = "450">

#### 논문에서 쓰는 모델들 (baseline 포함)

![image](https://github.daumkakao.com/storage/user/7666/files/230e4ccd-c314-40d2-a842-2e68a97dfebc)


### Results
- [[Amazon]], [[Douban]] 데이터셋에서 실험하였습니다.
- 오프라인 실험: 10%, 20%, 30% 랜덤하게 테스트 셋으로 ndcg, recall 계산 (target domain에서 콜드 유저로 인식)
![image](https://github.daumkakao.com/storage/user/7666/files/e68ebdd2-2ce0-427a-8841-854d1834f49a)

![image](https://github.daumkakao.com/storage/user/7666/files/4afe3780-a53e-4ceb-b4fc-24e7424a0161)

![image](https://github.daumkakao.com/storage/user/7666/files/ab625630-730e-4f19-ab5c-a8fe6c572153)

tldr; RA-VAE, SA-VAE가 베이스라인보다 더 성능이 좋음. baseline에서는 EMCDR이 제일 성능이 좋음.

#### 모델의 성능이 유저 활동성에 따라 달라지나? (robustness of the model)

테스트 셋은 10%으로.

![image](https://github.daumkakao.com/storage/user/7666/files/9f1ff4ee-d6cf-4eb7-8d83-dc95b1e2db3e)

tldr; 모든 그룹에 성능 좋아지고, 30회 이하 유저 그룹들에 베이스라인보다 더 성능이 좋아졌다 한다.

### Conclusion
- VAE 기반 cross-domain 추천을 할때 모델을 어떻게 짜는지가 중요한걸 볼수 있다. (e.g. 모델 architecture에서 sparsity issue를 줄인다던지)
- 기존에 쓰인 deterministic methods과 달리 VAE를 쓴 probabilistic approach도 cross-domain 추천에 잘 쓰일수 있다.


### Results

### Conclusion