import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 1. 웹 페이지 제목 및 소개
st.set_page_config(page_title="물로켓 수학-데이터 시뮬레이터", layout="wide")
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
# 수학 공식 기반 계산
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
        # 이론적 사거리 및 최고 높이
        theoretical_r = (base_v0**2 * np.sin(2 * r_rad)) / G
        theoretical_h = (base_v0**2 * (np.sin(r_rad)**2)) / (2 * G)
        
        # 현실적인 오차(Noise) 추가
        noise_r = np.random.normal(0, 1.2) - 0.5 
        noise_h = np.random.normal(0, 0.4) - 0.1
        
        actual_r = max(0, theoretical_r + noise_r)  # 사거리가 음수가 되지 않도록 방지
        actual_h = max(0, theoretical_h + noise_h)  # 높이가 음수가 되지 않도록 방지
        
        results.append({
            "실험 번호": idx + 1,
            "발사각도 (degree)": ang,
            "실제 측정 사거리 (m)": round(actual_r, 2),
            "실제 최고 높이 (m)": round(actual_h, 2)
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
        st.caption("이 데이터를 CSV 파일로 다운로드하여 엑셀이나 파이썬 판다스로 가져가 통계 분석 수업을 진행할 수 있습니다.")
        
        # CSV 다운로드 버튼
        csv = df_display.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 가상 데이터셋(.CSV) 다운로드",
            data=csv,
            file_name="water_rocket_experiment_data.csv",
            mime="text/csv"
        )

    # --- 기능 3: [신규 추가] 학생 주도 수학 탐구 활동 공간 ---
    st.divider()
    st.subheader("🧩 [학생 활동] 실험 데이터를 활용한 포물선 방정식 찾기")
    st.markdown("""
    위 테이블에서 **실험 번호 하나를 선택**하여 나만의 이차함수 모델을 완성해 보세요!
    * **가정**: 물로켓은 원점 $(0,0)$에서 발사되어 낙하하므로, 상수항 $c=0$인 $y = ax^2 + bx$ 형태를 가집니다.
    * **목표**: 주어진 **사거리(x절편)**와 **최고 높이(꼭짓점의 y좌표)**를 이용해 계수 $a$와 $b$를 구하고 그래프를 매칭하세요.
    """)

    # 1. 실험 번호 선택
    selected_num = st.selectbox("🎯 분석할 실험 번호를 선택하세요:", df_display["실험 번호"])
    student_row = df_display[df_display["실험 번호"] == selected_num].iloc[0]
    
    r_val = student_row["실제 측정 사거리 (m)"]
    h_val = student_row["실제 최고 높이 (m)"]
    
    # 힌트 및 정보 제공
    st.info(f"""
    📋 **선택한 실험의 단서**
    * **발사 및 착지점**: $(0,0)$ 및 $({r_val}, 0)$
    * **최고 도달 높이**: {h_val} m
    * *수학적 힌트*: 포물선은 대칭이므로 꼭짓점의 $x$좌표는 사거리의 절반인 $h = {r_val/2:.2f}$입니다. 즉, 꼭짓점 좌표는 $({r_val/2:.2f}, {h_val})$이 됩니다!
    """)

    # 2. 학생 입력 수식 칸
    st.markdown("### ✏️ 1단계: 방정식의 계수 $a, b$ 찾기")
    st.caption("꼭짓점 형식 $y = a(x-h)^2 + k$ 또는 인수분해 형식 $y = ax(x-R)$을 전개하여 $a$와 $b$를 구해보세요.")
    
    col_input_a, col_input_b = st.columns(2)
    with col_input_a:
        st_a = st.number_input("계수 a 입력 (주의: 위로 볼록하므로 음수입니다)", value=-0.1000, step=0.0001, format="%.4f")
    with col_input_b:
        st_b = st.number_input("계수 b 입력 (양수)", value=1.00, step=0.01, format="%.2f")

    # 3. 학생이 계산한 꼭짓점 입력 칸
    st.markdown("### ✏️ 2단계: 수식 기반 꼭짓점 직접 계산")
    st.caption("내가 정한 $a, b$ 값만을 이용하여 공식($x = -\\frac{b}{2a}$, $y = f(x)$)으로 도출되는 꼭짓점을 입력하세요.")
    
    col_v_x, col_v_y = st.columns(2)
    with col_v_x:
        st_vx = st.number_input("내가 계산한 꼭짓점 x좌표:", value=0.0, step=0.1)
    with col_v_y:
        st_vy = st.number_input("내가 계산한 꼭짓점 y좌표(최고높이):", value=0.0, step=0.1)

    # 4. 채점 및 시각화 버튼
    if st.button("🔍 나만의 함수 그래프 그리고 정답 검증하기"):
        
        # 실제 입력한 a, b 기반의 수학적 꼭짓점 정답 계산
        true_vx = -st_b / (2 * st_a) if st_a != 0 else 0
        true_vy = st_a * (true_vx**2) + st_b * true_vx
        
        # 정답 검증 (오차범위 0.2 이내 인정)
        is_vertex_correct = abs(st_vx - true_vx) < 0.2 and abs(st_vy - true_vy) < 0.2
        is_model_matching = abs(true_vy - h_val) < 0.3 and abs(true_vx - (r_val/2)) < 0.3
        
        # 결과 메시지 출력
        st.markdown("#### 📢 분석 결과 리포트")
        if is_vertex_correct:
            st.success(f"✅ **꼭짓점 계산 성공!** 입력하신 계수 $a, b$에 따른 이론적 꼭짓점 $({true_vx:.2f}, {true_vy:.2f})$을 정확하게 찾아내셨습니다.")
        else:
            st.error(f"❌ **꼭짓점 계산 오차 발생!** 입력한 계수 기반의 실제 꼭짓점은 $({true_vx:.2f}, {true_vy:.2f})$ 입니다. 계산 과정을 다시 점검해 보세요.")
            
        if is_model_matching:
            st.balloons()
            st.success("🎉 **완벽한 모델링!** 실제 물로켓의 실험 오차 데이터와 거의 일치하는 함수식을 찾아내셨습니다!")
        else:
            st.warning(f"💡 **모델 튜닝 필요**: 현재 함수 그래프의 최고 높이는 {true_vy:.2f}m로, 실제 실험 데이터의 최고 높이({h_val}m)와 차이가 있습니다. 계수 $a$를 조금 더 정밀하게 조절해 보세요.")

        # 학생이 만든 식 그래프로 시각화
        x_student = np.linspace(0, r_val * 1.1, 100)
        y_student = st_a * (x_student**2) + st_b * x_student
        y_student = np.clip(y_student, 0, None) # 0 이하 음수 방지
        
        fig_student = go.Figure()
        # 학생이 디자인한 포물선
        fig_student.add_trace(go.Scatter(x=x_student, y=y_student, mode='lines', name='내가 만든 수학 모델', line=dict(color='green', width=3)))
        # 실제 데이터 핵심 포인트 점으로 표시
        fig_student.add_trace(go.Scatter(x=[0, r_val], y=[0, 0], mode='markers', name='실제 발사/착지점', marker=dict(color='blue', size=12, symbol='x')))
        fig_student.add_trace(go.Scatter(x=[r_val/2], y=[h_val], mode='markers', name='실제 데이터 최고점', marker=dict(color='red', size=12, symbol='diamond')))
        # 학생이 입력한 꼭짓점 위치
        fig_student.add_trace(go.Scatter(x=[st_vx], y=[st_vy], mode='markers+text', name='내가 제출한 꼭짓점', text=["내 꼭짓점"], textposition="top center", marker=dict(color='orange', size=10)))

        fig_student.update_layout(
            title=f"실험 {selected_num}번 데이터 vs 내가 유도한 이차함수 그래프 비교",
            xaxis_title="수평 거리 (m)",
            yaxis_title="높이 (m)",
            yaxis=dict(range=[0, max(h_val * 1.5, 5)]),
            template="plotly_white"
        )
        st.plotly_chart(fig_student, use_container_width=True)
