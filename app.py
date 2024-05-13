import pandas as pd # pip install pandas openpyxl
import plotly.express as px # pip install plotly-express
import streamlit as st # pip install streamlit
import plotly.graph_objects as go # pip install plotly
from collections import Counter
import emoji # pip install emoji
from PIL import Image
from main import month_category_posts
from main import category_likes
from main import category_counts
from main import category_counts_likes
from main import category_counts_likes_divide
from main import month_category_good
from main import month_keyword
from main import keyword_frequency
from main import category_keyword
from main import month_posts
from main import month_good
from main import category_posts
from main import month_category_posts_good
from main import year_keyword
from main import year_good_fig1
from main import year_good_fig2
from main import year_category_good_fig1
from main import year_category_good_fig2
from main import emoji_good
from main import lenpost_good
from main import lenID_follower
from main import follower_good
from main import follower_post


st.set_page_config(page_title="🖼️4조의 시각화🖼️", layout='wide')

df = pd.read_excel("240510_df_2_1.xlsx")

#################
# ---- 메인 ----
#################

# 데이터 접었다 필 수 있게 만들어놓기
with st.expander("📑⛏️ 우리가 찾은 데이터 📑⛏️"):
	st.dataframe(df, height=200)
# -----------------------------

# 업종별
st.subheader("업종별")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2:
    tab1, tab2, tab3, tab4 = st.tabs(["데이터 개수", "총 좋아요 수", "각 카테고리별 데이터수, 좋아요수 계산","데이터수 대비 좋아요 수 비율"])
    with tab1:
        category_counts()
    with tab2:
        category_likes()
    with tab3:
        category_counts_likes()
    with tab4:
        category_counts_likes_divide()

st.markdown('---')


# 전체 키워드 빈도수 (상위 20개)
st.subheader("전체 키워드 빈도수 (상위 20개)")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    keyword_frequency()

# 업종별 많이 나오는 키워드수
st.subheader("업종별 많이 나오는 키워드수")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    category_keyword()

# 업종별 게시글수
st.subheader("업종별 게시글수")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    category_posts()

# 월별 많이 나오는 키워드수
st.subheader("월별 많이 나오는 키워드수")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    month_keyword()

# 월별 게시글수/좋아요수
st.subheader("월별 게시글수/좋아요수")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    tab1, tab2 = st.tabs(["월별 게시글 수", "월별 좋아요 수"])
    with tab1:
        month_posts()
    with tab2:
        month_good()

# 월별 대분류별 게시글수/좋아요수/게시글당평균좋아요비율
st.subheader("월별 대분류별 게시글수/좋아요수/비율")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    tab1, tab2, tab3 = st.tabs(["월별 대분류별 게시글 수", "월별 대분류별 좋아요 수", "월별 대분류별 게시글당 평균 좋아요 비율"])
    with tab1:
        month_category_posts()
    with tab2:
        month_category_good()
    with tab3:
        month_category_posts_good()

# 연도별 많이 나오는 키워드 수
st.subheader("연도별 많이 나오는 키워드 수")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    year_keyword()

### 겹쳐서 주석처리함
# 연도별 좋아요 수
# st.subheader("연도별 좋아요 수")
# col1, col2 = st.columns([1,4])
# with col1:
#     st.subheader("d d d d d d d d")
# with col2: 
#     tab1, tab2 = st.tabs(["막대그래프", "꺾은선그래프"])
#     with tab1:
#         year_good_fig1()
#     with tab2:
#         year_good_fig2()

# 연도별 대분류별 좋아요 합계
st.subheader("연도별 대분류별 좋아요 합계/게시물 수")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    tab1, tab2, tab3, tab4 = st.tabs(["좋아요-막대", "좋아요-꺾은선", "게시물수-막대", "게시물수-꺾은선"])
    with tab1:
        # 연도별 대분류별 좋아요 합계- 막대
        year_category_good_fig2()
    with tab2:
        # 연도별 대분류별 좋아요 합계- 꺾은선
        year_category_good_fig1()
    with tab3:
        # 연도별 대분류별 게시물수- 막대
        year_category_good_fig2()
    with tab4:
        # 연도별 대분류별 게시물수- 꺾은선
        year_category_good_fig1()

# 업종과 빈도의 연관성
# st.subheader("업종과 빈도의 연관성")
# def category_frequency():
#     # 스피어만 순위 상관계수 계산
#     year_count = df.groupby(['year','category_numeric']).agg(count=('post','count')).reset_index()
#     correlation = year_count[['category_numeric', 'count']].corr(method='spearman').iloc[0, 1]

#     # 산점도 그리기
#     fig = px.scatter(year_count, x='category_numeric', y='count',
#                     labels={'category_numeric': '업종', 'count': '빈도'},
#                     title=f'업종과 빈도의 연관성: 스피어만 순위 상관계수 {correlation:.2f}')

#     # 그래프 레이아웃 설정
#     fig.update_layout(xaxis_title='업종', yaxis_title='빈도')

#     # Streamlit에 그래프 표시
#     return st.plotly_chart(fig)
# category_frequency()

# 업종과 게시글 수의 상관관계 ## 이거 월별 대분류별 게시글 수랑 겹칠듯
# def category_post():

# 연도와 게시글 수의 상관관계
# def year_posts():

# 좋아요 수에 영향을 미치는 요인: follower수, 게시글길이, 이모티콘수
st.subheader("좋아요 수에 영향을 미치는 요인: follower수, 게시글길이, 이모티콘수")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    tab1, tab2, tab3 = st.tabs(["follower수", "게시글 길이", "이모티콘 수"])
    with tab1:
        # follower와 좋아요 수의 관계
        follower_good()
    with tab2:
        # 게시글 길이와 좋아요 수의 관계
        lenpost_good()
    with tab3:
        # 이모티콘 수와 좋아요 수의 관계
        emoji_good()
        

# follower 수에 영향을 미치는 요인: 게시글 수, 아이디 길이
st.subheader("follower 수에 영향을 미치는 요인: 게시글 수, 아이디 길이")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    tab1, tab2= st.tabs(["게시글 수","ID의 길이"])
    with tab1:
        # follower와 게시글 수의 관계
        follower_post()
    with tab2:
        # follower와 ID 길이의 관계
        lenID_follower()



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