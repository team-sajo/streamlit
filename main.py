import pandas as pd # pip install pandas openpyxl
import plotly.express as px # pip install plotly-express
import streamlit as st # pip install streamlit
import plotly.graph_objects as go # pip install plotly
from collections import Counter
import emoji # pip install emoji
from PIL import Image

df = pd.read_excel("240510_df_2_1.xlsx")
###########################
# ------ 함수들 --------
###########################

# ------------------------------

# 각 카테고리별 데이터 개수 계산
def category_counts():
    category_counts = df['대분류'].value_counts().reset_index()
    category_counts.columns = ['대분류', 'count']

    # 데이터 개수 시각화
    fig = px.bar(category_counts, x='대분류', y='count', title='업종별 데이터 개수',
                labels={'count': '데이터 개수', '대분류': '업종'}, color='count')
    
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'),    
)

    # Streamlit에 피규어 표시
    return st.plotly_chart(fig)

# 각 카테고리별 총 좋아요 수 계산
def category_likes():
    category_likes = df.groupby('대분류')['good'].sum().reset_index()

    # 좋아요 수 시각화
    fig = px.bar(category_likes, x='대분류', y='good', title='업종별 총 좋아요 수',
                labels={'good': '총 좋아요 수', '대분류': '업종'}, color='good')

    # Streamlit에 피규어 표시
    return st.plotly_chart(fig)

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
    fig.update_layout(title='업종별 데이터 개수 및 좋아요 수',xaxis_title='업종',yaxis_title='데이터 개수',
        legend_title='범례',plot_bgcolor='white')

    # 두 번째 y축 추가 설정
    fig.update_layout(yaxis2=dict(title='총 좋아요 수',overlaying='y',side='right'))

    # Streamlit에서 표시
    st.plotly_chart(fig)

# 데이터수 대비 좋아요 수 비율
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
    fig = px.bar(category_like_ratio_df, x='대분류', y='좋아요 수 비율', title='업종별 데이터수 대비 좋아요 수 비율',
                labels={'좋아요 수 비율': '좋아요 수 비율', '대분류': '업종'}, color='좋아요 수 비율')

    # 그래프 설정
    fig.update_layout(xaxis_title='업종', yaxis_title='좋아요 수 비율',
                    plot_bgcolor='white', xaxis={'categoryorder':'total descending'})

    # Streamlit에 피규어 표시
    return st.plotly_chart(fig)

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

