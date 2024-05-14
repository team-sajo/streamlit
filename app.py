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
from main import year_month_keyword
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
from main import year_category_post_fig1
from main import year_category_post_fig2
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

# 연-월별 대분류별 게시글수
# def gr50():
#     st.subheader("연-월별 대분류별 게시글수")
#     col1, col2 = st.columns([1,3])
#     with col1:
#         st.subheader("👀 INSIGHT")
#         st.markdown("- ")
#     with col2: 
#         month_category_posts()

# 연도별 대분류별 게시글수- 일단위
def gr51():
    st.subheader("연도별 대분류별 게시글수- 일단위")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- 관광지 게시글수가 꾸준히 증가함")
        st.markdown("- 20~24년도의 전체적인 추세를 알 수 있음")
    with col2: 
        category_posts_day()

# 연도별 대분류별 게시글수- 월단위
def gr52():
    st.subheader("연도별 대분류별 게시글수- 월단위")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- 식당 게시글수가 상위권에 위치함")
        st.markdown("- 관광지 게시글수가 점점 많아져서 24년도에는 가장 많음")
        st.markdown("- 전체적인 글의 개수가 많아짐")
    with col2: 
        category_posts_month()

# 연-월별 대분류별 좋아요 수
# def gr53():
#     st.subheader("연-월별 대분류별 좋아요 수")
#     col1, col2 = st.columns([1,4])
#     with col1:
#         st.subheader("👀 INSIGHT")
#         st.markdown("-")
#         st.markdown("-")
#         st.markdown("-")
#     with col2: 
#         month_category_good()

# 연-월별 많이 나오는 키워드
def gr54():
    st.subheader("연-월별 많이 나오는 키워드")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- 20년도 상반기에 '인생샷' 키워드가 압도적으로 많음 -> 20년도 상반기는 코로나 유행하기 시작한 시기 -> 코로나의 영향?")
        st.markdown("- 전체적으로 '오션뷰' 키워드가 계속 등장함 -> 오션뷰가 메리트 있는 항목임을 알 수 있음")
        st.markdown("- '제주여행' 키워드로 보아 제주는 여행지임을 유추할 수 있음")
    with col2: 
        year_month_keyword()

# 오래걸림..
# 많이 등장하는 키워드와 좋아요의 관계
def gr49():
    st.subheader("많이 등장하는 키워드와 좋아요의 관계")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- '디저트' 키워드가 포함된 게시물에 좋아요가 가장 많이 찍힘")
        st.markdown("- '제주도' 키워드가 포함된 게시물에 좋아요가 많이 찍힘 -> 사람들이 좋아요를 많이 눌러서?")
        st.markdown("- 키워드 양 자체는 '제주'가 많은데 이에 비해 좋아요 수는 적음")
    with col2: 
        keyword_good()

# 계정 ID별 월별 좋아요 수
def gr55():
    st.subheader("계정 ID별 월별 좋아요 수")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- @jejuplantes의 좋아요수가 22년 하반기에 급격하게 떨어짐")
        st.markdown("- @jeju_source의 좋아요수가 가장 꾸준함 ")
        st.markdown("- 한번 좋아요 수가 떨어지면 회복하기 쉽지 않음?")
    with col2: 
        ID_month_good()

# 월별 ID별 게시글 수 
def gr56():
    st.subheader("월별 ID별 게시글 수 ")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- 활동한만큼 좋아요수가 많아짐")
        st.markdown("- 게시글을 꾸준히 올려야 좋아요 수가 많아짐")
        st.markdown("- 평균적으로 60개 정도의 게시물을 올리니까 하루에 2개이상, 한달에 50개 이상의 게시물을 올리는 것이 효과적임")
    with col2: 
        ID_posts()
# -----------------------------
# 업종별 데이터수 & 좋아요수
def gr1():
    st.subheader("업종별 게시물수 & 좋아요수")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- 식당과 관련된 게시물 수가 압도적으로 많음")
        st.markdown("- 관광지와 숙소가 올리는 게시물 수 대비 좋아요가 잘 찍힘")
        st.markdown("- 이에 비해 식당은 게시물 수는 많지만 좋아요가 덜 찍힘")
    with col2:
        tab1, tab2, tab3, tab4 = st.tabs(["✅게시물수", "✅좋아요수", "✅게시물수 & 좋아요수","✅게시물수 대비 좋아요수"])
        with tab1:
            category_counts()
        with tab2:
            category_likes()
        with tab3:
            category_counts_likes()
        with tab4:
            category_counts_likes_divide()

