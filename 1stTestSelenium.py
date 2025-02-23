# 셀레니엄으로 크롬자동화를 만들기
# 먼저 콘다를 설치해야하네(파이참으로 어떻게 되긴하는데)
'''
import selenium
from selenium import webdriver
driverpath = '/Users/JJS/JUB/UTILITY/chrome-mac-x64'
driver = webdriver.Chrome(driverpath)
from selenium.webdriver.chorme.service import Service
from selenium import webdriver
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time




# 이건 뭐지?
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))

url = "https://www.naver.com/"
driver.get(url)
time.sleep(5)

# 오케 여기까지 성공/////////////////////////////////////////////////////
'''
# ChromeDriver 경로 설정
service = Service('/Users/JJS/JUB/UTILITY/chrome-mac-x64')
driver = webdriver.Chrome(service=service)
'''

# 웹사이트 열기
driver.get('https://www.google.com')

# 검색 상자 찾기
search_box = driver.find_element(By.NAME, 'q')

# 검색어 입력 및 검색 실행
search_box.send_keys('Selenium Python')
search_box.send_keys(Keys.RETURN)

# 검색 결과 페이지 제목 출력
print(driver.title)

# 브라우저 닫기
driver.quit()