import requests
import math

##############################################################################
# 기본위치 설정
location = "경기 김포시 김포대로 지하 710 (사우동)"

## 기본위치 쿼리문에 넣고 url만들기
url = f"https://dapi.kakao.com/v2/local/search/address.json?query={location}"

## API요청헤더(인증토큰-서버에 접근 권한 요청)
headers = {
    "Authorization" : f"KakaoAK 6da2d4ef4e4d4ac3f024dba116cd0233"
}

## requests모듈로 get요청 -> result에 get응답 저장
result = requests.get(url, headers = headers)

## 응답데이터를 json형태로 변환 -> 딕셔너리로 활용할 수 있음
json_obj = result.json()

# print('▼*80')
# print(json_obj)

## 기본위치의 위도 경도 값 뽑아내고 부동소수점->숫자로
latitude = float(json_obj['documents'][0]['y'])
longitude = float(json_obj['documents'][0]['x'])

##############################################################################
# 매개변수들을 기반으로 카카오 로컬 API에 적합한 검색 URL을 생성
def get_url(latitude, longitude, page):
    return f"https://dapi.kakao.com/v2/local/search/category.json?category_group_code=HP8&radius=20000&x={longitude}&y={latitude}&size=10&page={page}"

##############################################################################
# 두 지점의 위도와 경도를 사용하여 지구 표면을 따라 두 지점 간의 거리를 계산(*하버사인 공식*)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance
##############################################################################
# 지정된 위치(위도, 경도)에서 병원 목록(5페이지)을 가져오는 함수
def get_hospitals(latitude, longitude, num_pages = 5) :
    all_hospitals = []

    for page in range(1, num_pages + 1) :
        all_url = get_url(latitude, longitude, page)
        response = requests.get(all_url, headers = headers)

        if response.status_code == 200:
            data = response.json()
            hospitals = data.get('documents', [])
            all_hospitals.extend(hospitals)

        else:
            print(f"Error: {response.status_code}")
            break

    return all_hospitals

###############################[프로그램시작]###########################################
# 지정된 위치(위도, 경도)에서 병원 목록을 가져와 각 병원의 이름, 주소, 거리 정보를 출력
find_hospitals = get_hospitals(latitude, longitude, num_pages = 5)

for idx, hospital in enumerate(find_hospitals, 1):
    place_name = hospital['place_name']
    address = hospital['address_name']

    # 위도경도
    hospital_lat = float(hospital['y'])
    hospital_lon = float(hospital['x'])

    # 거리계산
    distance = haversine(latitude, longitude, hospital_lat, hospital_lon)

    #출력
    print(f"{idx}. {place_name} - {address} - 거리: {round(distance, 2)}m")