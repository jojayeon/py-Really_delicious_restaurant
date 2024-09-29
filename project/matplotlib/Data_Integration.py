# import json
# with open('daejeon_restaurants.json', 'r', encoding='utf-8') as f:
#     results = json.load(f)
#     print(results[1])
# with open('restaurant_analysis.json', "r", encoding="utf-8") as g:
#     asd = json.load(g)
#     print(asd[1])

import json

# a와 b의 JSON 데이터를 변수로 할당 (파일 경로는 비워둠)
with open('daejeon_restaurants.json', 'r', encoding='utf-8') as file_a, open('restaurant_analysis.json', 'r', encoding='utf-8') as file_b:
    a_data = json.load(file_a)
    b_data = json.load(file_b)

# b의 restaurant_name과 a의 restrntNm이 일치할 때 a의 원하는 정보를 b에 병합
for b_item in b_data:
    for a_item in a_data:
        if b_item['restaurant_name'] == a_item['restrntNm']:
            # a의 restrntAddr, mapLat, mapLot을 b에 추가
            b_item['restrntAddr'] = a_item['restrntAddr']
            b_item['mapLat'] = a_item['mapLat']
            b_item['mapLot'] = a_item['mapLot']

# 병합된 결과를 확인하고 저장 (파일명은 원하는 대로 지정 가능)
with open('merged_output.json', 'w', encoding='utf-8') as outfile:
    json.dump(b_data, outfile, ensure_ascii=False, indent=4)

print("병합이 완료되었습니다.")