# 전체 키워드 빈도수 (상위 20개)
def gr2():
    st.subheader("전체 키워드 빈도수 (상위 20개)")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- '제주'라는 키워드가 압도적으로 많음")
        st.markdown("- 맛집 키워드가 2등 -> 인스타에 음식 정보가 많다고 판단됨")
        st.markdown("- 키워드 '서귀포','애월','제주시' 존재 -> 제주도의 주요 지역명을 파악 가능")
    with col2: 
        keyword_frequency()

# 업종별 많이 나오는 키워드수
def gr3():
    st.subheader("업종별 많이 나오는 키워드수")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- 공통적으로 키워드 '제주'가 많이 나왔음")
        st.markdown("- 반려동물 업종에 앵무새가 많이 나왔음")
        st.markdown("- 식당 업종에 흑돼지가 눈에 띔")
    with col2: 
        category_keyword()

## 첫 번째거랑 겹쳐서 주석처리함
# 업종별 게시글수
# st.subheader("업종별 게시글수")
# col1, col2 = st.columns([1,4])
# with col1:
#     st.subheader("d d d d d d d d")
# with col2: 
#     category_posts()

# 월별 많이 나오는 키워드수
def gr4():
    st.subheader("월별 많이 나오는 키워드수")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- 제주, 맛집, 카페는 전체적으로 있음 -> 해당 키워드는 계절의 영향을 덜 받음을 추론 가능")
        st.markdown("- 6월에 특징적으로 키워드 수가 적어짐 -> 월별 게시글 수가 줄어든 것과 연관이 있을 수도?")
        st.markdown("- 9월 10월에 '서귀포' 키워드가 없음 -> ?")
        st.markdown("- 12월에 '크리스마스' 키워드가 있음")
    with col2: 
        month_keyword()

# 월별 게시글수/좋아요수
def gr5():
    st.subheader("월별 게시글수 & 좋아요수")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- 6월이 게시글 수가 특히 적고 11 ~ 1월이 게시글 수가 많음 -> 겨울이 성수기?")
        st.markdown("- 4월과 10월이 게시글수 대비 좋아요수가 많음 -> ?")
    with col2: 
        tab1, tab2 = st.tabs(["✅게시글 수", "✅좋아요 수"])
        with tab1:
            month_posts()
        with tab2:
            month_good()

# 월별 대분류별 게시글수 & 좋아요수 & 게시글당평균좋아요비율
def gr6():
    st.subheader("월별 대분류별 게시글수 & 좋아요수 & 평균")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- 식당 관련 게시물은 겨울에 많아짐")
        st.markdown("- 게시글수와 좋아요수는 대체로 정비례함(4월, 7월 제외)")
    with col2: 
        tab1, tab2, tab3 = st.tabs(["✅게시글수", "✅좋아요수", "✅게시글당 좋아요수"])
        with tab1:
            month_category_posts()
        with tab2:
            month_category_good()
        with tab3:
            month_category_posts_good()

# 연도별 많이 나오는 키워드 수
def gr7():
    st.subheader("연도별 많이 나오는 키워드 수")
    col1, col2 = st.columns([3,4])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- 20년도에 포토존, 감성, 분위기 등의 키워드가 특징적으로 나타남")
        st.markdown("- 20년도에 '인생샷'이라는 키워드가 높았는데 21년도부터는 없음 (코로나 떄문? 마스크, 비대면, 여행감소)")
        st.markdown("   - 비대면이라 사진의 중요성이 높아졌다?")
        st.markdown("   - 인생네컷 : 2017년에 출시, 2020년 이후부터 사람들에게 지칭됨(이 영향이 있지 않을까?)")
        st.markdown("   - 인생~~시리즈 유행해서 그러지 않았을까?")
        st.markdown("- 24년도에 '이벤트' 키워드가 생김 -> 리뷰이벤트?")
        st.markdown("- 연도별 게시글 수가 늘어나고 있음 -> 홍보성 게시글이 많아지고 있다?")
    with col2: 
        year_keyword()

