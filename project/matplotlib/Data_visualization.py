import folium
import webbrowser
import os

# 지도 생성 (대전 지역을 중심으로)
map_center = [36.34479, 127.43322]
mymap = folium.Map(location=map_center, zoom_start=13)

# 저장할 파일 경로와 파일명 설정 (상위 디렉토리로 나가기)
save_directory = '../'  # 현재 디렉토리의 상위 디렉토리로 이동
name = "basic_map.html"
map_filename = os.path.join(save_directory, name)

# 지도 저장
mymap.save(map_filename)

# 브라우저에서 파일 실행
webbrowser.open(name)

print(f"'{map_filename}' 파일이 상위 디렉토리에 저장되고 브라우저에서 열렸습니다.")
