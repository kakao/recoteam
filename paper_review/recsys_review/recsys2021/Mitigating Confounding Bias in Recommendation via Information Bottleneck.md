- Paper : https://dl.acm.org/doi/pdf/10.1145/3460231.3474263
- Authors : [[Dugang Liu]], [[Pengxiang Cheng]], [[Hong Zhu]], [[Zhenhua Dong]], [[Xiuqiang He]], [[Weike Pan]], [[Zhong Ming]]
- Reviewer : [[charlie.cs@kakaocorp.com]]
- Topics
	- #Privacy_Fairness_Bias
	- #Bias 
	- #RecSys2021

### Summary
* 추천 시스템에서 수집한 feedback 데이터의 bias를 효율적으로 완화(alleviate)할 수 있는 debiased information bottleneck (DIB) objective function을 제시하였습니다.
* 제시된 DIB objective function은 intractable 한데, 이를 information theory에 기반하여 tractable 한 solution으로 derive할 수 있었습니다.
* 기존 추천 시스템에서 debiased를 위한 대부분의 방법들은 bias generation process를 고려하지 않았기 때문에 특정 bias 가 발생하는 현상에서만 적용할 수 있는 문제가 있었습니다.
  * Related works: (1) heuristic-based (2) inverse propensity score-based (3) unbiased data augmentation (4) some theoretical tools-based
* 해당 논문에서는 confounding bias 라는 포괄적 형태의 bias를 정의하고, 이 bias를 완화하는 것에 초점을 두었습니다.

### Approach
#### Confounding Bias 

<img src="https://s2.loli.net/2022/01/11/wOSW7EnrHGF3CuR.png" alt="image-20220111043640043" width=100%>

* 일반적인 추천 시스템의 feedback event 생성 process는 Figure 1.(a)와 같습니다.

  * variable (the feature vector) `x`는 다음과 같은 세개의 변수로 구성되어 있다고 가정
    * Instrumental variables `I`, Confounder variables `C`, Adjustment variables `A`
  * 세 변수 중 `I`와 `C`는 treatment `T` 를 결정하고, 이는 outcome `y`에 간접적으로 영향을 미침
    * `T`는 시스템이 추천할 아이템을 선택하거나 아이템들을 rank 하는 과정을 의미하고, `y`는 추천 결과 (e.g. click)
    * 이 부분에서 position bias, popularity bias와 같은 다양한 bias가 feedback에 영향을 줌
  * `C` 와 `A`는 직접적으로 `y` 에 영향을 미침
    * unbiased feedback이 생성됨
  * 세 변수에 대한 구체적인 정의는 없지만, site된 논문(*Learning disentangled representations for counterfactual regression, ICLR 2020*)에서 예시를 통해 어느정도 이해할 수 있었음
    * 어떤 환자에 대한 context `x`를 기반으로 치료 방법 `T`를 정하고, 치료에 따른 결과 `y`가 있다고 가정
    * `I`는 환자의 재정 상태를 나타낼 수 있음: 부자면 높은 수준의 치료를 받거나 가난하면 저렴한 치료를 받아야 한다. 다만, 이것이 직접적으로 치료 결과에 영향을 미치진 않음
    * `C` 는 환자의 나이를 나타낼 수 있음: 나이에 따라 어떤 치료를 받는지도 결정되고, 나이가 치료 결과에 직접적인 영향을 미침
    * `A`는 환자의 유전적 정보를 나타낼 수 있음: 유전적 정보를 가지고 어떤 치료를 받을지는 일반적으로 고려하진 않지만, 이것이 치료 결과에 직접적인 영향을 미침 

* Confounding bias는 특정 bias들의 collection을 나타내며, 추천 시스템에서 간접적인 영향으로 인해 발생하는 the confusion of the observed feedback을 의미하게 됩니다.

  * 쉽게 말하면 Figure  1.(a) 와 1.(b)의 차이가 confounding bias 
  * Figure 1.(b)는 `x`를 고려하지 않은 추천이므로, uniform random 추천을 생각할 수 있습니다.

