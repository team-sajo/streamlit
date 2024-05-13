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

# 연-월별 대분류별 게시글수
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
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    # streamlit에 그래프 표시
    return st.plotly_chart(fig, use_container_width=True)
    
# 날짜별 대분류별 게시글 수
# def day_category_posts():
    df['year_month_day'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d').astype(str)

    # Prepare the pivot table
    df_pivot = df.pivot_table(index='year_month_day', columns='대분류', values='post', aggfunc='count').reset_index()
    df_pivot_long = df_pivot.melt(id_vars='year_month_day', var_name='대분류', value_name='게시글 수')

    # Convert year_month_day back to datetime for plotting
    df_pivot_long['year_month_day'] = pd.to_datetime(df_pivot_long['year_month_day'])

    # Now you can use dt accessor
    x_tickvals = df_pivot_long['year_month_day'].dt.strftime('%Y-%m')

    # Plot using Plotly
    fig = px.line(df_pivot_long, x='year_month_day', y='게시글 수', color='대분류',
                title='날짜별 대분류별 게시글 수',
                labels={'year_month_day': '날짜', '게시글 수': '게시글 수'},
                markers=True)
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=df_pivot_long['year_month_day'],
            ticktext=x_tickvals
        )
    )
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    return st.plotly_chart(fig, use_container_width=True)

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
        tickmode='array',
        tickvals=[str(x) for x in df_pivot_year.index],
        ticktext=[pd.to_datetime(x).strftime('%Y-%m') for x in df_pivot_year.index]
    )
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    # 스트림릿 애플리케이션에 그래프 표시
    st.plotly_chart(fig, use_container_width=True)

# 년도별 대분류별 게시글수- 월단위
def category_posts_month():
    # 날짜 데이터 처리
    df['year_month'] = pd.to_datetime(df['date']).dt.to_period('M')
    df['year_month'] = df['year_month'].astype(str)
    df_year_month = df.groupby(['year_month', '대분류']).size().reset_index(name='게시글')
    df_year_month['year_month'] = df_year_month['year_month'].astype(str)

    # 피벗테이블 생성
    df_pivot = df_year_month.pivot(index='year_month', columns='대분류', values='게시글')

    # 연도별로 데이터 준비
    years = df_year_month['year_month'].str.split('-').str[0].unique()

    with st.container():
        tabs = st.tabs([year for year in years])

        for tab, year in zip(tabs, years):
            df_year = df_pivot[df_pivot.index.str.startswith(year)]
            
            # 한글 월 이름으로 라벨 설정
            month_labels = pd.date_range(start=f'{year}-01', end=f'{year}-12', freq='ME').strftime('%Y-%m')
            month_korean = pd.date_range(start=f'{year}-01', end=f'{year}-12', freq='ME').strftime('%m월')
            
            # 그래프 생성
            fig = px.line(df_year, x=df_year.index, y=df_year.columns,
                          labels={'value': '게시글 수', 'variable': '대분류'},
                          title=f'{year}년도 대분류별 게시글 수')
            fig.update_xaxes(title_text='월', tickvals=month_labels, ticktext=month_korean)
            fig.update_yaxes(title_text='게시글 수')
            fig.update_layout(
                margin=dict(l=60, r=40, t=60, b=40),
                paper_bgcolor="#ECF8E0",
                plot_bgcolor="white",
                title_font=dict(color='black'))

            with tab:
                st.plotly_chart(fig, use_container_width=True)

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
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    # 각 선에 대한 마커 설정
    markers = ['circle', 'square', 'triangle-up', 'diamond', 'x-thin']
    for i, trace in enumerate(fig.data):
        trace.marker.symbol = markers[i % len(markers)]
        trace.marker.size = 10  # 마커 크기 조절

    # Streamlit으로 그래프 출력
    return st.plotly_chart(fig, use_container_width=True)

