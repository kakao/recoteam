import sys

# 데이터 입력
num_sim_user_top_N = int(sys.stdin.readline())  # 유사도 top N 사용자에 대하여 예측 평점 계산
num_item_rec_top_M = int(sys.stdin.readline())  # 예측 평점 top M 아이템 출력
num_users = int(sys.stdin.readline())  # 전체 사용자 수
num_items = int(sys.stdin.readline())  # 전체 아이템 수
num_rows = int(sys.stdin.readline())  # 입력 row 개수

rating_data = {}  # {사용자 ID: {아이템 ID: 평점}} 형태로 저장
items = set()  # 모든 아이템을 모아놓은 set

# row 입력
for _ in range(num_rows):
    user, item, rating = sys.stdin.readline().split(' ')
    user = int(user)
    item = int(item)
    rating = float(rating)

    if user not in rating_data:
        rating_data[user] = {}
    rating_data[user][item] = rating

    items.add(item)

# 사용자 별 평균 평점 계산
user_average_rating = dict()  # {사용자 ID: 평균 평점} 형태로 저장
for user, item_ratings in rating_data.items():
    user_average_rating[user] = sum(item_ratings.values()) / len(item_ratings)

num_reco_users = int(sys.stdin.readline())  # 추천할 사용자 수

for _ in range(num_reco_users):
    query_user = int(sys.stdin.readline())  # 추천할 사용자 ID
    user_sim = dict()  # {사용자 ID: 유사도} 형태로 저장

    # 사용자 별 유사도(cosine similarity) 계산 (query_user 자신과는 계산 안함)
    for user in rating_data.keys() - {query_user}:
        user_ratings = rating_data[user]
        query_user_ratings = rating_data[query_user]
        intersection_items = rating_data[query_user].keys() & rating_data[user].keys()

        numerator = sum(user_ratings[item] * query_user_ratings[item] for item in intersection_items)
        denominator = sum(rating ** 2 for rating in user_ratings.values()) ** 0.5
        denominator *= sum(rating ** 2 for rating in query_user_ratings.values()) ** 0.5
        # 유사도 계산해서 저장 (계산되지 않는 경우 0으로 정의)
        user_sim[user] = numerator / denominator if denominator > 0.0 else 0.0

    # 유사도 기준으로 정렬. [(사용자 ID, 유사도), ...] 형태의 list of tuple로 저장
    nearest = sorted(user_sim.items(), key=lambda x: x[1], reverse=True)

    predicted_rating = list()  # 예측 평점 (높은 순서에 따라 추천됨). [(아이템 ID, 예측 평점), ...] 형태의 list of tuple로 저장

    # 이미 평가한 정보가 있으면 예측 평점을 계산하지 않음
    for item in items - rating_data[query_user].keys():
        sum_k = 0  # normalizing factor k 계산을 위한 sum. k = 1 / sum_k
        sum_u = 0  # SUM for u' in U [simil(u, u') * (r_u'i - r_u')]

        # 유사도 top N 사용자에 대해 계산
        for user, similarity in nearest[:num_sim_user_top_N]:
            # 사용자가 아이템을 평가하지 않았으면 계산하지 않음
            if item not in rating_data[user]:
                continue

            sum_u += similarity * (rating_data[user][item] - user_average_rating[user])
            sum_k += abs(similarity)

        # 아이템의 예측 평점 (r_ui)
        # 유사도 top N 사용자가 모두 아이템을 평가하지 않았으면 이 아이템에 대해 예측할 수 없음 (0으로 정의)
        r_ui = user_average_rating[query_user] + (1 / sum_k) * sum_u if sum_k > 0.0 else 0.0

        predicted_rating += [(item, r_ui)]  # 예측 평점 list에 저장

    predicted_rating.sort(key=lambda x: x[1], reverse=True)  # 예측 평점 list 정렬
    print(' '.join(str(item_rating[0]) for item_rating in predicted_rating[:num_item_rec_top_M]))  # 추천 리스트 출력
