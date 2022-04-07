- Paper : https://dl.acm.org/doi/10.1145/3460231.3474248
- Authors : [[Olivier Jeunen]], [[Bart Goethals]]
- Reviewer : [[charlie.cs@kakaocorp.com]]
- Topics
	- #Algorithmic_Advances 
	- #Bandits_and_Reinforcement_Learning 
	- #RecSys2021

### Summary
- "equity of exposure" principle 이 어떻게 추천을 위한 top-K contextual bandit의 문제에 적용될 수 있는지 조사(investigate)한 논문입니다.
	- equity of exposure: 동일한 relevance를 가진 아이템들은 동일한 노출이 있을 것을 기대하게 됩니다.(_items of equal relevance should receive equal exposure in expectation_)
- 기존 추천 시스템의 사용자 중심 utility(click or relevance)에 대한 최적화 방식은 시스템 내 다른 관계자(stakeholders)들에겐 악영향을 끼칠 수 있습니다.
	- 예시) 음악 스트리밍, 음식 배달, e-commerce, 그리고 viewtab
- top-K contextual bandits 추천에서 relevance-fairness trade-off 문제를 다룰 수 있는 EARS (Exposure-Aware aRm Selection) 알고리즘을 제시하였습니다.
	- model-agnostic algorithm이라 기존 bandit system에 적용이 가능합니다.

### Approach
#### Intuition
* 사용자마다 추천 결과에 적용된 diversify의 반응이 다르며, 랜덤한 추천에 대해서 얼마나 열려(openness)있는지의 정도 또한 다양하다는 것을 관찰한 연구가 있습니다.
  * _Investigating Listeners’ Responses to Divergent Recommendations. R. Mehrotra, et al. RecSys' 20_
* 이를 통해 단순히 모든 사용자에게 relevance-fairness의 trade-off 정도를 동일하게 적용하기 보다는 특정 유저 군에 한하여 적용하면 좋을 수 있습니다.
  * 예시) good choice for *diverse* and *average* users, but worse for *focused* users. 
  * <img src="https://s2.loli.net/2021/12/14/SAWGsy6zX3rC5aP.png" width="70%" />   .    
     * x-axis: top-12 items for a given user.   
     * y-axis: the probability of relevance over these items for that user.

#### Exposure-Aware aRm Selection (EARS)
* 아이템이 클릭될 확률 `P(C)` 는 사용자가 이 아이템이 연관 있다고 고려할 확률 `P(R)`과 그 사용자에게 노출될 확률 `P(E)` 로 factorize될 수 있습니다.
  * <img src="https://tva1.sinaimg.cn/large/008i3skNgy1gxcz1xaqdkj30gc02y0sq.jpg" width="50%" />    
* 그리고 fairness of exposure을 목적하는 알고리즘은 다음과 같은 두 조건부 확률 분포 간 statistical divergence, 즉 disparity를 최소화하는 것으로 볼 수 있습니다.: `D(P(A|R); P(A|C))`

  * 본 논문에서는 f-divergences로 Hellinger distance를 사용합니다.
* EARS algorithm Figure
  * <img src="https://s2.loli.net/2021/12/14/Tu2U6VRj71MECck.png" width="70%" />  
  * Default bandit 알고리즘으로 logistic regression thompson sampling을 사용합니다.
    * *An Empirical Evaluation of Thompson Sampling. L. Li, et al. NIPS' 11*
  * EARS의 목적은 최대 ε 만큼의 expected clicks을 잃으면서 disparity를 최소화하는 것입니다. 
    * Algorithm 4.(3)의 greedy policy에서 얻을 수 있는 추천 결과에 diversifying(shuffling)을 적용했을 경우(4.(4)의 equity policy), 최대 (1 - ε) * 100 % 만큼의 expected clicks 을 보존하는 선까지 disparity를 최소화합니다.
    * In experiments, `ε={0.01, 0.025, 0.05, 0.1}`
  * shuffle 방식은 random shuffling
    * 위에서 설명한 ε 조건을 만족할 수 있을 때까지 K값을 감소시키면서 shuffle을 진행합니다.
    * Why? 상위 추천 결과에서 shuffle을 진행해야 expected clicks 손해가 적고, 그에 따른 disparity 감소가 크기 때문입니다.

