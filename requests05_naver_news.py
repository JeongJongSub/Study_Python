
import requests

client_id = "SNH3x0XWPFE_CcuifvsE"
client_secret = "CTKR8I1fN1"

query = input('검색할 단어를 입력하세요?')


url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=100"

res = requests.get(url,headers={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret})

if(res.status_code==200):
    data=res.json()
    print('[네이버 OPEN API서버에서 받은 데이타]',data,sep='\n')
    newses=data.get("items")
    print(f'<< {query} 관련 네이버 뉴스 기사들 >>')
    for news in newses:
        print(f"[제목] {news['title']}\t[링크] {news['link']}\t[기사일] {news['pubDate']}\t[기사내용] {news['description']}")

else:
    print("Error Code:" + res.status_code)
