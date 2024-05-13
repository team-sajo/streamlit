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
from main import month_category_posts
from main import category_posts_day
from main import category_posts_month
from main import month_category_good
from main import keyword_good
from main import month_keyword
from main import ID_month_good
from main import ID_posts


st.set_page_config(page_title="🖼️여행은역시제주조🖼️", layout='wide')

df = pd.read_excel("240510_df_2_1.xlsx")

#################
# ---- 메인 ----
#################


# 데이터 접었다 필 수 있게 만들어놓기
with st.expander("📑⛏️ 우리가 찾은 데이터 📑⛏️"):
	st.dataframe(df, height=250)
# -----------------------------
# # 연-월별 대분류별 게시글수
# st.subheader("연-월별 대분류별 게시글수")
# col1, col2 = st.columns([1,4])
# with col1:
#     st.subheader("d d d d d d d d")
# with col2: 
#     month_category_posts()

# # 년도별 대분류별 게시글수
# st.subheader("년도별 대분류별 게시글수")
# col1, col2 = st.columns([1,4])
# with col1:
#     st.subheader("d d d d d d d d")
# with col2: 
#     category_posts_day()

# # 년도별 대분류별 게시글수- 월단위
# st.subheader("년도별 대분류별 게시글수- 월단위")
# col1, col2 = st.columns([1,4])
# with col1:
#     st.subheader("d d d d d d d d")
# with col2: 
#     category_posts_month()

# # 연-월별 대분류별 좋아요 수
# st.subheader("연-월별 대분류별 좋아요 수")
# col1, col2 = st.columns([1,4])
# with col1:
#     st.subheader("d d d d d d d d")
# with col2: 
#     month_category_good()

# # 연-월별 많이 나오는 키워드
# st.subheader("연-월별 많이 나오는 키워드")
# col1, col2 = st.columns([1,4])
# with col1:
#     st.subheader("d d d d d d d d")
# with col2: 
#     month_keyword()

# # 계정 ID별 월별 좋아요 수
# st.subheader("계정 ID별 월별 좋아요 수")
# col1, col2 = st.columns([1,4])
# with col1:
#     st.subheader("d d d d d d d d")
# with col2: 
#     ID_month_good()

# # 월별 ID별 게시글 수 
# st.subheader("월별 ID별 게시글 수 ")
# col1, col2 = st.columns([1,4])
# with col1:
#     st.subheader("인사이트")
#     st.markdown("- 활동한만큼 좋아요수가 많아진다."
#                 "- 게시글을 꾸준히 올려야 좋아요 수가 많아진다."
#                 "- 평균적으로 60개 정도의 게시물을 올리니까 하루에 2개이상, 한달에 50개 이상의 게시물을 올리는 것이 효과적이다.")
# with col2: 
#     ID_posts()
# -----------------------------
# 업종별
st.subheader("업종별")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("인사이트")
    st.markdown("- 관광지가 올리는 것 대비 좋아요수가 잘 찍힌다.")
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
    st.subheader("인사이트")
    st.markdown("- 월 별 특징적으로 나와 있는 것은?"
                "- 제주, 맛집, 카페는 전체적으로 있다. = 계절의 영향을 덜 받는다."
                "- 9월 10월에 서귀포가 없다."
                "- 12월은 크리스마스가 있다."
                "- 6월에 특징적으로 키워드 수가 적어졌다.=월 별 게시글 수가 줄어든 것과 연관이 있을 수 있다.")
with col2: 
    month_keyword()

# 월별 게시글수/좋아요수
st.subheader("월별 게시글수/좋아요수")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
    st.markdown("- 알 수 있는 점"
    "- 6월이 게시글 수가 적다."
    "- 11 ~ 1월이 게시글 수가 많다.")
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
    st.markdown("- 겨울에 식당이 많이 늘어난다???"
"- 게시글 수만큼 좋아요수도 늘어나는 경향이 있다(4월, 7월 제외)")
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
    st.markdown("- 20년도에 포토존, 감성, 분위기 등의 키워드가 특징적으로 나타난다."
"- 20년도에 '인생샷'이라는 키워드가 높았는데, 21년도부터는 볼 수 없다. (코로나 떄문일까요? 마스크, 비대면, 여행감소)"
"- 비대면이라 사진의 중요성이 높아졌다?"
"- 인생네컷 : 2017년에 출시, 2020년 이후부터 사람들에게 지칭됨(이 영향이 있지 않을까?)"
"- 인생~~시리즈 유행해서 그러지 않았을까?"
"- 24년도에 이벤트가 생겼다(리뷰이벤트?)"
"- 연도별 게시글 수가 늘어나고 있다고 추측한다. (홍보성 게시글이 많아지고 있다.))")
with col2: 
    year_keyword()

### 겹쳐서 주석처리함
# 연도별 좋아요 수
# st.subheader("연도별 좋아요 수")
# col1, col2 = st.columns([1,4])
# with col1:
#     st.subheader("d d d d d d d d")
#     st.markdown(""- 23년도부터 관광지의 연도별 좋아요 수가 식당의 좋아요 수보다 많아졌다")
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
# st.markdown("어떤 업종이 많이 나오면 다른 업종들의 수는 줄어든다")
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
st.sidebar.image(image, width=300)

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