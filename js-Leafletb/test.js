// 지도 생성 및 초기 위치 설정
var map = L.map('map').setView([36.3507, 127.3975], 13);

// OSM 타일 레이어 추가
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

const markers = L.markerClusterGroup();

// JSON 파일에서 데이터를 불러와 마커 생성
fetch('../other_data/o_data/data.json')
  .then(response => response.json())
  .then(data => {
    data.forEach(location => {
      console.log(location)
      const marker = L.marker([location.mapLat, location.mapLot]);
      marker.bindPopup(`
        <h1>${location.restaurant_name}</h1>
        주소: ${location.restrntAddr}<br>
        평점: ${location.rating}<br>
        전화번호: <a href="tel:${location.tel}">${location.restrntInqrTel
        }</a><br>
        <a href="${location.detail_url}" target="_blank">카카오 맵 바로가기</a>
        `, { maxWidth: 300 });
      markers.addLayer(marker);
      });
      map.addLayer(markers);
  })
  .catch(error => console.error('Error loading JSON:', error));
