import selenium
print(selenium.__version__) # 버전확인

#//* 셀레니움 라이브러리
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#//* 웹드라이버 메니저
from webdriver_manager.chrome import ChromeDriverManager

#//* 파이썬 표준 라이브러리
import time

#1. 웹 드라이버를 위한 Service객체 생성
##1-1. 수동으로 설치 시
# service = Service(executable_path='chromedriver.exe')
##1-2. pip웹드라이버 설치 시
service = Service(ChromeDriverManager().install())

#2. 웹 드라이버 객체 생성
driver = webdriver.Chrome(service=service)

#3. 웹 드라이버 옵션 설정(떳다 사라짐 막기)
## 크롬브라우저용 옵션 객체 생성
options = webdriver.ChromeOptions()
### 옵션1) 브라우저 닫히지 않게
options.add_experimental_option('detach',True)
### 옵션2) 브라우저 보이지 않게
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
### 옵션3) 전체화면
options.add_argument('--start-fullscreen')

#4. 사이트 요청
driver.get("https://www.naver.com")

print(driver.page_source) # html 소스
with open('D:\\JJS\WORKSPACE\\Python\\Study_Python\\naver.html','w',encoding='utf8') as f:
    f.write(driver.page_source)

print(driver.current_url) # 웹드라이버 현재 URL



#브라우저 닫기
driver.quit()