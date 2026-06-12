import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 1. 웹 페이지 제목 및 기본 설정 (layout은 wide 유지)
st.set_page_config(page_title="물로켓 융합 시뮬레이터", page_icon="🚀", layout="wide")

# =====================================================================
# 🎨 CSS 커스텀 스타일링 (1번 링크와 유사한 웹앱 느낌의 세련된 UI 적용)
# =====================================================================
st.markdown("""
<style>
    /* 기본 폰트 적용 (Pretendard) */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif !important;
    }
    
    /* 상단 여백 최소화 및 기본 헤더 숨기기 */
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* 앱 메인 배경색 (살짝 시원한 톤의 밝은 회색) */
    [data-testid="stAppViewContainer"] {
        background-color: #f1f5f9;
    }
    
    /* 사이드바 디자인 (흰색 배경에 부드러운 그림자) */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        box-shadow: 2px 0 12px rgba(0,0,0,0.05);
        padding-top: 2rem;
    }
    
    /* 주요 제목 스타일 (강조된 밑줄) */
    h1 {
        color: #1e3a8a !important;
        font-weight: 800 !important;
        border-bottom: 3px solid #0ea5e9;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    h2, h3, h4, h5 {
        color: #334155 !important;
        font-weight: 700 !important;
    }
    
    /* 메트릭(수치 결과) 박스 디자인 - 카드형 UI */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 6px solid #0ea5e9;
        margin-bottom: 10px;
    }
    [data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 800 !important;
        font-size: 28px !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 16px !important;
        color: #64748b !important;
    }
    
    /* 버튼 입체적 디자인 (그라데이션 및 애니메이션) */
    div.stButton > button {
        background: linear-gradient(135deg, #0ea5e9, #2563eb);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(37, 99, 235, 0.4);
        color: white;
    }
    
    /* 알림창 디자인 부드럽게 */
    div[data-testid="stAlert"] {
        border-radius: 10px;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* 슬라이더 및 입력창 주변을 흰색 카드로 묶기 */
    .stSlider, .stNumberInput, .stTextInput, .stSelectbox {
        background-color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        margin-bottom: 8px;
    }
    
    /* 데이터프레임 테두리 둥글게 */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)
# =====================================================================

st.title("🚀 물로켓 비행 궤적 & 데이터 분석 시뮬레이터")
st.markdown("""
이 프로그램은 물로켓의 발사 조건에 따른 **이차함수 비행 궤적**을 시뮬레이션하고, 
**'물의 양(mL)'과 '수평 이동 거리(m)' 사이의 통계적 인과관계**를 분석하여 미래 데이터를 예측하는 수학·데이터 분석 융합 교육 도구입니다.
""")

# 중력 가속도 상수 및 각도 고정
G = 9.8
ANGLE = 45  

st.sidebar.header("🛠️ 궤적 시뮬레이션 컨트롤 패널")
st.sidebar.caption("실제 실험처럼 물의 양을 조절하여 날려보세요.")
water_vol = st.sidebar.slider("물로켓 속 물의 양 (mL)", min_value=100, max_value=700, value=400, step=10)

if 'prev_traj' not in st.session_state:
    st.session_state['prev_traj'] = None  
if 'curr_params' not in st.session_state:
    st.session_state['curr_params'] = {'water_vol': water_vol, 'x': [], 'y': []}

# --- 기능 1: 궤적 계산 ---
theoretical_r = 40 - 0.0002 * ((water_vol - 400) ** 2)
v0 = np.sqrt(theoretical_r * G)

rad = np.radians(ANGLE)
t_flight = (2 * v0 * np.sin(rad)) / G  
max_range = (v0**2 * np.sin(2 * rad)) / G  
max_height = (v0**2 * (np.sin(rad)**2)) / (2 * G)  

t_space = np.linspace(0, t_flight, 100)
x_coords = v0 * np.cos(rad) * t_space
y_coords = v0 * np.sin(rad) * t_space - 0.5 * G * t_space**2

if water_vol != st.session_state['curr_params']['water_vol']:
    st.session_state['prev_traj'] = st.session_state['curr_params'].copy()
    st.session_state['curr_params'] = {'water_vol': water_vol, 'x': x_coords, 'y': y_coords}
elif len(st.session_state['curr_params']['x']) == 0:
    st.session_state['curr_params'] = {'water_vol': water_vol, 'x': x_coords, 'y': y_coords}

fig = go.Figure()

if st.session_state['prev_traj'] is not None and len(st.session_state['prev_traj']['x']) > 0:
    prev = st.session_state['prev_traj']
    fig.add_trace(go.Scatter(
        x=prev['x'], y=prev['y'], mode='lines', 
        name=f"이전 궤적 ({prev['water_vol']}mL)", 
        line=dict(color='#94a3b8', width=2, dash='dash'), opacity=0.6
    ))

fig.add_trace(go.Scatter(
    x=x_coords, y=y_coords, mode='lines', 
    name=f"현재 궤적 ({water_vol}mL)", line=dict(color='#2563eb', width=4)
))

# Plotly 디자인도 앱 CSS에 맞게 모던하게 수정
fig.update_layout(
    title=f"<b>공간 속 비행 궤적 비교</b> (발사각: {ANGLE}° 고정)",
    xaxis_title="<b>수평 거리 (m)</b>", yaxis_title="<b>높이 (m)</b>",
    yaxis=dict(range=[0, 15], gridcolor='#e2e8f0'), 
    xaxis=dict(range=[0, 45], gridcolor='#e2e8f0'),
    template="plotly_white",
    paper_bgcolor='rgba(0,0,0,0)',  # 배경을 투명하게 하여 카드와 어울리게 함
    plot_bgcolor='#f8fafc',
    margin=dict(l=40, r=40, t=60, b=40),
    legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99, bgcolor="rgba(255,255,255,0.8)")
)

# 레이아웃 분할
col1, col2 = st.columns([2.2, 1])
with col1:
    # 캔버스 느낌을 주기 위해 그래프를 스타일된 컨테이너에 넣습니다.
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader("📊 궤적 역학 지표")
    st.metric(label="🎯 최종 사거리 (R)", value=f"{max_range:.2f} m")
    st.metric(label="🔝 최고 도달 높이 (H)", value=f"{max_height:.2f} m")
    st.metric(label="⏱️ 총 비행 시간", value=f"{t_flight:.2f} 초")

st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

# --- 기능 2: 가상 데이터셋 생성 ---
st.subheader("📈 통계 분석용 실험 데이터셋 생성")
st.write("발사각을 고정하고, **물의 양(100mL ~ 700mL)**을 변화시키며 반복 실험한 실제 측정 데이터를 수집합니다.")

if st.button("🎲 물의 양 기준 새로운 실험 데이터 생성하기"):
    water_volumes = np.repeat(np.arange(100, 701, 100), 5)
    results = []
    for idx, water in enumerate(water_volumes):
        theoretical_r = 40 - 0.0002 * ((water - 400) ** 2)
        noise = np.random.normal(0, 1.5)
        actual_r = max(0, theoretical_r + noise)
        actual_h = max(0, (actual_r / 4) + np.random.normal(0, 0.4)) 
        
        results.append({
            "실험 번호": idx + 1,
            "물의 양 (mL)": water,
            "실제 측정 사거리 (m)": round(actual_r, 2),
            "실제 최고 높이 (m)": round(actual_h, 2)
        })
    st.session_state['rocket_data'] = pd.DataFrame(results)

if 'rocket_data' in st.session_state:
    df_display = st.session_state['rocket_data']
    
    col_df, col_down = st.columns([2.2, 1])
    with col_df:
        st.dataframe(df_display, use_container_width=True, height=250)
    with col_down:
        st.info("📂 **데이터 수집 완료**\n\n생성된 데이터를 다운로드하여 외부 분석 도구에서 활용하거나 아래의 탐구 활동으로 넘어가세요.")
        csv = df_display.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 데이터셋(.CSV) 다운로드", data=csv,
            file_name="water_volume_experiment.csv", mime="text/csv"
        )

    st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)
    
    # --- 기능 3: 궤적 방정식 유도 ---
    st.subheader("🧩 [활동 1] 궤적 포물선 방정식 유도하기")
    
    selected_num = st.selectbox("🎯 분석할 비행 데이터를 고르세요:", df_display["실험 번호"])
    student_row = df_display[df_display["실험 번호"] == selected_num].iloc[0]
    
    r_val = student_row["실제 측정 사거리 (m)"]
    h_val = student_row["실제 최고 높이 (m)"]
    
    st.success(f"**실험 단서** ➡️ 원점(0,0), 낙하지점({r_val}, 0), 최고높이 {h_val}m")

    col_act, col_cal = st.columns([1.8, 1.2])
    with col_act:
        st.markdown("##### 🎨 1단계: 개형 스케치")
        sketch_r = st.slider("예상 낙하지점:", min_value=0.0, max_value=float(r_val*1.5), value=float(r_val*0.8), key="sk_r")
        sketch_h = st.slider("예상 최고높이:", min_value=0.0, max_value=float(h_val*1.5), value=float(h_val*0.7), key="sk_h")

        st.markdown("##### ✏️ 2단계: 수식 계수 입력 ($y = ax^2 + bx$)")
        c1, c2 = st.columns(2)
        with c1:
            st_a = st.number_input("계수 a:", value=-0.1000, step=0.0001, format="%.4f")
            st_vx = st.number_input("꼭짓점 x:", value=0.0, step=0.1)
        with c2:
            st_b = st.number_input("계수 b:", value=1.00, step=0.01, format="%.2f")
            st_vy = st.number_input("꼭짓점 y:", value=0.0, step=0.1)

    with col_cal:
        st.markdown("##### 🧮 수학 보조 계산기")
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
        fig_c.add_trace(go.Scatter(x=[0, r_val], y=[0, 0], mode='markers', name='실제 착지', marker=dict(color='#2563eb', size=12, symbol='x')))
        fig_c.add_trace(go.Scatter(x=[r_val/2], y=[h_val], mode='markers', name='실제 최고점', marker=dict(color='#ef4444', size=12, symbol='diamond')))
        fig_c.add_trace(go.Scatter(x=x_space, y=y_sk, mode='lines', name='내 스케치 개형', line=dict(color='#f59e0b', dash='dash')))
        fig_c.add_trace(go.Scatter(x=x_space, y=y_st, mode='lines', name='내 수식 그래프', line=dict(color='#10b981', width=3)))
        fig_c.update_layout(title="궤적 탐구 검증 뷰", template="plotly_white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#f8fafc')
        st.plotly_chart(fig_c, use_container_width=True)

    st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

    # --- 기능 4: 관계 분석 및 예측 ---
    st.subheader("📊 [활동 2] 물의 양 vs 사거리 분석 및 데이터 예측")
    st.write("실험 데이터의 정점(최적값)을 찾아 **꼭짓점 형식 $R = a(W - h)^2 + k$**를 도출하고, 미지의 물의 양에 대한 거리를 예측합니다.")

    col_an1, col_an2 = st.columns([1.8, 1.2])

    with col_an1:
        st.markdown("##### ✏️ 1단계: 전체 데이터를 대표하는 회귀 모델 설계")
        w1, w2, w3 = st.columns(3)
        with w1: fit_h = st.number_input("최적 물의 양 (꼭짓점 h):", value=350.0, step=10.0)
        with w2: fit_k = st.number_input("최대 사거리 (꼭짓점 k):", value=35.0, step=0.5)
        with w3: fit_a = st.number_input("방향/폭 계수 (a):", value=-0.00010, step=0.00001, format="%.5f")

        st.markdown("##### 🔮 2단계: 미지의 데이터 예측하기")
        predict_w = st.slider("예측해볼 미지의 물의 양 (mL):", min_value=50, max_value=900, value=450, step=10)
        student_pred_r = fit_a * ((predict_w - fit_h) ** 2) + fit_k

    with col_an2:
        st.markdown("##### 🎯 내 공식 예측 결과")
        st.metric(label=f"💡 {predict_w}mL 입력 시 예측 거리", value=f"{student_pred_r:.2f} m")
        
        err = abs(fit_h - 400)
        if err < 30 and abs(fit_k - 40) < 2:
            st.success("🎯 완벽합니다! 전체 실험 데이터를 대변하는 최적화 방정식을 찾았습니다.")
        elif err < 70:
            st.info("💡 경향성은 파악했으나 정점의 위치를 조금 더 튜닝해보세요.")
        else:
            st.warning("⚠️ 입력한 파라미터가 실제 흐름과 차이가 큽니다.")

    w_axis = np.linspace(50, 850, 200)
    student_curve_r = fit_a * ((w_axis - fit_h) ** 2) + fit_k
    
    fig_a = go.Figure()
    fig_a.add_trace(go.Scatter(
        x=df_display["물의 양 (mL)"], y=df_display["실제 측정 사거리 (m)"],
        mode='markers', name='실험 데이터 산점도',
        marker=dict(color='rgba(37, 99, 235, 0.5)', size=10)
    ))
    fig_a.add_trace(go.Scatter(
        x=w_axis, y=student_curve_r, mode='lines', name='내 예측 방정식 선', line=dict(color='#ef4444', width=3)
    ))
    fig_a.add_trace(go.Scatter(
        x=[predict_w], y=[student_pred_r], mode='markers+text', name='🎯 가상 예측 지점',
        text=[f"{student_pred_r:.1f}m"], textposition="top center", marker=dict(color='#f59e0b', size=15, symbol='star')
    ))

    fig_a.update_layout(
        title="<b>물의 양(통제 변인) vs 수평 사거리 관계 차트</b>",
        xaxis_title="<b>넣은 물의 양 (mL)</b>", yaxis_title="<b>수평 사거리 (m)</b>",
        xaxis=dict(range=[0, 950], gridcolor='#e2e8f0'), yaxis=dict(range=[0, 55], gridcolor='#e2e8f0'),
        template="plotly_white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#f8fafc',
        legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99, bgcolor="rgba(255,255,255,0.8)")
    )
    st.plotly_chart(fig_a, use_container_width=True)
