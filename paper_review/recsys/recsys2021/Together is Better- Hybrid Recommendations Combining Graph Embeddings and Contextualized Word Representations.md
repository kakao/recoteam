# Together is Better- Hybrid Recommendations Combining Graph Embeddings and Contextualized Word Representations

- Paper : <https://dl.acm.org/doi/abs/10.1145/3460231.3474272>
- Authors : Marco Polignano, Cataldo Musto, Marco de Gemmis, Pasquale Lops, Giovanni Semeraro
- Reviewer : tony.yoo
- Topics
  - [#Language_and_Knowledge](../../topics/Language%20and%20Knowledge.md)
  - #Graph
  - #Sequence_Modeling
  - [#RecSys2021](RecSys2021.md)

## Summary

Main author: [Marco Polignano](https://scholar.google.it/citations?user=sjQSYGQAAAAJ&hl=it) - BERT 기반의 감정 분석 연구를 많이 하신것 같습니다.

- 두 가지 다른 정보(interaction feedback, text information)로 부터 user, item 임베딩을 얻는 hybrid 방법 제시하였습니다.
  - 정보를 융합하는 방법은 두 가지 concatenation 방법을 제시하였습니다.
  - 기본 architecture: Two-tower 모델과 같습니다.

<img src="https://user-images.githubusercontent.com/38134957/165453439-f3d2480f-69d5-487b-905f-7640927d1085.png" style="zoom:50%;" />

양쪽 방향이 같은 구조를 띄무로 한쪽 방향에 대해서만 표현하였습니다.
| Entity-based | Feature-based |
|--|--|
| <img src="https://user-images.githubusercontent.com/38134957/165453456-d22d9141-eca7-4fe9-b305-d194de75c8b1.png" width="80%"> | <img src="https://user-images.githubusercontent.com/38134957/165453460-f28ad0a6-44a5-4da4-a111-0404affc513b.png" width="80%"> |
|각 entity의 intrinsic charateristic 을 배움 | heterogenous 한 두 entity 사이의 relationship을 배움 |

다음의 두가지 모듈로 구성되있고, Sota 모델로 바꾸는게 쉽게 가능합니다.

- Collaborative Filtering 모듈: graph embedding 방법을 사용합니다.
- Content-based 모듈: contextual word representation 방법을 사용합니다.

## Approach

### Graph Embedding

다음 두개의 모델 사용. (이 외에도 TransR, TransD, ... 많은 모델 존재. [survey paper](https://www.mdpi.com/2073-8994/13/3/485/htm) 참고.)

- [TransE, NIPS'13](https://papers.nips.cc/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html)
- [TransH, AAAI'14](https://ojs.aaai.org/index.php/AAAI/article/view/8870)

이 모델은 본래 Knowledge graph 에서 entity(head)-relation-entity(tail)의 triple 정보를 임베딩에 반영하고자 한 방법. 추천시스템에서 유저, 아이템을 entity, 평점을 relation으로 생각 가능. 다음과 같은 관계로 임베딩.

| - | TransE | TransH |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Architecture | <img src="https://user-images.githubusercontent.com/38134957/165453533-45b48c87-ceff-4e82-b009-3be1322d6f94.png" style="zoom:40%;" /> | <img src="https://user-images.githubusercontent.com/38134957/165453540-f5375f62-a31a-46a5-b700-4a599d34b6b9.png" style="zoom:40%;" /> |
| Score function | $\Vert \textbf{h} + \textbf{d}_r - \textbf{t} \Vert _{2}^2$ | $\Vert \textbf{h}_{\bot} + \textbf{d}*r - \textbf{t}_{\bot} \Vert _{2}^2$ |

> TransE 에서 "동일 entity가 여러 relation에서 구분이 안된다"는 단점을 TransH에서 hyperplane을 도입시킴으로써 해결.

### Contextual Word Reprentation

Text 정보를 임베딩. 둘다 Transformer 기반의 모델. (자세한 설명 생략)

- [BERT, NAACL'19](https://arxiv.org/abs/1810.04805)
- [USE, ICLR'19](https://arxiv.org/abs/1804.07461)

## Results

### Dataset

비교적 적은 데이터셋. 참고할 점은 train, test 셋을 나눌때, positive 비율을 train과 동일하게 나눔.
<img src="https://user-images.githubusercontent.com/38134957/165453586-8ba4b994-2d45-4f58-9594-e3a810679141.png" style="zoom:80%;" />

### Protocol

[TestRating](https://dl.acm.org/doi/10.1145/2043932.2043996) strategy 사용. 각 유저별로 테스트 셋에 있는 rating만 예측. ranking을 구할때는 예측한 평점들을 sorting하여 구함.
<img src="https://user-images.githubusercontent.com/38134957/165453619-20aa2173-20a3-4c76-be9f-634204d3dd5c.png" style="zoom:50%;" />

> **비평:** 이 방법을 사용하면 topk 보다 test 아이템의 수가 적으면 무조껀 ranking안에 포함되고, 순서 맞추기 싸움이 됨. 기본적으로 ndcg가 높음.
>
> <img src="https://user-images.githubusercontent.com/38134957/165453674-e668d165-7bef-43ed-b43b-986877cb9753.png" style="zoom:50%;" />

### Performance

| error-based | ranking-based |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![image](https://user-images.githubusercontent.com/38134957/165453712-4c0144d4-9802-4c9b-8ac9-4bc9578647c4.png) | ![image](https://user-images.githubusercontent.com/38134957/165453719-41a29bbd-3260-446f-8d0d-df40f7293eaf.png) |
| ![image](https://user-images.githubusercontent.com/38134957/165453712-4c0144d4-9802-4c9b-8ac9-4bc9578647c4.png) | ![image](https://user-images.githubusercontent.com/38134957/165454052-433ede9d-1b49-4a8f-bc79-51a69dfe878a.png) |

- TransE 와 TransH의 우위는 domain 에 따라 다르다.
- 논문 제목에서 강조하듯 Together is better. Collaborative 방법과 content방법의 시너지 효과.
- concatenate 방법은 Feature based 방법이 더 효과적.

[Open benchmark - Movielens 1M](https://paperswithcode.com/sota/collaborative-filtering-on-movielens-1m?metric=nDCG%4010)

<img src="https://user-images.githubusercontent.com/38134957/165454097-c7ce869c-3680-46fb-9697-ce6219b308b4.png" style="zoom:50%;" />

위의 오픈 벤치 마킹 정보에 의한 nDCG@10 Score와는 다른 test evaluation 프로토콜을 사용하였기 때문에 참고 부탁드립니다.

## Conclusion

- user, item 임베딩을 얻는 두가지 hybrid 방법(entity, feature-based)을 제시하였습니다.
- 모델 architecture가 simple하여 sota 모델을 쉽게 적용 가능할 수 있고 성능도 우수합니다.

### Weak points

- CF 기반 모델에서 interaction 정보만 사용할 거면 굳이 graph model을 쓸 필요는 없을 것 같습니다. CF Sota를 넣어도 될 것 같습니다.

> 저자는 이후에 knowledge graph정보를 추가로 넣어 볼 예정이라고하였는데 baseline으로 사용할 big picture?...
>
> attention 매커니즘도 적용해 볼 것이라고 했는데, 왜 안해봤을까.. 분명해봤는데 성능이 안좋은것이었을까?.. 하는 의문이 있었습니다.

- Test protocol로 TestRating 기법을 사용했는데, 이 방법은 ranking 비교에는 좀 맞지 않은 설정입니다. 차라리 leave-one-out 을 사용하는게 좋을것 같습니다.
