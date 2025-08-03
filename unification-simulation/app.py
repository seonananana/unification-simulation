
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
#
# -----------------------------
st.header("2. 통일 전후 물류비용 비교")
try:
    img = Image.open("data/container.png")
    st.image(img, caption="통일 전후 물류비용 비교", use_column_width=True)
except:
    st.warning("이동시간 비교 이미지가 누락되어 있습니다.")


# -----------------------------
# SECTION 3: 
# -----------------------------
st.header("3. 통일 전후 tcr비교")
col1, col2 = st.columns(2)

try:
    with col1:
        img = Image.open("data/mtcr.png")
        st.image(img, caption="통일 전후 mtcr 비교", use_column_width=True)
except:
    st.warning("mtcr 이미지를 불러올 수 없습니다.")

try:
    with col2:
        img = Image.open("data/utcr.png")
        st.image(img, caption="통일 전후 utcr 비교", use_column_width=True)
except:
    st.warning("utcr 이미지를 불러올 수 없습니다.")

# -----------------------------
# SECTION 4: 
# -----------------------------
st.header("4. 통일 후 물류비용 감소 예측")
try:
    img = Image.open("data/timer.png")
    st.image(img, caption="통일 후 물류비용 감소 예측", use_column_width=True)
except:
    st.warning("이동시간 비교 이미지가 누락되어 있습니다.")
