
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(layout="wide")
st.title("남북통일 교통망 통합 시뮬레이션 플랫폼")

# -----------------------------
# SECTION 1: 정적 그래프 출력
# -----------------------------
st.header("1. 통일 전후 이동시간 비교")
try:
    img = Image.open("data/이동시간_단축_비교.png")
    st.image(img, caption="통일 전후 주요 구간 이동시간 비교", use_column_width=True)
except:
    st.warning("이동시간 비교 이미지가 누락되어 있습니다.")

# -----------------------------
# SECTION 2: 거리/속도 데이터 요약
# -----------------------------
st.header("2. 거리 및 속도 요약 (통일 전 vs 통일 후)")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 통일 전 거리/속도")
    try:
        df_pre = pd.read_excel("data/통일전_거리+속도.xlsx", engine="openpyxl")
        st.dataframe(df_pre)
    except:
        st.error("통일전_거리+속도.xlsx 파일이 필요합니다.")

with col2:
    st.subheader("📍 통일 후 거리/속도")
    try:
        df_post = pd.read_excel("data/통일후_경의선.xlsx", engine="openpyxl")
        st.dataframe(df_post)
    except:
        st.error("통일후_경의선.xlsx 파일이 필요합니다.")

# -----------------------------
# SECTION 3: 사용자 입력 기반 시뮬레이션
# -----------------------------
st.header("3. 사용자 입력 기반 시뮬레이션")

routes = df_post["구간"].dropna().unique() if '구간' in df_post.columns else ["서울-평양", "서울-신의주"]
start = st.selectbox("출발지", sorted(set([r.split('-')[0] for r in routes])))
end = st.selectbox("도착지", sorted(set([r.split('-')[1] for r in routes])))
mode = st.radio("통일 상태", ["통일 전", "통일 후"], horizontal=True)
year = st.slider("예상 연도", 2025, 2035, 2025)

# -----------------------------
# SECTION 4: 시뮬레이션 함수
# -----------------------------
def simulate(start, end, mode, year):
    route = f"{start}-{end}"
    df = df_post if mode == "통일 후" else df_pre
    try:
        row = df[df["구간"] == route].iloc[0]
        dist = row["총 거리(km)"]
        time = row["총 시간(h)"]
    except:
        dist = 600
        time = dist / (150 if mode == "통일 후" else 80)
    # 가상의 시계열 예측
    traffic = [dist * (1 + 0.03 * (y - 2025)) for y in range(2025, 2036)]
    return round(dist, 1), round(time, 1), traffic

if st.button("🚀 시뮬레이션 실행"):
    dist, time, traffic = simulate(start, end, mode, year)

    st.subheader("📊 결과 요약")
    st.write(f"**총 거리**: {dist} km")
    st.write(f"**예상 소요 시간**: {time:.1f} 시간")

    st.subheader("📈 연도별 물류량 예측")
    df_line = pd.DataFrame({
        "연도": list(range(2025, 2036)),
        "예상 물류량 (톤)": traffic
    })
    fig = px.line(df_line, x="연도", y="예상 물류량 (톤)", markers=True)
    st.plotly_chart(fig, use_container_width=True)