### Results ([github](https://github.com/olivierjeunen/EARS-recsys-2021))

* Real-world data from the [[Deezer]] music streaming platform
  * Relevance information between 862 playlists (items) and 974,960 users.
  * Users are represented by a dense 97d feature vector.
  * 추천 결과 수: top- `K`=12 
  * 매 round 마다 사용자를 20,000명 복원 추출하여 추천 결과 제공하고, batch로 parameter를 업데이트합니다.

* EARS algorithm에서 tolerance parameter ε 값을 조절해가며 실험하였습니다.: `{0.01, 0.025, 0.05, 0.1}  ` 
  * baseline은 greedy approach
* Carousel-기반의 추천 환경 (*Personalization in Music Streaming Apps with Contextual Bandits. W.Bendada. et al. Recsys' 20*)
  * <img src="https://s2.loli.net/2021/12/14/HlxNMSPs6ZYOVnR.png" width="30%" />  
  * 사용자가 추천 결과를 보다가 중간에 포기할 확률 abandonment parameter `γ(=0.9)` 을 포함합니다.
* EARS에서 사용할 Expected clicks 값 계산
  * Greedy approach
    * <img src="https://tva1.sinaimg.cn/large/008i3skNgy1gxd09llzwnj30x20cidgw.jpg" width="75%" />  

  * Shuffling approach
    * greedy 와 동일하지만, 추천 결과를 K개까지 shuffling 한 모든 조합에 대해서 expected clicks을 일일이 구해야하므로 `O(K!)` 만큼의 비용이 소모됩니다.
    * 논문에서는 이를 효율적으로 계산하기 위한 방법을 제시했고, `O(K*2^(K-1)*(K-1))`까지 복잡도를 줄였다고 합니다.


#### 실험 결과

<img src="https://s2.loli.net/2021/12/14/X9FnyGpm5DLSN7T.png" />  

* Figure 4(a): EARS’ Impact on Expected Reward
  * `ε=0.01`일 때 greedy 보다 성능이 좋았는데, 이에 대한 이유를 두 가지로 설명합니다.
    * (1) EARS의 rank 방식을 통해 positional bias를 완화하여 모델이 `P(R)` 대신 `P(C)`를 학습하게 됩니다.
    * (2) top-K list를 랜덤으로 섞으면서 매 라운드마다 배치로 학습할 데이터가 더욱 diverse 해집니다.
* Figure 4(b): EARS’ Impact on Exposure Disparity
  * greedy 방식이 가장 큰 disparity를 보였고, ε이 증가할수록 조금씩 감소합니다.
* Figure 4(c): EARS’ Relevance-Fairness Trade-Off
  * Rounds 20부터 수렴까지 4(a)와 4(b)의 measurement를 plot
  * expected clicks과 expected disparity의 linear한 관계를 확인할 수 있었습니다.
  * `ε=0.01`의 경우 greedy 방식에 비교했을 때, expected reward 증가와 disparity 감소를 보입니다.

### Conclusion
* 컨텐츠의 노출에 따라 수익이 발생하는 환경이면 이와 관련된 이슈가 있을 것 같다는 생각이 들었습니다.
* 제안된 EARS 알고리즘은 cost가 높고, 단순 랜덤 셔플 방식이라 실제로 적용하기는 좋아보이지 않았습니다. (K 또한 낮았음)
* 다만, 사용자에 따라 다양화가 적용되는 정도가 달라져야 한다는 insight를 얻을 수 있어서 좋았습니다.