# 월별 대분류별 게시글당 평균 좋아요 비율
def month_category_posts_good():
    # 게시글 수와 좋아요 수를 함께 그룹화하고 집계
    grouped = df.groupby(['month', '대분류']).agg(post_count=('post', 'count'),good_sum=('good', 'sum')).reset_index()

    # 게시글당 평균 좋아요 비율 계산
    grouped['average_like_ratio'] = (grouped['good_sum'] / grouped['post_count'] / 100).round(4)

    # Plotly를 사용한 그래프 그리기
    fig = px.bar(grouped, x='month', y='average_like_ratio', color='대분류',
                labels={'month': '월', 'average_like_ratio': '좋아요 비율 (%)', '대분류': '업종'},
                title='월별 대분류별 게시글당 평균 좋아요 비율')

    # 그래프 레이아웃 설정
    fig.update_layout(
        xaxis_title='월',
        yaxis_title='좋아요 비율 (%)',
        plot_bgcolor='white',
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

# 연도별 많이 나오는 키워드수
def year_keyword():
    # 연도별로 데이터를 그룹화
    years = sorted(df['year'].unique())
    tabs = st.tabs([f"{year}" for year in years])
    
    for idx, tab in enumerate(tabs):
        year = years[idx]
        year_data = df[df['year'] == year]
        
        # 빈 Counter 객체 생성
        keyword_counter = Counter()
        
        # 해당 연도의 데이터에서 '키워드2' 열의 값을 합치기
        merged_keywords = ' '.join([keyword.strip("'[],") for keyword in year_data['키워드2']])
        
        # 토큰화하여 Counter 객체 업데이트
        tokens = merged_keywords.split()
        keyword_counter.update(tokens)
        
        # 가장 많이 등장하는 키워드 10개를 선택
        most_common_keywords = keyword_counter.most_common(10)
        keywords, counts = zip(*most_common_keywords)
        
        # 데이터프레임 생성
        data = pd.DataFrame({'Keyword': keywords, 'Frequency': counts})
        
        # Plotly를 사용한 그래프 그리기
        fig = px.bar(data, x='Keyword', y='Frequency', title=f'{year}년 가장 많이 등장하는 키워드 (상위 10개)',
                     labels={'Frequency': '빈도', 'Keyword': '키워드'})
        fig.update_layout(xaxis_title='키워드', yaxis_title='빈도', plot_bgcolor='white', xaxis_tickangle=-45)
        
        # 탭에 그래프 추가
        with tab:
            st.plotly_chart(fig)

# 연도별 좋아요수
def year_good_fig1():
    # 연도별로 '좋아요' 수 집계
    grouped_good = df.groupby('year').agg(good_sum=('good', 'sum')).reset_index()

    # Plotly를 사용한 그래프 그리기
    fig1 = px.bar(grouped_good, x='year', y='good_sum',
                labels={'year': '연도', 'good_sum': '좋아요 합계'},
                title='연도별 좋아요 합계')

    # 그래프 레이아웃 설정
    fig1.update_layout(
        xaxis_title='연도',
        yaxis_title='좋아요 합계',
        plot_bgcolor='white',
        xaxis_tickmode='linear',  # 모든 연도 레이블 표시
        xaxis_dtick=1  # 1년 간격으로 눈금 설정
    )
    # streamlit 막대그래프 그리기
    st.plotly_chart(fig1)
def year_good_fig2():
    # 연도별로 '좋아요' 수 집계
    grouped_good = df.groupby('year').agg(good_sum=('good', 'sum')).reset_index()

    # Plotly를 사용한 꺾은선 그래프 그리기
    fig2 = px.line(grouped_good, x='year', y='good_sum',
                labels={'year': '연도', 'good_sum': '좋아요 합계'},
                title='연도별 좋아요 합계',
                markers=True)  # 점 표시 추가

    # 그래프 레이아웃 설정
    fig2.update_layout(
        xaxis_title='연도',
        yaxis_title='좋아요 합계',
        plot_bgcolor='white',
        xaxis_tickmode='linear',  # 모든 연도 레이블 표시
        xaxis_dtick=1  # 1년 간격으로 눈금 설정
    )

    # streamlit 막대그래프 그리기
    st.plotly_chart(fig2)

# 연도별 대분류별 좋아요 합계
def year_category_good_fig1():
    # 연도와 대분류별 'good' 열의 합을 계산한 데이터프레임 생성
    grouped_good = df.groupby(['year', '대분류']).agg(good_sum=('good', 'sum')).reset_index()

    # Plotly 그래프 객체 생성
    fig1 = go.Figure()

    # 각 대분류별로 그래프를 그립니다.
    for category in grouped_good['대분류'].unique():
        data = grouped_good[grouped_good['대분류'] == category]
        fig1.add_trace(go.Scatter(
            x=data['year'],
            y=data['good_sum'],
            mode='lines+markers',
            name=category  # 범례 이름 설정
        ))

    # 그래프 레이아웃 설정
    fig1.update_layout(
        title='꺾은선 그래프',
        xaxis=dict(title='연도'),
        yaxis=dict(title='좋아요 합계'),
        legend_title="대분류",
        plot_bgcolor='white'
    )

    # x축 설정: 모든 연도 표시
    fig1.update_xaxes(tickmode='array', tickvals=grouped_good['year'].unique())

    # Streamlit에 그래프 표시
    st.plotly_chart(fig1)
def year_category_good_fig2():
    # 연도와 대분류별 'good' 열의 합을 계산한 데이터프레임 생성
    grouped_good = df.groupby(['year', '대분류']).agg(good_sum=('good', 'sum')).reset_index()

    # Plotly 그래프 객체 생성
    fig2 = go.Figure()

    # 각 대분류별로 막대 그래프를 그립니다.
    for category in grouped_good['대분류'].unique():
        data = grouped_good[grouped_good['대분류'] == category]
        fig2.add_trace(go.Bar(
            x=data['year'],
            y=data['good_sum'],
            name=category,  # 범례 이름 설정
            marker=dict(opacity=0.7)  # 막대의 투명도 설정
        ))

    # 그래프 레이아웃 설정
    fig2.update_layout(
        title='막대그래프',
        xaxis=dict(title='연도', type='category'),
        yaxis=dict(title='좋아요 합계'),
        legend_title="대분류",
        barmode='stack',  # 스택드 막대 그래프 설정
        plot_bgcolor='white'
    )

    # x축 설정: 연도 별로 정렬
    fig2.update_xaxes(categoryorder='array', categoryarray=sorted(grouped_good['year'].unique()))

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig2)

# 연도별 대분류별 게시물수
def year_category_post_fig1():
    grouped_post_count = df.groupby(['year', '대분류']).agg(post_count=('post', 'count')).reset_index()
    fig1 = go.Figure()
    for category in grouped_post_count['대분류'].unique():
        data = grouped_post_count[grouped_post_count['대분류'] == category]
        fig1.add_trace(go.Bar(
            x=data['year'],
            y=data['post_count'],
            name=category,
            opacity=0.7
        ))
    fig1.update_layout(
        xaxis_title='연도',
        yaxis_title='게시물 수',
        barmode='group',
        legend_title="대분류"
    )
    return st.plotly_chart(fig1)
