![wleh](https://github.com/user-attachments/assets/d8aa61b8-8fa8-4e21-8606-49b88b53ed1c)

📝 한 줄 소개

대전의 착한식당 데이터를 기반으로 평점과 리뷰를 자연어처리로 분석, 맛집을 지도에 시각화하는 Python 기반 프로젝트


📚 프로젝트 개요

대전의 착한식당 데이터를 수집하여,

카카오 API를 통해 각 식당의 평점 및 리뷰 데이터를 가져오고

자연어처리(NLP) 기술로 리뷰를 분석

착한식당 여부, 평점, 리뷰분류 3가지 기준으로 맛집을 선별

선별된 맛집을 웹 지도에 시각화

중점 기술: 리뷰 텍스트 분석(자연어처리)

🚀 주요 기능

착한식당 데이터 수집 및 전처리

카카오 API로 평점·리뷰 데이터 자동 수집

KoNLPy 활용한 리뷰 감성 분석 및 분류

착한식당, 평점, 리뷰분류 3요소로 맛집 선별

선정된 맛집을 지도에 마커로 표시


🛠️ 기술 스택

Python

카카오 API

KoNLPy (자연어처리)

JavaScript 

leaflet.js (지도 시각화)


🗂️ 파일/폴더 구조

html/

└── index.html

js-Leafletb/

└── map.html

other_data/

└── data.json

project/

├── other_data

│   ├── final_preprocessing/

│   ├── find_ccd/

│   ├── franchise_filter/

│   ├── kakaoAPI/

│   ├── KoNLPy/

│   ├── o_data/

│   ├── Playwright_crawler/

│   └── savemap/

├── requirements.txt

├── .gitignore

├── .python-version

└── package.json


폴더 설명

other_data/ : 데이터

final_preprocessing/: 데이터 전처리

find_ccd/, franchise_filter/: 착한식당 및 프랜차이즈 필터링

kakaoAPI/: 카카오 API 연동 및 데이터 수집

KoNLPy/: 리뷰 자연어처리 분석

o_data/: 추후 업데이트 데이터

html/: 지도 시각화 웹 페이지

js-Leafletb/ : leaflet.js으로 지도 만들기


🌐 배포 사이트

[배포 사이트 바로가기](https://vercel.com/jojayeons-projects/py-really-delicious-restaurant)


🗒️ 커밋 컨벤션

new: 신규 기능/파일 추가

data: 데이터 관련 작업

Fix: 버그 수정/로직 개선

Del: 파일/기능 삭제


📅 프로젝트 상태 

대전 데이터만 사용하면 만들어진 상태 충남 데이터로 확장 중 


📬 연락처

jojayeon6152@gmail.com
