from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# 크롬 드라이버 경로 (설치한 경로에 맞게 수정)
driver_path = r'C:/Program Files/chromedriver-win64/chromedriver.exe'

# ChromeOptions 설정
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--user-data-dir=C:/Users/USER/AppData/Local/Google/Chrome/User Data")  # 사용자 프로필 사용
chrome_options.add_argument("--profile-directory=Default") 

# JSON 파일에서 식당 이름 로드
with open('C:/Users/USER/py-Really_delicious_restaurant/project/other_data/o_data/restaurant_coordinates.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# 결과를 저장할 리스트
results = []

def fetch_restaurant_info(name):
    # 서비스 객체 생성 및 드라이버 초기화
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print(f"검색 중: {name}")
        search_url = f'https://map.kakao.com/?q={name}'
        driver.get(search_url)
        
        time.sleep(1)  # 페이지 로딩 대기

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
        return {
            'restaurant_name': name,
            'rating': rating,
            'reviews': reviews,  # 리스트로 저장
            'detail_url': detail_url 
        }

    except Exception as e:
        print(f"식당: {name} 정보를 가져오는 데 실패했습니다: {e}")
        return None  # 오류 발생 시 None 반환
    finally:
        driver.quit()  # 드라이버 종료

# 병렬 처리
with ThreadPoolExecutor(max_workers=5) as executor:  # 최대 10개의 스레드
    future_to_name = {executor.submit(fetch_restaurant_info, restaurant['restrntNm']): restaurant['restrntNm'] for restaurant in restaurants}
    
    for future in as_completed(future_to_name):
        name = future_to_name[future]
        try:
            result = future.result()
            if result:
                results.append(result)
                # print(f"식당: {result['restaurant_name']} 정보 가져오기 성공")
            else:
                print(f"식당: {name} 정보를 가져오는 데 실패했습니다.")
        except Exception as exc:
            print(f"식당: {name} 정보를 가져오는 도중 예외 발생: {exc}")

# JSON 파일로 저장
save_directory = './o_data/'  # 현재 디렉토리의 o_data 폴더
os.makedirs(save_directory, exist_ok=True)  # o_data 폴더가 없으면 생성

with open(os.path.join(save_directory, 'restaurant_reviews.json'), 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=4)

print("모든 작업이 완료되었습니다.")
