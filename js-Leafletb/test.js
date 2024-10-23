// 지도 생성 및 초기 위치 설정
var map = L.map('map').setView([36.3507, 127.3975], 13);

// OSM 타일 레이어 추가
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
}).addTo(map);

const markers = L.markerClusterGroup();
let markerArray = []; // 모든 마커를 저장할 배열

// JSON 파일에서 데이터를 불러와 마커 생성
fetch('../other_data/o_data/data.json')
.then(response => response.json())
.then(data => {
  data.forEach(location => {
    const marker = L.marker([location.mapLat, location.mapLot]);
    marker.bindPopup(`
      <h1>${location.restaurant_name}</h1>
      주소: ${location.restrntAddr}<br>
      평점: ${location.rating}<br>
      전화번호: <a href="tel:${location.tel}">${location.restrntInqrTel}</a><br>
      <a href="${location.detail_url}" target="_blank">카카오 맵 바로가기</a>
    `, { maxWidth: 300 });

    markers.addLayer(marker);
    markerArray.push({ marker, restaurant_name: location.restaurant_name, restrntAddr: location.restrntAddr });
  });
  map.addLayer(markers);
})
.catch(error => console.error('Error loading JSON:', error));

// 검색 기능
function searchLocations() {
  const searchTerm = document.getElementById('search-input').value.toLowerCase();
  const filteredMarkers = markerArray.filter(item =>
      item.restaurant_name.toLowerCase().includes(searchTerm) || 
      item.restrntAddr.toLowerCase().includes(searchTerm)
  );

  if (filteredMarkers.length > 0) {
      const firstMatch = filteredMarkers[0].marker;
      map.setView(firstMatch.getLatLng(), 19); // 기본 줌 레벨
      firstMatch.openPopup();
  } else {
      alert('찾는 결과가 없습니다.');
  }

  const cityMarkers = new Set(); // 구와 동을 포함할 시의 마커를 저장할 집합

  markerArray.forEach(item => {
    const addrParts = item.restrntAddr.split(' '); // 공백으로 주소 분리
    if (addrParts.length >= 3) {
      const [city, district, neighborhood] = addrParts;
      if (searchTerm.includes(city)) {
        // 시 검색 시 해당 시의 모든 마커로 중심 설정
        const latLngs = filteredMarkers.map(marker => marker.marker.getLatLng());
        const avgLat = latLngs.reduce((sum, latLng) => sum + latLng.lat, 0) / latLngs.length;
        const avgLng = latLngs.reduce((sum, latLng) => sum + latLng.lng, 0) / latLngs.length;
        map.setView([avgLat, avgLng], 13); // 시로 줌
      } else if (searchTerm.includes(district)) {
        // 구 검색 시 해당 구의 모든 마커로 중심 설정
        const latLngs = filteredMarkers.filter(item => item.restrntAddr.includes(district)).map(marker => marker.marker.getLatLng());
        if (latLngs.length > 0) {
          const avgLat = latLngs.reduce((sum, latLng) => sum + latLng.lat, 0) / latLngs.length;
          const avgLng = latLngs.reduce((sum, latLng) => sum + latLng.lng, 0) / latLngs.length;
          map.setView([avgLat, avgLng], 15); // 구로 줌
        }
      } else if (searchTerm.includes(neighborhood)) {
        // 동 검색 시 해당 동의 모든 마커로 중심 설정
        const latLngs = filteredMarkers.filter(item => item.restrntAddr.includes(neighborhood)).map(marker => marker.marker.getLatLng());
        if (latLngs.length > 0) {
            const avgLat = latLngs.reduce((sum, latLng) => sum + latLng.lat, 0) / latLngs.length;
            const avgLng = latLngs.reduce((sum, latLng) => sum + latLng.lng, 0) / latLngs.length;
            map.setView([avgLat, avgLng], 16); // 동으로 줌
        }
      }
    }
  });
}