# logistics_calc.py
import pandas as pd
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

def run_logistics_comparison(before_path, after_path, nk_path):
    df_before = pd.read_excel(before_path)
    df_before['위도(y)'] = pd.to_numeric(df_before['위도(y)'], errors='coerce')
    df_before['경도(x)'] = pd.to_numeric(df_before['경도(x)'], errors='coerce')
    df_before['거리(km)'] = pd.to_numeric(df_before['거리(km)'], errors='coerce')

    거리_list = []
    for idx in range(len(df_before)):
        if idx + 1 >= len(df_before):
            거리_list.append(0)
            continue
        lat1, lon1 = df_before.loc[idx, ['위도(y)', '경도(x)']]
        lat2, lon2 = df_before.loc[idx + 1, ['위도(y)', '경도(x)']]
        if not np.isnan(lat1) and not np.isnan(lon1) and not np.isnan(lat2) and not np.isnan(lon2):
            dist = haversine(lat1, lon1, lat2, lon2)
        else:
            dist = np.nan
        거리_list.append(df_before.loc[idx, '거리(km)'] if pd.notna(df_before.loc[idx, '거리(km)']) else dist)
    df_before['거리(km)'] = 거리_list
    df_before['속도(km/h)'] = pd.to_numeric(df_before['속도(km/h)'], errors='coerce').fillna(34)
    df_before['시간(h)'] = df_before['거리(km)'] / df_before['속도(km/h)']

    df_after = pd.read_excel(after_path)
    df_after['속도(km/h)'] = pd.to_numeric(df_after['속도(km/h)'], errors='coerce')
    df_after['시간(h)'] = df_after['거리(km)'] / df_after['속도(km/h)']

    df_nk = pd.read_csv(nk_path, encoding='euc-kr')
    target_nk_stations = ['판문역', '평산역', '사리원역', '구성역', '신의주역']
    nk_filtered = df_nk[df_nk['지명'].isin(target_nk_stations)][['지명', 'Y좌표', 'X좌표']]
    nk_filtered = nk_filtered.set_index('지명').loc[target_nk_stations].reset_index()

    distances = []
    for i in range(len(nk_filtered)-1):
        lat1, lon1 = nk_filtered.loc[i, ['Y좌표', 'X좌표']]
        lat2, lon2 = nk_filtered.loc[i+1, ['Y좌표', 'X좌표']]
        distances.append(haversine(lat1, lon1, lat2, lon2))

    df_nk_dist = pd.DataFrame({
        '출발지': target_nk_stations[:-1],
        '도착지': target_nk_stations[1:],
        '거리(km)': distances,
        '속도(km/h)': 40
    })
    df_nk_dist['시간(h)'] = df_nk_dist['거리(km)'] / df_nk_dist['속도(km/h)']

    df_after_renamed = df_after.rename(columns={'출발역': '출발지', '도착역': '도착지'})[['출발지', '도착지', '거리(km)', '속도(km/h)', '시간(h)']]
    df_after_full = pd.concat([df_after_renamed, df_nk_dist], ignore_index=True)

    return {
        '통일 전 거리': df_before['거리(km)'].sum(),
        '통일 전 시간': df_before['시간(h)'].sum(),
        '통일 후 거리': df_after_full['거리(km)'].sum(),
        '통일 후 시간': df_after_full['시간(h)'].sum(),
    }
