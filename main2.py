import pandas as pd # pip install pandas openpyxl
import plotly.express as px # pip install plotly-express
import streamlit as st # pip install streamlit
import plotly.graph_objects as go # pip install plotly
from collections import Counter
import emoji # pip install emoji
from PIL import Image

df = pd.read_excel("240510_df_2_1.xlsx")

st.set_page_config(page_title="🖼️여행은역시제주조🖼️", layout='wide')

df = pd.read_excel("240510_df_2_1.xlsx")

###########################
# ------ 함수들 --------
###########################

# 연-월별 대분류별 게시글수

# 날짜별 대분류별 게시글 수
def day_category_posts():
    df['date'] = pd.to_datetime(df['date'])  # 'date' 열을 datetime 형식으로 변환
    df['year_month_day'] = df['date'].dt.strftime('%Y-%m-%d')  # 연도-월-일 형식으로 날짜 변환

    # 연도와 월로 그룹화하여 게시글 수 요약
    date_ = df.groupby(['year_month_day', '대분류']).size().reset_index(name='게시글')
    df_pivot = date_.pivot(index='year_month_day', columns='대분류', values='게시글')

    # Plotly를 사용하여 선 그래프 생성
    fig = px.line(df_pivot, x=df_pivot.index, y=df_pivot.columns,
                labels={'value': '게시글 수', 'year_month_day': '날짜', 'variable': '대분류'},
                markers=True, title='날짜별 대분류별 게시글 수')

    # x축 눈금 설정
    fig.update_xaxes(
        tickangle=45,
        tickmode='array',
        tickvals=[str(x) for x in df_pivot.index],
        ticktext=[x.strftime('%Y-%m') for x in pd.to_datetime(df_pivot.index)]
    )

    # streamlit에 그래프 표시
    return st.plotly_chart(fig)

# 년도별 대분류별 게시글수- 일단위
def category_posts_day():
    df['date'] = pd.to_datetime(df['date'])  # 'date' 열을 datetime 형식으로 변환
    df['year_month_day'] = df['date'].dt.strftime('%Y-%m-%d')

    # 스트림릿의 사이드바에서 연도 선택
    selected_year = st.sidebar.selectbox('연도 선택', df['date'].dt.year.unique())

    # 선택된 연도에 대한 데이터 필터링
    df_year = df[df['date'].dt.year == selected_year]

    # pivot_table을 사용하여 데이터 재구성
    df_pivot_year = df_year.pivot_table(index='year_month_day', columns='대분류', values='post', aggfunc='count')

    # Plotly를 사용하여 선 그래프 생성
    fig = px.line(df_pivot_year, x=df_pivot_year.index, y=df_pivot_year.columns,
                labels={'value': '게시글 수', 'year_month_day': '날짜', 'variable': '대분류'},
                title=f'{selected_year}년도 대분류별 게시글 수')

    # x축 눈금 설정: 연도-월 형식으로 표시
    fig.update_xaxes(
        tickangle=45,
        tickmode='array',
        tickvals=[str(x) for x in df_pivot_year.index],
        ticktext=[pd.to_datetime(x).strftime('%Y-%m') for x in df_pivot_year.index]
    )

    # 스트림릿 애플리케이션에 그래프 표시
    st.plotly_chart(fig)

# 년도별 대분류별 게시글수- 월단위
def category_posts_month():
    # Group data by year-month and category
    df['year_month'] = df['date'].dt.to_period('M')
    df['year_month'] = df['year_month'].astype(str)
    df_year_month = df.groupby(['year_month', '대분류']).size().reset_index(name='게시글')
    df_year_month['year_month'] = df_year_month['year_month'].astype(str)

    # Create pivot table
    df_pivot = df_year_month.pivot(index='year_month', columns='대분류', values='게시글')

    # Plot data year by year with Plotly
    years = df_year_month['year_month'].str.split('-').str[0].unique()
    for year in years:
        df_year = df_pivot[df_pivot.index.str.startswith(year)]
        fig = px.line(df_year, x=df_year.index, y=df_year.columns,
                    labels={'value': '게시글 수', 'variable': '대분류'},
                    title=f'{year}년도 대분류별 게시글 수')
        fig.update_xaxes(title_text='월')
        fig.update_yaxes(title_text='게시글 수')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)

