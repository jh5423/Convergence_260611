import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 1. 웹 페이지 제목 및 소개
st.set_page_config(page_title="물로켓 수학-데이터 융합 시뮬레이터", layout="wide")
st.title("🚀 물로켓 포물선 궤적 및 물의 양 변인통제 데이터 분석기")
st.markdown("""
이 프로그램은 물로켓의 발사 조건에 따른 **이차함수 비행 궤적**을 시뮬레이션하고, 
**'물의 양(mL)'과 '수평 이동 거리(m)' 사이의 통계적 인과관계**를 분석하여 미래 데이터를 예측하는 수학·데이터 분석 융합 교육 도구입니다.
""")

# 중력 가속도 상수 (m/s^2)
G = 9.8

# 사이드바: 시뮬레이션 변수 제어
st.sidebar.header("🛠️ 궤적 시뮬레이션 설정")
angle = st.sidebar.slider("발사 각도 (도)", min_value=10, max_value=80, value=45, step=5)
v0 = st.sidebar.slider("초기 발사 속도 (m/s)", min_value=5, max_value=30, value=15, step=1)

# --- 상태 저장소 초기화 (이전 그래프 잔상 효과를 위함) ---
if 'prev_traj' not in st.session_state:
    st.session_state['prev_traj'] = None  # 이전 궤적 데이터
if 'curr_params' not in st.session_state:
    st.session_state['curr_params'] = {'angle': angle, 'v0': v0, 'x': [], 'y': []}

# --- 기능 1: 포물선 궤적 계산 및 시각화 ---
rad = np.radians(angle)
t_flight = (2 * v0 * np.sin(rad)) / G  # 총 체공 시간
max_range = (v0**2 * np.sin(2 * rad)) / G  # 이론상 최대 사거리
max_height = (v0**2 * (np.sin(rad)**2)) / (2 * G)  # 이론상 최고 높이

t_space = np.linspace(0, t_flight, 100)
x_coords = v0 * np.cos(rad) * t_space
y_coords = v0 * np.sin(rad) * t_space - 0.5 * G * t_space**2

if angle != st.session_state['curr_params']['angle'] or v0 != st.session_state['curr_params']['v0']:
    st.session_state['prev_traj'] = st.session_state['curr_params'].copy()
    st.session_state['curr_params'] = {'angle': angle, 'v0': v0, 'x': x_coords, 'y': y_coords}
elif len(st.session_state['curr_params']['x']) == 0:
    st.session_state['curr_params'] = {'angle': angle, 'v0': v0, 'x': x_coords, 'y': y_coords}

fig = go.Figure()

# 잔상 그래프
if st.session_state['prev_traj'] is not None and len(st.session_state['prev_traj']['x']) > 0:
    prev = st.session_state['prev_traj']
    fig.add_trace(go.Scatter(
        x=prev['x'], y=prev['y'], mode='lines', 
        name=f"이전 궤적 (각도: {prev['angle']}°, 속도: {prev['v0']}m/s)", 
        line=dict(color='gray', width=2, dash='dash'), opacity=0.5
    ))

# 현재 그래프
fig.add_trace(go.Scatter(
    x=x_coords, y=y_coords, mode='lines', 
    name=f"현재 궤적 (각도: {angle}°, 속도: {v0}m/s)", line=dict(color='blue', width=4)
))

fig.update_layout(
    title="물로켓 비행 궤적 비교 (공간 속 포물선)",
    xaxis_title="수평 거리 (m)", yaxis_title="높이 (m)",
    yaxis=dict(range=[0, 50]), xaxis=dict(range=[0, 100]),
    template="plotly_white", legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
)

col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader("📊 궤적 수학 분석 결과")
    st.metric(label="🎯 최종 사거리 (R)", value=f"{max_range:.2f} m")
    st.metric(label="🔝 최고 도달 높이 (H)", value=f"{max_height:.2f} m")
    st.metric(label="⏱️ 총 비행 시간", value=f"{t_flight:.2f} 초")

