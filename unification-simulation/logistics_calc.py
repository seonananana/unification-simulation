import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2):
    """두 지점 간의 haversine 거리 계산 (단위: km)"""
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def run_logistics_comparison(before_path, after_path, nk_path):
    # 파일 로드
    try:
        df_before = pd.read_excel(before_path)
        df_after = pd.read_excel(after_path)
        df_nk = pd.read_csv(nk_path, encoding="euc-kr")
    except UnicodeDecodeError:
        df_nk = pd.read_csv(nk_path, encoding="utf-8")

    # 북한 지도 컬럼 정리
    df_nk = df_nk.rename(columns={
        "지명": "역명",
        "Y좌표": "위도",
        "X좌표": "경도"
    })

    # 좌표 병합 함수
    def attach_coordinates(df):
        df = df.copy()
        df = df.merge(df_nk[["역명", "위도", "경도"]], left_on="출발역", right_on="역명", how="left")
        df = df.rename(columns={"위도": "출발_위도", "경도": "출발_경도"}).drop(columns=["역명"])

        df = df.merge(df_nk[["역명", "위도", "경도"]], left_on="도착역", right_on="역명", how="left")
        df = df.rename(columns={"위도": "도착_위도", "경도": "도착_경도"}).drop(columns=["역명"])
        return df

    # 좌표 부여
    df_after = attach_coordinates(df_after)

    # 거리 재계산 및 시간 계산
    df_after["계산_거리(km)"] = df_after.apply(
        lambda row: haversine(row["출발_위도"], row["출발_경도"], row["도착_위도"], row["도착_경도"]),
        axis=1
    )
    df_after["계산_시간(h)"] = df_after["계산_거리(km)"] / df_after["속도(km/h)"]

    # 결과 계산
    before_total_time = df_before["총 시간(h)"].sum()
    after_total_time = df_after["계산_시간(h)"].sum()

    return {
        "통일 전 시간": before_total_time,
        "통일 후 시간": after_total_time,
        "감소 시간": before_total_time - after_total_time,
        "df_통일후": df_after
    }
