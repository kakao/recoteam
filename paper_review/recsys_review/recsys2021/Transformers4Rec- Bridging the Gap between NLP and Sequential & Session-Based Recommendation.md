- Paper : <https://dl.acm.org/doi/10.1145/3460231.3474255>
- Authors : [[Gabriel de Souza Pereira Moreira]], [[Sara Rabhi]], [[Jeong Min Lee]], [[Ronay Ak]], [[Even Oldridge]]
- Reviewer : [[marv.20@kakaocorp.com]]
- Topics
  - #Language_and_Knowledge
  - #Semi-Supervised_Learning
  - #Sequential_Recommendation
  - #RecSys2021

### Summary

- NLP와 sequential / session 기반 추천 방식이 유사한데, 최근 NLP의 수많은 모델 구조들을 바로 추천에 적용할 수 있게끔 huggingface transformers 라이브러리 기반의 transformer4rec 라이브러리를 공개하였습니다. Huggingface의 모델 구조를 적용, 튜닝하는 것으로 2개의 2021 이커머스 챌린지에서 우승할 수 있었습니다.
- casual language modeling에서 자주 쓰였던 학습방법들인 masked LM, permutation LM, replacement token detection 방법론들을 비교하여 보았습니다.
- 사이드 정보를 결합하여 추천해보았습니다.

### Approach

#### NLP 모델들과 Sequential / Session 기반 추천의 관계

![image](https://user-images.githubusercontent.com/38134957/165446726-6ebf29d3-91c8-4ddd-a968-8e2dfcb8ff36.png)

#### LM 학습기법들 비교 (CLM, MLM, PLM, RTD)

![The possible transformation of MLM and PLM, where w i and p i represent token and position embeddings. [M ] is the special mask token used in MLM. The left side of MLM (a) can be seen as bidirectional AR streams (in blue and yellow, respectively) at the right side. For MLM (b) and PLM (c), the left sides are in original order, and the right sides are in permuted order, which are regarded as a unified view.](https://www.researchgate.net/profile/Rui-Wang-17/publication/341369190/figure/fig4/AS:890933465849856@1589426499052/The-possible-transformation-of-MLM-and-PLM-where-w-i-and-p-i-represent-token-and.png)

- causal language model (CLM) : next token prediction
- masked language model (MLM) : masked token prediction
- permuation languagem model (PLM) : permutation + next token prediction

#### Transformer4Rec 구조

![image](https://user-images.githubusercontent.com/38134957/165446737-bfbd5f4a-619f-46f8-9753-ab0f1c925eb5.png)

- 데이터 전처리, 피처 엔지니어링 : NVTabular
  - sequential reco를 위한 ops : grouping time-sorted interactions, truncating first/last N interactions
- Meta architecture
  - feature processing module : sparse categorical, continuous -> normalized and combined
  - sequence masking module : CLM, MLM, PLM
  - prediction head module : tasks (item prediction, sequence-level prediction)

### Results

- RQ1. 다양한 모델 아키텍쳐 실험 결과
- RQ2. 다양한 학습 방식 실험 결과
- RQ3. item embedding을 다양한 feature들의 결합으로 변형

![image](https://user-images.githubusercontent.com/38134957/165446761-2f16c809-ea69-44a5-9169-e6570ba8c84d.png)

### Conclusion

- sequential recommendation이 NLP의 발전을 따라가기만 하는 형태여서 비판적이었는데 이를 실용적으로 풀어낸 게 인상깊었습니다.
- winning solution은 존재하지 않았습니다. 오히려 그렇기 때문에 데이터셋이나 환경에 따라 다양한 모델을 자유롭게 실험해볼 수 있어야 하고, 그런 의미에서 이 논문의 가치가 있다고 생각합니다.
- 사이드 정보를 넣는 방식이 인상 깊었습니다. 상당히 간단해서 어느 구좌 / 메타이던지 사용해볼 수 있을 것 같습니다.
