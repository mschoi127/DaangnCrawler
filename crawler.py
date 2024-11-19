import time
import json
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 검색 키워드 입력
search_keyword = input("검색 키워드를 입력하세요: ")

# 지역별 URL 리스트
regions = [
    "https://www.daangn.com/kr/buy-sell/?in=%EC%97%AD%EC%82%BC%EB%8F%99-6035&search=",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%B2%AD%EB%8B%B4%EB%8F%99-386&search=",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%85%BC%ED%98%84%EB%8F%99-6031&search=",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%8C%80%EC%B9%98%EB%8F%99-6032&search=",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%82%BC%EC%84%B1%EB%8F%99-6034&search=",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%95%95%EA%B5%AC%EC%A0%95%EB%8F%99-385&search=",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%8B%A0%EC%82%AC%EB%8F%99-382&search=",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%97%AD%EC%82%BC1%EB%8F%99-392&search=",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%8F%84%EA%B3%A1%EB%8F%99-6033&search=",
    "https://www.daangn.com/kr/buy-sell/?in=%EA%B0%9C%ED%8F%AC%EB%8F%99-6030&search="
]

# Selenium 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 요청 수 초기화 및 시간 기록
total_requests = 0
search_page_requests = 0
detail_page_requests = 0
start_time = datetime.now()

# 전체 데이터를 저장할 리스트
all_data = []

# 지역별 데이터 수집
for region_url in regions:
    main_url = f"{region_url}{search_keyword}"

    # 검색 결과 페이지에 접근하고 첫 요청 카운트
    driver.get(main_url)
    total_requests += 1
    search_page_requests += 1

    # '더보기' 버튼을 반복적으로 클릭하여 전체 물품 로드
    while True:
        try:
            more_button = driver.find_element(By.CSS_SELECTOR, "#main-content > div._6vo5t01._6vo5t00._588sy4n8._588sy4nl._588sy4o4._588sy4on._588sy4ou._588sy4p7._588sy4k2._588sy4kf._588sy4ky._588sy4lh._588sy4lo._588sy4m1._588sy4n._588sy462 > div > section > div > div._13tpfox8._588sy4r8 > button")
            more_button.click()
            time.sleep(1)  # 로딩 시간 대기
            total_requests += 1
            search_page_requests += 1
        except:
            print(f"{main_url} 더보기 버튼이 더 이상 없습니다.")
            break

    # 로드된 페이지 소스를 BeautifulSoup으로 파싱
    soup = BeautifulSoup(driver.page_source, "html.parser")
    getItem = soup.select("#main-content > div._6vo5t01._6vo5t00._588sy4n8._588sy4nl._588sy4o4._588sy4on._588sy4ou._588sy4p7._588sy4k2._588sy4kf._588sy4ky._588sy4lh._588sy4lo._588sy4m1._588sy4n._588sy462 > div > section > div > div._13tpfox1._13tpfox0._588sy462._13tpfox3 > a")
    
    # 각 아이템에 대해 필요한 정보 추출
    data = []
    for item in getItem:
        # 메인 페이지에서 추출하는 데이터
        title = item.get('data-title')
        price = item.get('data-price')
        link = item.get('href')
        item_url = f"https://www.daangn.com{link}"
        
        # 이미지 URL 추출
        img_tag = item.select_one('div._1b153uwf._1b153uwe._588sy49e._588sy41b._588sy4ck > noscript > span > img')
        img_url = img_tag['src'] if img_tag else None

        # 상태 정보 추출
        status_tag = item.select_one('div._1b153uwf._1b153uwe._588sy49e._588sy41b._588sy4ck > span._1b153uws._1b153uwr._588sy41y._1b153uwu')
        status = status_tag.text.strip() if status_tag else "판매중"

        # 지역 추출
        region_tag = item.select_one('div._1b153uwo._1b153uwn._588sy462 > div._1b153uwq._1b153uwp._588sy41w._588sy462._588sy41b')
        region = region_tag.text.strip() if region_tag else "지역 정보 없음"

        # 상세 페이지에 접근하여 추가로 데이터 추출
        driver.get(item_url)
        time.sleep(1)  # 페이지 로드 대기
        total_requests += 1
        detail_page_requests += 1
        detail_soup = BeautifulSoup(driver.page_source, "html.parser")

        # 상세 페이지 데이터 추출 (기존 코드 사용)
        image_tags = detail_soup.select('div._588sy41b._588sy462 img._1io8bol1')
        image_urls = [img['src'] for img in image_tags if img.has_attr('src')]
        seller_profile_tag = detail_soup.select_one('div._1ry6htk0 a')
        seller_profile = seller_profile_tag['href'] if seller_profile_tag else None
        seller_nickname_tag = detail_soup.select_one('span._1ry6htkk')
        seller_nickname = seller_nickname_tag.text.strip() if seller_nickname_tag else "닉네임 정보 없음"
        seller_region_tag = detail_soup.select_one('a._1ry6htk13')
        seller_region = seller_region_tag.text.strip() if seller_region_tag else "지역 정보 없음"
        manner_temp_tag = detail_soup.select_one('span._1kkdjtzl')
        manner_temp = manner_temp_tag.text.strip().replace("°C", "") if manner_temp_tag else "온도 정보 없음"
        detail_status_tag = detail_soup.select_one('span.vqbuc9b')
        detail_status = detail_status_tag.text.strip() if detail_status_tag else "상태 정보 없음"
        title_tag = detail_soup.select_one('h1.vqbuc9f')
        detail_title = title_tag.text.strip() if title_tag else "제목 정보 없음"
        category_tag = detail_soup.select_one('a.vqbuc9i')
        category = category_tag.text.strip() if category_tag else "카테고리 정보 없음"
        time_tag = detail_soup.select_one('time')
        post_time = time_tag['datetime'] if time_tag and time_tag.has_attr('datetime') else "등록 시간 정보 없음"
        time_passed = time_tag.text.strip() if time_tag else "경과 시간 정보 없음"
        price_tag = detail_soup.select_one('h3.vqbuc9k')
        detail_price = price_tag.text.strip() if price_tag else "가격 정보 없음"
        description_tag = detail_soup.select_one('p.vqbuc9m')
        description = description_tag.text.strip() if description_tag else "상세 설명 없음"
        info_tags = detail_soup.select('div.vqbuc9p span')
        chat_count = info_tags[0].text.replace("채팅 ", "") if len(info_tags) > 0 else "0"
        interest_count = info_tags[1].text.replace("관심 ", "") if len(info_tags) > 1 else "0"
        view_count = info_tags[2].text.replace("조회 ", "") if len(info_tags) > 2 else "0"

        # 상세 페이지 데이터 추가
        detailed_data = {
            "image_links": image_urls,
            "seller_profile_link": seller_profile,
            "seller_nickname": seller_nickname,
            "seller_region": seller_region,
            "seller_manner_temp": manner_temp,
            "detail_status": detail_status,
            "detail_title": detail_title,
            "category": category,
            "post_time": post_time,
            "time_passed": time_passed,
            "detail_price": detail_price,
            "description": description,
            "chat_count": chat_count,
            "interest_count": interest_count,
            "view_count": view_count
        }

        # 메인 페이지 데이터와 병합
        item_data = {
            "main_page_data": {
                "status": status,
                "title": title,
                "price": price,
                "region": region,
                "link": item_url,
                "img_url": img_url
            },
            "detailed_page_data": detailed_data
        }

        # 리스트에 추가
        data.append(item_data)

    # 지역별 데이터를 전체 데이터 리스트에 병합
    all_data.extend(data)

