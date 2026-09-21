import streamlit as st
import pandas as pd


# ---------------------------------------
# 페이지 설정
# ---------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("1년치 일별 박스오피스 데이터를 시간의 흐름에 따라 살펴봅니다.")


# ---------------------------------------
# 데이터 주소
# ---------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# ---------------------------------------
# 데이터 불러오기
# ---------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 진짜 날짜로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자로 변환
    number_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in number_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


# ---------------------------------------
# 데이터 로딩
# ---------------------------------------
try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.write(e)
    st.stop()


# ---------------------------------------
# 그래프 1
# ---------------------------------------
st.header("📈 그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 하나 선택하면 날짜에 따른 "
    "해당 영화의 일관객 변화를 확인할 수 있습니다."
)


# 영화 목록
movie_list = sorted(
    df["영화명"].dropna().unique()
)


# 영화 선택
selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


# 선택한 영화만 추출
movie_df = df[
    df["영화명"] == selected_movie
].copy()


# 날짜순 정렬
movie_df = movie_df.sort_values("날짜")


# 날짜를 인덱스로 사용
chart_data = movie_df[
    ["날짜", "일관객"]
].dropna()

chart_data = chart_data.set_index("날짜")


# ---------------------------------------
# 선 그래프
# ---------------------------------------
st.line_chart(
    chart_data,
    y="일관객",
    x_label="날짜",
    y_label="일관객 수(명)",
    height=500
)


# ---------------------------------------
# 그래프 설명
# ---------------------------------------
st.markdown("###
