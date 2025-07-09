import os
import pandas as pd
import json

# Excel 파일 읽기
df = pd.read_excel('C:/Users/Administrator/jojayeon/py-Really_delicious_restaurant/project/other_data/o_data/all_delicious_restaurant.xlsx', engine='openpyxl')

# 원하는 열 선택
selected_columns = df[['업소명', '도로명주소', '전화번호','소재지주소', '영업상태구분코드', '음식의유형']]

# 영업상태구분코드가 1인 항목만 필터링
filtered_data = selected_columns[selected_columns['영업상태구분코드'] == 1]

# JSON으로 변환
json_data = filtered_data.to_json(orient='records', force_ascii=False)

# 현재 디렉토리의 data 폴더 설정
save_directory = './o_data/'
os.makedirs(save_directory, exist_ok=True)  # data 폴더가 없으면 생성

# JSON 문자열을 파일로 저장
json_file_path = os.path.join(save_directory, 'daejeon_restaurants.json')
with open(json_file_path, 'w', encoding='utf-8') as outfile:
    outfile.write(json_data)  # JSON 문자열을 파일에 직접 쓰기

print("영업 중인 데이터가 성공적으로 저장되었습니다.")