# 연-월별 대분류별 좋아요 수
def month_category_good():
    # 연-월, 대분류로 groupby하여 'good' 열의 합계 계산
    df_year_month = df.groupby(['year_month', '대분류'])['good'].sum().reset_index(name='total_good')

    # 피벗 테이블을 사용하여 데이터 재구성
    df_pivot = df_year_month.pivot(index='year_month', columns='대분류', values='total_good')

    # Plotly를 사용하여 선 그래프 생성
    fig = px.line(df_pivot, x=df_pivot.index, y=df_pivot.columns, markers=True, 
                labels={'value': '좋아요 수', 'variable': '대분류', 'year_month': '날짜'},
                title='연-월별 대분류별 좋아요 수')

    # x축과 y축의 레이블 설정
    fig.update_xaxes(title_text='날짜', tickangle=-45)
    fig.update_yaxes(title_text='좋아요 수')

    # 각 선에 대한 마커 설정
    markers = ['circle', 'square', 'triangle-up', 'diamond', 'x-thin']
    for i, trace in enumerate(fig.data):
        trace.marker.symbol = markers[i % len(markers)]
        trace.marker.size = 10  # 마커 크기 조절

    # Streamlit을 사용하여 그래프 출력
    return st.plotly_chart(fig)

# 연-월별 많이 나오는 키워드
def month_keyword():
    # 년-월별로 키워드 카운터 객체를 저장할 딕셔너리 생성
    keyword_counters_by_year_month = {}

    # 년-월별로 데이터를 그룹화하여 반복 처리
    for year_month, group in df.groupby(df['date'].dt.to_period('M')):
        keyword_counter = Counter()
        
        # '키워드2' 열에서 키워드 합치기
        merged_keywords = ' '.join([keyword.strip("'[],") for keyword in group['키워드2']])
        tokens = merged_keywords.split()  # 공백 기준으로 토큰화
        keyword_counter.update(tokens)  # 카운터 객체 업데이트
        
        # 년-월별 키워드 빈도수 저장
        keyword_counters_by_year_month[year_month] = keyword_counter

    # 각 년-월별로 그래프를 생성
    for year_month, keyword_counter in keyword_counters_by_year_month.items():
        keyword_counter_most_common = keyword_counter.most_common(10)  # 가장 빈도 높은 10개 키워드
        keywords, counts = zip(*keyword_counter_most_common)
        
        # Plotly 막대 그래프 생성
        fig = go.Figure(data=[go.Bar(x=keywords, y=counts)])
        fig.update_layout(
            title=f'{year_month}년-월별 가장 많이 등장하는 키워드',
            xaxis_title="키워드",
            yaxis_title="빈도",
            xaxis={'categoryorder':'total descending'}  # 내림차순으로 정렬
        )
        
        # Streamlit으로 그래프 출력
        st.plotly_chart(fig)

# 많이 등장하는 키워드와 좋아요의 관계
def keyword_good():
    # 년-월별로 키워드 카운터 객체를 저장할 딕셔너리 생성
    keyword_counters_by_year_month = {}

    # 년-월별로 데이터를 그룹화하여 반복 처리
    for year_month, group in df.groupby(df['date'].dt.to_period('M')):
        keyword_counter = Counter()
        
        # '키워드' 열에서 키워드 합치기
        merged_keywords = ' '.join([keyword.strip("'[],") for keyword in group['키워드']])
        tokens = merged_keywords.split()  # 공백 기준으로 토큰화
        keyword_counter.update(tokens)  # 카운터 객체 업데이트
        
        # 년-월별 키워드 빈도수 저장
        keyword_counters_by_year_month[year_month] = keyword_counter

    # 각 키워드의 빈도수와 좋아요 수를 매핑할 딕셔너리 생성
    keyword_likes_mapping = {}

    # 각 년-월별로 좋아요 수를 더하여 매핑 딕셔너리 업데이트
    for year_month, group in df.groupby(df['date'].dt.to_period('M')):
        for keyword, count in keyword_counters_by_year_month[year_month].items():
            likes = group[group['키워드'].apply(lambda x: keyword in x)]['good'].sum()
            keyword_likes_mapping[keyword] = keyword_likes_mapping.get(keyword, 0) + likes

    # 각 년-월별로 결과를 리스트에 추가하여 데이터프레임으로 변환
    results = []
    for year_month, keyword_counter in keyword_counters_by_year_month.items():
        for keyword, count in keyword_counter.items():
            results.append({
                '년-월': year_month.strftime('%Y-%m'), 
                '키워드': keyword, 
                '좋아요 수': keyword_likes_mapping.get(keyword, 0)
            })

    result_df = pd.DataFrame(results)

    # Streamlit을 사용하여 결과 데이터프레임 출력
    st.write(result_df)

    # 가장 많이 사용된 키워드와 그 좋아요 수에 대한 막대 그래프를 Plotly로 생성
    fig = go.Figure()
    for year_month, keyword_counter in keyword_counters_by_year_month.items():
        keyword_counter_most_common = keyword_counter.most_common(10)
        keywords, counts = zip(*keyword_counter_most_common)
        likes = [keyword_likes_mapping.get(k, 0) for k in keywords]
        
        fig.add_trace(go.Bar(x=keywords, y=likes, name=str(year_month)))

    fig.update_layout(
        title='년-월별 가장 많이 사용된 키워드의 좋아요 수',
        xaxis_title='키워드',
        yaxis_title='좋아요 수',
        barmode='group'
    )

    # Streamlit으로 그래프 출력
    st.plotly_chart(fig)
    
