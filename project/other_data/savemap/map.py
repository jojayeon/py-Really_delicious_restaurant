import folium
from folium.plugins import MarkerCluster
import webbrowser
import os
import json

# JSON 파일에서 레스토랑 데이터 로드
with open('./o_data/filtered_merged_output.json', 'r', encoding='utf-8') as file:
    restaurant_data = json.load(file)

# 지도 생성 (대전 지역을 중심으로)
map_center = [36.35111, 127.385]
mymap = folium.Map(location=map_center, zoom_start=12)

# 마커 클러스터 추가
marker_cluster = MarkerCluster().add_to(mymap)

# 각 레스토랑에 마커 추가
for restaurant in restaurant_data:
    tel_link = f"<a href='tel:{restaurant['restrntInqrTel']}'>{restaurant['restrntInqrTel']}</a>"

    folium.Marker(
        location=[float(restaurant["mapLat"]), float(restaurant["mapLot"])],
        popup=folium.Popup(
            f"<h1>{restaurant['restaurant_name']}</h1>"
            f"주소: {restaurant['restrntAddr']}<br>"
            f"평점: {restaurant['rating']}<br>"
            f"전화번호: {tel_link}<br>"
            f"<a href='{restaurant['detail_url']}' target='_blank'>카카오 맵 바로가기</a>",
            max_width=300
        ),
        icon=folium.Icon(color='blue')
    ).add_to(marker_cluster)

# HTML로 저장할 파일 경로와 파일명 설정
save_directory = '../html2'  # 현재 디렉토리의 상위 디렉토리로 이동
name = "all_restaurant_map.html"
map_filename = os.path.join(save_directory, name)

# 지도 저장
mymap.save(map_filename)

# 브라우저에서 파일 실행 (전체 경로 지정)
webbrowser.open('file://' + os.path.abspath(map_filename))

print(f"'{map_filename}' 파일이 상위 디렉토리에 저장되고 브라우저에서 열렸습니다.")
