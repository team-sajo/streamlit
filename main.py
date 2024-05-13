import pandas as pd # pip install pandas openpyxl
import plotly.express as px # pip install plotly-express
import streamlit as st # pip install streamlit
import plotly.graph_objects as go # pip install plotly
from collections import Counter

st.set_page_config(page_title="🖼️4조의 시각화🖼️", layout='wide')

df = pd.read_excel("240510_df_2_1.xlsx")

# 데이터 접었다 필 수 있게 만들어놓기
with st.expander("데이터 보기"):
	st.dataframe(df, height=200)

#################
# ---- 메인 ----
#################

# 각 카테고리별 데이터 개수 계산
def category_counts():
    category_counts = df['대분류'].value_counts().reset_index()
    category_counts.columns = ['대분류', 'count']

    # 데이터 개수 시각화
    fig1 = px.bar(category_counts, x='대분류', y='count', title='카테고리별 데이터 개수',
                labels={'count': '데이터 개수', '대분류': '카테고리'}, color='count')

    # Streamlit에 피규어 표시
    return st.plotly_chart(fig1)
category_counts()

# 각 카테고리별 총 좋아요 수 계산
def category_likes():
    category_likes = df.groupby('대분류')['good'].sum().reset_index()

    # 좋아요 수 시각화
    fig2 = px.bar(category_likes, x='대분류', y='good', title='카테고리별 총 좋아요 수',
                labels={'good': '총 좋아요 수', '대분류': '카테고리'}, color='good')

    # Streamlit에 피규어 표시
    return st.plotly_chart(fig2)
category_likes()

# 각 카테고리별 데이터수, 좋아요수 계산
def category_counts_likes():
    # 각 카테고리별 데이터 개수 계산
    category_counts = df['대분류'].value_counts()
    category_counts.sort_index(ascending=False, inplace=True)

    # 각 카테고리별 총 좋아요 수 계산
    category_likes = df.groupby('대분류')['good'].sum()
    category_likes.sort_index(ascending=False, inplace=True)

    # Plotly 그래프 생성
    fig = go.Figure()

    # 카테고리별 데이터 개수를 막대 그래프로 추가
    fig.add_trace(go.Bar(
        x=category_counts.index,
        y=category_counts,
        name='데이터 개수',
        marker_color='skyblue'
    ))

    # 좋아요 수를 꺾은선 그래프로 추가
    fig.add_trace(go.Scatter(
        x=category_likes.index,
        y=category_likes,
        name='총 좋아요 수',
        mode='lines+markers',
        marker_color='salmon',
        yaxis='y2'
    ))

    # 레이아웃 설정
    fig.update_layout(
        title='카테고리별 데이터 개수 및 좋아요 수',
        xaxis_title='카테고리',
        yaxis_title='데이터 개수',
        legend_title='범례',
        plot_bgcolor='white'
    )

    # 두 번째 y축 추가 설정
    fig.update_layout(
        yaxis2=dict(
            title='총 좋아요 수',
            overlaying='y',
            side='right'
        )
    )

    # Streamlit에서 표시
    st.plotly_chart(fig)
category_counts_likes()

# 카테고리 대비 좋아요 수 비율
def category_counts_likes_divide():
    # 각 카테고리별 데이터 개수 계산
    category_counts = df['대분류'].value_counts()

    # 각 카테고리별 총 좋아요 수 계산
    category_likes = df.groupby('대분류')['good'].sum()

    # 각 카테고리별 좋아요 수의 평균 계산
    category_like_ratio = category_likes / category_counts

    # 좋아요 수 비율을 데이터 프레임으로 변환
    category_like_ratio_df = category_like_ratio.reset_index()
    category_like_ratio_df.columns = ['대분류', '좋아요 수 비율']

    # 데이터 시각화
    fig = px.bar(category_like_ratio_df, x='대분류', y='좋아요 수 비율', title='카테고리 대비 좋아요 수 비율',
                labels={'좋아요 수 비율': '좋아요 수 비율', '대분류': '카테고리'}, color='좋아요 수 비율')

    # 그래프 설정
    fig.update_layout(xaxis_title='카테고리', yaxis_title='좋아요 수 비율',
                    plot_bgcolor='white', xaxis={'categoryorder':'total descending'})

    # Streamlit에 피규어 표시
    return st.plotly_chart(fig)
category_counts_likes_divide()

