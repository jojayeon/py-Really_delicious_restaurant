import requests
import json
# 공공데이터포털 API URL 및 키 (실제 API URL과 키로 교체)
api_url = 'https://apis.data.go.kr/6300000/openapi2022/restrnt/getrestrnt?'  # 예시 URL, 실제 URL로 수정 필요
service_key = "dpEPUK36yqhSZNgzBL5MGZgpiVG2Q12SzEbTGv0kFXlqDuOKTFrOvaih2+BHmcBEMp/hqy5qSaLYvVAG/w75pw=="  # 공공데이터포털에서 발급받은 서비스 키

# API에서 대전 지역 데이터를 가져오는 함수
def fetch_daejeon_data():
    params = {
        'serviceKey': service_key,
        'pageNo': '1',              # 페이지 번호
        'numOfRows': '100',          # 한 번에 가져올 데이터 수
    }
    full_url = requests.Request('GET', api_url, params=params).prepare().url
    print(f"Request URL: {full_url}")
    response = requests.get(full_url)
    # 응답 상태 코드 확인
    print(f"HTTP Status Code: {response.status_code}")

    # 응답 내용을 텍스트로 출력하여 확인
    print("Response Content:")
    print(response.text)

    # 응답이 성공했는지 확인
    if response.status_code == 200:
        # JSON 파싱을 시도
        try:
            data = response.json()
            # 가져온 데이터를 JSON 파일로 저장
            with open('daejeon_restaurants.json', 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            print("데이터가 성공적으로 저장되었습니다.")
        except json.JSONDecodeError:
            print("JSON 디코딩에 실패했습니다. 응답이 JSON 형식이 아닙니다.")
    else:
        print(f"Error: {response.status_code}")

# 함수 호출
fetch_daejeon_data()