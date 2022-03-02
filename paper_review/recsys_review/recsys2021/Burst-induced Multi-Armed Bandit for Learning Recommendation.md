## # Burst-induced Multi-Armed Bandit for Learning Recommendation
- Paper : https://dl.acm.org/doi/10.1145/3460231.3474250
- Authors : [[Rodrigo Alves]], [[Antoine Ledent]], [[Marius Kloft]]
- Reviewer : [[charlie.cs@kakaocorp.com]]
- Topics
	- [[Algorithmic Advances]]
	- [[Bandits and Reinforcement Learning]]
	- [[_RecSys2021]]

### Summary
- non-stationary & context-free MAB 상황에서 Cold-start recommendation (CSR) 을 위한 방법인 BMAB (Burst-induced MAB)을 제시하였습니다.
- 기존 non-stationary MAB(EXP3, Discounted-UCB etc.)의 방식과 비교되는 특징은 다음과 같습니다.
	1. context-free: feature vector가 필요하지 않습니다.
	2. reward 분포의 변화를 확인하는 대신, 시스템의 temporal dynamics를 활용합니다.

### Approach
#### Intuition
- 추천 환경에는 크게 두가지 상태가 있다고 가정: loyal (stable) state 그리고 curious (unstable) state
- 전체 time horizon은 일정 구간으로 나뉘어져서, 두 state 중 하나가 발생한다고 가정함
- loyal state는 구간에 상관없이, curious state는 구간마다 stationary payoff distribution를 가진다고 주장
	<img src="https://github.daumkakao.com/storage/user/8505/files/3a8902da-6ff6-4230-a59f-7a6ea0b8c22f" width=65%>
- state 마다 MAB 모델을 세우고, 특정 state 상황에 해당하는 모델을 이용하여 추천을 진행

#### Burst-induced MAB (BMAB)
- Algorithm
	1. 두 state (loyal, curious)마다 각각 K개의 beta parameter를 두고, orcale이 timestamp마다 어떤 state인지 알려줌
	2. state를 확인하면, 해당 state의 beta parameter를 통해 일반적인 Thompson Sampling 추천을 진행
	3. 만약 curious (s = 1) 에서 loyal (s = 0) 상태로 넘어가는 경우, curious state에 해당하는 beta parameter를 decay
	<img src="https://tva1.sinaimg.cn/large/008i3skNgy1gwg5vya71xj30ou0j6gno.jpg"  width=75%>

#### State Detector
- 매 timestamp 마다 어떤 state인지 파악하는 orcale을 구성하기 위해서는 homoheneous Poisson process에 대한 intensity (`lambda_L`)가 알려져 있다는 가정이 요구됨
	- intensity (function)는 쉽게 말하면 특정 구간에서 발생한 이벤트의 rate
	- 이 가정의 존재 이유는 문제 초기 정의 시, time series 가 두가지 stochastic point process의 mixture에 의해 생성된다는 가정이 있었기 때문
		- loyal: a homogeneous Possion process (HPP) with intensity `lambda_L`
		- curious: a piece-wise homogeneous Poisson process (PW-HPP) with intensity `lambda_C(t)`
	- 해당 intensity를 몰라도 쉽게 유추할 수 있다고 주장
	- 예시 (HPP with `lambda_L=3`, PW-HPP with `lambda_C in (0.15, 15)`)
		![image-20211123140547188](https://tva1.sinaimg.cn/large/008i3skNgy1gwp03l9ztij32wq0rawlv.jpg)
- Algorithm
  - state를 추정할 timestep 구간을 사이즈가 `Delta` 인 window로 나누고, 해당 구간이 intensity 가 `lambda_L` 인 Possion process에서 생성되었는지 검증
  - 즉, window 내 분포는 shape가 `Delta-1` 이고 scale이 `lambda_L` 인 Gamma distribution을 따르는지 확인
  - 해당 분포를 따른다면 loyal (`0`) 그렇지 않다면 curious (`1`)
	<img src="https://tva1.sinaimg.cn/large/008i3skNgy1gwg60ntwk5j30p40go0u5.jpg" alt="image-20211115224032770" width="65%" />
   - `q` 는 Gamma 분포의 quantile function
    - quantile function의 shape값이 `lambda-1` 인 이유는 `t_{i-\Delta+1}` 부터 event counting이 진행되기 때문
    - hypothesis testing의 목적은 burst period를 확인하기 위한 목적 (calm period는 loyal 에게 dominated)
      - 만약 `delta=0.95`라면 test는 다음과 같이 해석될 수 있음 
        : scale이 `lambda_L`인 event가 `Delta-1`번 발생할때까지 걸리는 time interval 분포 중, interval `Delta_i`가 분포의 quntaile 5% 내에 존재하는가?
      - 쉽게 말하면, 기존에 이벤트가 `N` 번 발생하는데 `X` 만큼 걸렸는데, `Y`는 그보다 더 짧은가?
- 해당 intensity를 몰라도 쉽게 유추할 수 있다고 주장
  - solve with EM - Burstiness scale: A parsimonious model for characterizing random series of events. In Proceedings of the 22nd ACM SIGKDD

### Results
- 합성 데이터, 실제 데이터 모두를 사용해서 제안한 방법을 평가하였습니다.
  - 제안한 방법들: BMAB-O (oracle), BMAB-R (detector) 
  - 실제 데이터의 경우, 전체 timeseries에서 일정 구간은 `lambda_L` 을 추정하는 구간으로 사용하고 나머지는 평가에 사용하였습니다.
- metric: average of the observed reward (`R(T)/N`), and its standard deviation
  - the user liked (Behance, MovieLens), searched (Google trends) or clicked on (Outbrain)
- baseline은 크게 세가지로 나뉩니다.
  - stationary: TS
  - non-stationary: EXP3
  - piece-wise stationary: EXP3DD, DUCB, MUCB, WMD

<img src="https://github.daumkakao.com/storage/user/8505/files/eef0ee00-4c7e-11ec-80d3-4771963435e9" alt="image-20211115222133822" style="zoom:50%;" />
- `K` : the number of arms, `N`: the number of events, `T`: the observed time
- 제안한 BMAB-R이 모든 dataset에서 reward가 우세하였습니다.
- [[MovieLens]]의 경우 제안한 방법이 TS과 거의 차이가 없었는데 이는 가장 인기있는 다섯개의 아이템이 stationary 하기 때문이라고 주장하였습니다.