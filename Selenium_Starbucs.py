#//* 셀레니움 라이브러리
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#//* 웹드라이버 메니저
from webdriver_manager.chrome import ChromeDriverManager

#//* 뷰티플수프 
from bs4 import BeautifulSoup

#//* 파이썬 표준 라이브러리
import time
import os,json,csv,re

#함수만들기
def starbucks():
    try:
        #01. WebDriver객체 생성
        service = Service(ChromeDriverManager().install())

        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach',True)
        options.add_argument('headless')

        driver = webdriver.Chrome(service=service,options=options)

        #02. 스타벅스 매장 찾기 로딩
        driver.get('https://www.starbucks.co.kr/store/store_map.do')

        #03. 지역버튼 찾고 클릭 처리하기(정적인 요소)(XPATH 복사해오기)
        local = driver.find_element(By.XPATH,'//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/header[2]/h3/a')
        local.send_keys(Keys.ENTER)

        #04. 서울버튼 클릭하기(동적인 요소)
        # NoSuchElementExceptiond에러
        # seoul = driver.find_element(By.XPATH,'//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/article[2]/div[1]/div[2]/ul/li[1]/a')
        seoul = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/article[2]/div[1]/div[2]/ul/li[1]/a')))
        seoul.click()

        #05. 전체 버튼 찾고 클릭 처리(동적인 요소)
        inSeoul = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mCSB_2_container"]/ul/li[1]/a')))
        inSeoul.click()

        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mCSB_3_container > ul > li')))

        #06. Beautifulsoup로 스크래핑 서울 전체 매장 스크래핑
        soup = BeautifulSoup(driver.page_source,'html.parser')
        liTags = soup.select('#mCSB_3_container > ul > li')#[Tag,Tag,....]
        print(len(liTags))
        print(liTags[0].get_text().strip())
        
        #[{},{},{},...]형태로 크롤링한 매장 저장
        stores=[] 

        for liTag in liTags:
            print(liTag.get_text().strip())

        pattern = re.compile(r'(.+)\s{3}(.+)(\d{4}-\d{4})\s.+')
        for liTag in liTags:
            match=pattern.match(liTag.get_text().strip())
            if match:
                stores.append(dict(zip(['store','location','contact'],[match.group(1),match.group(2),match.group(3)])))

        print(stores)
        print(len(stores))
        #  파이썬 객체(stores)를 JSON파일로 저장
        with open('starbucks.json','w',encoding='utf8') as f:
            #f.write(stores)#TypeError: write() argument must be str, not list
            f.write(json.dumps(stores,indent=4,ensure_ascii=False))

        # 파이썬 객체(stores)를 CSV파일로 저장
        with open('starbucks.csv', 'w', encoding='utf8',newline='') as f:
            writer = csv.DictWriter(f,fieldnames=stores[0].keys())
            writer.writeheader()
            writer.writerows(stores)

    except TimeoutException as e:
        print('찾는 요소가 없어요:',e)
    finally:
        pass
        #driver.quit()

if __name__ == '__main__':
    starbucks()  