# 드라이버 종료
driver.quit()

# 종료 시간 및 작업 시간 계산
end_time = datetime.now()
duration = end_time - start_time

# 데이터 파일명 설정
timestamp = end_time.strftime("%Y%m%d_%H%M%S")
data_filename = f"daangn_10p_{timestamp}_{search_keyword}.json"

# JSON 파일로 저장
with open(data_filename, "w", encoding="utf-8") as json_file:
    json.dump(all_data, json_file, ensure_ascii=False, indent=4)

# 크롤링 요약 정보 기록
result_summary = {
    "search_keyword": search_keyword,
    "total_requests": total_requests,
    "search_page_requests": search_page_requests,
    "detail_page_requests": detail_page_requests,
    "total_items": len(all_data),
    "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
    "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
    "duration": str(duration)
}

# result.json에 기록 추가
try:
    with open("result.json", "r", encoding="utf-8") as result_file:
        result_data = json.load(result_file)
except FileNotFoundError:
    result_data = []

result_data.append(result_summary)

with open("result.json", "w", encoding="utf-8") as result_file:
    json.dump(result_data, result_file, ensure_ascii=False, indent=4)

# 결과 출력
print(f"데이터가 '{data_filename}' 파일로 저장되었습니다.")
print("요약 정보가 'result.json'에 기록되었습니다.")
print(f"파싱한 데이터의 수: {len(all_data)}")
print(f"총 요청 수: {total_requests}")