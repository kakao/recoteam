- Paper : https://arxiv.org/abs/2109.08052
- Authors : [[Ambareesh Revanur]], [[Vijay Kuma]], [[Deepthi Sharma]]
- Reviewer : matthew.g@kakaocorp.com
- Topics
	- #Real-World_Concerns 
	- #Semi-Supervised_Learning 
	- #RecSys2021

### Summary
- Semi-Supervised Learning을 사용한 다른 모델들과 다르게, conditional mask를 통해서 color와 pattern 같은 attribute를 학습하는 것이 아니라 color, shape를 직접적으로 변경해주는 self-supervised learning의 방법론을 적용하였습니다.
- pseudo-labeling를 이용하여 unlabeled-image를 이용하여 학습을 진행하였습니다.
- [[Polyvore]], [[Polyvore-D]], newly created [[Fashion outfit]] dataset에 대해서, 적은 수의 labeled data를 사용하였고, text 등과 같은 metadata 를 전혀 사용하지 않았음에도 supervised method에 준하는 결과를 만들었습니다.

### Introduction

#### Fashion Compatibility

- 이 논문의 main task. 한글로 번역하면 **잘 어울리는 룩 만들기** 정도?로 볼 수 있을 것 같습니다.

> compose matching clothing items that are appealing and complement well.

#### Problem & Contribution

- 기존에는 handcraft labeling 을 했었으나 그걸 매번 진행하기에는 번거롭고 cost가 많이 듭니다.
- 이를 해결하고자 **semi-supervised learning** 기법을 적용하였습니다.
  - 적은 양의 labeled data, 많은 양의 unlabeled data를 이용하여 supervised training에 준하는 학습 효과를 냄과 동시에, supervised learning의 단점인 overfitting을 해소하고, 일반화 성능을 끌어올리고자 하였습니다.
  - 다양한 기법 및 방법론이 존재하는데, 더 자세한 내용은 이 [포스팅](https://sanghyu.tistory.com/177)이 도움이 되었으니 읽어보시면 좋을 것 같습니다.
  - 이 논문에서는 다양한 기법 중에 아래와 같은 기법들을 도입하였습니다.
    - Proxy-label 기법 (labeled data로 학습한 뒤, unlabeled data를 labeling하고 그걸로 재학습.)
    - consistency regularization 기법 (기존 데이터에 대해서 일부 perturbated 된 데이터에 대해서도 예측의 결과는 일관성이 있어야 한다.)

#### Main Assumption
- 기존 모델들처럼 각각의 attrbute를 implicit하게 배우는 것이 아니라 (MMoE와 같은 형태로 K개로 표현된 FFN의 모음으로 모델 구성.), explicit하게 attribute를 설정 (color, shape) 하고 해당 부분에 대한 특징을 표현하는 Representation을 찾고자 하였습니다.

### Approach
- 원하는 것은 `visual representation for the task of fashion compatibility`를 학습하는 것입니다.
  - Metric Learning을 적용한 목적함수를 설계하여 compatible한 아이템끼리의 embedding은 가깝게 하고자 하였습니다.
  - 이를 위해 (Anchor, pseudo-positive, negative) triplet을 만들어 학습을 진행하였습니다.

#### Loss
$$
\mathcal{L} = \mathcal{L_l} + \lambda_{ss}\mathcal{L_{ss}} + \lambda_{pseudo}\mathcal{L_{pseudo}}\\
\mathcal{L_l} = \max{(0, d(\phi_A, \phi_P) - d(\phi_A, \phi_N) + m)}\\
\mathcal{L_ss} = \max{(0, d(\hat{\phi_{u}}, \hat{\phi_{[s]}}) - d(\hat{\phi_{u}}, \hat{\phi_{[a]}}) + m)}\\
\mathcal{L_{pseudo}} = \max{(0, d(\hat{\phi_{A}}, \hat{\phi_{P}}) - d(\hat{\phi_{u}}, \hat{\phi_{N}}) + m)}
$$
- Loss on Labeled item
	기존에 존재하는 labeled data (A, P, N) 에 대해서는 A와 P는 가깝게, A와 N은 멀어지도록 학습을 진행하였습니다. 추가로 margin loss도 두었습니다.

#### Loss on Consistency Regularization
- Self-supervised learning에서 일반적으로 사용되는 접근을 차용하였습니다.
  - Consistency Regularization의 가설 중 `perturbation`에 해당하는 전처리 방법을 self-supervised learning 관련 논문에서 영감을 받아 적용하였습니다.
- `fashion compatibility를 위해서는 fashion item을 구분하는 중요한 attribute (color, shape)에 대한 구분 능력이 필요하다`는 전제를 이용하여, 한 아이템에 대해서 color와 shape를 바꾼 negative sample과의 discrepancy를 늘리는 방향으로 학습을 진행하였습니다.
- 이러한 방법론들이 이미지를 돌리거나, color jittering을 하거나, 이미지에 대한 직소 퍼즐 형태의 퀴즈를 풀거나 하는 self-supervised learning에서의 pretext task와 비슷한 경향이 있어서 논문에서 그렇게 언급한 것으로 보입니다.

#### Data Augmentation on Pseudo-Labeled Data
- (A, P, N) 에 대해서 embedding space에서의 nearest element (A', P', N')를 on-the-fly로 계산하고 이에 대한 margin loss를 계산하였습니다.
- 계산 상의 속도를 높이고자 mini-batch 내에서만 nearest element를 찾는 방법을 취하였습니다.

#### Model Structure
- siamese network와 비슷한 구조를 가지고 있습니다.
  - ImageNet pretrained CNN (ResNet18) -> fully-connected layer per category ($W_c$)
- 학습 파라미터는 다음과 같습니다.
	- 256 batch size for labeled data, 1024 batch size for unlabeled data
	- margin $m$ 을 0.4 for margin loss
	- $\lambda_{ss}=0.1\quad\lambda_{pseudo}=1$
	- adam optimizer, lr 5e-5, 10 epochs

### Results
- [[Polyvore]] (패션 커머스 서비스, ssense에 최근 합병됨) dataset, [[Polyvore-disjoint]] (Polyvore 중에서 train/valid/test에 중복된 이미지가 없도록 처리한 것), [[Fashion outfits]] (e-commerce platform에서 데이터를 크롤링하고 **같은 세션에서 산 아이템의 경우 compatible하다고 가정**)를 이용하여 학습을 진행하였습니다.
- 5%의 labeled data만을 이용하여 supervised learning에 준하는 학습 결과를 얻을 수 있었으며 100%를 적용하면 supervised model들을 상회하는 성능을 보여주었습니다.
