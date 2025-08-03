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
    img = Image.open("이동시간_단축_비교.png")
    col1, col2, col3 = st.columns([1, 2, 1])  # 가운데 정렬
    with col2:
        st.image(img, caption="통일 전후 주요 구간 이동시간 비교", use_container_width=True)
except:
    st.warning("이동시간 비교 이미지가 누락되어 있습니다.")

# -----------------------------
st.header("2. 통일 전후 물류비용 비교")
try:
    img = Image.open("container.png")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(img, caption="통일 전후 물류비용 비교", use_container_width=True)
except:
    st.warning("물류비용 비교 이미지가 누락되어 있습니다.")

# -----------------------------
st.header("3. 통일 전후 TCR 비교")
col1, col2 = st.columns(2)
try:
    with col1:
        img = Image.open("mtcr.png")
        st.image(img, caption="MTCR 비교", use_container_width=True)
except:
    st.warning("MTCR 이미지가 누락되어 있습니다.")
try:
    with col2:
        img = Image.open("utcr.png")
        st.image(img, caption="UTCR 비교", use_container_width=True)
except:
    st.warning("UTCR 이미지가 누락되어 있습니다.")

# -----------------------------
st.header("4. 통일 후 물류비용 감소 예측")
try:
    img = Image.open("timer.png")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(img, caption="통일 후 물류비용 감소 예측", use_container_width=True)
except:
    st.warning("타이머 이미지가 누락되어 있습니다.")
