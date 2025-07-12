import sys
import codecs
import time
from datetime import datetime, timedelta
import random
import requests
import json
import csv
import os
import pandas as pd
import folium 
import webbrowser
from folium.plugins import HeatMap
import pickle
import csv
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
# def main():
#     page = 1
#     data_count = 100
#     total_result_list = []

#     while True:
#         data_list = getCrawlData(page, data_count)
#         if data_list == None:
#             break

#         total_result_list += data_list
#         page += 1

#         if page >= 99:
#             break
#         elif len(data_list) < data_count:
#             break

#         time.sleep(random.uniform(1, 2))

#     save_to_csv(total_result_list)

#     print(f"Total data collected: {len(total_result_list)}")
#     exit(1)

# def getCrawlData(page_number, data_count):
#     api_key = '6c7rt6bp66_37et6_oee7jc373c37777'
#     url = "https://open.jejudatahub.net/api/proxy/atDab6t8218btaa122b26DDtbatD86t1/" + api_key

#     params = {
#         'number': page_number,
#         'limit': data_count
#     }

#     try:
#         res = requests.get(url, params=params)
#         res.raise_for_status() 
#     except requests.exceptions.RequestException as e:
#         print(f"Error calling the API: {e}")
#         return None

#     try:
#         res_json = res.json()
#         return res_json['data']
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON: {e}")
#         return None

# def save_to_csv(data_list):
#     if not data_list:
#         print("No data to save.")
#         return

#     directory = "c:/Users/kangj/Downloads" 
#     filename = "crawled_data.csv"
#     full_path = directory + filename  

#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     keys = data_list[0].keys()  
#     with open(full_path, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=keys)
#         writer.writeheader()
#         writer.writerows(data_list)

#     print(f"Data saved to {full_path}")

# if __name__ == '__main__':
#     main()


# csv_file_path = "c:/Users/kangj/Downloadscrawled_data.csv"
# df = pd.read_csv(csv_file_path)

# field_mapping = {
#     "chargingPlace": "충전소위치",
#     "chargingPlaceDetail": "충전소위치상세",
#     "holiday": "휴점일",
#     "startTime": "이용가능시작시간",
#     "endTime": "이용가능종료시간",
#     "chargingFlag": "완속충전가능여부",
#     "quickChargingFlag": "급속충전가능여부",
#     "quickChargingType": "급속충전기타입",
#     "chargerCount": "완속충전기개수",
#     "quickChargerCount": "급속충전기개수",
#     "parkingFeeFlag": "주차료부과여부",
#     "addressJibun": "지번주소",
#     "addressDoro": "도로명주소",
#     "anagementCompany": "관리업체",
#     "latitude": "위도",
#     "longitude": "경도",
#     "provider": "제공기관명",
#     "baseDate": "기준일",
# }
# df = df.rename(columns=field_mapping)

# new_csv_file_path = "C:/Users/kangj/Downloads/제주 전기차충전소API.csv"
# df.to_csv(new_csv_file_path, index=False, encoding="utf-8-sig")

# jeju_df= pd.read_csv("C:/Users/kangj/Downloads/제주 전기차충전소API.csv")
# jeju_df['행정구역'] = jeju_df['도로명주소'].apply(lambda x: str(x).split()[1] if isinstance(x, str) and len(x.split()) > 1 else '미상')
# jeju_df=jeju_df[["충전소위치","충전소위치상세","휴점일", "이용가능시작시간","이용가능종료시간", "완속충전가능여부","급속충전가능여부",
#                     "급속충전기타입","완속충전기개수"
#                     ,"급속충전기개수","주차료부과여부", "행정구역","지번주소","도로명주소","관리업체","위도","경도","제공기관명","기준일"]]
# jeju_df.to_csv("c:/Users/kangj/Downloads/제주 전기차 충전소 API.csv", index=False, encoding='utf-8-sig')


div = "c:/Users/kangj/Downloads/제주 전기차 충전소 API.csv"
dd = pd.read_csv(div, encoding='UTF-8')
dd['위도경도'] = dd[['위도', '경도']].values.tolist()
dd= dd.drop_duplicates(subset=['충전소위치', '충전소위치상세', '휴점일', '이용가능시작시간', '이용가능종료시간', 
                               '완속충전가능여부', '급속충전가능여부', '급속충전기타입', '완속충전기개수', '급속충전기개수', 
                               '주차료부과여부', '행정구역', '지번주소', '도로명주소', '관리업체', '위도', '경도', '제공기관명'])
