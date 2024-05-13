import pandas as pd # pip install pandas openpyxl
import plotly.express as px # pip install plotly-express
import streamlit as st # pip install streamlit
import plotly.graph_objects as go # pip install plotly
from collections import Counter
import emoji # pip install emoji
from PIL import Image
from main import month_category_posts
from main import category_posts_day
from main import category_posts_month
from main import month_category_good
from main import keyword_good
from main import month_keyword
from main import ID_month_good
from main import ID_posts


df = pd.read_excel("240510_df_2_1.xlsx")

st.set_page_config(page_title="🖼️여행은역시제주조🖼️", layout='wide')

df = pd.read_excel("240510_df_2_1.xlsx")

#################
# ---- 메인 ----
#################

# 데이터 접었다 필 수 있게 만들어놓기
with st.expander("데이터 보기"):
	st.dataframe(df, height=200)

# 연-월별 대분류별 게시글수
st.subheader("연-월별 대분류별 게시글수")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    month_category_posts()

# # 오류나는부분1/1
# # 날짜별 대분류별 게시글수
# st.subheader("날짜별 대분류별 게시글수")
# col1, col2 = st.columns([1,4])
# with col1:
#     st.subheader("d d d d d d d d")
# with col2: 
#     day_category_posts()

# 년도별 대분류별 게시글수
st.subheader("년도별 대분류별 게시글수")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    category_posts_day()

# 년도별 대분류별 게시글수- 월단위
st.subheader("년도별 대분류별 게시글수- 월단위")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    category_posts_month()

# 연-월별 대분류별 좋아요 수
st.subheader("연-월별 대분류별 좋아요 수")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    month_category_good()

# 연-월별 많이 나오는 키워드
st.subheader("연-월별 많이 나오는 키워드")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    month_keyword()

# 많이 등장하는 키워드와 좋아요의 관계
st.subheader("많이 등장하는 키워드와 좋아요의 관계")
st.subheader("의문점")
st.markdown("- 제주도가 많이 찍혔는데, 그이유가 사람들이 좋아요를 많이 눌러서다?")
keyword_good()

# 계정 ID별 월별 좋아요 수
st.subheader("계정 ID별 월별 좋아요 수")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    ID_month_good()

# 월별 ID별 게시글 수 
st.subheader("월별 ID별 게시글 수 ")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("인사이트")
    st.markdown("- 활동한만큼 좋아요수가 많아진다."
                "- 게시글을 꾸준히 올려야 좋아요 수가 많아진다."
                "- 평균적으로 60개 정도의 게시물을 올리니까 하루에 2개이상, 한달에 50개 이상의 게시물을 올리는 것이 효과적이다.")
with col2: 
    ID_posts()

####################
# ---- 사이드바 ----
####################

# 이미지 파일 열기
image = Image.open('그림3.png')
# Streamlit 앱에 이미지 표시
st.sidebar.image(image, width=70)
st.sidebar.header("역시여행은제주조")

st.sidebar.header("항목을 선택하세요:")

year = st.sidebar.multiselect(
    "Select Year",
    options = df["year"].unique(),
    default = df["year"].unique()
)

month = st.sidebar.multiselect(
    "Select Month",
    options = df["month"].unique(),
    default = df["month"].unique()
)

대분류 = st.sidebar.multiselect(
    "Select 업종(대분류)",
    options = df["대분류"].unique(),
    default = df["대분류"].unique()
)

df_selection = df.query(
    "year == @year & month == @month & 대분류 == @대분류"
)