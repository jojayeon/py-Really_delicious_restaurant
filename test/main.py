from celery_app import crawl_restaurant_data
import json
import os

# JSON 파일에서 식당 이름 로드
with open('C:/Users/USER/py-Really_delicious_restaurant/project/other_data/o_data/restaurant_coordinates1.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# 결과를 저장할 리스트
results = []

# Celery 작업 분배
tasks = []
for restaurant in restaurants:
    # Celery에 작업 추가
    task = crawl_restaurant_data.delay(restaurant)
    tasks.append(task)

# 작업 완료 후 결과 모으기
for task in tasks:
    result = task.get()  # 작업 결과 기다리기
    if result:
        results.append(result)

# JSON 파일로 저장
save_directory = './o_data/'
os.makedirs(save_directory, exist_ok=True)

with open(os.path.join(save_directory, 'restaurant_reviews.json'), 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=4)
