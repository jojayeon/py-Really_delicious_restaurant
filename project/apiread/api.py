import requests
import json

# 공공데이터포털 API URL 및 키
api_url = 'https://apis.data.go.kr/6300000/openapi2022/restrnt/getrestrnt'
service_key = "dpEPUK36yqhSZNgzBL5MGZgpiVG2Q12SzEbTGv0kFXlqDuOKTFrOvaih2+BHmcBEMp/hqy5qSaLYvVAG/w75pw=="

# API에서 대전 지역 데이터를 가져오는 함수
def fetch_daejeon_data():
    page_no = 1
    all_data = []  # 모든 데이터를 저장할 리스트

    while True:
        params = {
            'serviceKey': service_key,
            'pageNo': str(page_no),     # 현재 페이지 번호
            'numOfRows': '50',         # 한 번에 가져올 데이터 수
        }

        # 전체 URL 출력
        full_url = requests.Request('GET', api_url, params=params).prepare().url

        response = requests.get(full_url)

        if response.status_code == 200:
            try:
                data = response.json()
                
                # 데이터가 없으면 반복 종료
                if not data.get('response', {}).get('body', {}).get('items', []):
                    print("더 이상 데이터가 없습니다.")
                    break
                
                # 가져온 데이터를 리스트에 추가
                all_data.extend(data['response']['body']['items'])
                print(f"현재 페이지: {page_no}, 가져온 데이터 수: {len(data['response']['body']['items'])}")
                
                # 페이지 번호 증가
                page_no += 1

            except json.JSONDecodeError:
                print("JSON 디코딩에 실패했습니다. 응답이 JSON 형식이 아닙니다.")
                break
        else:
            print(f"Error: {response.status_code}")
            break

    # 모든 데이터를 JSON 파일로 저장
    with open('daejeon_restaurants.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=4)
    print("모든 데이터가 성공적으로 저장되었습니다.")

# 함수 호출
fetch_daejeon_data()
