from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
import os

# 크롬 드라이버 경로 (설치한 경로에 맞게 수정)
driver_path = r'C:\Program Files\chromedriver-win64\chromedriver.exe'

# ChromeOptions 설정
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data")  # 사용자 프로필 사용
chrome_options.add_argument("--profile-directory=Default") 

# 서비스 객체 생성
service = Service(driver_path)

# 드라이버 초기화
driver = webdriver.Chrome(service=service, options=chrome_options)

# JSON 파일에서 식당 이름 로드
with open('./data/daejeon_restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# 결과를 저장할 리스트
results = []

# 식당 이름으로 검색
for restaurant in restaurants:  # 리스트를 순회
    name = restaurant['restrntNm']  # 식당 이름
    print(name)
    
    search_url = f'https://map.kakao.com/?q={name}'
    driver.get(search_url)
    
    time.sleep(1)  # 페이지 로딩 대기

    try:
        # 검색 결과가 나올 때까지 대기
        time.sleep(1)
        
        # 검색 결과의 첫 번째 상세보기 링크 찾기
        moreview_link = driver.find_element(By.CSS_SELECTOR, "#info\\.search\\.place\\.list > li > div.info_item > div.contact.clickArea > a.moreview")
        
        detail_url = moreview_link.get_attribute('href')
        # 첫 번째 상세보기 링크 클릭
        moreview_link.click()
        
        time.sleep(1)  # 로딩 대기

        # 새 탭으로 전환
        driver.switch_to.window(driver.window_handles[-1])
        
        time.sleep(1)  # 페이지 로딩 대기

        # 평점 가져오기
        rating_element = driver.find_element(By.CSS_SELECTOR, "#mArticle > div.cont_evaluation > div.ahead_info > div > em.num_rate")
        rating = rating_element.text

        # 모든 리뷰 가져오기
        reviews = []
        for _ in range(10):  # 최대 10번 시도
            try:
                more_reviews_button = driver.find_element(By.CSS_SELECTOR, "#mArticle > div.cont_evaluation > div.evaluation_review > a > span.txt_more")
                more_reviews_button.click()
                time.sleep(1)  # 클릭 후 로딩 대기
            except Exception:
                break  # 버튼이 더 이상 존재하지 않으면 종료

        # 리뷰 가져오기
        review_elements = driver.find_elements(By.CSS_SELECTOR, "#mArticle > div.cont_evaluation > div.evaluation_review > ul > li > div.comment_info > p > span")
        
        
        for review_element in review_elements:
            reviews.append(review_element.text)

        # 결과 저장
        results.append({
            'restaurant_name': name,
            'rating': rating,
            'reviews': reviews,  # 리스트로 저장
            'detail_url': detail_url 
        })

        print(f"식당: {name}, 평점: {rating}, 리뷰: {reviews}, 상세보기 URL: {detail_url}")
        
        # 새 탭 닫기 후 원래 탭으로 전환
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
    except Exception as e:
        print(f"식당: {name} 정보를 가져오는 데 실패했습니다: {e}")

# JSON 파일로 저장

save_directory = './data/'  # 현재 디렉토리의 ab 폴더
os.makedirs(save_directory, exist_ok=True)  # ab 폴더가 없으면 생성

with open(os.path.join(save_directory, 'restaurant_reviews.json'), 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=4)

driver.quit()
