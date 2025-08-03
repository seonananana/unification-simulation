import pandas as pd

def calculate_travel_time(df):
    """거리와 속도로 이동 시간 계산 (시간 단위)"""
    df["이동시간"] = df["거리(km)"] / df["속도(km/h)"]
    return df

def run_logistics_comparison(before_path, after_path, nk_path):
    """
    통일 전/후 물류 비교 분석
    - before_path: 통일 전 데이터 엑셀 경로
    - after_path: 통일 후 데이터 엑셀 경로
    - nk_path: 북한 역 위치 CSV (지명, 위도/경도)
    """
    # 1. 데이터 불러오기
    df_before = pd.read_excel(before_path)
    df_after = pd.read_excel(after_path)
    df_nk = pd.read_csv(nk_path)

    # 2. 열 이름 표준화
    df_before = df_before.rename(columns={
        "출발역": "출발역", 
        "도착역": "도착역", 
        "거리(km)": "거리(km)", 
        "속도(km/h)": "속도(km/h)"
    })
    df_after = df_after.rename(columns={
        "출발역": "출발역", 
        "도착역": "도착역", 
        "거리(km)": "거리(km)", 
        "속도(km/h)": "속도(km/h)"
    })
    df_nk = df_nk.rename(columns={
        "지명": "역명", 
        "Y좌표": "위도", 
        "X좌표": "경도"
    })

    # 3. 이동 시간 계산
    df_before = calculate_travel_time(df_before)
    df_after = calculate_travel_time(df_after)

    # 4. 총 시간 계산
    total_time_before = df_before["이동시간"].sum()
    total_time_after = df_after["이동시간"].sum()

    # 5. 반환
    return {
        "통일 전 시간": total_time_before,
        "통일 후 시간": total_time_after,
        "통일 전 구간 수": len(df_before),
        "통일 후 구간 수": len(df_after),
    }
