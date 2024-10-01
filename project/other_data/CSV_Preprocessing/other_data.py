import warnings
import pandas as pd

# 경고 메시지 무시
warnings.filterwarnings("ignore")

# Excel 파일 읽기
df = pd.read_excel('C:/Users/Administrator/py-Really_delicious_restaurant/project/other_data/data/all_delicious_restaurant.xlsx', engine='openpyxl')

# 원하는 열 선택
selected_columns = df[['업소명', '도로명주소', '소재지주소', '전화번호', '영업상태구분코드', '음식의유형']]

# 결과 출력
print(selected_columns.head(10))


# 기본데이터에 영성상태 구분코드가 없는 것이 있을 줄알고 작업했으니 앖어서 제외
# # '영업상태구분코드' 열에서 NaN 값이 없는 행만 선택
# filtered_data = selected_columns.dropna(subset=['영업상태구분코드'])
# print(filtered_data.head(10))
# total_columns = df.shape[0]
# total_columns2 = filtered_data.shape[0]
# print(f"1총 열의 개수: {total_columns}")
# print(f"2총 열의 개수: {total_columns2}")