# 연-월별 많이 나오는 키워드
def year_month_keyword():
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

    # Streamlit 탭 컨테이너 생성
    with st.container():
        tabs = st.tabs([str(year_month) for year_month in keyword_counters_by_year_month.keys()])

        # 각 탭에 해당하는 그래프 추가
        for tab, (year_month, keyword_counter) in zip(tabs, keyword_counters_by_year_month.items()):
            keyword_counter_most_common = keyword_counter.most_common(10)  # 가장 빈도 높은 10개 키워드
            keywords, counts = zip(*keyword_counter_most_common)
            
            # Plotly 막대 그래프 생성
            fig = go.Figure(data=[go.Bar(x=keywords, y=counts)])
            fig.update_layout(
                title=f'{year_month}에 가장 많이 등장하는 키워드',
                xaxis_title="키워드",
                yaxis_title="빈도",
                xaxis={'categoryorder':'total descending'}  # 내림차순으로 정렬
            )
            fig.update_layout(
            margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
            paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
            plot_bgcolor="white",    # 플롯 영역 배경색 설정
            title_font=dict(color='black'))
            
            # 현재 탭에 streamlit으로 그래프 출력
            with tab:
                st.plotly_chart(fig, use_container_width=True)

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
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    # Streamlit으로 그래프 출력
    st.plotly_chart(fig, use_container_width=True)
    
# 계정 ID별 월별 좋아요 수
def ID_month_good():
    # 'date' 열을 기준으로 월을 추출하여 새로운 열에 저장
    df['month'] = df['date'].dt.to_period('M').astype(str)

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
    fig.update_layout(xaxis_title='연도', yaxis_title='좋아요 수', legend_title_text='ID')
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))
    fig.update_xaxes(tickangle=45)

    # Streamlit으로 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

# 월별 ID별 게시글 수 
def ID_posts():
    # 'date' 열을 기준으로 월을 추출하여 새로운 열에 저장
    df['month'] = df['date'].dt.to_period('M').astype(str)

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
    fig.update_layout(xaxis_title='연도', yaxis_title='게시글 수', legend_title_text='ID')
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))
    fig.update_xaxes(tickangle=45)

    # Streamlit으로 그래프 출력
    st.plotly_chart(fig, use_container_width=True)


# ------------------------------
# ------------------------------