def year_category_post_fig2():
    grouped_post_count = df.groupby(['year', '대분류']).agg(post_count=('post', 'count')).reset_index()
    fig2 = go.Figure()
    for category in grouped_post_count['대분류'].unique():
        data = grouped_post_count[grouped_post_count['대분류'] == category]
        fig2.add_trace(go.Scatter(
            x=data['year'],
            y=data['post_count'],
            mode='lines+markers',
            name=category
        ))
    fig2.update_layout(
        xaxis_title='연도',
        yaxis_title='게시물 수',
        legend_title="대분류"
    )
    return st.plotly_chart(fig2)

# 이모티콘 수와 좋아요 수의 관계
def emoji_good():
    def count_emojis(text):
        return sum(1 for i in text if emoji.is_emoji(i))

    # 'post' 열에 이모티콘 개수 계산하여 새로운 열에 저장
    df['emoji_count'] = df['post'].apply(count_emojis)

    # 상관관계 계산
    correlation = df[['emoji_count', 'good']].corr().iloc[0, 1]

    # 산점도 그리기
    fig = px.scatter(df, x='emoji_count', y='good', trendline="ols",
                    labels={'emoji_count': 'Emoji 개수', 'good': 'Good'},
                    title=f'Emoji 개수와 Good 열의 상관관계: {correlation:.2f}')

    # 그래프 레이아웃 설정
    fig.update_layout(xaxis_title='Emoji 개수', yaxis_title='Good')

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig)

# 게시글 길이와 좋아요 수의 관계
def lenpost_good():
    # 게시글 길이 계산
    df['post_len'] = df['post'].apply(len)

    # 상관관계 계산
    correlation = df[['post_len', 'good']].corr().iloc[0, 1]

    # 산점도 그리기
    fig = px.scatter(df, x='post_len', y='good', trendline="ols",
                    labels={'post_len': '게시글 길이', 'good': '좋아요'},
                    title=f'게시글 길이와 좋아요의 상관관계: {correlation:.2f}')

    # 그래프 레이아웃 설정
    fig.update_layout(xaxis_title='게시글 길이', yaxis_title='좋아요')

    # Streamlit에 그래프 표시
    st.plotly_chart(fig)

# 아이디 길이와 follower의 관계
def lenID_follower():
    # 팔로워 데이터 집계
    followers = df.groupby('ID')['follower'].unique()
    followers = pd.DataFrame(followers)
    followers.reset_index(inplace=True)
    followers['ID_length'] = followers['ID'].apply(len)
    followers = followers.explode('follower')
    followers['follower'] = followers['follower'].astype('int')

    # 상관관계 계산
    correlation = followers[['ID_length', 'follower']].corr().iloc[0, 1]

    # 산점도 그리기
    fig = px.scatter(followers, x='ID_length', y='follower',
                    labels={'ID_length': '아이디 길이', 'follower': '팔로워 수'},
                    title=f'아이디 길이와 팔로워의 상관관계: {correlation:.2f}')

    # 그래프 레이아웃 설정
    fig.update_layout(xaxis_title='아이디 길이', yaxis_title='팔로워')

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig)

# follower와 좋아요 수의 관계
def follower_good():
    # 팔로워 수와 좋아요 수 집계
    fg = df.groupby(['ID', 'follower']).agg(good_sum=('good', 'sum')).reset_index()

    # 상관관계 계산
    correlation = fg['follower'].corr(fg['good_sum'])

    # 산점도 그리기
    fig = px.scatter(fg, x='follower', y='good_sum', trendline="ols",
                    labels={'follower': '팔로워 수', 'good_sum': '좋아요 수'},
                    title=f'팔로워 수와 좋아요 수의 상관관계: {correlation:.2f}')

    # 그래프 레이아웃 설정
    fig.update_layout(xaxis_title='팔로워 수', yaxis_title='좋아요 수')

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig)

# follower와 게시글 수의 관계
def follower_post():
    # 팔로워 수와 게시글 수 집계
    fp = df.groupby(['ID', 'follower']).agg(post_count=('post', 'count')).reset_index()

    # 상관관계 계산
    correlation = fp['follower'].corr(fp['post_count'])

    # 산점도 그리기
    fig = px.scatter(fp, x='follower', y='post_count', trendline="ols",
                    labels={'follower': '팔로워 수', 'post_count': '게시글 수'},
                    title=f'팔로워수와 게시글 수의 상관관계: {correlation:.2f}')

    # 그래프 레이아웃 설정
    fig.update_layout(xaxis_title='팔로워 수', yaxis_title='게시글 수')

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig)