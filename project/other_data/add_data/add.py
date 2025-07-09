import json
import os

# JSON 파일이 있는 디렉토리 경로
directory_path = 'C:/Users/Administrator/jojayeon/py-Really_delicious_restaurant/project/other_data/o_data/ccd_crawler_data'
# 합쳐진 데이터를 저장할 리스트
merged_data = []

# 디렉토리 내 모든 JSON 파일 읽기
for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            merged_data.extend(data)  # 데이터를 리스트에 추가

# 합쳐진 데이터를 새로운 JSON 파일로 저장
with open('merged_data.json', 'w', encoding='utf-8') as output_file:
    json.dump(merged_data, output_file, ensure_ascii=False, indent=4)

print("JSON 파일들이 성공적으로 합쳐졌습니다.")
