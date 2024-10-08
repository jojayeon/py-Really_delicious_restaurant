# -*- coding: utf-8 -*-
import json
from konlpy.tag import Okt
import os

# JSON 파일에서 데이터 로드
with open('./o_data/restaurant_reviews.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# Okt 객체 생성
okt = Okt()

# 평점이 가장 높은 식당과 가장 낮은 식당 (리뷰 5개 이상인 경우만)
highest_rated_restaurant = None
lowest_rated_restaurant = None
highest_rating = float('-inf')  # 가장 낮은 초기화
lowest_rating = float('inf')     # 가장 높은 초기화

# 긍정적/부정적/중립적 리뷰 방향 카운트
positive_reviews = 0
negative_reviews = 0
neutral_reviews = 0

# 평점 상태 카운트
above_4_count = 0
below_4_count = 0
normal_4_count = 0

# 식당별 긍정적 및 부정적 언어 카운트
restaurant_analysis = []

# 리뷰 분석 및 평점 비교 (리뷰 개수 5개 이상인 식당 대상으로)
for restaurant in results:
    # 평점 변환 (점 단어 제거 후 변환)
    rating_text = restaurant['rating'].replace('점', '').strip()  # '점' 제거
    rating = float(rating_text)  # 문자열을 float로 변환
    
    # 리뷰 개수
    review_count = len(restaurant['reviews'])
    
    # 리뷰 개수가 5개 이상인 경우에만 평점 비교
    if review_count >= 6:
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
        words = okt.morphs(review)  # 리뷰에서 명사 추출
        for word in words:
            if word in ["좋다", "맛있다", "훌륭하다", "추천하다", "만족", "친절", "좋은", "좋고", "맛있습니다",
"천국", "맛있음", "맛있어요", "최고", "맛있게", "좋았음", "맛있고",
"좋아요", "최고예요", "만족합니다", "추천해요", "훌륭해요", "친절해요", "편리해요", "감동이에요","좋아하고 있었다", "최고라고 생각했다", "만족하고 있었다", "추천하고 싶었다", "훌륭하다고 느꼈다","좋았다", "최고였다", "만족했다", "추천했다", "훌륭했다", "맛있었다", "친절했다", "편리했다", "감동이었다","맛있다고 생각했다", "친절하다고 느꼈다", "편리하다고 생각했다","최고고", "훌륭하고", "친절하고", "편리하고", "감동이고","재구매하고","좋았다", "최고였다", "만족했다", "추천했다", "훌륭했다", "맛있었다", "친절했다", "편리했다", "감동이었다","좋았다", "최고였다", "만족했다", "추천했다", "훌륭했다", "맛있었다", "친절했다", "편리했다", "감동이었다","대만족", "완벽해요", "환상적이에요", "멋져요","대박이에요", "강추합니다", "꼭 가보세요","최상급이에요", "감탄했어요", "인상적이에요", "놀라워요", "기대 이상이에요", "또 오고 싶어요","재방문 의사 있어요", "가성비 최고예요", "믿고 먹어요", "맛집이에요", "숨은 보석이에요", "특별해요", "독특해요", "신선해요", "깔끔해요", "청결해요", "분위기 좋아요","서비스가 좋아요", "가격이 합리적이에요", "양이 많아요", "퀄리티가 높아요"]:
                positive_count += 1
            elif word in ['나쁘다', '불만', '실망', '싫다', '싫은', '후회', '불친절', '불만족', '별로', '불친절하다', 
'최악', '맛없고', '별로예요', '실망이에요', '후회해요', '불만이에요', '형편없어요', '맛없어요', 
'불친절해요', '불편해요', '비추천이에요', '다시는 안 살 거예요', '실망이고', '후회하고', '불만이고', 
'형편없고', '불친절하고', '불편하고', '비추천이고', '다시는 안 사고', '별로였다', '실망이었다', 
'후회했다', '불만이었다', '형편없었다', '맛없었다', '불친절했다', '불편했다', '비추천이었다', 
'다시는 안 샀다', '실망이다', '실망스럽다', '실망했다', '실망하고', '후회한다', '후회됐다', '후회스럽다', 
'불만이다', '불만스럽다', '불만족스럽다', '형편없다', '맛없다', '불편하다', '비추천이다', '비추한다', 
'비추하고', '최악이다', '최악이었다', '최악이고', '끔찍하다', '끔찍했다', '끔찍하고', '별로다', '별로고', 
'쓰레기같다', '쓰레기였다', '쓰레기고', '엉망이다', '엉망이었다', '엉망이고', '한심하다', '한심했다', 
'한심하고', '짜증난다', '짜증났다', '짜증나고', '답답하다', '답답했다', '답답하고', '지겹다', '지겨웠다', 
'지겹고', '귀찮다', '귀찮았다', '귀찮고', '힘들다', '힘들었다', '힘들고', '고통스럽다', '고통스러웠다', 
'고통스럽고', '괴롭다', '괴로웠다', '괴롭고', '불쾌하다', '불쾌했다', '불쾌하고', '불만족스럽다', 
'불만족스러웠다', '불만족스럽고', '미흡하다', '미흡했다', '미흡하고', '부족하다', '부족했다', '부족하고', 
'허술하다', '허술했다', '허술하고', '부실하다', '부실했다', '부실하고', '낙제점이다', '낙제점이었다', 
'낙제점이고', '불합격이다', '불합격이었다', '불합격이고', '저질이다', '저질이었다', '저질이고', '무능하다', 
'무능했다', '무능하고', '무책임하다', '무책임했다', '무책임하고', '부적절하다', '부적절했다', '부적절하고', 
'부당하다', '부당했다', '부당하고', '불공정하다', '불공정했다', '불공정하고', '불합리하다', '불합리했다', 
'불합리하고', '비효율적이다', '비효율적이었다', '비효율적이고', '비생산적이다', '비생산적이었다', '비생산적이고', 
'비현실적이다', '비현실적이었다', '비현실적이고', '다시는 안 간다', '다시 오지 않을 것이다', '추천하지 않는다', 
'다시는 안 갈 거예요','안', '않', '못', '없', '아니', '말', '들지', '싫', '별로', '그닥']:
                negative_count += 1

    # 긍정적/부정적 판단
    if positive_count > negative_count:
        sentiment = "긍정적"
        positive_reviews += 1
    elif negative_count > positive_count:
        sentiment = "부정적"
        negative_reviews += 1
    else:
        sentiment = "중립적"
        neutral_reviews += 1

    # 평점이 4.0 이상인지 여부 확인
    if rating >= 3.7:
        rating_status = "3.7 이상 맛집입니다"
        above_4_count += 1
    elif rating <=3.3:
        rating_status = "3.3 이하 가지 마세요"
        below_4_count += 1
    else:
        rating_status = "평범합니다"
        normal_4_count += 1

    # 식당별 분석 결과 저장
    restaurant_analysis.append({
        'restaurant_name': restaurant['restaurant_name'],
        'positive_count': positive_count,
        'negative_count': negative_count,
        'sentiment': sentiment,
        'rating': rating,
        'review_count': review_count,  # 리뷰 개수 추가
        'rating_status': rating_status,  # 평점 상태 추가
        'detail_url': restaurant.get('detail_url', 'N/A') 
    })
save_directory = './o_data/'  # 현재 디렉토리의 ab 폴더
os.makedirs(save_directory, exist_ok=True)  # ab 폴더가 없으면 생성

# 결과를 JSON 파일로 저장
with open(os.path.join(save_directory, 'restaurant_analysis.json'), 'w', encoding='utf-8') as outfile:
    json.dump(restaurant_analysis, outfile, ensure_ascii=False, indent=4)

print("분석 결과가 restaurant_analysis.json 파일에 저장되었습니다.")
# 결과 출력
print("식당별 긍정적/부정적 분석 결과:")
for analysis in restaurant_analysis:
    print(f"식당 이름: {analysis['restaurant_name']}, 평점: {analysis['rating']}, 리뷰 개수: {analysis['review_count']}")
    print(f"긍정적 단어 수: {analysis['positive_count']}, 부정적 단어 수: {analysis['negative_count']}, 리뷰 방향: {analysis['sentiment']}, 평점 상태: {analysis['rating_status']}")

# 리뷰 개수 5개 이상인 경우, 가장 높은 평점을 가진 식당 출력
if highest_rated_restaurant:
    print("\n리뷰 5개 이상에서 가장 높은 평점을 가진 식당:")
    print(f"식당 이름: {highest_rated_restaurant['restaurant_name']}, 평점: {highest_rating}, 리뷰 개수: {len(highest_rated_restaurant['reviews'])}")

# 리뷰 개수 5개 이상인 경우, 가장 낮은 평점을 가진 식당 출력
if lowest_rated_restaurant:
    print("\n리뷰 5개 이상에서 가장 낮은 평점을 가진 식당:")
    print(f"식당 이름: {lowest_rated_restaurant['restaurant_name']}, 평점: {lowest_rating}, 리뷰 개수: {len(lowest_rated_restaurant['reviews'])}")

# 긍정적/부정적/중립적 리뷰 방향 총 개수 출력
print("\n리뷰 방향 통계:")
print(f"긍정적 리뷰 개수: {positive_reviews}")
print(f"부정적 리뷰 개수: {negative_reviews}")
print(f"중립적 리뷰 개수: {neutral_reviews}")

# 평점 상태 통계 출력
print("\n평점 상태 통계:")
print(f"4.0 이상 맛집입니다: {above_4_count}개")
print(f"평범합니다: {normal_4_count}개")
print(f"3.3 이하 입니다 주의 하세요: {below_4_count}개")