#### The proposed method: DIB objective function

 <img src="https://s2.loli.net/2022/01/11/AMLDoOWieNzfFnp.png" alt="image-20220111050625755" style="zoom:80%;" />

* 이 논문에서는 위에서 언급한 confounding bias가 embedding representation에 반영된다고 가정하고, embedding vector에 포함된 biased component `r`과 unbiased component `z`를 각각 학습 후, 실제 추천을 진행할 때는 `z`로만 구성된 feature vector로 treatment `T`를 선택하는 방향을 제시하였습니다.
* `r`과 `z`를 제대로 학습하기 위해서는 다음과 같은 조건들을 만족해야 합니다.
  1. biased된 변수의 영향을 줄이기 위해서 `z` 가 `x`에 대해 overfit 되면 안됩니다.
  2. `z`는 label `y`를 정확하게 예측할 수 있도록 학습합니다. (direct effect 최대화)
  3. `r`과 `z` 는 가능한 독립이어야 합니다. (to get a better distinction)
  4. `r` 도 (`z` 정도 까지는 아니지만) `y` 를 예측할 수 있도록 학습합니다. (indirect effect)
* 위와 같은 네 가지 조건을 만족하기 위해 다음과 같은 DIB objective function을 최소화 하는 방향으로 학습합니다.
  : <img src="https://s2.loli.net/2022/01/11/t4miVPOTF3BjWwc.png" alt="image-20220111051804149" style="zoom:80%;" />
  * `I(z;x)` 는 `x`와 `z`의 mutual information을 나타냅니다.
* 이 함수는 최적화 하기에는 intractable 하므로, information theory에 기반하여 다음과 같이 conditional entropy 형태로 표현할 수 있습니다.
  : <img src="https://s2.loli.net/2022/01/11/3HfXnKrsVFodJlw.png" alt="image-20220111052034787" style="zoom: 80%;" />
  * (a)는 `y`와 `y_z`간 cross entropy, (b)는 `y` 와 `y_r` 간 cross entropy, (c)는 `y`와  `y_{z,r}` 간 cross entropy
    * 여기서 `y_z`는 unbiased component `z`를 사용해서 생성된 label 이고, `y_r` 과 `y_{z,r}` 도 비슷한 맥락으로 생성된 label 
  * (d)는 embedding representation의 robustness를 추가하기 위한 regularization term
    * variational approximation을 활용하여 `z`는 Gaussian 분포를 따른다고 가정했습니다.

#### Complement optimization process of DIB

<img src="https://s2.loli.net/2022/01/11/TiRa7SY62OHDKdX.png" alt="image-20220111052747711" width=70%/>

### Results

* 기존의 추천 모델 Matrix Factorization (MF)과 neural collaborative filtering (NCF)에 DIB를 적용하여 학습했을 때, 상대적으로 어느정도의 성능 향상이 있는지 실험하였습니다.
  * 측정 metrics: AUC, precision (P@K), recall (R@K), 그리고 nDCG(@50)
* 두 개의 dataset을 사용: Yahoo! R3, Product
  * [[Yahoo! R3]]: 15,400 명 사용자의 1,000개 곡에 대한 ratings
  * [[Product]]: 300,000 명 사용자의 122개 광고에 대한 click records
  * test를 위해 unbiased 데이터를 확보해야 하는데, 이를 위해 일정 유저 군에게 랜덤 추천을 진행했다고 합니다.
* Baselines
  * MF, NCF (classic reco models) / IPS, SNIPS (IPS-based) / AT, Rel, CVIB (theoretical tools-based)

#### MF

![image-20220111052916688](https://s2.loli.net/2022/01/11/CD2OhbjpTRe3ukA.png)

* 제안한 DIB-MF가 가장 높은 성능을 보였습니다.
* dataset 사이즈가 커질수록 상대적으로 높은 성능을 보였습니다.

#### NCF

![image-20220111053025025](https://s2.loli.net/2022/01/11/LGXFpr7stONHVjd.png)

* metric@K 가 높을수록 좋은 성능을 보였습니다.