# 계정 ID별 월별 좋아요 수
def ID_month_good():
    # 'date' 열을 기준으로 월을 추출하여 새로운 열에 저장
    df['month'] = df['date'].dt.to_period('M')

    # 월별, ID별로 좋아요 수를 합산
    monthly_likes = df.groupby(['month', 'ID'])['good'].sum().reset_index()

    # Plotly를 사용하여 각 ID별로 선 그래프 생성
    fig = px.line(monthly_likes, x='month', y='good', color='ID',
                labels={
                    'month': '월',
                    'good': '좋아요 수',
                    'ID': 'ID'
                },
                title='월별 ID별 좋아요 수')

    # 그래프 세부사항 설정
    fig.update_traces(marker=dict(size=3))  # 마커 크기 조절
    fig.update_layout(xaxis_title='월', yaxis_title='좋아요 수', legend_title_text='ID')
    fig.update_xaxes(tickangle=45)

    # Streamlit을 사용하여 그래프 출력
    st.plotly_chart(fig)

# 월별 ID별 게시글 수 
def ID_posts():
    # 'date' 열을 기준으로 월을 추출하여 새로운 열에 저장
    df['month'] = df['date'].dt.to_period('M')

    # 월별, ID별로 게시글 수를 카운트
    monthly_count = df.groupby(['month', 'ID'])['post'].count().reset_index()

    # Plotly를 사용하여 각 ID별로 선 그래프 생성
    fig = px.line(monthly_count, x='month', y='post', color='ID',
                labels={
                    'month': '월',
                    'post': '게시글 수',
                    'ID': 'ID'
                },
                title='월별 ID별 게시글 수')

    # 그래프 세부사항 설정
    fig.update_traces(marker=dict(size=5))  # 마커 크기 조절
    fig.update_layout(xaxis_title='월', yaxis_title='게시글 수', legend_title_text='ID')
    fig.update_xaxes(tickangle=45)

    # Streamlit을 사용하여 그래프 출력
    st.plotly_chart(fig)

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
    def month_category_posts():
        df = pd.read_excel('240512_df.xlsx',parse_dates=['date'])
        df['date'] = pd.to_datetime(df['date'])  # 'date' 열을 datetime 형식으로 변환
        df['year_month'] = df['date'].dt.to_period('M')

        # 연도와 월로 그룹화하여 게시글 수 요약
        df_year_month = df.groupby(['year_month', '대분류']).size().reset_index(name='게시글')

        # Pandas Period를 문자열로 변환
        df_year_month['year_month'] = df_year_month['year_month'].dt.strftime('%Y-%m')

        # pivot을 사용하여 데이터 재구성
        df_pivot = df_year_month.pivot(index='year_month', columns='대분류', values='게시글')

        # Plotly를 사용하여 선 그래프 생성
        fig = px.line(df_pivot, x=df_pivot.index, y=df_pivot.columns,
                    labels={'value': '게시글 수', 'year_month': '날짜', 'variable': '대분류'},
                    markers=True, title='연-월별 대분류별 게시글 수')

        # streamlit에 그래프 표시
        return st.plotly_chart(fig)
    month_category_posts()

# 날짜별 대분류별 게시글수
st.subheader("날짜별 대분류별 게시글수")
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
    day_category_posts()

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
col1, col2 = st.columns([1,4])
with col1:
    st.subheader("d d d d d d d d")
with col2: 
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
    st.subheader("d d d d d d d d")
with col2: 
    ID_posts()
