from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os
import json
import csv
import re

def hira_health():
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        options.add_argument('--window-size=1920,1080')
        driver = webdriver.Chrome(service=service, options=options)

        driver.get('https://www.hira.or.kr/ra/hosp/getHealthMap.do?tabgbn=03&WT.ac=HIRA%EA%B1%B4%EA%B0%95%EC%A7%80%EB%B0%94%EB%A1%9C%EA%B0%80%EA%B8%B0#')

        # 지역 클릭
        region = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="hosp-form"]/div[2]/a')))
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", region)
        region.click()
        print("지역 선택 클릭 성공")

        # 서울 클릭
        seoul = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sidoCdMap"]/li[2]/a')))
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", seoul)
        driver.execute_script("arguments[0].click();", seoul)
        print("서울 선택 클릭 성공")

        # 확인 버튼 클릭
        confirm_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'btnSearchJuso')))
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", confirm_button)
        driver.execute_script("arguments[0].click();", confirm_button)
        print("확인 버튼 클릭 성공")

        # 병원 목록이 로드될 때까지 대기
        time.sleep(10)  # 10초 대기

        # 병원 목록 가져오기
        hospitals_loaded = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="resultLayer2"]/div[2]/div/ul/li')))
        print("병원 목록 로드 성공")

        # BeautifulSoup로 스크래핑
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        li_tags = soup.select('#resultLayer2 > div:nth-child(2) > div > ul > li')

        print(f"크롤링된 병원 목록 수: {len(li_tags)}")

        hospitals = []

        for li in li_tags[:10]:  # 상위 10개 병원만 크롤링
            name_tag = li.select_one('a.tit')
            address_tag = li.select_one('span[onclick^="HospitalMap.hospYkihoMap"]')

            if name_tag and address_tag:
                name = name_tag.get_text(strip=True)
                address = address_tag.get_text(strip=True).replace('주소', '')
                hospitals.append({'name': name, 'address': address})

        print(f"추출된 병원 정보 수: {len(hospitals)}")

        if not hospitals:
            print("병원 정보를 추출하지 못했습니다. HTML 구조가 변경되었을 수 있습니다.")

        with open('D:\\JJS\WORKSPACE\\Python\\Study_Python\\hira_health_seoul_top10.json', 'w', encoding='utf8') as f:
            f.write(json.dumps(hospitals, indent=4, ensure_ascii=False))

        with open('D:\\JJS\WORKSPACE\\Python\\Study_Python\\hira_health_seoul_top10.csv', 'w', encoding='utf8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=hospitals[0].keys() if hospitals else [])
            writer.writeheader()
            if hospitals:
                writer.writerows(hospitals)

    except TimeoutException as e:
        print('찾는 요소가 없어요:', e)
    except ElementNotInteractableException as e:
        print('요소와 상호작용할 수 없어요:', e)
    finally:
        driver.quit()

if __name__ == '__main__':
    hira_health()
