from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from celery_app import app  # Celery 앱 임포트

# 크롬 드라이버 경로 (설치한 경로에 맞게 수정)
driver_path = r'C:/Program Files/chromedriver-win64/chromedriver.exe'

# ChromeOptions 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--user-data-dir=C:/Users/USER/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument("--profile-directory=Default") 

# 서비스 객체 생성
service = Service(driver_path)

@app.task
def crawl_restaurant_data(restaurant):
    driver = webdriver.Chrome(service=service, options=chrome_options)

    name = restaurant['restrntNm']  # 식당 이름
    print(f"크롤링 중: {name}")

    search_url = f'https://map.kakao.com/?q={name}'
    driver.get(search_url)

    time.sleep(1)  # 페이지 로딩 대기

    try:
        # 검색 결과의 첫 번째 상세보기 링크 찾기
        moreview_link = driver.find_element(By.CSS_SELECTOR, "#info\\.search\\.place\\.list > li > div.info_item > div.contact.clickArea > a.moreview")
        detail_url = moreview_link.get_attribute('href')

        # 상세보기 링크 클릭
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
        for _ in range(10):
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

        # 드라이버 종료
        driver.quit()

        return {
            'restaurant_name': name,
            'rating': rating,
            'reviews': reviews,
            'detail_url': detail_url
        }

    except Exception as e:
        driver.quit()
        print(f"식당: {name} 정보를 가져오는 데 실패했습니다: {e}")
        return None
