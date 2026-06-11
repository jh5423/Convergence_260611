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

    # --- 기능 3: [업그레이드] 학생 주도 수학 탐구 활동 및 그래프 개형 비교 공간 ---
    st.divider()
    st.subheader("🧩 [학생 활동] 실험 데이터를 활용한 포물선 방정식 예측 및 모델링")
    st.markdown("""
    위 테이블에서 **실험 번호 하나를 선택**하여 나만의 수학 모델을 만들어보세요.
    계산에 치치지 않도록 우측의 **'보조 계산기'**를 활용하고, 수식을 풀기 전 **'직관적 개형'**을 먼저 조절해 보세요!
    """)

    # 1. 실험 번호 선택 및 데이터 추출
    selected_num = st.selectbox("🎯 분석할 실험 번호를 선택하세요:", df_display["실험 번호"])
    student_row = df_display[df_display["실험 번호"] == selected_num].iloc[0]
    
    r_val = student_row["실제 측정 사거리 (m)"]
    h_val = student_row["실제 최고 높이 (m)"]
    
    st.info(f"""
    📋 **선택한 실험의 타겟 단서**
    * **원점 및 낙하지점**: $(0,0)$ 및 $({r_val}, 0)$
    * **실제 최고 높이**: {h_val} m
    * *힌트*: 포물선은 대칭이므로, 이론적인 꼭짓점의 $x$좌표는 사거리의 절반인 **{r_val/2:.2f}** 근처가 됩니다!
    """)

    # 레이아웃 분할: 왼쪽(활동 영역) / 오른쪽(수학 보조 계산기)
    col_activity, col_calc = st.columns([1.8, 1.2])

    with col_activity:
        # 단계 A: 직관적 개형 예측 (연필 스케치 대용)
        st.markdown("### 🎨 1단계: 내 직관으로 그래프 개형 스케치하기")
        st.caption("수식을 계산하기 전, 아래 슬라이더를 움직여 파란색/빨간색 타겟 점을 통과할 것 같은 '상상 속 그래프 모양'을 눈으로 먼저 맞춰보세요.")
        
        sketch_r = st.slider("내가 예상하는 낙하 거리 설정:", min_value=0.0, max_value=float(r_val*1.5), value=float(r_val*0.8), step=0.1)
        sketch_h = st.slider("내가 예상하는 최고 높이 설정:", min_value=0.0, max_value=float(h_val*1.5), value=float(h_val*0.7), step=0.1)

        # 단계 B: 실제 계산 결과 입력
        st.markdown("### ✏️ 2단계: 수식 기반 계수 $a, b$ 및 꼭짓점 계산하기")
        st.caption("인수분해형 $y = ax(x-R)$ 또는 꼭짓점형 $y = a(x-h)^2 + k$를 전개하여 도출한 계수와 꼭짓점을 입력하세요.")
        
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            st_a = st.number_input("계수 a 입력 (예: -0.0512)", value=-0.1000, step=0.0001, format="%.4f")
            st_vx = st.number_input("계산된 꼭짓점 x좌표:", value=0.0, step=0.1)
        with col_in2:
            st_b = st.number_input("계수 b 입력 (예: 1.15)", value=1.00, step=0.01, format="%.2f")
            st_vy = st.number_input("계산된 꼭짓점 y좌표 (최고높이):", value=0.0, step=0.1)

    with col_calc:
        st.markdown("### 🧮 뚝딱 수학 보조 계산기")
        st.caption("연립방정식이나 꼭짓점 좌표를 풀 때 생기는 복잡한 소수점 계산을 도와줍니다. 수식을 입력하고 Enter를 누르세요.")
        
        calc_input = st.text_input("계산기 입력창 (예시: -4.35 / (10.2**2) 또는 12.4 / 2 )", value="")
        if calc_input:
            try:
                # 학생들이 자주 실수하는 기호 ^를 파이썬의 **로 치환
                safe_expr = calc_input.replace('^', '**')
                # 기본적인 사칙연산 및 숫자 기호만 허용 (보안 처리)
                if all(c in "0123456789+-*/.() \t*^" for c in calc_input):
                    calc_res = eval(safe_expr)
                    st.metric(label="💡 계산 결과값", value=f"{calc_res:.6f}")
                    st.code(f"입력한 식: {calc_input}  ->  결과: {calc_res}", language="text")
                else:
                    st.error("숫자, 사칙연산(+, -, *, /), 괄호, 제곱(**) 기호만 입력할 수 있습니다.")
            except Exception as e:
                st.error("수식에 오류가 있습니다. 형식을 다시 확인해 주세요.")
        
        st.markdown("""
        ---
        💡 **풀이 도우미 팁 (인수분해 형식 활용)**
        물로켓 함수는 $y = ax(x - R)$ 로 둘 수 있습니다.
        1. 이 식에 꼭짓점 좌표 $(R/2, H)$를 대입합니다.
        2. $H = a \\times \\frac{R}{2} \\times (-\\frac{R}{2}) = -a \\times \\frac{R^2}{4}$
        3. 따라서 $a = -\\frac{4H}{R^2}$ 가 됩니다. 
        4. 위 계산기에 `-4 * [최고높이] / ([사거리]**2)`를 입력하여 $a$를 쉽게 구해보세요!
        """)

    # 4. 채점 및 시각화 버튼 구역
    st.markdown("---")
    if st.button("🔍 내 예측 개형과 계산 수식 그래프 겹쳐서 비교하기"):
        
        # [데이터 1] 학생이 슬라이더로 맞춘 직관적 예측 개형 계산
        # y = a_g * x * (x - R_g) 형식에서 최고높이가 H_g가 되도록 계수 자동 매칭
        x_space = np.linspace(0, max(r_val, sketch_r) * 1.1, 120)
        if sketch_r > 0:
            a_sketch = -4 * sketch_h / (sketch_r ** 2)
            y_sketch = a_sketch * x_space * (x_space - sketch_r)
            y_sketch = np.clip(y_sketch, 0, None)
        else:
            y_sketch = np.zeros_like(x_space)

        # [데이터 2] 학생이 입력한 수식 기반 그래프 계산
        y_student = st_a * (x_space**2) + st_b * x_space
        y_student = np.clip(y_student, 0, None)
        
        # 수식 기반 실제 꼭짓점 계산 정답
        true_vx = -st_b / (2 * st_a) if st_a != 0 else 0
        true_vy = st_a * (true_vx**2) + st_b * true_vx
        
        # 결과 리포트 판정
        is_vertex_correct = abs(st_vx - true_vx) < 0.2 and abs(st_vy - true_vy) < 0.2
        is_model_matching = abs(true_vy - h_val) < 0.3 and abs(true_vx - (r_val/2)) < 0.3
        
        # 메시지 출력
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            if is_vertex_correct:
                st.success(f"✅ **꼭짓점 계산 성공!** 내가 적은 수식의 계산상 꼭짓점 $({true_vx:.2f}, {true_vy:.2f})$과 입력값이 일치합니다.")
            else:
                st.error(f"❌ **꼭짓점 계산 검증 실패**: 입력하신 $a, b$ 수식의 실제 꼭짓점은 $({true_vx:.2f}, {true_vy:.2f})$입니다. 공식을 다시 확인해보세요.")
        with col_res2:
            if is_model_matching:
                st.balloons()
                st.success("🎉 **실험 데이터 피팅 완료!** 실제 물로켓의 궤적을 완벽하게 대변하는 수식을 찾았습니다!")
            else:
                st.warning("💡 **모델 수정 필요**: 수식 그래프가 실제 실험 데이터 점(X, 다이아몬드)을 정확히 지나도록 계수 $a, b$를 정밀하게 조정해보세요.")

        # Plotly를 이용한 3중 그래프 시각화 (실제 점 vs 눈대중 예측 vs 수식 계산)
        fig_compare = go.Figure()
        
        # 1. 실제 데이터 핵심 포인트 (기준점)
        fig_compare.add_trace(go.Scatter(x=[0, r_val], y=[0, 0], mode='markers', name='실제 발사/착지점', marker=dict(color='blue', size=14, symbol='x')))
        fig_compare.add_trace(go.Scatter(x=[r_val/2], y=[h_val], mode='markers', name='실제 최고 높이점', marker=dict(color='red', size=14, symbol='diamond')))
        
        # 2. 1단계: 학생이 눈대중/직관으로 그린 예측 개형 (주황색 점선 - 연필 느낌)
        fig_compare.add_trace(go.Scatter(x=x_space, y=y_sketch, mode='lines', name='[1단계] 내 직관적 예측 개형', line=dict(color='orange', width=2.5, dash='dash')))
        
        # 3. 2단계: 학생이 계산해서 입력한 수학 모델 (녹색 실선)
        fig_compare.add_trace(go.Scatter(x=x_space, y=y_student, mode='lines', name='[2단계] 내 수식 계산 그래프', line=dict(color='green', width=3.5)))
        
        # 4. 학생이 제출한 꼭짓점 마커 위치
        fig_compare.add_trace(go.Scatter(x=[st_vx], y=[st_vy], mode='markers+text', name='내가 제출한 꼭짓점 위치', text=["제출 꼭짓점"], textposition="top center", marker=dict(color='purple', size=11, symbol='circle')))

        fig_compare.update_layout(
            title=f"실험 {selected_num}번: 직관적 개형 vs 계산 수식 모델 vs 실제 데이터 비교",
            xaxis_title="수평 거리 (m)",
            yaxis_title="높이 (m)",
            yaxis=dict(range=[0, max(h_val * 1.5, 6)]),
            xaxis=dict(range=[0, max(r_val * 1.2, 10)]),
            template="plotly_white",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        st.plotly_chart(fig_compare, use_container_width=True)
