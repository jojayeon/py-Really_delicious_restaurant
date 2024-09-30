import folium
from folium.plugins import MarkerCluster
import webbrowser
import os
import json

# JSON 파일에서 레스토랑 데이터 로드
with open('./data/filtered_merged_output.json', 'r', encoding='utf-8') as file:
    restaurant_data = json.load(file)

# 지도 생성 (대전 지역을 중심으로)
map_center = [36.35111, 127.385]
mymap = folium.Map(location=map_center, zoom_start=13)

# 마커 클러스터 추가
marker_cluster = MarkerCluster().add_to(mymap)

# 각 레스토랑에 마커 추가
for restaurant in restaurant_data:
    folium.Marker(
        location=[float(restaurant["mapLat"]), float(restaurant["mapLot"])],
        popup=folium.Popup(
            f"<h1>{restaurant['restaurant_name']}</h1>"
            f"주소: {restaurant['restrntAddr']}<br>"
            f"평점: {restaurant['rating']}<br>"
            f"<a href='{restaurant['detail_url']}' target='_blank'>상세보기</a>",
            max_width=300  # 팝업의 최대 너비를 설정하여 가로로 넓게 표시
        ),
        icon=folium.Icon(color='blue')  # 마커 색상 설정
    ).add_to(marker_cluster)  # 마커 클러스터에 추가

# 검색 기능을 위한 HTML 코드 추가
search_html = """
<div style="position: fixed; top: 10px; left: 10px; z-index: 9999; background: white; padding: 10px; border-radius: 5px;">
    <input type="text" id="search" placeholder="식당 이름 검색..." style="width: 200px;"/>
    <button id="searchButton">검색</button>
</div>
<script>
    var markers = [];
    var markerCluster = L.markerClusterGroup();
    var restaurantData = %s;

    // 기존 마커 클러스터 제거
    mymap.eachLayer(function(layer) {
        if (layer instanceof L.MarkerClusterGroup) {
            mymap.removeLayer(layer);
        }
    });

    // 레스토랑 데이터를 기반으로 마커 추가
    function addMarkers(data) {
        markers = [];
        for (var i = 0; i < data.length; i++) {
            var restaurant = data[i];
            var marker = L.marker([restaurant.mapLat, restaurant.mapLot]).bindPopup("<strong>" + restaurant.restaurant_name + "</strong><br>주소: " + restaurant.restrntAddr + "<br>평점: " + restaurant.rating + "<br><a href='" + restaurant.detail_url + "' target='_blank'>상세보기</a>");
            markers.push(marker);
            markerCluster.addLayer(marker);
        }
        mymap.addLayer(markerCluster);
    }

    // 검색 필터 기능
    function searchMarkers() {
        var searchTerm = document.getElementById('search').value.toLowerCase();
        markerCluster.clearLayers();  // 기존 마커 클러스터 초기화
        var filteredData = restaurantData.filter(function(restaurant) {
            return restaurant.restaurant_name.toLowerCase().includes(searchTerm);
        });
        addMarkers(filteredData);
    }

    document.getElementById('searchButton').onclick = searchMarkers;

    addMarkers(restaurantData);  // 초기 마커 추가
</script>
""" % json.dumps(restaurant_data)  # restaurant_data를 JSON 문자열로 변환

# HTML로 검색 기능 추가
mymap.get_root().html.add_child(folium.Element(search_html))

# 저장할 파일 경로와 파일명 설정 (상위 디렉토리로 나가기)
save_directory = '../html'  # 현재 디렉토리의 상위 디렉토리로 이동
name = "restaurant_map2.html"
map_filename = os.path.join(save_directory, name)

# 지도 저장
mymap.save(map_filename)

# 브라우저에서 파일 실행 (전체 경로 지정)
webbrowser.open('file://' + os.path.abspath(map_filename))

print(f"'{map_filename}' 파일이 상위 디렉토리에 저장되고 브라우저에서 열렸습니다.")