# 각 카테고리별 데이터 개수 계산
def category_counts():
    category_counts = df['대분류'].value_counts().reset_index()
    category_counts.columns = ['대분류', 'count']

    # 데이터 개수 시각화
    fig = px.bar(category_counts, x='대분류', y='count', title='업종별 데이터 개수',
                labels={'count': '데이터 개수', '대분류': '업종'}, color='count')
    
    fig.update_layout(
    margin=dict(l=60, r=40, t=50, b=30),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    # Streamlit에 피규어 표시
    return st.plotly_chart(fig, use_container_width=True)

# 각 카테고리별 좋아요 수 계산
def category_likes():
    category_likes = df.groupby('대분류')['good'].sum().reset_index()

    # 좋아요 수 시각화
    fig = px.bar(category_likes, x='대분류', y='good', title='업종별 좋아요 수',
                labels={'good': '좋아요 수', '대분류': '업종'}, color='good',
                category_orders={'대분류': ['식당', '관광지', '카페', '쇼핑', '숙소', '반려동물', '미분류']})
    
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    # Streamlit에 피규어 표시
    return st.plotly_chart(fig, use_container_width=True)

# 각 카테고리별 데이터수, 좋아요수 계산
def category_counts_likes():
    # 원하는 순서 지정
    order = ['식당', '관광지', '카페', '쇼핑', '숙소', '반려동물', '미분류']
    
    # 각 카테고리별 데이터 개수 계산
    category_counts = df['대분류'].value_counts().reindex(order)
    
    # 각 카테고리별 총 좋아요 수 계산
    category_likes = df.groupby('대분류')['good'].sum().reindex(order)

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
    fig.update_layout(title='업종별 데이터 개수 및 좋아요 수', xaxis_title='업종', yaxis_title='데이터 개수',
                      legend_title='범례', margin=dict(l=60, r=40, t=60, b=40),
                      paper_bgcolor="#ECF8E0", plot_bgcolor="white", title_font=dict(color='black'))

    # 두 번째 y축 추가 설정
    fig.update_layout(yaxis2=dict(title='총 좋아요 수', overlaying='y', side='right'))

    # Streamlit에서 표시
    return st.plotly_chart(fig, use_container_width=True)

# 게시물수 대비 좋아요 수 비율
def category_counts_likes_divide():
    order = ['식당', '관광지', '카페', '쇼핑', '숙소', '반려동물', '미분류']
    
    # 각 카테고리별 데이터 개수 계산
    category_counts = df['대분류'].value_counts()

    # 각 카테고리별 총 좋아요 수 계산
    category_likes = df.groupby('대분류')['good'].sum()

    # 각 카테고리별 좋아요 수의 평균 계산
    category_like_ratio = category_likes / category_counts

    # 좋아요 수 비율을 데이터 프레임으로 변환 및 순서 정렬
    category_like_ratio_df = category_like_ratio.reindex(order).reset_index()
    category_like_ratio_df.columns = ['대분류', '좋아요 수 비율']

    # 데이터 시각화
    fig = px.bar(category_like_ratio_df, x='대분류', y='좋아요 수 비율', title='업종별 데이터수 대비 좋아요 수 비율',
                 labels={'좋아요 수 비율': '좋아요 수 비율', '대분류': '업종'}, color='좋아요 수 비율',
                 category_orders={'대분류': order})  # 순서 지정

    # 그래프 설정
    fig.update_layout(xaxis_title='업종', yaxis_title='좋아요 수 비율',
                      margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
                      paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
                      plot_bgcolor="white",    # 플롯 영역 배경색 설정
                      title_font=dict(color='black'))

    # Streamlit에 피규어 표시
    return st.plotly_chart(fig, use_container_width=True)

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
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))
    # Streamlit에 피규어 표시
    return st.plotly_chart(fig, use_container_width=True)

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
    tabs = st.tabs([f"✅{industry}" for industry in keyword_counters_by_industry.keys()])

    # 각 탭에 대해 그래프 생성 및 표시
    for i, (industry, keyword_counter) in enumerate(keyword_counters_by_industry.items()):
        top_keywords = keyword_counter.most_common(10)
        keywords, frequencies = zip(*top_keywords)
        
        fig = go.Figure(go.Bar(x=keywords, y=frequencies, marker_color='blue'))
        fig.update_layout(title=f'상위 10개 키워드 빈도수- {industry}',
                        xaxis_title='키워드',
                        yaxis_title='빈도수')
        fig.update_layout(
        margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
        paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
        plot_bgcolor="white",    # 플롯 영역 배경색 설정
        title_font=dict(color='black'))
        
        with tabs[i]:
            st.plotly_chart(fig, use_container_width=True)

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
    tabs = st.tabs([f"✅{month}월" for month in sorted(keyword_counters_by_month.keys())])

    # 각 탭에 대해 그래프 생성 및 표시
    for i, (month, keyword_counter) in enumerate(sorted(keyword_counters_by_month.items())):
        top_keywords = keyword_counter.most_common(10)
        keywords, frequencies = zip(*top_keywords)
        
        # Plotly 막대 그래프 생성
        fig = go.Figure(go.Bar(x=keywords, y=frequencies, marker_color='blue'))
        fig.update_layout(title=f'{month}월 - 상위 10개 키워드 빈도수',
                        xaxis_title='키워드',
                        yaxis_title='빈도수')
        fig.update_layout(
        margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
        paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
        plot_bgcolor="white",    # 플롯 영역 배경색 설정
        title_font=dict(color='black'))
        
        with tabs[i]:
            st.plotly_chart(fig, use_container_width=True)

# 업종별 게시글수
def category_posts():
    # 대분류를 기준으로 그룹화하고, 각 그룹에서 'post' 열 값의 빈도를 계산합니다.
    grouped_counts = df.groupby('대분류').agg(post_count = ('post', 'count'))

    # Plotly를 사용한 그래프 그리기
    fig = px.bar(grouped_counts, x=grouped_counts.index, y='post_count',
                labels={'x': '대분류', 'post_count': '포스트 수'},
                title='업종별 게시글 수')
    fig.update_layout(xaxis_title='월', yaxis_title='포스트 수')
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))
    fig.update_traces(marker_color='skyblue')  # 막대 색상 설정
    fig.add_hline(y=grouped_counts['post_count'].mean(), line_dash="dash", line_color="red", annotation_text="평균 게시글 수")

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig, use_container_width=True)

