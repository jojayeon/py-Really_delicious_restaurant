import requests
import json




# 공공데이터포털 API URL 및 키 (실제 API URL과 키로 교체)
api_url = 'https://apis.data.go.kr/6300000/openapi2022/restrnt/getrestrnt?'  # 예시 URL, 실제 URL로 수정 필요
service_key = 'dpEPUK36yqhSZNgzBL5MGZgpiVG2Q12SzEbTGv0kFXlqDuOKTFrOvaih2%2BBHmcBEMp%2Fhqy5qSaLYvVAG%2Fw75pw%3D%3D'  # 공공데이터포털에서 발급받은 서비스 키

# API에서 대전 지역 데이터를 가져오는 함수
def fetch_daejeon_data():
    params = {
        'serviceKey': service_key,
        'pageNo': '1',              # 페이지 번호
        'numOfRows': '100',          # 한 번에 가져올 데이터 수
        'type': 'json',              # 응답 데이터 타입
    }

    response = requests.get(api_url, params=params)

    # 응답이 성공했는지 확인
    if response.status_code == 200:
        data = response.json()  # JSON 형식으로 변환

        # 가져온 데이터를 JSON 파일로 저장
        with open('daejeon_restaurants.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print("데이터가 성공적으로 저장되었습니다.")
    else:
        print(f"Error: {response.status_code}")

# 함수 호출
fetch_daejeon_data()