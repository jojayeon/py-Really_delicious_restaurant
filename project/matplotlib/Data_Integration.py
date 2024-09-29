import json

# a와 b의 JSON 데이터를 변수로 할당 (파일 경로는 비워둠)
with open('daejeon_restaurants.json', 'r', encoding='utf-8') as file_a, open('restaurant_analysis.json', 'r', encoding='utf-8') as file_b:
    a_data = json.load(file_a)
    b_data = json.load(file_b)

# sentiment가 '긍정적'이고 rating이 3.7 이상인 항목만 필터링
filtered_b_data = [b_item for b_item in b_data if b_item['sentiment'] == '긍정적' and b_item['rating'] >= 3.7]

# 필터링된 데이터에서 b의 restaurant_name과 a의 restrntNm이 일치할 때 a의 원하는 정보를 b에 병합
for b_item in filtered_b_data:
    for a_item in a_data:
        if b_item['restaurant_name'] == a_item['restrntNm']:
            # a의 restrntAddr, mapLat, mapLot을 b에 추가
            b_item['restrntAddr'] = a_item['restrntAddr']
            b_item['mapLat'] = a_item['mapLat']
            b_item['mapLot'] = a_item['mapLot']


    # 제외할 항목을 제거
    if 'positive_count' in b_item:
        del b_item['positive_count']
    if 'negative_count' in b_item:
        del b_item['negative_count']
    if 'review_count' in b_item:
        del b_item['review_count']

# 병합된 결과를 확인하고 저장 (파일명은 원하는 대로 지정 가능)
with open('filtered_merged_output.json', 'w', encoding='utf-8') as outfile:
    json.dump(filtered_b_data, outfile, ensure_ascii=False, indent=4)

print("필터링, 항목 제외 및 병합이 완료되었습니다.")