st.divider()

# --- 기능 2: [수정] 물의 양에 따른 가상 실험 데이터셋 생성 ---
st.subheader("📈 통계 분석용 가상 실험 데이터셋 생성 (변인: 물의 양)")
st.write("발사각(45°)과 공기압을 고정하고, **물의 양(100mL ~ 700mL)**을 변화시키며 반복 실험했을 때의 실제 측정 데이터를 생성합니다.")
st.caption("※ 물리적으로 물의 양이 너무 적으면 추진력이 부족하고, 너무 많으면 로켓이 무거워져 사거리는 '특정 부피'에서 극대화되는 이차함수 관계를 가집니다.")

if st.button("🎲 물의 양 기준 새로운 실험 데이터 생성하기"):
    # 100mL부터 700mL까지 100mL 간격으로 각 5회씩 반복 (총 35회 실험)
    water_volumes = np.repeat(np.arange(100, 701, 100), 5)
    
    results = []
    for idx, water in enumerate(water_volumes):
        # 이론적 배경 모델 설정: 최적의 물의 양은 400mL일 때 사거리 40m 정점 유도
        # 수식: Range = 40 - 0.0002 * (water - 400)^2
        theoretical_r = 40 - 0.0002 * ((water - 400) ** 2)
        
        # 현실적인 환경 오차 노이즈 반영
        noise = np.random.normal(0, 1.5)
        actual_r = max(0, theoretical_r + noise)
        
        # 45도 발사이므로 최고 높이는 대략 사거리의 1/4 수준 형성
        actual_h = max(0, (actual_r / 4) + np.random.normal(0, 0.4))
        
        results.append({
            "실험 번호": idx + 1,
            "물의 양 (mL)": water,
            "실제 측정 사거리 (m)": round(actual_r, 2),
            "실제 최고 높이 (m)": round(actual_h, 2)
        })
        
    df = pd.DataFrame(results)
    st.session_state['rocket_data'] = df

