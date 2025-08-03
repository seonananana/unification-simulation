import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
from logistics_calc import run_logistics_comparison

# 페이지 설정
st.set_page_config(layout="wide")
st.title("남북통일 교통망 통합 시뮬레이션 플랫폼")

# ----------------------------
# SECTION 1~4: 이미지 표시
# ----------------------------

# 이미지 표시 함수 (가운데 정렬)
def centered_image(path, caption=""):
    try:
        img = Image.open(path)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(img, caption=caption, use_container_width=True)
    except:
        st.warning(f"{caption or path} 이미지가 누락되어 있습니다.")

# 1. 통일 전후 이동시간 비교
st.header("1. 통일 전후 이동시간 비교")
centered_image("이동시간_단축_비교.png", "통일 전후 주요 구간 이동시간 비교")

# 2. 통일 전후 물류비용 비교
st.header("2. 통일 전후 물류비용 비교")
centered_image("container.png", "물류비용 비교")

# 3. 통일 전후 TCR 비교
st.header("3. 통일 전후 TCR 비교")
col1, col2 = st.columns(2)
with col1:
    centered_image("mtcr.png", "MTCR")
with col2:
    centered_image("utcr.png", "UTCR")

# 4. 통일 후 물류비용 감소 예측
st.header("4. 통일 후 물류비용 감소 예측")
centered_image("timer.png", "절감 예측 타이머")

# ----------------------------
# SECTION 5: 시나리오 기반 절감액 예측
# ----------------------------

st.header("5. 통일 시나리오 기반 물류비용 절감 예측")

# 파일 경로 설정
before_path = "data/before_unification.xlsx"
after_path = "data/after_unification.xlsx"
nk_path = "data/nk_station_map.csv"

# 경로 확인
st.sidebar.subheader("🔍 경로 확인")
st.sidebar.write("통일전 파일 존재:", os.path.exists(before_path))
st.sidebar.write("통일후 파일 존재:", os.path.exists(after_path))
st.sidebar.write("북한역 파일 존재:", os.path.exists(nk_path))

try:
    # 물류 비교 실행
    result = run_logistics_comparison(before_path, after_path, nk_path)
    time_saved = result["통일 전 시간"] - result["통일 후 시간"]
    unit_cost = 800  # 억 원/시간
    base_saving_input = time_saved * unit_cost

    # 시나리오 선택
    st.sidebar.subheader("📌 시나리오 선택")
    scenario = st.sidebar.selectbox("예측 시나리오", ["보수적", "기준", "공격적"])

    growth_rate_map = {
        "보수적": 0.01,
        "기준": 0.03,
        "공격적": 0.05
    }
    growth_rate = growth_rate_map[scenario]

    # 예측 연도 설정
    forecast_years = st.sidebar.slider("예측 연도 수", 1, 15, 5)
    start_year = 2024
    years = list(range(start_year, start_year + forecast_years + 1))

    # 절감액 예측 (지수 성장 기반)
    savings = [base_saving_input * ((1 + growth_rate) ** i) for i in range(len(years))]
    df_forecast = pd.DataFrame({"연도": years, "절감액(억원)": savings}).set_index("연도")

    # 시각화
    st.subheader("📈 예측 결과 시각화 (시나리오 반영)")
    st.line_chart(df_forecast)

    # 예측 테이블
    st.subheader("📄 예측 데이터 테이블")
    st.dataframe(df_forecast.style.format("{:.2f}"))

except FileNotFoundError as e:
    st.error(f"❌ 파일을 찾을 수 없습니다: {e.filename}")
except Exception as e:
    st.error(f"❌ 예측 중 오류 발생: {e}")
