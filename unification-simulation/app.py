import streamlit as st
import pandas as pd
import numpy as np
import os  
from PIL import Image
from statsmodels.tsa.arima.model import ARIMA
from logistics_calc import run_logistics_comparison

st.set_page_config(layout="wide")
st.title("남북통일 교통망 통합 시뮬레이션 플랫폼")

# -----------------------------
# SECTION 1: 정적 그래프 출력
# -----------------------------
st.header("1. 통일 전후 이동시간 비교")
try:
    img = Image.open("이동시간_단축_비교.png")
    col1, col2, col3 = st.columns([1, 2, 1])  # 가운데 정렬
    with col2:
        st.image(img, use_container_width=True)
except:
    st.warning("이동시간 비교 이미지가 누락되어 있습니다.")

#2 -----------------------------
st.header("2. 통일 전후 물류비용 비교")
try:
    img = Image.open("container.png")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(img, use_container_width=True)
except:
    st.warning("물류비용 비교 이미지가 누락되어 있습니다.")

#3-----------------------------
st.header("3. 통일 전후 TCR 비교")
col1, col2 = st.columns(2)
try:
    with col1:
        img = Image.open("mtcr.png")
        st.image(img, use_container_width=True)
except:
    st.warning("MTCR 이미지가 누락되어 있습니다.")
try:
    with col2:
        img = Image.open("utcr.png")
        st.image(img, use_container_width=True)
except:
    st.warning("UTCR 이미지가 누락되어 있습니다.")

#4 -----------------------------
st.header("4. 통일 후 물류비용 감소 예측")
try:
    img = Image.open("timer.png")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(img, use_container_width=True)
except:
    st.warning("타이머 이미지가 누락되어 있습니다.")
#5 -----------------------------
st.header("5. 통일 시나리오 기반 물류비용 절감 예측")

# 파일 경로 설정
st.sidebar.subheader("🔍 경로 확인")
data_dir = "../data"
before_path = "data/before_unification.xlsx"
after_path = "data/after_unification.xlsx"
nk_path = "data/nk_station_map.csv"

st.sidebar.write("통일전 파일 존재:", os.path.exists(before_path))
st.sidebar.write("통일후 파일 존재:", os.path.exists(after_path))
st.sidebar.write("북한역 파일 존재:", os.path.exists(nk_path))

# 계산 실행
try:
    result = run_logistics_comparison(before_path, after_path, nk_path)
    time_saved = result["통일 전 시간"] - result["통일 후 시간"]
    unit_cost = 800  # 억 원/시간 기준
    base_saving_input = time_saved * unit_cost

    st.sidebar.subheader("📌 시나리오 선택")
    scenario = st.sidebar.selectbox("예측 시나리오", ["보수적", "기준", "공격적"])

    if scenario == "보수적":
        growth_rate = 1.0
    elif scenario == "기준":
        growth_rate = 2.0
    else:
        growth_rate = 4.0

    forecast_years = st.sidebar.slider("예측 연도 수", 1, 15, 5)
    start_year = 2024
    end_year = 2024

    # 시계열 생성
    year_range = list(range(start_year, end_year + 1))
    savings = [base_saving_input for _ in year_range]
    df = pd.DataFrame({"연도": year_range, "절감액_기준": savings}).set_index("연도")

    # ARIMA 예측
    model = ARIMA(df["절감액_기준"], order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_years)
    forecast_years_range = list(range(end_year + 1, end_year + 1 + forecast_years))
    forecast_df = pd.DataFrame({"예측 절감액": forecast.values}, index=forecast_years_range)

    # 결과 시각화
    st.subheader("📈 예측 결과 시각화 (현실 기반 + 시나리오)")
    full_df = pd.concat([df["절감액_기준"], forecast_df["예측 절감액"]])
    st.line_chart(full_df)

    st.subheader("📄 예측 데이터 테이블")
    st.dataframe(full_df.rename("절감액").to_frame().style.format("{:.2f}"))

except FileNotFoundError as e:
    st.error(f"❌ 파일을 찾을 수 없습니다: {e.filename}")
except Exception as e:
    st.error(f"예측 중 오류 발생: {e}")

