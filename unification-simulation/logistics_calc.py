import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2):
    """두 위경도 좌표 간 haversine 거리(km) 계산"""
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def run_logistics_comparison(before_path, after_path, nk_path):
    # 데이터 로드 (인코딩 예외 처리 포함)
    try:
        df_before = pd.read_excel(before_path)
        df_after = pd.read_excel(after_path)
        df_nk = pd.read_csv(nk_path, encoding="euc-kr")
    except UnicodeDecodeError:
        df_nk = pd.read_csv(nk_path, encoding="utf-8")

    # 북한 역 좌표 컬럼명 정리
    df_nk = df_nk.rename(columns={
        "지명": "역명",
        "Y좌표": "위도",
        "X좌표": "경도"
    })

    # 좌표 붙이기
    def attach_coordinates(df):
        df = df.copy()
        df = df.merge(df_nk[["역명", "위도", "경도"]], left_on="출발지", right_on="역명", how="left")
        df = df.rename(columns={"위도": "출발_위도", "경도": "출발_경도"}).drop(columns=["역명"])
        df = df.merge(df_nk[["역명", "위도", "경도"]], left_on="도착지", right_on="역명", how="left")
        df = df.rename(columns={"위도": "도착_위도", "경도": "도착_경도"}).drop(columns=["역명"])
        return df

    df_after = attach_coordinates(df_after)

    # 거리 및 시간 계산
    df_after["계산_거리(km)"] = df_after.apply(
        lambda row: haversine(row["출발_위도"], row["출발_경도"], row["도착_위도"], row["도착_경도"]),
        axis=1
    )
    df_after["계산_시간(h)"] = df_after["계산_거리(km)"] / df_after["평균 속도(km/h)"]

    # 전체 소요 시간 비교
    before_total_time = df_before["총 시간(h)"].sum()
    after_total_time = df_after["계산_시간(h)"].sum()

    return {
        "통일 전 시간": before_total_time,
        "통일 후 시간": after_total_time,
        "감소 시간": before_total_time - after_total_time,
        "df_통일후": df_after
    }