### 겹쳐서 주석처리함
# 연도별 좋아요 수
# st.subheader("연도별 좋아요 수")
# col1, col2 = st.columns([1,3])
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
def gr8():
    st.subheader("연도별 대분류별 좋아요 합계 & 게시글 수")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- 해가 갈수록 좋아요가 늘어나고 있음. 게시글수가 증가해서 그런 것으로 추정됨")
        st.markdown("- 2022년도에 좋아요수, 게시글수가 급작스럽게 증가함")
    with col2: 
        tab1, tab2, tab3, tab4 = st.tabs(["✅좋아요-막대", "✅좋아요-꺾은선", "✅게시글수-막대", "✅게시글수-꺾은선"])
        with tab1:
            # 연도별 대분류별 좋아요 합계- 막대
            year_category_good_fig2()
        with tab2:
            # 연도별 대분류별 좋아요 합계- 꺾은선
            year_category_good_fig1()
        with tab3:
            # 연도별 대분류별 게시물수- 막대
            year_category_post_fig1()
        with tab4:
            # 연도별 대분류별 게시물수- 꺾은선
            year_category_post_fig2()

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
def gr9():
    st.subheader("좋아요수에 영향을 미치는 요인: 팔로워수, 게시글길이, 이모티콘수")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- 팔로워수가 많을수록 좋아요 수가 많은 경향이 있음")
        st.markdown("- 게시글 길이가 길다고 해서 좋아요수가 많은 건 아님")
        st.markdown("- 게시글 안에 이모티콘의 수와 좋아요 수는 거의 관련이 없음")
    with col2: 
        tab1, tab2, tab3 = st.tabs(["✅팔로워수", "✅게시글 길이", "✅이모티콘수"])
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
def gr10():
    st.subheader("팔로워수에 영향을 미치는 요인: 게시글수, ID 길이")
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader("👀 INSIGHT")
        st.markdown("- 게시글수와 팔로워수는 어느정도 정비례함")
        st.markdown("- 계정의 ID길이와 팔로워수는.. 관련이 없음!")
    with col2: 
        tab1, tab2= st.tabs(["✅게시글 수","✅ID 길이"])
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
st.sidebar.image(image, width=308)

st.sidebar.header("그래프를 선택하세요:")

status2 = st.sidebar.radio('시계열분석', ['선택x',
                                        # '연-월별 대분류별 게시글수', #시계열분석
                                        '연도별 대분류별 게시글수- 일단위', #시계열분석
                                        '연도별 대분류별 게시글수- 월단위', #시계열분석
                                        # '연-월별 대분류별 좋아요 수', #시계열분석
                                        '✅연-월별 많이 나오는 키워드', # 시계열분석
                                        '많이 등장하는 키워드와 좋아요의 관계', #시계열분석
                                        '✅계정 ID별 월별 좋아요수', # 시계열분석
                                        '✅월별 ID별 게시글수', # 시계열분석
                                    ])

# if status2 == '연-월별 대분류별 게시글수' : #시계열분석
#     gr50()
if status2 == '연도별 대분류별 게시글수- 일단위': #시계열분석
    gr51()
elif status2 == '연도별 대분류별 게시글수- 월단위' : # 시계열분석
    gr52()
# elif status2 == '연-월별 대분류별 좋아요 수' : # 시계열분석
#     gr53()
elif status2 == '✅연-월별 많이 나오는 키워드' : # 시계열분석
    gr54()
elif status2 == '많이 등장하는 키워드와 좋아요의 관계': #시계열분석
    gr49()
elif status2 == '✅계정 ID별 월별 좋아요수' : # 시계열분석
    gr55()
elif status2 == '✅월별 ID별 게시글수' : # 시계열분석
    gr56()


status = st.sidebar.radio('요소분석', ['선택x',
                                    '업종별 게시물수 & 좋아요수',
                                    '전체 키워드 빈도수(상위20개)',
                                    '업종별 많이 나오는 키워드수',
                                    '월별 많이 나오는 키워드수',
                                    '월별 게시글수 & 좋아요수',
                                    '월별 대분류별 게시글수 & 좋아요수 & 비율',
                                    '연도별 많이 나오는 키워드수',
                                    '연도별 대분류별 좋아요 합계 & 게시물수',
                                    '좋아요수에 영향을 미치는 요인',
                                    '팔로워수에 영향을 미치는 요인'])
if status == '업종별 게시물수 & 좋아요수' :
    gr1()
elif status == '전체 키워드 빈도수(상위20개)' :
    gr2()
elif status == '업종별 많이 나오는 키워드수' :
    gr3()
elif status == '월별 많이 나오는 키워드수' :
    gr4()
elif status == '월별 게시글수 & 좋아요수' :
    gr5()
elif status == '월별 대분류별 게시글수 & 좋아요수 & 비율' :
    gr6()
elif status == '연도별 많이 나오는 키워드수' :
    gr7()
elif status == '연도별 대분류별 좋아요 합계 & 게시물수' :
    gr8()
elif status == '좋아요수에 영향을 미치는 요인' :
    gr9()
elif status == '팔로워수에 영향을 미치는 요인' :
    gr10()