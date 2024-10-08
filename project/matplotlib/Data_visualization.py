import folium
import webbrowser
import os
import json

# JSON 파일에서 레스토랑 데이터 로드
with open('./data/filtered_merged_output.json', 'r', encoding='utf-8') as file:
    restaurant_data = json.load(file)

# 지도 생성 (대전 지역을 중심으로)
map_center = [36.35111, 127.385]
mymap = folium.Map(location=map_center, zoom_start=13)

# 각 레스토랑에 마커 추가
for restaurant in restaurant_data:

    detail_url = f'<a href="{restaurant["detail_url"]}" target="_blank">주소 바로가기</a>' if restaurant["detail_url"] else "N/A"

    folium.Marker(
        location=[float(restaurant["mapLat"]), float(restaurant["mapLot"])],
        popup=folium.Popup(
            f"<h1>{restaurant['restaurant_name']}</h1>"
            f"주소: {restaurant['restrntAddr']}<br>"
            f"평점: {restaurant['rating']}<br>"
            f"상세보기: {detail_url}",
            max_width=300  # 팝업의 최대 너비를 설정하여 가로로 넓게 표시
        ),
        icon=folium.Icon(color='blue')  # 마커 색상 설정
    ).add_to(mymap)

# 저장할 파일 경로와 파일명 설정 (상위 디렉토리로 나가기)
save_directory = '../html'  # 현재 디렉토리의 상위 디렉토리로 이동
name = "restaurant_map.html"
map_filename = os.path.join(save_directory, name)

# 지도 저장
mymap.save(map_filename)

# 브라우저에서 파일 실행 (전체 경로 지정)
webbrowser.open('file://' + os.path.abspath(map_filename))

print(f"'{map_filename}' 파일이 상위 디렉토리에 저장되고 브라우저에서 열렸습니다.")
