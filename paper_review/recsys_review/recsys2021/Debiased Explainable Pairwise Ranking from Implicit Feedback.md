- Paper : https://arxiv.org/pdf/2107.14768.pdf
- Authors : [[Khalil Damak]], [[Sami Khenissi]], [[Olfa Nasraoui]]
- Reviewer : [[hee.yoon@kakaocorp.com]]
- Topics
	- #Privacy_Fairness_Bias
	- #Matrix_Factorization
	- #Explainable_Recommendation
	- #RecSys2021 

### Summary
- 기존 Bayesian Personalized Ranking(BPR) 대비하여 explainability를 늘리고 exposure bias를 잡은 논문입니다.
	- 기존 BPR 모델은 설명 불가능한 블랙박스 모델이었습니다. -> a novel explainable loss function and a corresponding Matrix Factorization-based model called Explainable Bayesian Personalized Ranking (EBPR) that generates recommendations along with item-based explanations.
	- 기존 BPR 모델은 Missing Not At Random (MNAR) 데이터 특성 때문에 exposure bias에 취약했었습니다. -> an unbiased estimator for the ideal EBPR loss.


### Approach
#### BPR
- objective function:
  <img width="403" alt="Screen Shot 2021-12-12 at 3 50 33 PM" src="https://github.daumkakao.com/storage/user/2969/files/3fb89e5c-099b-40bc-a5e7-df1a80e796d8">


#### Explainable BPR
- objective function:
  <img width="412" alt="Screen Shot 2021-12-12 at 3 49 04 PM" src="https://github.daumkakao.com/storage/user/2969/files/ac6b9b9d-890b-441c-afc3-7246f7eec729"> 
- E_ui+ (1 - E_ui-) 부분은 (u, i+, i-) 인스턴스의 컨트리뷰션의 비중을 정하는 역할을 합니다. Positive 아이템의 설명력이 높을수록, negative 아이템의 설명력이 낮을수록 학습 기여도가 높습니다. 결과적으로 생성된 추천결과의 상위 아이템들은 더 높은 설명력을 가질 것이라고 기대할 수 있습니다.
- For instance, in the extreme case where either the positive item is not explainable at all or the negative item is completely explainable, the update equation is zeroed out. Hence, no contribution will come from the corresponding instance to the learning. This is reasonable and desirable since the aforementioned case depicts a non explainable preference, where either the positive item is not explainable or the negative item is explainable. Either case undermines the explainability of the preference. (설명가능하지 않은 아이템을 소비한 것은 학습에 포함이 안됩니다. 아래 E_ui 정의를 참고하면, 유저가 소비한 아이템의 이웃 아이템을 유저가 소비한 이력이 없으면 학습에 포함이 안됩니다.)

- explainability matrix: 
  - E_ui = items the user interacted from the neighboring items / len(neighboring items)  
    - 이웃한 아이템 중에서 해당 유저와의 인터랙션이 발생한 아이템의 비중입니다.
    - similarity의 계산: 별도의 데이터가 아닌, rating 메트릭스 기반으로 cosine similarity를 계산합니다.
  - for a specific item, the more neighboring items a given user has interacted with, the higher the explainability of that item will be to this user.  
  - 학습 시작 전, 미리 계산하는 방식입니다.
  - <img width="411" alt="Screen Shot 2021-12-12 at 3 52 02 PM" src="https://github.daumkakao.com/storage/user/2969/files/950e0ea9-bf79-437e-bd3c-1fabd6d244e4">
  - <img width="405" alt="Screen Shot 2021-12-12 at 3 52 16 PM" src="https://github.daumkakao.com/storage/user/2969/files/3120d4b4-a5dd-42af-885d-9191f5ffa2df">
  - neighborhood size
    - <img width="820" alt="Screen Shot 2021-12-12 at 4 21 10 PM" src="https://github.daumkakao.com/storage/user/2969/files/c374b85e-696f-4741-93ad-a2554a47554a">