# 전체 키워드 빈도수 (상위 20개)
def keyword_frequency():
    # 빈 Counter 객체 생성
    keyword_counter = Counter()

    # '키워드2' 열의 값을 합치기
    merged_keywords = ' '.join([keyword.strip("'[],") for keyword in df['키워드2']])

    # 토큰화하여 Counter 객체 업데이트
    tokens = merged_keywords.split()  # 키워드를 공백을 기준으로 분리하여 토큰화
    keyword_counter.update(tokens)  # Counter 객체 업데이트

    # 가장 많이 등장하는 상위 20개 키워드 추출
    top_20_keywords = keyword_counter.most_common(20)

    # DataFrame으로 변환
    keywords_df = pd.DataFrame(top_20_keywords, columns=['Keyword', 'Frequency'])

    # 데이터 시각화
    fig = px.bar(keywords_df, x='Keyword', y='Frequency', title='전체 키워드 빈도수 (상위 20개)',
                labels={'Frequency': '빈도', 'Keyword': '키워드'})
    fig.update_traces(texttemplate='%{y}', textposition='outside')  # 막대 위에 빈도 수 표시
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=-45)  # 텍스트 크기 조정 및 x축 라벨 회전

    # Streamlit에 피규어 표시
    return st.plotly_chart(fig)
keyword_frequency()

# 업종별 많이 나오는 키워드수
def category_keyword():
    # 빈 Counter 객체를 각 대분류별로 저장할 딕셔너리 생성
    keyword_counters_by_industry = {}

    # 업종별로 데이터를 그룹화하여 반복
    for industry, group in df.groupby('대분류'):
        # 빈 Counter 객체 생성
        keyword_counter = Counter()
        
        # 각 그룹에서 '키워드2' 열의 값을 합치기
        merged_keywords = ' '.join([keyword.strip("'[],") for keyword in group['키워드2']])
        
        # 토큰화하여 Counter 객체 업데이트
        tokens = merged_keywords.split()  # 키워드를 공백을 기준으로 분리하여 토큰화
        keyword_counter.update(tokens)  # Counter 객체 업데이트
        
        # 해당 대분류의 키워드 빈도수를 딕셔너리에 저장
        keyword_counters_by_industry[industry] = keyword_counter
    
    # Streamlit 탭 생성
    tabs = st.tabs([f"{industry}" for industry in keyword_counters_by_industry.keys()])

    # 각 탭에 대해 그래프 생성 및 표시
    for i, (industry, keyword_counter) in enumerate(keyword_counters_by_industry.items()):
        top_keywords = keyword_counter.most_common(10)
        keywords, frequencies = zip(*top_keywords)
        
        fig = go.Figure(go.Bar(x=keywords, y=frequencies, marker_color='blue'))
        fig.update_layout(title=f'{industry} - 상위 10개 키워드 빈도수',
                        xaxis_title='키워드',
                        yaxis_title='빈도수',
                        plot_bgcolor='white')
        
        with tabs[i]:
            st.plotly_chart(fig)
category_keyword()

# 월별 많이 나오는 키워드수
def month_keyword():
    # 빈 Counter 객체를 각 월별로 저장할 딕셔너리 생성
    keyword_counters_by_month = {}

    # 월별로 데이터를 그룹화하여 반복
    for month, group in df.groupby('month'):
        # 빈 Counter 객체 생성
        keyword_counter = Counter()
        
        # 각 그룹에서 '키워드' 열의 값을 합치기
        merged_keywords = ' '.join([keyword.strip("'[],") for keyword in group['키워드2']])
        
        # 토큰화하여 Counter 객체 업데이트
        tokens = merged_keywords.split()
        keyword_counter.update(tokens)

        # 해당 월의 키워드 빈도수를 딕셔너리에 저장
        keyword_counters_by_month[month] = keyword_counter

    # Streamlit 탭 생성
    tabs = st.tabs([f"{month}월" for month in sorted(keyword_counters_by_month.keys())])

    # 각 탭에 대해 그래프 생성 및 표시
    for i, (month, keyword_counter) in enumerate(sorted(keyword_counters_by_month.items())):
        top_keywords = keyword_counter.most_common(10)
        keywords, frequencies = zip(*top_keywords)
        
        # Plotly 막대 그래프 생성
        fig = go.Figure(go.Bar(x=keywords, y=frequencies, marker_color='blue'))
        fig.update_layout(title=f'{month}월 - 상위 10개 키워드 빈도수',
                        xaxis_title='키워드',
                        yaxis_title='빈도수',
                        plot_bgcolor='white')
        
        with tabs[i]:
            st.plotly_chart(fig)
month_keyword()

