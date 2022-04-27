- Paper : <https://dl.acm.org/doi/10.1145/3460231.3474253>
- Authors : [[Yu Liang]], [[Martijn C. Willemsen]]
- Reviewer : [[jinny.kk@kakaocorp.com]]
- Topics
  - #Interactive_Recommendation
  - #Music_Recommendation
  - #RecSys2021

### Summary

- 유저의 preference가 시간이 지남에 따라 어떻게 발전하는지는 많이 연구되지 않았다는 문제의식에서 출발하여 음악 도메인에서 유저들의 short-term, long-term preference간의 관계를 이해해보고자 한 논문입니다.

### Approach

#### 접근 방법

- 음악 도메인에서 유저들의 short-term, long-term preference간의 관계를 이해해보자.
  - 정의: short-term은 session 내에서의 소비, long-term은 whole history에서의 소비를 뜻한다.
  - 그걸 이해하면 시간에 따라 유저의 취향이 어떻게 발전하는지 이해할 수 있을 것이고, 유저가 새로운 취향을 탐색할 때 어떻게 행동하는지 이해할 수 있을 것이고, 탐색 툴에서 우리가 유저를 어떻게 서포팅해주면 좋을지도 생각해볼 수 있을 것이기 때문이다.
- 왜냐?
  - 유저의 취향이 시간이 지남에 따라 어떻게 발전하는지 취향의 stability가 있는지, 그들간의 관계는 under-explored되었다.
  - 이전 연구들이 보인 것들은, 단기 취향 ≠ 장기 취향인 것 같더라, 그리고 음악 도메인에선 유저의 음악적 전문성에 따라 청취 행태 (다양성, 추천 시스템 사용 방식)가 다르더라 정도였다.
- 논문의 도메인: 음악

#### Research Questions

- RQ 1: 시간에 따라 유저 취향이 어떻게 변화하는지 이해해보자. (users's preference consistency)
  - 스터디 디자인: data는 (다른 스터디에서 수집한) 스포티파이에서 319명의 유저들의 청취 기록을 사용했다. short (최근 4주), medium (최근 6달), long-term (모든 기록) preference는 track-level, artist-level, tag-level로 측정했다.
  - 유저의 음악적 전문성이 높을수록 (높은 MSAE 점수) 시간에 따른 더 일관된 (consistent) 취향을 가지더라.
  - short-term 과 medium-term 취향의 일관성이나, medium-term과 long-term 취향의 일관성 > short-term과 long-term 취향의 일관성. (어찌 보면 당연하긴 한 듯하지만..)
- RQ 2: 유저는 새로운 취향을 어떤 방식으로 탐색할까?
  - (유저의 음악적 전문성에 따라 새로운 음악 장르를 탐색하는 방식이 달라질까?)
  - 스터디 디자인: 저자들이 수행한 이전 연구가 이미 있고, 거기에 새로운 분석을 추가한 느낌이다. 어쨌든, 유저들에게 장르 목록을 주고 탐색할 장르를 선택하게 했다.
  - 유저들은 현재 취향에 가까운 장르를 탐색하는 경향을 보였다.
    - 유저의 음악적 전문성이 낮을수록 (낮은 MSAE 점수) 취향이 less stable 하더라. 그래서 탐색할 때 (well-developed된) long-term 취향의 장르에 가까운 장르를 탐색하더라.
    - 유저의 음악적 전문성이 높을수록 (높은 MSAE 점수) 취향이 stable 하더라. 그래서 short, medium, long-term 취향의 것을 비슷비슷한 수준으로 탐색하더라.
- RQ 3: 그렇다면 유저가 현재 취향보다 좀더 멀리 떨어진 취향을 탐색하도록 넛지할 수 있을까?
  - 스터디 디자인: 저자들이 고안한 interaction tool을 유저들이 사용하게 하였고, 2 X 3의 default conditions에서 between-subjects로 실험을 진행했다. 설정이 유저가 더 기존 취향으로부터 더 멀리 탐색하도록 넛지할 수 있는지 등을 분석하였다.
    - 2 X 3 default conditions
      - genre presentation order: 유저 취향에서 가까운 순 - 유저 취향에서 멀리 있는 순
      - 장르 내 플레이 리스트의 personalization-level을 컨트롤하는 slider position: fully personalized - middle - fully representative
  - RQ 3-1: 시스템의 Default order of genre presentation에 따라 유저가 현재 취향에서 좀더 먼 취향을 탐색하도록 넛지할 수 있을까?
    - 넛지할 수 있더라. 하지만 음악적 전문성이 높을수록 이에 영향 받는 정도가 적더라.
  - RQ 3-2: 시스템의 slider position의 default 세팅에 따라 유저들이 선택하는 추천의 개인화 정도가 달라질까?
    - 유저의 slider interaction 횟수에 따라 유저별로 경향성이 다르게 나타났다. Fig 6 참고.
      - low interaction group: final slider position은 default slider position에 강하게 영향 받았다.
      - medium interaction group: default slider position의 반대 방향으로 slider를 이동시켰다.
      - high interaction group: default에 덜 영향을 받았고, mixed position으로 slider를 이동시켰다.
    - 대체로 유저들이 선택한 slider position으로 미루어 볼 때, 최적은 personalization과 representativeness 사이 어딘가에서 형성되더라.
  - RQ 3-3: 유저들이 기꺼이 탐색하고자 하는 거리가 유저의 음악적 전문성에 따라 달리 나타날까?
  - path model을 구축해서 (Fig 7) default setting이 유저의 (현재 취향으로부터의) 탐색 거리에 영향을 끼칠 수 있다고 분석했다.

### Conclusion

- `Strong Points?`
  - 음악적 전문성에 따라 시간에 따른 유저 취향의 일관성 정도가 다르다는 걸 분석했다는 점이 흥미로웠다.
  - 유저들이 컨트롤할 수 있는 어떠한 디폴트 세팅이 주어졌을 때 어떤 방식으로 새로운 장르를 탐색하는지 분석한 점이 흥미로웠다.
- `Weak Points?`
  - 논문에서는 "취향"을 CB적으로 정의하였고, CF적으로 정의한 것은 아니다.
  - 분석 논문인 것 같고, 그래서 이를 추천 시스템이 어떻게 반영해야 하는지의 방향성을 제시하지는 않는 것 같다.
  - 음악 도메인이라 유저의 전문성이 하나의 factor가 되었는데, 다른 도메인에선 다른 것이 factor가 될 수 있을 것 같다.
