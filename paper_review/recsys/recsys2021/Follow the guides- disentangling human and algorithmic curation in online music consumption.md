# Follow the guides- disentangling human and algorithmic curation in online music consumption

- Paper : <https://arxiv.org/abs/2109.03915>
- Authors : Quentin Villermet, Jérémie Poiroux, Manuel Moussallam, Thomas Louail, Camille Roth
- Reviewer : jinny.kk
- Topics
  - [#Applications-Driven_Advances](../../topics/Applications-Driven%20Advances.md)
  - #Music_Recommendation
  - [#RecSys2021](RecSys2021.md)

## Summary

- Contribution
  1. algorithmic guidance에 대한 유저의 태도에 따라 유저군을 선분류하고 각 유저군별로 나눠서 콘텐츠 소비 방식을 분석하였습니다.
      - “추천”이라는 개입이 유저의 소비 컨텐츠 다양성에 어떤 영향을 끼치는가는 논란이 많은 뜨거운 감자였다. 기존 연구들의 대부분은 유저들을 뭉뚱그려서 혹은 binary category (성별, 나이)로 나누어서 결과를 분석했는데 이 논문의 저자들은 유저가 플랫폼을 사용하는 타입별로 그 영향이 다르게 나타나므로 유저들의 그룹을 access mode에 따라 구분해서 영향을 분석하였습니다.
  2. platform recommendation을 algorithmic 과 editorial로 나눠서 살펴보았습니다.
  3. platform recommendation과 offline radio recommendation 간의 관계를 살펴보았습니다.
- Key Observations
  - 음악 플랫폼에서 유저들이 음악을 주로 소비하는 경로 access mode (organic, algorithmic, editorial)에 따라 네 가지 유저그룹으로 (a, e, o, o+) 나누고, 유저들이 소비하는 음악의 다양성 (두 가지 디멘션: dispersion & artist popularity)을 유저 그룹별로 복합적으로 분석한 논문입니다. (그래서 정리하면서 좀 헷갈림...)
  - 소비의 diversity를 두 가지 디멘션에서 보았는데, 유저가 총 소비한 곡들 중 unique 곡들의 비중 측면 (dispersion)과 유저가 소비하는 음악의 아티스트의 인기도 측면 (popularity)입니다.
  - dispersion 측면에선
    - very organic users 보다 어떤 형태로든지 추천을 사용하는 유저들의 dispersion 값이 높았고,
    - 각각의 유저 클래스에서 각자의 main access mode를 통한 소비의 dispersion이 낮았습니다 (=그쪽에서 exploitation이 일어나는 것을 관찰하였습니다.)
    - (오프라인 vs 플랫폼) 라디오 프로그램들의 플레이리스트 dispersion < 온라인 플랫폼 내 대부분 유저들의 소비 dispersion
  - artist popularity 측면에선
    - algorithmic user들은 인기 있는 곡을 under-consume했고 editorial user들은 인기 있는 곡을 over consume하는 모습을 보였으며,
    - 모든 유저 클래스에 대해서 공통적으로 대체로 algorithmic access mode를 통해서는 덜 인기있는 곡들이, editorial access mode를 통해서는 인기 있는 곡들이 소비되는 경향이 보였습니다.
    - (오프라인 vs 플랫폼) 라디오 플레이리스트나 온라인 플랫폼 유저들이나 곡들의 평균 popularity는 비슷비슷했습니다.
  - 그리고 dispersion과 artist popularity간에 mild correlation도 관찰되었습니다.

## Results

### Dataset

- Deezer (프랑스 음악 스트리밍 플랫폼) 2019년 1년동안 8639명의 구독자들의 play history (총 51m 개) (어떤 유저가 어떤 가수의 어떤 노래를 몇 분간 들었는지) + 노래에 접근한 경로 (access mode) (직접 검색, 추천 등)
- 동일 기간동안 프랑스의 라디오 방송국 39곳의 플레이리스트 히스토리를 사용하였습니다.

### User Practices

#### Modes of access and user behavior classes

- Three types of content access mode
  - organic (self-selected)
  - algorithmic (suggested by recommendation engine)
  - editorial (human curation)
- 유저의 플레이 히스토리에서 각각의 access mode의 비율 (Pa (algorithmic), Pe (editorial), Po (organic))에 따라 유저 클래스를 4가지로 분류함.
  - `fig 1` 에 나타나듯 대부분의 유저가 organic mode 에 많이 의존하고 있긴 한데
    - 그럼에도 불구하고 구분이 가능하긴 하고 k means를 통해 `user class`을 4가지로 나누었습니다.
    - a (989명), e (655명), o (1614명), o+ (5381명)
    - 각 유저 클래스별로 number of plays의 분포는 비슷했습니다 (= 모든 클래스에는 active한 유저 덜 active한 유저가 모두 있습니다. 평균 activity는 e 유저 클래스에서 다소 낮긴 했습니다) (`fig 1 - right`)

#### Two dimensions of diversity

- dispersion: (functional diversity - denoting the lack of redundancy in the listening history)
  - 정의 = S (number of unique songs) /  P (number of plays)
  - `fig 2 - left`
    - 각 유저 클래스별로 linear model을 fit해서 경향성을 보았더니 모든 유저 클래스에서 activity (P) 와 dispersion은 inverse relationship을 보였습니다.
    - 하지만 동일 P에 대해선, o+ 인 유저들이 가장 낮은 dispersion을 보였습니다. 즉, algorithmic이든 editorial이든 어떤 형태로든 플랫폼의 추천 모드를 활용하는 유저군들에서 dispersion 값이 더 높게 나타났습니다.
      - o+ 유저들은 플랫폼을 “digital librarian”이 아니라 “digital library”로 사용하는 것이라고 표현하였습니다.
      - “even a moderate use of some form of recommendation is generally associated with a higher level of exploration.”라고 해석하였습니다.
  - `fig 3`
    - 각 유저 클래스에서 각 access mode 별로 dispersion 값들을 확인했는데 모든 유저 클래스에 대해 각 클래스가 중점적으로 사용하는 access mode에서의 dispersion 값이 낮았다. 예를 들어 algorithmic 유저 클래스에선 alogrithmic access mode에서 dispersion이 낮고 이랬다.
    - “Users tend to prioritize exploitation in their preferred mode of access, and favor exploration in the others, in terms of more dispersed plays.”
- artist popularity (semantic diversity - denoting the tilt toward songs by more popular artists.)
  - 정의 = 그 아티스트의 곡들의 재생 횟수를 바탕으로 아티스트들을 4개의 인기도 구간으로 나눔 (각 인기도 구간의 재생 횟수 합이 비슷하게 되도록)
    - 인기도 구간: (높은 인기도) v1 - v2 - v3 - v4 (낮은 인기도)
  - `Table 2`
    - 곡들은 아티스트의 인기도에 상관없이 대부분 organic access mode를 통해 소비되는 비중이 가장 높았다.
    - algorithmic access mode는 중간 인기도의 곡들을 주로 소비하는 통로가 됨을 알 수 있고, editorial access mode는 높은 인기도의 곡들의 비중이 많음. organic은 제일 인기 있거나 제일 인기 낮은 곡들의 비중이 많음.
  - `fig 4 -left`
    - artist popularity와 dispersion이 서로 연관이 되어 있다. 인기도 낮은 아티스트 곡 소비하는 (x축 우측) 유저들의 dispersion 값이 더 높더라 (y축).

#### User types and access mode biases

- user type, access mode, diversity가 어떻게 상호 작용을 하는지 “disentangle”한 그래프가 `fig 5.` 그래프의 y축이 완전히 이해 가는 것은 아님.
  - 각 유저 타입별로 소비하는 곡들의 인기도 경향성이 어떻게 되는지를 보여준 건데, access mode에 따라 세분화한 게 밑에 있는 그림.
  - `fig 5 - top` : algorithmic users under-consume popular artists, editorial users over-consume popular artists, organic users favor less popular artists in monotonous manner, and very organic users 는 인기도 양 극단에서의 소비가 “약간 더” 많다. (그림에서 잘 보이지 않기는 하는 듯..)
  - `fig 5 - bottom` : 유저 타입 구분 없이 모두 전반적으로, algorithmic access로 덜 유명한 아티스트 곡 소비가 되고 editorial access는 인기 있는 아티스트 곡 소비로 치우치고 organic은 그 사이 어디쯤을 보여주는 것으로 해석함.

### The diversity of human-assisted guidance

- 바로 위에서 관찰한 것 중에서, algorithm으로는 덜 유명한 곡 소비를, editor들은 유명한 곡 소비를 이끌어내는 경향성이 보인다는 점이 있는데, 이를 좀더 확인하기 위해 전통적인 오프라인의 editorial 추천이라고 볼 수 있는 라디오 프로그램 플레이리스트를 분석했다.
- `fig 6 - left`
  - 대부분의 user type이 라디오 프로그램들보다 높은 dispersion을 보여줬다. 즉 라디오 프로그램은 보다 제한적인 카탈로그에서의 exploitation으로 기울어져 있다는 이야기.
  - 그리고 색깔 그라데이션 보면 알 수 있듯, dispersion과 popularity의 mild correlation도 볼 수 있다.
- `fig 6 - right`: 대부분의 user type이 중간 부근에 있다. 즉 해석하면 “while online music listening practices seem to foster functional diversity (dispersion), in terms of semantic diversity (popularity) they seem, on average, to be neither significantly above nor significantly below the mass of the radios we focus on.”

### Concluding Remarks

- future work로 언급하는 것들
  - “the chronology of access modes to a song probably carries valuable information.” (특정 곡이 어떤 access mode를 통해 최초 발견되었는가.)
  - “user trajectories and transitions between classes”

## Conclusion

- 우리의 경우도 비즈니스 로직이 항상 끼어 들어가서 human curation에 의한 것과 알고리즘에 의한 것이 복합적으로 섞여 있는 경우가 많은 것 같아서 공감이 되었다. 몇 가지 디테일들은 잘 이해 못 한 것도 있는데, 나름 흥미로운 논문이었다.
  - (diversity를 functional diversity (number of unique songs played / total number of plays) 와 semantic diversity (popularity) 로 나누고, semantic diversity를 보기 위해 왜 embedding space를 사용한 diversity가 아니라 인기도를 보았는지를 기술했는데, 그 이유가 잘 이해가 안 갔다.)
- primary access mode 별로 유저들을 분류하고, 각 access mode 별로 소비하는 음악의 다양성이 어떻게 달라지는지 분석하고, 알고리즘이든 사람이든 큐레이션을 이용하는 유저집단이 좀더 다양한 소비를 한다는 분석 내용이 인상적이었다.
- 기존의 filter bubble 효과를 주장한 논문들과는 달리 이 논문에선 오히려 추천 알고리즘을 이용하는 유저군에서 다양성 수치가 높게 나왔다는 점이 의외였고 추천 알고리즘에 의해 filter bubble에 갇힌다가 myth일 수도 있겠다는 생각이 들었다. 문제는 이 논문이 사용한 데이터셋인 Deezer 음악 플랫폼이 사용하는 추천 알고리즘이 무엇인지에 대한 설명이 없다는 점이다. 추천 알고리즘과 filter bubble에 대해 상반된 결론을 내리는 논문들을 다 모아놓고 리뷰해보면 어떨지.
