import json

# JSON 파일을 불러올 경로 설정
input_path = './o_data/restaurant_coordinates.json'
output_path = './find_CCD.json'

# JSON 파일에서 데이터 불러오기
with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# '충청남도'가 포함된 객체를 필터링
filtered_data = [obj for obj in data if (obj.get('restrntDtlAddr') and '충청남도' in obj['restrntDtlAddr']) or (obj.get('restrntAddr') and '충청남도' in obj['restrntAddr'])]

# 필터링된 데이터를 새 JSON 파일로 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)

print(f"필터링된 데이터가 {output_path}에 저장되었습니다.")
