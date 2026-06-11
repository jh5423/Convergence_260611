import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# [중요] 임포트 바로 다음에 위치해야 하며, 다른 어떤 스트림잇 함수보다 먼저 실행되어야 에러가 안 납니다.
st.set_page_config(page_title="물로켓 수학-데이터 시뮬레이터", layout="wide")

# 웹 페이지 제목 및 소개
st.title("🚀 물로켓 포물선 궤적 및 가상 데이터 생성기")
st.markdown("""
이 프로그램은 물로켓의 발사 조건에 따른 **이차함수 궤적(포물선 운동)**을 시뮬레이션하고, 
통계 분석을 위한 **가상 실험 데이터셋**을 생성하는 교육용 도구입니다.
""")

# 중력 가속도 상수 (m/s^2)
G = 9.8

# 사이드바: 시뮬레이션 변수 제어
st.sidebar.header("🛠️ 발사 조건 설정 (시뮬레이션)")
angle = st.sidebar.slider("발사 각도 (도)", min_value=10, max_value=80, value=45, step=5)
v0 = st.sidebar.slider("초기 발사 속도 (m/s)", min_value=5, max_value=30, value=15, step=1)

# --- 기능 1: 포물선 궤적 계산 및 시각화 ---
rad = np.radians(angle)
t_flight = (2 * v0 * np.sin(rad)) / G  # 총 체공 시간
max_range = (v0**2 * np.sin(2 * rad)) / G  # 이론상 최대 사거리
max_height = (v0**2 * (np.sin(rad)**2)) / (2 * G)  # 이론상 최고 높이

# 궤적 좌표 데이터 생성 (0초부터 총 체공시간까지 100개의 구간으로 나눔)
t_space = np.linspace(0, t_flight, 100)
x_coords = v0 * np.cos(rad) * t_space
y_coords = v0 * np.sin(rad) * t_space - 0.5 * G * t_space**2

# Plotly를 이용한 인터랙티브 그래프 시각화
fig = go.Figure()
fig.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='lines', name='물로켓 궤적', line=dict(color='blue', width=3)))
fig.update_layout(
    title=f"물로켓 비행 궤적 (발사각: {angle}°, 초기속도: {v0}m/s)",
    xaxis_title="수평 거리 (사거리: m)",
    yaxis_title="높이 (m)",
    yaxis=dict(range=[0, max(max_height * 1.2, 5)]),
    xaxis=dict(range=[0, max(max_range * 1.1, 10)]),
    template="plotly_white"
)

# 화면 레이아웃 분할 (왼쪽: 그래프, 오른쪽: 주요 수학적 정량 값)
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 이론적 수학 분석 결과")
    st.metric(label="🎯 최종 사거리 (가로축 끝점)", value=f"{max_range:.2f} m")
    st.metric(label="🔝 최고 도달 높이 (이차함수 꼭짓점)", value=f"{max_height:.2f} m")
    st.metric(label="⏱️ 총 비행 시간", value=f"{t_flight:.2f} 초")

st.divider()

# --- 기능 2: 데이터 분석 수업을 위한 가상 데이터셋 생성 ---
st.subheader("📈 통계 분석용 가상 실험 데이터셋 생성")
st.write("발사각을 15도부터 75도까지 변화시키며 여러 번 실험했을 때, **실제 야외 환경의 오차(바람, 공기저항 등)**가 반영된 데이터셋을 생성합니다.")

if st.button("🎲 새로운 가상 실험 데이터셋 생성하기"):
    # 가상 데이터 생성용 변수
    angles_test = np.repeat(np.arange(15, 76, 15), 5)  # 15, 30, 45, 60, 75도를 각각 5번씩 반복 (총 25회 실험)
    base_v0 = 15  # 기준 속도 15m/s 고정
    
    results = []
    for idx, ang in enumerate(angles_test):
        r_rad = np.radians(ang)
        # 이론적 사거리
        theoretical_r = (base_v0**2 * np.sin(2 * r_rad)) / G
        
        # 현실적인 오차(Noise) 추가
        noise = np.random.normal(0, 1.2) - 0.5 
        actual_r = max(0, theoretical_r + noise)  # 사거리가 음수가 되지 않도록 방지
        
        results.append({
            "실험 번호": idx + 1,
            "발사각도 (degree)": ang,
            "이론적 사거리 (m)": round(theoretical_r, 2),
            "실제 측정 사거리 (m)": round(actual_r, 2),
            "오차 (m)": round(actual_r - theoretical_r, 2)
        })
        
    df = pd.DataFrame(results)
    st.session_state['rocket_data'] = df

# 생성된 데이터가 세션에 존재할 경우 화면에 표시
if 'rocket_data' in st.session_state:
    df_display = st.session_state['rocket_data']
    
    col_df, col_down = st.columns([2, 1])
    with col_df:
        st.dataframe(df_display, use_container_width=True)
    
    with col_down:
        st.write("📂 **수업 활용 팁**")
        st.caption("이 데이터를 CSV 파일로 다운로드하여 엑셀이나 구글 스프레드시트, 또는 파이썬 판다스로 가져가 이차함수 회귀분석이나 통계 그래프 그리기 수업을 진행할 수 있습니다.")
        
        # CSV 다운로드 버튼
        csv = df_display.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 가상 데이터셋(.CSV) 다운로드",
            data=csv,
            file_name="water_rocket_experiment_data.csv",
            mime="text/csv"
        )