- 추천 결과 서빙시 explainability 기반으로 해석된 결과를 제공 가능합니다. (참조 논문에서 언급한 방식)
  - 참조 논문(Using Explainability for Constrained Matrix Factorization): https://uknowledge.uky.edu/cgi/viewcontent.cgi?article=1017&context=ccs2
  - item 기반 explainability 사용시: 
    - <img width="335" alt="Screen Shot 2021-12-12 at 3 54 52 PM" src="https://github.daumkakao.com/storage/user/2969/files/b2833846-699f-4cd6-aa68-efe46af407c5">
  - user 기반 explainability 사용시: 
    - <img width="262" alt="Screen Shot 2021-12-12 at 3 54 35 PM" src="https://github.daumkakao.com/storage/user/2969/files/a39dcad5-c035-4dde-a061-6f2b48397562">

#### Unbiased Explainable BPR (UEBPR)
- objective function: 
  - <img width="403" alt="Screen Shot 2021-12-12 at 4 00 27 PM" src="https://github.daumkakao.com/storage/user/2969/files/e0379ba6-16e7-49d5-9ffa-7f1b2d69c25e">
- 가정
  - <img width="80" alt="Screen Shot 2021-12-12 at 4 06 32 PM" src="https://github.daumkakao.com/storage/user/2969/files/54c5ff7b-c33c-4a95-b033-a80d0d416776">
  - Y_u,i: user 가 item 과 인터렉션을 했는지 여부 (예: 클릭 여부) = 노출이 되고, 관련성도 있다
  - O_u,i: user 에게 item 이 노출됐는지 여부
    - <img width="237" alt="Screen Shot 2021-12-12 at 4 10 31 PM" src="https://github.daumkakao.com/storage/user/2969/files/4d6aa615-e9eb-4543-95a4-9fe95265f337">
  - R_u,i: user 에게 item 이 관련성이 있는지 여부
    - <img width="96" alt="Screen Shot 2021-12-12 at 4 10 41 PM" src="https://github.daumkakao.com/storage/user/2969/files/93494b23-b59e-4e80-952e-8ecd48e152e2">
    - <img width="137" alt="Screen Shot 2021-12-12 at 4 11 54 PM" src="https://github.daumkakao.com/storage/user/2969/files/0d081826-b9d7-4809-ab6c-2b55fc211012">

##### Unbiased BPR Loss (UBPR)
- objective function:
<img width="413" alt="Screen Shot 2021-12-12 at 3 58 15 PM" src="https://github.daumkakao.com/storage/user/2969/files/21ba83bd-b9a2-48f5-b6f2-bed697eca197">

##### Ideal Explainable BPR
- objective function:
<img width="403" alt="Screen Shot 2021-12-12 at 3 59 26 PM" src="https://github.daumkakao.com/storage/user/2969/files/e0158398-e647-4a39-8b24-886d0579af8a">

<img width="425" alt="Screen Shot 2021-12-12 at 4 13 40 PM" src="https://github.daumkakao.com/storage/user/2969/files/6c276c83-eb01-4d05-a064-0751824717c0">

##### Partially Unbiased Explainable BPR (pUEBPR)
- objective function:
<img width="396" alt="Screen Shot 2021-12-12 at 4 02 12 PM" src="https://github.daumkakao.com/storage/user/2969/files/a7980f51-6d5b-4e06-a894-cffe0abd025d">

### Results
<img width="815" alt="Screen Shot 2021-12-12 at 4 04 03 PM" src="https://github.daumkakao.com/storage/user/2969/files/85a02fd4-1df4-4080-8803-49ba02c85424">
<img width="816" alt="Screen Shot 2021-12-12 at 4 04 25 PM" src="https://github.daumkakao.com/storage/user/2969/files/b5cd71f1-e087-410b-ad33-3a065102928b">
