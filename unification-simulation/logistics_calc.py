import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

# Haversine 거리 계산 함수
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # 지구 반지름 (km)
    return c * r

def run_logistics_comparison(before_path, after_path, nk_path):
    # 통일 전 데이터 로드
    df_before = pd.read_excel(before_path)

    # 통일 후 데이터 로드
    df_after = pd.read_excel(after_path)

    # 북한 역 위치 데이터 로드 (인코딩 예외 처리 포함)
    try:
        df_nk = pd.read_csv(nk_path, encoding='euc-kr')
    except UnicodeDecodeError:
        df_nk = pd.read_csv(nk_path, encoding='utf-8')

    # 필요한 컬럼 선택 및 전처리
    df_nk = df_nk[["역명", "경도", "위도"]].dropna()

    # 통일 후 역 위치 보완
    merged = pd.merge(df_after, df_nk, left_on="도착지", right_on="역명", how="left")
    merged = pd.merge(merged, df_nk, left_on="출발지", right_on="역명", how="left", suffixes=("_도착", "_출발"))

    # 거리 계산
    merged["거리"] = merged.apply(lambda row: haversine(row["경도_출발"], row["위도_출발"], row["경도_도착"], row["위도_도착"]), axis=1)

    # 평균 속도 기반 시간 추정
    avg_speed_kmh = 50  # 화물철도 평균 속도 (가정)
    merged["예상시간"] = merged["거리"] / avg_speed_kmh

    # 총 시간 계산
    total_time_before = df_before["총 시간(h)"].sum()
    total_time_after = merged["예상시간"].sum()

    return {"통일 전 시간": total_time_before, "통일 후 시간": total_time_after}
