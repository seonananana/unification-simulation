import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from statsmodels.tsa.arima.model import ARIMA

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
# -----------------------------
st.header("5. 통일 시나리오 기반 물류비용 절감 예측")

from statsmodels.tsa.arima.model import ARIMA

st.sidebar.subheader("📌 예측 시나리오 입력")
base_saving_input = st.sidebar.number_input("기준 절감액 (억 원)", min_value=10000, max_value=200000, value=50000, step=1000)
growth_rate = st.sidebar.slider("연평균 물류 수요 증가율 (%)", 0.0, 10.0, 2.0)
forecast_years = st.sidebar.slider("예측 연도 수", 1, 15, 5)
start_year = st.sidebar.number_input("기준 시작 연도", min_value=2000, max_value=2025, value=2010)
end_year = st.sidebar.number_input("기준 종료 연도", min_value=2020, max_value=2030, value=2024)

# 시계열 생성
year_range = list(range(start_year, end_year + 1))
savings = [base_saving_input * (1 + growth_rate / 100) ** (i - start_year) for i in year_range]
df = pd.DataFrame({"연도": year_range, "절감액": savings}).set_index("연도")

# ARIMA 예측
try:
    model = ARIMA(df["절감액"], order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_years)
    forecast_years_range = list(range(end_year + 1, end_year + 1 + forecast_years))
    forecast_df = pd.DataFrame({"예측 절감액": forecast.values}, index=forecast_years_range)

    # 그래프
    st.subheader("📈 예측 결과 시각화")
    st.line_chart(pd.concat([df["절감액"], forecast_df["예측 절감액"]]))

    # 표
    st.subheader("📄 예측 결과 테이블")
    st.dataframe(forecast_df.style.format("{:.2f}"))
except Exception as e:
    st.error(f"예측 중 오류 발생: {e}")