# 업종별 게시글수
def category_posts():
    # 대분류를 기준으로 그룹화하고, 각 그룹에서 'post' 열 값의 빈도를 계산합니다.
    grouped_counts = df.groupby('대분류').agg(post_count = ('post', 'count'))

    # Plotly를 사용한 그래프 그리기
    fig = px.bar(grouped_counts, x=grouped_counts.index, y='post_count',
                labels={'x': '대분류', 'post_count': '포스트 수'},
                title='업종별 게시글 수')
    fig.update_layout(xaxis_title='월', yaxis_title='포스트 수',
                    plot_bgcolor='white')
    fig.update_traces(marker_color='skyblue')  # 막대 색상 설정
    fig.add_hline(y=grouped_counts['post_count'].mean(), line_dash="dash", line_color="red", annotation_text="평균 게시글 수")

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig)
category_posts()

# 월별 게시글수
def month_posts():
    # 대분류를 기준으로 그룹화하고, 각 그룹에서 'post' 열 값의 빈도를 계산합니다.
    grouped_counts = df.groupby('month').agg(post_count=('post', 'count'))

    # Plotly를 사용한 그래프 그리기
    fig = px.bar(grouped_counts, x=grouped_counts.index, y='post_count',
                labels={'x': '월', 'post_count': '포스트 수'},
                title='월별 게시글 수')
    fig.update_layout(xaxis_title='월', yaxis_title='포스트 수', xaxis=dict(tickmode='linear', dtick=1),
                    plot_bgcolor='white')
    fig.update_traces(marker_color='skyblue')  # 막대 색상 설정
    fig.add_hline(y=grouped_counts['post_count'].mean(), line_dash="dash", line_color="red", annotation_text="평균 게시글 수")

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig)
month_posts()

# 월별 대분류별 게시글수
def month_category_posts():
    # 그룹화 및 집계
    grouped_counts = df.groupby(['month', '대분류']).agg(post_count=('post', 'count')).reset_index()

    # Plotly를 사용한 그래프 그리기
    fig = px.bar(grouped_counts, x='month', y='post_count', color='대분류',
                labels={'month': '월', 'post_count': '게시글 수', '대분류': '업종'},
                title='월별 대분류별 게시글 수')

    # 막대 그래프에 대한 세부 설정
    fig.update_layout(
        xaxis_title='월',
        yaxis_title='게시글 수',
        plot_bgcolor='white',
        xaxis=dict(tickmode='linear', dtick=1),
        legend_title='업종',
        barmode='stack'
    )

    # 범례 위치 조정
    fig.update_layout(legend=dict(
        title='업종',
        orientation='h',
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig)
month_category_posts()

# 월별 좋아요수
def month_good():
    # 그룹화 및 집계
    grouped_counts = df.groupby('month').agg(post_count=('good', 'sum')).reset_index()

    # Plotly를 사용한 그래프 그리기
    fig = px.bar(grouped_counts, x='month', y='post_count',
                labels={'month': '월', 'post_count': '좋아요 수'},
                title='월별 좋아요 수')
    fig.update_layout(
        xaxis_title='월', yaxis_title='좋아요 수', plot_bgcolor='white',
        xaxis=dict(tickmode='linear', dtick=1),  # 눈금 간격을 1로 설정하여 모든 레이블 표시
        yaxis=dict(tickmode='linear', dtick=100000),
    )
    fig.update_traces(marker_color='skyblue')  # 막대 색상 설정

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig)
month_good()

# 월별 대분류별 좋아요수
def month_category_good():
    # 그룹화 및 집계
    grouped_counts = df.groupby(['month', '대분류']).agg(post_count=('good', 'sum')).reset_index()

    # Plotly를 사용한 그래프 그리기
    fig = px.bar(grouped_counts, x='month', y='post_count', color='대분류',
                labels={'month': '월', 'post_count': '좋아요 수', '대분류': '업종'},
                title='월별 대분류별 좋아요 수', barmode='stack')

    # 그래프 레이아웃 설정
    fig.update_layout(
        xaxis_title='월',
        yaxis_title='좋아요 수',
        plot_bgcolor='white',
        legend_title='업종',
        xaxis=dict(tickmode='linear', dtick=1),
        yaxis=dict(tickmode='linear', dtick=100000),
        legend=dict(orientation='h', yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig)
month_category_good()

####################
# ---- 사이드바 ----
####################

st.sidebar.header("항목을 선택하세요:")
ID = st.sidebar.multiselect(
    "Select ID",
    options = df["ID"].unique(),
    default = df["ID"].unique()
)

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
    "ID == @ID & year == @year & month == @month & 대분류 == @대분류"
)