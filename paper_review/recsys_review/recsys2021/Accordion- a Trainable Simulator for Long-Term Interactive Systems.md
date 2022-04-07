- Paper : https://dl.acm.org/doi/10.1145/3460231.3474259
- Authors : [[James McInerney]], [[Ehtsham Elahi]], [[Justin Basilico]], [[Yves Raimond]], [[Tony Jebara]]
- Reviewer : [[hee.yoon@kakaocorp.com]]
- Topics
	- #Metrics_and_Evaluation
	- #RecSys2021 

### Summary
- 유저와 인터렉션이 있는 시스템 기반의 트레인 가능한 시뮬레이터를 개발하였습니다.
  - 구성은 다음과 같습니다.
    - 유저가 visit 할지 여부를 결정하는 visit model
    - 유저에게 해당 시점에 어떤 아이템이 추천될지 결정하는 recommedation imitator
    - 유저가 추천된 아이템을 클릭할지 결정하는 user selection model
  - 컨트리뷰션
    - 이 중에서 visit model 를 inhomogeneous Poisson process 로 구현한 부분이 중요한 컨트리뷰션이라고 볼 수 있습니다.
    - (비교 시뮬레이터가 Norm IPS인데) 왜 Norm IPS 에 비해, sim2real gap 을 더 줄일 수 있는가? 
      - 추천 퀄리티에 따라 impression수 자체가 차이가 날 수 있는 부분을 시뮬레이션에 녹여 모델링함
  - code: https://github.com/jamesmcinerney/accordion

### Approach
- Simulator Data Generation Algorithm:
  <img width="425" alt="Screen Shot 2022-01-17 at 4 53 23 PM" src="https://github.daumkakao.com/storage/user/2969/files/4b0d10a9-6fb7-4e08-a614-fd5ddad3691d">
- 구조도 
<img width="878" alt="Screen Shot 2022-01-18 at 11 45 00 AM" src="https://github.daumkakao.com/storage/user/2969/files/d0e685c8-7471-46ba-8b15-593dc844bd7a">

- Visit Model
	- Global Intensity + State-based intensity + Recent Activity intensity using Hawkes
  - user_state, time 이 주어졌을 때 유저의 intensity를 리턴
- Recommender Imitator (= Impression Model?)
  - user_state 가 주어졌을 때, item 을 리턴
	- 컨트롤 폴리시 목적으로는 imitator 를 학습하여 사용할 수도 있고,
        - 타겟 폴리시 목적으로는 실험하고자 하는 모델로 대체하여 사용할 수 있는 것으로 추정. (Non negative Matrix Factorization 으로 Hyperparameter Fitting 시뮬레이션 Section 4.2 참고) 
- User Selection Model
	- user_state, item 이 주어졌을때 reward 를 리턴


#### Visit Model
- <img width="415" alt="Screen Shot 2022-01-18 at 11 38 02 AM" src="https://github.daumkakao.com/storage/user/2969/files/af395907-53fe-4eb6-b5a9-dfb696c8983c">
- <img width="893" alt="Screen Shot 2022-01-18 at 11 42 25 AM" src="https://github.daumkakao.com/storage/user/2969/files/22a7c0dc-627d-4af6-96e2-ef51939ffd5d">
- Inhomogeneous Poisson Process:
    <img width="458" alt="Screen Shot 2022-01-18 at 11 37 22 AM" src="https://github.daumkakao.com/storage/user/2969/files/8de21259-beda-4a36-bcfd-dc82b0452519">
- Hawkes Intensity:
  - 과거 추천 아이템에 유저가 긍정적으로 반응했을 경우 더 커짐
  - <img width="416" alt="Screen Shot 2022-01-18 at 11 39 46 AM" src="https://github.daumkakao.com/storage/user/2969/files/5b97454b-96a4-48e0-bd78-0bbc9176a704">

#### Marking Distribution = Recommendation Imitator (Impression Model) * User Selection Model
<img width="414" alt="Screen Shot 2022-01-18 at 11 58 20 AM" src="https://github.daumkakao.com/storage/user/2969/files/5d344130-a819-432e-8217-fb3408d3c907">
- Both the impression model and user selection model use as   
  - input: a bag of words representation of previous user interactions with items 
  - and map these though a dense network 
  - output: to a multinomial distribution over items.


### Results
AB 테스트 결과를 얼마나 재현 가능한가? 를 평가하였습니다.
<img width="883" alt="Screen Shot 2022-01-18 at 5 13 12 PM" src="https://github.daumkakao.com/storage/user/2969/files/f135eecd-706c-4ada-a8d6-5b5e71439281">
