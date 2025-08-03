import pandas as pd
import numpy as np
import os


def run_logistics_comparison(before_path, after_path, nk_path):
    # 파일 로딩 함수 (인코딩 자동 감지 포함)
    def load_excel_or_csv(path):
        ext = os.path.splitext(path)[-1]
        try_encodings = ["utf-8-sig", "cp949", "euc-kr"]
        for enc in try_encodings:
            try:
                if ext == ".xlsx":
                    return pd.read_excel(path)
                elif ext == ".csv":
                    return pd.read_csv(path, encoding=enc)
            except Exception:
                continue
        raise FileNotFoundError(f"파일을 열 수 없습니다: {path}")

    # 1. 북한 역 위치 파일
    nk_df = load_excel_or_csv(nk_path)
    if not all(col in nk_df.columns for col in ["지명", "X좌표", "Y좌표"]):
        raise ValueError("❌ 북한 파일에는 '지명', 'X좌표', 'Y좌표' 컬럼이 포함되어야 합니다.")

    # 북한 역 위치 딕셔너리
    coord_dict = {
        row["지명"]: (row["X좌표"], row["Y좌표"])
        for _, row in nk_df.iterrows()
    }

    # 거리/속도 기반 총 소요시간 계산 함수
    def calculate_total_time(df, label):
        required_cols = ["출발역", "도착역", "거리(km)", "속도(km/h)"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"❌ '{label}' 파일에 '{col}' 컬럼이 없습니다.")
        
        # 문자열을 숫자로 변환 (에러 시 NaN)
        df["거리(km)"] = pd.to_numeric(df["거리(km)"], errors="coerce")
        df["속도(km/h)"] = pd.to_numeric(df["속도(km/h)"], errors="coerce")

        df.dropna(subset=["거리(km)", "속도(km/h)"], inplace=True)

        # 시간 계산
        df["시간(h)"] = df["거리(km)"] / df["속도(km/h)"]
        total_time = df["시간(h)"].sum()

        return round(total_time, 2)

    # 2. 통일 전 데이터
    before_df = load_excel_or_csv(before_path)
    before_total_time = calculate_total_time(before_df, "통일 전")

    # 3. 통일 후 데이터
    after_df = load_excel_or_csv(after_path)
    after_total_time = calculate_total_time(after_df, "통일 후")

    return {
        "통일 전 시간": before_total_time,
        "통일 후 시간": after_total_time,
        "절감 시간": round(before_total_time - after_total_time, 2)
    }