# 월별 게시글수
def month_posts():
    # 대분류를 기준으로 그룹화하고, 각 그룹에서 'post' 열 값의 빈도를 계산합니다.
    grouped_counts = df.groupby('month').agg(post_count=('post', 'count'))

    # Plotly를 사용한 그래프 그리기
    fig = px.bar(grouped_counts, x=grouped_counts.index, y='post_count',
                labels={'x': '월', 'post_count': '포스트 수'},
                title='월별 게시글 수')
    fig.update_layout(xaxis_title='월', yaxis_title='포스트 수', xaxis=dict(tickmode='linear', dtick=1))
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))
    fig.update_traces(marker_color='skyblue')  # 막대 색상 설정
    fig.add_hline(y=grouped_counts['post_count'].mean(), line_dash="dash", line_color="red", annotation_text="평균 게시글 수")

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig, use_container_width=True)

# 월별 좋아요수
def month_good():
    # 그룹화 및 집계
    grouped_counts = df.groupby('month').agg(post_count=('good', 'sum')).reset_index()

    # Plotly를 사용한 그래프 그리기
    fig = px.bar(grouped_counts, x='month', y='post_count',
                labels={'month': '월', 'post_count': '좋아요 수'},
                title='월별 좋아요 수')
    fig.update_layout(
        xaxis_title='월', yaxis_title='좋아요 수',
        xaxis=dict(tickmode='linear', dtick=1),  # 눈금 간격을 1로 설정하여 모든 레이블 표시
        yaxis=dict(tickmode='linear', dtick=100000),
    )
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))
    fig.update_traces(marker_color='skyblue')  # 막대 색상 설정

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig, use_container_width=True)

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
        xaxis=dict(tickmode='linear', dtick=1),
        legend_title='업종',
        barmode='stack'
    )
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    # 범례 위치 조정
    fig.update_layout(legend=dict(orientation='v', yanchor="top", y=1.02, xanchor="left", x=8))

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig, use_container_width=True)

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
        legend_title='업종',
        xaxis=dict(tickmode='linear', dtick=1),
        yaxis=dict(tickmode='linear', dtick=100000),
        legend=dict(orientation='v', yanchor="top", y=1.02, xanchor="left", x=8)
    )
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig, use_container_width=True)

# 월별 대분류별 게시글당 평균 좋아요 비율
def month_category_posts_good():
    # 게시글 수와 좋아요 수를 함께 그룹화하고 집계
    grouped = df.groupby(['month', '대분류']).agg(post_count=('post', 'count'),good_sum=('good', 'sum')).reset_index()

    # 게시글당 평균 좋아요 비율 계산
    grouped['average_like_ratio'] = (grouped['good_sum'] / grouped['post_count'] / 100).round(4)

    # Plotly를 사용한 그래프 그리기
    fig = px.bar(grouped, x='month', y='average_like_ratio', color='대분류',
                labels={'month': '월', 'average_like_ratio': '좋아요 수', '대분류': '업종'},
                title='월별 대분류별 게시글당 평균 좋아요수')

    # 그래프 레이아웃 설정
    fig.update_layout(
        xaxis_title='월',
        yaxis_title='좋아요수',
        barmode='stack',
        xaxis=dict(tickmode='linear', dtick=1)
    )
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    # 범례 위치 조정
    fig.update_layout(legend=dict(orientation='v', yanchor="top", y=1.02, xanchor="left", x=8))

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig, use_container_width=True)

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
        fig.update_layout(xaxis_title='키워드', yaxis_title='빈도', xaxis_tickangle=-45)
        fig.update_layout(
        margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
        paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
        plot_bgcolor="white",    # 플롯 영역 배경색 설정
        title_font=dict(color='black'))
        # 탭에 그래프 추가
        with tab:
            st.plotly_chart(fig, use_container_width=True)

