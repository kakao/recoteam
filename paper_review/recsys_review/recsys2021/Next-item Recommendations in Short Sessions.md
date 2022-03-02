## Next-item Recommendations in Short Sessions
- Paper : https://arxiv.org/abs/2107.07453
- Authors : [[Wenzhuo Song]], [[Shoujin Wang]], [[Yan Wang]], [[Shengsheng Wang]]
- Reviewer : [[marv.20@kakaocorp.com]]
- Topics
	- [[Algorithmic Advances]]
	- [[Sequential Recommendation]]
	- [[Cold Start]]
	- [[Few-Shot Learning]]
	- [[_RecSys2021]]

### Summary
- 짧은 길이의 세션에 대해, 유사한 유저들의 세션을 가져온 다음(global module), 유저의 현재 세션과 결합(local module)한 뒤 Few-Shot Learning을 통해 추천(prediction module)하는 모델을 제안하였습니다.
- [[Delicious]], [[Reddit]] 데이터셋에서 기존 single / multi session 기반 모델들보다 좋은 성능을 보여주었습니다. 세션길이가 짧을 때 더 우수한 상대 지표를 보여주었습니다.

### Approach
#### 1. 문제 정의

- 실제 환경에서의 세션 기반 추천에서 대부분은 매우 짧은 세션입니다. 짧은 세션에서는 문맥에 대한 정보가 매우 제한적이고, 유사한 유저의 정보를 효율적으로 사용하지 못하며, 관련 있는 세션들을 어떻게 결합할 지에 대한 연구도 잘 이뤄지지 못했습니다.
- 이 논문에서는 현재 세션과 유사한 세션을 찾고, 이를 현재 세션의 정보와 결합하여 추천을 내보내는 INSERT 모델을 제안하였습니다.



#### 2. 모델 구조
<img width="600" alt="Screen Shot 2022-01-18 at 3 16 27 PM" src="https://github.daumkakao.com/storage/user/6543/files/c88e3927-c7a6-449d-8313-03dfe979fefe">

- Global Module : 유사한 유저들의 세션 정보를 활용하는 모듈입니다.
	- Candidate Similar Session Sets : 같은 아이템을 얼마나 interact하는 지의 여부로 판단됩니다.
	<img width="150" alt="Screen Shot 2022-01-18 at 4 46 21 PM" src="https://github.daumkakao.com/storage/user/6543/files/da025854-cc8d-4d83-ba69-65b37e721901">
	
	- Session Encoder : weighted sum of item embedding입니다.
	- SSRN : candidate에서 item embedding 각각에 대해 RNN을 구한 다음 similarity의 max pool을 취하게 됩니다.
	<img width="600" alt="Screen Shot 2022-02-14 at 6 34 49 PM" src="https://github.daumkakao.com/storage/user/6543/files/05ac5713-2649-4efc-b187-55d7d2bf5661">
- Local Module : item sequence -> GRU
- Prediction Module :  MLP + softmax


### Results
<img width="743" alt="Screen Shot 2022-01-18 at 4 40 09 PM" src="https://github.daumkakao.com/storage/user/6543/files/094531e6-8936-4d46-be7e-f664067c403b">

<img width="679" alt="Screen Shot 2022-01-18 at 4 40 28 PM" src="https://github.daumkakao.com/storage/user/6543/files/efbaf9dc-8b0c-4a9c-973d-82e8a9829e08">

- [[Delicious]], [[Reddit]]에서 짧은 세션들을 뽑아 평가하였습니다.
- 논문에서 제안된 모델이 기존 session-based 모델들보다 짧은 세션에서 더 좋은 성능을 보였습니다.

### Conclusion
- FSL이라고 하지만 FSL의 장점인 in-context learning이 잘 발휘되어 보이지는 않았습니다.
- 세션 기반 추천에서 유사 유저의 세션을 넣는 방법은 참고할 만한 부분인 것 같습니다.