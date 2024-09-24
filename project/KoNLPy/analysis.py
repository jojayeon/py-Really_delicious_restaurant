import json
from konlpy.tag import Okt

# JSON 파일에서 데이터 로드
with open('restaurant_reviews.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# Okt 객체 생성
okt = Okt()

# 평점이 가장 높은 식당과 가장 낮은 식당 (리뷰 4개 이상인 경우만)
highest_rated_restaurant = None
lowest_rated_restaurant = None
highest_rating = float('-inf')  # 가장 낮은 초기화
lowest_rating = float('inf')     # 가장 높은 초기화

# 식당별 긍정적 및 부정적 언어 카운트
restaurant_analysis = []

# 리뷰 분석 및 평점 비교 (리뷰 개수 4개 이상인 식당 대상으로)
for restaurant in results:
    # 평점 변환 (점 단어 제거 후 변환)
    rating_text = restaurant['rating'].replace('점', '').strip()  # '점' 제거
    rating = float(rating_text)  # 문자열을 float로 변환
    
    # 리뷰 개수
    review_count = len(restaurant['reviews'])
    
    # 리뷰 개수가 4개 이상인 경우에만 평점 비교
    if review_count >= 5:
        # 평점 비교
        if rating > highest_rating:
            highest_rating = rating
            highest_rated_restaurant = restaurant
        
        if rating < lowest_rating:
            lowest_rating = rating
            lowest_rated_restaurant = restaurant

    # 리뷰 분석
    positive_count = 0
    negative_count = 0

    for review in restaurant['reviews']:
        words = okt.nouns(review)  # 리뷰에서 명사 추출
        for word in words:
            if word in ["좋다", "맛있다", "훌륭하다", "추천하다", "만족"]:
                positive_count += 1
            elif word in ["나쁘다", "형편없다", "불만", "실망", "싫다"]:
                negative_count += 1

    # 긍정적/부정적 판단
    if positive_count > negative_count:
        sentiment = "긍정적"
    elif negative_count > positive_count:
        sentiment = "부정적"
    else:
        sentiment = "중립적"

    # 식당별 분석 결과 저장
    restaurant_analysis.append({
        'restaurant_name': restaurant['restaurant_name'],
        'positive_count': positive_count,
        'negative_count': negative_count,
        'sentiment': sentiment,
        'rating': rating,
        'review_count': review_count  # 리뷰 개수 추가
    })

# 결과 출력
print("식당별 긍정적/부정적 분석 결과:")
for analysis in restaurant_analysis:
    print(f"식당 이름: {analysis['restaurant_name']}, 평점: {analysis['rating']}, 리뷰 개수: {analysis['review_count']}")
    print(f"단어 수: {analysis['positive_count']}, 부정적 단어 수: {analysis['negative_count']}, 리뷰 방향: {analysis['sentiment']}")

# 리뷰 개수 4개 이상인 경우, 가장 높은 평점을 가진 식당 출력
if highest_rated_restaurant:
    print("\n리뷰 5개 이상에서 가장 높은 평점을 가진 식당:")
    print(f"식당 이름: {highest_rated_restaurant['restaurant_name']}, 평점: {highest_rating}, 리뷰 개수: {len(highest_rated_restaurant['reviews'])}")

# 리뷰 개수 4개 이상인 경우, 가장 낮은 평점을 가진 식당 출력
if lowest_rated_restaurant:
    print("\n리뷰 5개 이상에서 가장 낮은 평점을 가진 식당:")
    print(f"식당 이름: {lowest_rated_restaurant['restaurant_name']}, 평점: {lowest_rating}, 리뷰 개수: {len(lowest_rated_restaurant['reviews'])}")
