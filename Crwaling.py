import requests
print(dir(requests))


# 방법1)
# request()로 모든 요청 가능
# method 키워드 인수에 요청 방식 지정
res = requests.get(url='https://www.dogdrip.net/dogdrip',headers={'User-Agent':'Mozilla/5.0'})
# print(res,type(res))
# print('----------------')
# print(res.encoding)
# print(res.status_code)
# print(res.url)
# print(res.headers)
# print(res.text)
# print(res.content)
res.encoding='utf-8'
# print(res.text)
# print(res.content)
'''
with open('daum_requests.html','w',encoding='utf-8') as f:
    f.write(res.text)
'''

url='https://images.pexels.com/photos/3081487/pexels-photo-3081487.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500'
res = requests.get(url=url)
print(res.request.method)
with open('landscape3.jpeg','wb')as f:
    f.write(res.content)