mask = dd['행정구역'] == '미상'  
dd.loc[mask, '행정구역'] = dd.loc[mask, '지번주소'].apply(
    lambda x: str(x).split()[1] if isinstance(x, str) and len(x.split()) > 1 else '미상')
dd.to_csv("C:/Users/kangj/Downloads/제주 전기차 충전소 정보.csv", index=False, encoding='utf-8-sig')

charger = pd.read_csv("C:/Users/kangj/Downloads/제주 전기차 충전소 정보.csv",encoding='UTF-8')
charger = charger[
    (charger['위도'] >= 33.0) & (charger['위도'] <= 33.78) &
    (charger['경도'] >= 126.0) & (charger['경도'] <= 127.0)
].reset_index(drop=True)

region_counts = charger['행정구역'].value_counts()
print("행정구역별 충전소 개수")
print(region_counts)
print("\n")

quickcharger = charger.groupby('행정구역')['급속충전기개수'].sum()
slowcharger = charger.groupby('행정구역')['완속충전기개수'].sum()
print("행정구역별 급속충전기 개수")
print(quickcharger)
print("행정구역별 완속충전기 개수")
print(slowcharger)
print("\n")

charger['읍면동'] = charger['지번주소'].apply(lambda x: str(x).split()[2] if isinstance(x, str) and len(x.split()) > 2 else '미상')
mask2 = charger['읍면동'] == '미상'
charger.loc[mask2, '읍면동'] = charger.loc[mask2, '도로명주소'].apply(
    lambda x: str(x).split()[2] if isinstance(x, str) and len(x.split()) > 2 else '미상')
region_counts2 = charger['읍면동'].value_counts()
region_counts2 = region_counts2.head(6)
print("읍면동별 충전소 개수")
print(region_counts2)
print('\n')
many_quickcharger = charger.groupby('읍면동')['급속충전기개수'].sum()
many_quickcharger=many_quickcharger.sort_values(ascending=False)
many_quickcharger= many_quickcharger.head(5)
many_slowcharger = charger.groupby('읍면동')['완속충전기개수'].sum()
many_slowcharger = many_slowcharger.sort_values(ascending=False)
many_slowcharger = many_slowcharger.head(5)
print("읍면동 별 급속충전기 개수 순위")
print(many_quickcharger)
print('\n')
print("읍면동 별 완속충전기 개수 순위")
print(many_slowcharger)


m = folium.Map([33.48992, 126.4985], zoom_start=12)

group_fast_only = folium.FeatureGroup(name='급속충전만 가능')
group_slow_only = folium.FeatureGroup(name='완속충전만 가능')
group_both = folium.FeatureGroup(name='급속, 완속 모두 가능')

for i in range(len(charger)):
    latlon = charger.loc[i, ['위도', '경도']].tolist()
    mark = charger.loc[i, '충전소위치']
    charger1 = charger.loc[i, '완속충전기개수']
    charger2 = charger.loc[i, '급속충전기개수']
    holiday = charger.loc[i, '휴점일']
    parking = '주차료 부과' if charger.loc[i, '주차료부과여부'] else '주차료 미부과'
    juso1 = charger.loc[i, '도로명주소']
    juso2 = charger.loc[i, '지번주소']
    fast_ok = charger.loc[i, '급속충전가능여부']
    slow_ok = charger.loc[i, '완속충전가능여부']

    if charger1 == 0 and charger2 >= 1:
        color = "blue"
    elif charger1 >= 1 and charger2 == 0:
        color = "red"
    else:
        color = "green"

    popup_html = f"""
        <b>{mark}</b><br>
        휴점일: {holiday}<br>
        주차료: {parking}<br>
        완속충전기: {charger1}대<br>
        급속충전기: {charger2}대<br>
        도로명주소: {juso1}<br>
        지번주소: {juso2}
    """

    marker = folium.CircleMarker(
        location=latlon,
        color=color,
        radius=2,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=mark,
        fill=True,
        fill_opacity=0.7
    )

    # 필터 조건에 따라 그룹에 추가
    if fast_ok and slow_ok:
        marker.add_to(group_both)
    elif fast_ok and not slow_ok:
        marker.add_to(group_fast_only)
    elif not fast_ok and slow_ok:
        marker.add_to(group_slow_only)
        
# 그룹을 지도에 추가
group_both.add_to(m)
group_fast_only.add_to(m)
group_slow_only.add_to(m)


# LayerControl 추가
folium.LayerControl(collapsed=False).add_to(m)

# 저장 및 열기
m.save("jejuelectric_heatmap.html")
webbrowser.open("jejuelectric_heatmap.html")




