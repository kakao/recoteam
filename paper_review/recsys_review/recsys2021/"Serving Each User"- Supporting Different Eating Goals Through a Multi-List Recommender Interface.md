- Paper : <https://doi.org/10.1145/3460231.3474232>
- Authors : [[Alain Starke]], [[Edis Asotic]], [[Christoph Trattner]]
- Reviewer : [[bell.park@kakaocorp.com]], [[marv.20@kakaocorp.com]]
- Topics
  - #Users_in_Focus
  - #Diversity
  - #RecSys2021

### Summary

- 음식 추천 시스템에서, 유저의 다양한 목적을 만족시키기 위해 어떻게 노출시키면 좋을지(인터페이스)에 대해서 연구한 논문입니다.
- 추천 결과를 single-list와 multi-list 각각의 방법으로 노출했을 때 어떠한 차이가 있는지 유저 스터디로 비교 분석하였습니다.
- 리스트 간의 순서를 정하는 모델이나 로직이 없다는 것은 아쉽지만, 현실적인 접근이라고 생각됩니다.

### Approach

- 기본적으로 현재 보고있는 레시피와 유사한 레시피를 추천하는 연관 추천 환경입니다.
- 저자들이 직접 레시피 데이터를 긁어와서 5가지 추천 리스트를 구성하였습니다.
  - Similar recipies - 레시피 이름 TF-IDF indexing후 top-5 similarity
  - Fewer Calories - top-40 similarity 후 칼로리 작은 순서대로 top-5
  - Fewer Carbohydrates - top-40 similarity 후 탄수화물 작은 순서대로 top-5
  - Less Fat - top-40 similarity 후 지방 작은 순서대로 top-5
  - More Fiber - top-40 similarity 후 섬유질 큰 순서대로 top-5
- 366명의 실험 참가자를 모집해서 실험을 진행하였습니다.
  - 실험 참가자 마다 5번의 실험을 진행
    - 참가자가 레시피를 검색해서 들어가면 아래 2가지 중 하나의 화면이 노출
      - 미리 준비된 5개의 리스트 중 하나를 골라 노출
      - 5개의 리스트를 전부 노출
    - 설명은 붙이는 경우도 있고 안붙이는 경우(Similar recipies)도 있음
    - 참가자는 레시피를 하나 고르고 레시피와 추천에 대해 만족도를 리포트

### Results

- 참가자의 피드백을 Structural Equation Modeling (SEM) 기법으로 분석하였습니다.
- 주목할 만한 결론은 다음과 같습니다.
  - Multi-list로 노출하면 설명 여부와 상관 없이 참가자들이 더 다양하게 추천된다고 느낍니다. (higher **perceived** diversity)
    - 실제로 다양하게 노출하는 것과는 다르고, 참가자들이 그렇게 느꼈다는 부분이 중요하다고 합니다.
  - 참가자들이 다양하게 추천된다고 느끼면, 아래 두 가지 현상이 나타납니다.
    - 하나의 아이템을 고르는데는 어려움을 느낍니다. (higher level of diversity, higher level of choice difficulty)
    - 추천의 만족도가 증가합니다. (perceived diversity was also positively related to choice satisfaction)
  - 참가자들이 추천이 나온 이유를 이해하면, 추천이 더 다양하다고 느낍니다.
  - Single-list 노출 시에는 추천에 대한 설명을 붙여주었을 때 참가자 만족도가 올라가지만, Multi-list 노출 시에는 설명이 있을 때 만족도가 소폭 하락하였습니다.
