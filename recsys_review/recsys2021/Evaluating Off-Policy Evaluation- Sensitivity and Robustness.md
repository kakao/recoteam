## Evaluating Off-Policy Evaluation: Sensitivity and Robustness
- Paper : https://arxiv.org/abs/2108.13703
- Authors : [[Yuta Saito]], [[Takuma Udagawa]], [[Haruka Kiyohara]], [[Kazuki Mogi]], [[Yusuke Narita]], [[Kei Tateno]]
- Reviewer : [[iggy.ll@kakaocorp.com]]
- Topics
	- [[Metrics and Evaluation]]
	- [[_RecSys2021]]

### Summary
- 이 논문의 목표는 online에 올려보지 않고 모델을 평가하는 것입니다.
![image](https://github.daumkakao.com/storage/user/8290/files/d6c35341-c62a-43d6-b3cf-9faf3b12a36a)
- 모델: 유저가 페이지에 접속했을 때, 유저의 정보, 시간 정보 등을 활용해 A안/B안/C안 중 어떤게 나을 지 확률적으로 결정합니다. e.g., [0.4, 0.3, 0,3]

![image](https://github.daumkakao.com/storage/user/8290/files/bb384d2d-d4dc-4772-8fd9-4033ad1949ea)
- context x: 유저가 접속한 시간, 유저 정보 등.
- action: 보여준 페이지 레이아웃
- reward:유저가 클릭했거나 안 했거나, 우리가 보여준 레이아웃에 따른 유저의 행동 결과(숫자)
 여기서 문제는 $p(r_i...)$를 알 수가 없다는 점과, 모델이 아이템을 선택해서 보여주어야 그에 대한 결과를 만들 수 있다는 점이 있습니다.

### Approach
Off Policy Evaluation은 두 가지 분류로 나눌 수 있습니다.
 1. Direct Method (DM): mean reward 자체를 estimate하는 방법
 2. Inverse Propensity Weight (IPW), SNIPW: logging policy, or base policy의 log를 요구하는 방법
그리고 저 두 가지 방법을 함께 사용하는 방법들도 있습니다.: DR, SNDR, Switch-DR, DRos

DM은 모델을 하나 더 만들어야 하기 때문에, 이 모델에 관한 하이퍼패러미터를 또 신경써주어야 합니다.

![image](https://github.daumkakao.com/storage/user/8290/files/bfc00e1a-9c31-4afc-9a37-8865276f245d)


### Conclusion
- mean reward를 estimate하기 어렵기 때문에  계열의 방법은 사용하지 않는게 좋을 것 같습니다.
- SNIPW가 일반적으로 가장 괜찮았습니다. (적절히 Calibration해줄 수 있다면 IPW를 써도 괜찮을 것 같습니다.)
- 적절히 Calibration해줄 수 있다면 logging policy를 estimate한 값으로 (logging policy를 따라하도록 다른 모델을 학습해서) 사용해도 나쁘지 않아 보입니다.
  - 이건 조금 이상한게, logging policy를 이미 갖고 있으면 이를 사용하지 왜 다른 estimator를 더 만들어야 하는지는 잘 모르겠습니다.

![image](https://github.daumkakao.com/storage/user/8290/files/29f60c79-0304-484d-adc6-ba399e1025f8)