# 데이터가 존재할 경우 출력
if 'rocket_data' in st.session_state:
    df_display = st.session_state['rocket_data']
    
    col_df, col_down = st.columns([2, 1])
    with col_df:
        st.dataframe(df_display, use_container_width=True)
    with col_down:
        st.write("📂 **데이터 수집 완료**")
        st.caption("생성된 데이터를 다운로드하여 외부 분석 도구에서 활용하거나, 아래 준비된 학생 탐구 활동 섹션으로 이동하여 분석을 이어가세요.")
        csv = df_display.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 가상 데이터셋(.CSV) 다운로드", data=csv,
            file_name="water_volume_experiment_data.csv", mime="text/csv"
        )

    # --- 기능 3: 학생 주도 수학 탐구 활동 공간 (궤적 방정식) ---
    st.divider()
    st.subheader("🧩 [활동 1] 비행 데이터 한 개를 골라 포물선 궤적 방정식 유도하기")
    
    selected_num = st.selectbox("🎯 분석할 실험 번호를 고르세요:", df_display["실험 번호"])
    student_row = df_display[df_display["실험 번호"] == selected_num].iloc[0]
    
    r_val = student_row["실제 측정 사거리 (m)"]
    h_val = student_row["실제 최고 높이 (m)"]
    w_val = student_row["물의 양 (mL)"]
    
    st.info(f"선택한 {selected_num}번 실험 단서 (물의 양: {w_val}mL) ➡️ 원점(0,0), Landing점({r_val}, 0), 최고높이 {h_val}m")

    col_activity, col_calc = st.columns([1.8, 1.2])
    with col_activity:
        st.markdown("##### 🎨 1단계: 눈대중으로 개형 스케치하기")
        sketch_r = st.slider("예상 낙하지점:", min_value=0.0, max_value=float(r_val*1.5), value=float(r_val*0.8), key="sk_r")
        sketch_h = st.slider("예상 최고높이:", min_value=0.0, max_value=float(h_val*1.5), value=float(h_val*0.7), key="sk_h")

        st.markdown("##### ✏️ 2단계: 수식 계산값 입력 ($y = ax^2 + bx$)")
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            st_a = st.number_input("계수 a:", value=-0.1000, step=0.0001, format="%.4f")
            st_vx = st.number_input("꼭짓점 x:", value=0.0, step=0.1)
        with c_col2:
            st_b = st.number_input("계수 b:", value=1.00, step=0.01, format="%.2f")
            st_vy = st.number_input("꼭짓점 y:", value=0.0, step=0.1)

    with col_calc:
        st.markdown("##### 🧮 뚝딱 보조 계산기")
        calc_input = st.text_input("수식 입력창 (예: -4 * 8.5 / (34.2**2))", value="", key="calc1")
        if calc_input:
            try:
                safe_expr = calc_input.replace('^', '**')
                if all(c in "0123456789+-*/.() \t*^" for c in calc_input):
                    st.metric(label="계산 결과", value=f"{eval(safe_expr):.6f}")
                else: st.error("허용되지 않은 문자 포함")
            except: st.error("식 오류")

    if st.button("🔍 궤적 그래프 매칭 확인하기"):
        x_space = np.linspace(0, max(r_val, sketch_r) * 1.1, 100)
        a_sk = -4 * sketch_h / (sketch_r ** 2) if sketch_r > 0 else 0
        y_sk = np.clip(a_sk * x_space * (x_space - sketch_r), 0, None)
        y_st = np.clip(st_a * (x_space**2) + st_b * x_space, 0, None)
        
        fig_c = go.Figure()
        fig_c.add_trace(go.Scatter(x=[0, r_val], y=[0, 0], mode='markers', name='실제 착지', marker=dict(color='blue', size=12, symbol='x')))
        fig_c.add_trace(go.Scatter(x=[r_val/2], y=[h_val], mode='markers', name='실제 최고점', marker=dict(color='red', size=12, symbol='diamond')))
        fig_c.add_trace(go.Scatter(x=x_space, y=y_sk, mode='lines', name='내 예측 개형', line=dict(color='orange', dash='dash')))
        fig_c.add_trace(go.Scatter(x=x_space, y=y_st, mode='lines', name='내 수식 그래프', line=dict(color='green', width=3)))
        fig_c.update_layout(title="궤적 탐구 검증 선형 뷰", template="plotly_white")
        st.plotly_chart(fig_c, use_container_width=True)

    # --- 기능 4: [신규 추가] 물의 양 vs 사거리 관계 분석 및 데이터 분석 공간 ---
    st.divider()
    st.subheader("📊 [활동 2] 데이터 분석: 물의 양에 따른 사거리 방정식 도출 및 미래 예측")
    st.markdown("""
    이번에는 공간 속 비행선이 아니라, **전체 실험 데이터 분산 차트**를 보고 학습합니다.
    * **X축**: 물의 양 (mL) / **Y축**: 실제 측정 사거리 (m)
    * **목표**: 데이터 분포의 정점(최적값)을 찾아 **꼭짓점 형식의 이차함수 식 $R = a(W - h)^2 + k$**를 도출하고, 미지의 물의 양에 대한 거리를 예측하세요.
    """)

    col_an_left, col_an_right = st.columns([1.8, 1.2])

    with col_an_left:
        st.markdown("##### ✏️ 1단계: 전체 데이터 경향성을 대표하는 모델 설계")
        st.caption("산점도의 정점(꼭짓점) 위치를 유추하여 표준/꼭짓점 형태의 파라미터를 입력하세요.")
        
        col_w1, col_w2, col_w3 = st.columns(3)
        with col_w1:
            fit_h = st.number_input("최적의 물의 양 예측 (꼭짓점 h, mL):", value=350.0, step=10.0)
        with col_w2:
            fit_k = st.number_input("최대 사거리 예측 (꼭짓점 k, m):", value=35.0, step=0.5)
        with col_w3:
            fit_a = st.number_input("그래프의 폭과 방향 결정 (계수 a):", value=-0.00010, step=0.00001, format="%.5f")

        st.markdown("##### 🔮 2단계: 유도한 방정식을 바탕으로 미래 데이터 예측하기")
        st.caption("만약 우리가 실험하지 않은 양의 물을 넣는다면 얼마만큼 날아갈까요? 내가 만든 식으로 시뮬레이션해 봅니다.")
        predict_w = st.slider("예측해보고 싶은 미지의 물의 양 선택 (mL):", min_value=50, max_value=900, value=450, step=10)
        
        # 학생 공식 기반 예측 계산
        student_pred_r = fit_a * ((predict_w - fit_h) ** 2) + fit_k
        # 실제 내부 시뮬레이션 참값 이론값 계산 비교용
        true_pred_r = max(0, 40 - 0.0002 * ((predict_w - 400) ** 2))

    with col_an_right:
        st.markdown("##### 🎯 내 수학 모델 기반 예측 리포트")
        st.metric(label=f"💡 물 {predict_w}mL 입력 시 내가 예측한 수평 이동 거리", value=f"{student_pred_r:.2f} m")
        
        # 모델 적합도 체크 피드백
        error_at_optimal = abs(fit_h - 400)
        if error_at_optimal < 30 and abs(fit_k - 40) < 2:
            st.success("🎯 대단합니다! 전체 실험 데이터를 완벽하게 대변하는 최적화 방정식을 찾아내셨습니다.")
        elif error_at_optimal < 70:
            st.info("💡 데이터 경향성은 파악했으나 정점의 위치를 조금 더 세밀하게 튜닝할 수 있습니다. 그래프를 다시 보며 수정해 보세요.")
        else:
            st.warning("⚠️ 입력한 파라미터가 데이터의 실제 흐름과 차이가 큽니다. 슬라이더나 수치를 변경해 보세요.")

    # 분석 시각화 플로팅
    w_axis = np.linspace(50, 850, 200)
    student_curve_r = fit_a * ((w_axis - fit_h) ** 2) + fit_k
    
    fig_analysis = go.Figure()
    # 1. 실제 실험 데이터 전체 산점도 표시
    fig_analysis.add_trace(go.Scatter(
        x=df_display["물의 양 (mL)"], y=df_display["실제 측정 사거리 (m)"],
        mode='markers', name='실제 수집된 실험 데이터들',
        marker=dict(color='rgba(30, 58, 138, 0.6)', size=9, symbol='circle')
    ))
    # 2. 학생이 유도한 예측 곡선 표시
    fig_analysis.add_trace(go.Scatter(
        x=w_axis, y=student_curve_r,
        mode='lines', name='내가 유도한 추세 예측 방정식',
        line=dict(color='crimson', width=3)
    ))
    # 3. 예측하겠다고 지정한 가상의 포인트 표시
    fig_analysis.add_trace(go.Scatter(
        x=[predict_w], y=[student_pred_r],
        mode='markers+text', name='🎯 내 공식 기반 예측 지점',
        text=[f"{student_pred_r:.1f}m 예측"], textposition="top center",
        marker=dict(color='gold', size=14, symbol='star')
    ))

    fig_analysis.update_layout(
        title="📊 물의 양(통제 변인) vs 물로켓 사거리 분석 회귀선 매칭 차트",
        xaxis_title="넣은 물의 양 (mL)", yaxis_title="수평 사거리 (m)",
        xaxis=dict(range=[0, 950]), yaxis=dict(range=[0, 55]),
        template="plotly_white", legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99)
    )
    st.plotly_chart(fig_analysis, use_container_width=True)
