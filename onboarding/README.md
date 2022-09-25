# 추천팀 온보딩

_카카오 추천팀에 입사하기 전에 미리 보시면 좋을 내용들을 정리해놓은 문서입니다._

## 목차
1. 추천 기술 관련 자료
   1. 수학/ML 기초
   2. 추천 알고리즘
   3. 그 외

2. ...

## 추천 기술 관련 자료
*해당 내용은 방대하므로(특히 수학/ML 기초) 필요한 부분들 위주로 보시기 바랍니다.*
### 수학/ML 기초
* 추천 시스템은 머신러닝의 응용분야로서 머신러닝에 대한 기초지식을 탄탄히 다지는 것은 큰 도움이 됩니다
* 기본적인 Linear Algebra, Statistical Inference, Convex Optimization에 대해 익숙하지 않다면 이에 대한 학습이 필요 할 수 있습니다
* 대표적인 ML 교재 최소 1개 이상을 정독해본 경험을 가지는 것을 추천드립니다
  * [Introduction to Statistical Learning (ISLR)](https://www.statlearning.com/)
  * [Elements of Statistical Learning (ESL)](https://hastie.su.domains/Papers/ESLII.pdf)
  * [Machine Learning: A Probabilistic Perspective (Murphey 책)](https://probml.github.io/pml-book/)
  * [Pattern Recognition an Machine Learning (Bishop 책)](https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf)
  * ... etc.
* 딥러닝 교재, 최신 추천시스템은 뉴럴넷을 활용하는 경우도 많고 자연어, 이미지 등의 데이터를 활용하는 경우도 있습니다
  * [Deep Learning Book](https://www.deeplearningbook.org/)
  * ... etc.

### 추천 알고리즘
* 대표적인 올드스쿨 알고리즘들, 해당 알고리즘들은 논문이 발표된지 오래되었지만 아직도 대중적으로 많이 활용되고 있음
  * iALS ([Collaborative Filtering for Implicit Feedback Datasets](http://yifanhu.net/PUB/cf.pdf))
  * BPR ([BPR: Bayesian Personalized Ranking from Implicit Feedback](https://arxiv.org/pdf/1205.2618.pdf))
  * LinUCB ([A Contextual-Bandit Approach to Personalized News Article Recommendation](https://arxiv.org/pdf/1003.0146.pdf))
* 카카오 테크블로그에 카카오 추천시스템에 대하여 주제별로 설명한 글들
  * [테크 블로그: 추천 시스템](https://github.com/kakao/recoteam#%EC%B6%94%EC%B2%9C-%EC%8B%9C%EC%8A%A4%ED%85%9C)
* 추천 관련 최신 논문들을 서칭해보고 abstract와 related works를 읽어보면 최신 연구방향과 그 기반이 되는 주요 논문들을 알 수 있음
  * 추천 관련 대표 학회들: RecSys, WWW, SIGIR, KDD, WSDM, CIKM, AAAI, IJCAI, ICML, NeurIPS, ... etc.
* (좋은 논문인지와 별개로) 대표적으로 유명한 추천 알고리즘 논문들
  * [BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations from Transformer, CIKM'19](https://arxiv.org/abs/1904.06690)
  * [Variational Autoencoders for Collaborative Filtering, WWW'18](https://dl.acm.org/doi/10.1145/3178876.3186150)
  * [Neural Collaborative Filtering, WWW'17](https://dl.acm.org/doi/10.1145/3038912.3052569)
  * [Recommending What Video to Watch Next: A Multitask Ranking System, RecSys'19](https://daiwk.github.io/assets/youtube-multitask.pdf)
  * [Collaborative Metric Learning, WWW'17](https://vision.cornell.edu/se3/wp-content/uploads/2017/03/WWW-fp0554-hsiehA.pdf)

### 그 외
* 강화학습
  * 실시간 추천시스템은 사용자와 상호작용하며 사용자들의 취향을 파악하고 추천을 해주는 시스템으로서 강화학습 framework이 잘 어울린다는 평가가 많다, 특히 Multi-Armed Bandit, Contextual-Bandit 등은 팀 내에서도 많이 사용된다
  * [강화학습 대표 교재 (Reinforcement Learning: An Introduction)](http://incompleteideas.net/book/the-book.html))
  * [David Silver 강의](https://www.davidsilver.uk/teaching/)

## Section2
...