# 연도별 좋아요수
def year_good_fig1():
    # 연도별로 '좋아요' 수 집계
    grouped_good = df.groupby('year').agg(good_sum=('good', 'sum')).reset_index()

    # Plotly를 사용한 그래프 그리기
    fig = px.bar(grouped_good, x='year', y='good_sum',
                labels={'year': '연도', 'good_sum': '좋아요 합계'},
                title='연도별 좋아요 합계')

    # 그래프 레이아웃 설정
    fig.update_layout(
        xaxis_title='연도',
        yaxis_title='좋아요 합계',
        plot_bgcolor='white',
        xaxis_tickmode='linear',  # 모든 연도 레이블 표시
        xaxis_dtick=1  # 1년 간격으로 눈금 설정
    )
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))
    # streamlit 막대그래프 그리기
    st.plotly_chart(fig, use_container_width=True)
def year_good_fig2():
    # 연도별로 '좋아요' 수 집계
    grouped_good = df.groupby('year').agg(good_sum=('good', 'sum')).reset_index()

    # Plotly를 사용한 꺾은선 그래프 그리기
    fig = px.line(grouped_good, x='year', y='good_sum',
                labels={'year': '연도', 'good_sum': '좋아요 합계'},
                title='연도별 좋아요 합계',
                markers=True)  # 점 표시 추가

    # 그래프 레이아웃 설정
    fig.update_layout(
        xaxis_title='연도',
        yaxis_title='좋아요 합계',
        plot_bgcolor='white',
        xaxis_tickmode='linear',  # 모든 연도 레이블 표시
        xaxis_dtick=1  # 1년 간격으로 눈금 설정
    )
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    # streamlit 막대그래프 그리기
    st.plotly_chart(fig, use_container_width=True)

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
        title='연도별 대분류별 좋아요수 꺾은선 그래프',
        xaxis=dict(title='연도'),
        yaxis=dict(title='좋아요 합계'),
        legend_title="대분류"
    )
    fig1.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    # x축 설정: 모든 연도 표시
    fig1.update_xaxes(tickmode='array', tickvals=grouped_good['year'].unique())

    # Streamlit에 그래프 표시
    st.plotly_chart(fig1, use_container_width=True)
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
        title='연도별 대분류별 좋아요수 막대그래프',
        xaxis=dict(title='연도', type='category'),
        yaxis=dict(title='좋아요 합계'),
        legend_title="대분류",
        barmode='stack',  # 스택드 막대 그래프 설정
        plot_bgcolor='white'
    )
    fig2.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    # x축 설정: 연도 별로 정렬
    fig2.update_xaxes(categoryorder='array', categoryarray=sorted(grouped_good['year'].unique()))

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig2, use_container_width=True)

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
        title='연도별 대분류별 게시물수 막대그래프',
        xaxis_title='연도',
        yaxis_title='게시물 수',
        barmode='group',
        legend_title="대분류"
    )
    fig1.update_layout(
        margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
        paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
        plot_bgcolor="white",    # 플롯 영역 배경색 설정
        title_font=dict(color='black')
    )
    return st.plotly_chart(fig1, use_container_width=True)
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
        title='연도별 대분류별 게시물수 꺾은선 그래프',
        xaxis_title='연도',
        yaxis_title='게시물 수',
        legend_title="대분류"
    )
    fig2.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))
    return st.plotly_chart(fig2, use_container_width=True)

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
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))

    # Streamlit에 그래프 표시
    return st.plotly_chart(fig, use_container_width=True)

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
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))
    # Streamlit에 그래프 표시
    st.plotly_chart(fig, use_container_width=True)

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
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))
    # Streamlit에 그래프 표시
    return st.plotly_chart(fig, use_container_width=True)

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
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))
    # Streamlit에 그래프 표시
    return st.plotly_chart(fig, use_container_width=True)

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
    fig.update_layout(
    margin=dict(l=60, r=40, t=60, b=40),  # 그래프의 마진 조정
    paper_bgcolor="#ECF8E0",   # 그래프 배경색 설정
    plot_bgcolor="white",    # 플롯 영역 배경색 설정
    title_font=dict(color='black'))
    # Streamlit에 그래프 표시
    return st.plotly_chart(fig, use_container_width=True)