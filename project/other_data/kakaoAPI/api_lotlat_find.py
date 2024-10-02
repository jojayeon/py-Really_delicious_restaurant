import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# 카카오 API 키
API_KEY = '89caee802f11ff470ddddb709c3d88b5'  # 여기에 발급받은 카카오 API 키를 입력하세요.

def get_coordinates(restaurant):
    # 카카오 API URL
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    
    # 요청 헤더에 API 키 추가
    headers = {
        'Authorization': f'KakaoAK {API_KEY}'  # 카카오 API 키를 헤더에 추가
    }
    
    # 요청 파라미터 설정
    params = {
        'query': restaurant['업소명'],  # 검색할 식당 이름
        'size': 10  # 반환할 결과 개수 (최대 15)
    }
    
    # API 요청
    response = requests.get(url, headers=headers, params=params)
    
    # 요청 성공 여부 확인
    if response.status_code == 200:
        data = response.json()
        # 결과에서 좌표 정보 추출
        if data['documents']:
            document = data['documents'][0]  # 첫 번째 결과만 사용
            # 반환할 데이터 구성
            return {
                "restrntNm": restaurant['업소명'],
                "restrntAddr": restaurant['도로명주소'],
                "restrntInqrTel": restaurant['전화번호'],
                "restrntDtlAddr": restaurant['소재지주소'],
                "foodType": restaurant['음식의유형'],
                "mapLat": document['y'],
                "mapLot": document['x']
            }
    return None  # 좌표를 찾지 못한 경우

# JSON 파일 읽기
with open('C:/Users/Administrator/jojayeon/py-Really_delicious_restaurant/project/other_data/o_data/daejeon_restaurants.json', 'r', encoding='utf-8') as file:
    restaurants = json.load(file)

# 좌표 정보를 저장할 리스트
coordinates_list = []

# ThreadPoolExecutor를 사용하여 병렬로 요청 처리
with ThreadPoolExecutor(max_workers=5) as executor:
    future_to_restaurant = {executor.submit(get_coordinates, restaurant): restaurant for restaurant in restaurants}
    for future in as_completed(future_to_restaurant):
        result = future.result()
        if result:
            coordinates_list.append(result)

# 결과를 JSON 파일로 저장
with open('C:/Users/Administrator/jojayeon/py-Really_delicious_restaurant/project/other_data/o_data/restaurant_coordinates.json', 'w', encoding='utf-8') as file:
    json.dump(coordinates_list, file, ensure_ascii=False, indent=4)

print("좌표 정보가 restaurant_coordinates.json 파일에 저장되었습니다.")
