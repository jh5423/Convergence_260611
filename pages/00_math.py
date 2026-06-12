import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 1. 웹 페이지 제목 및 기본 설정
st.set_page_config(page_title="물로켓 수학-데이터 융합 시뮬레이터", page_icon="🚀", layout="wide")

# =====================================================================
# 🎨 CSS 커스텀 스타일링 (웹앱 느낌의 세련된 UI 적용)
# =====================================================================
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif !important;
    }
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #f1f5f9;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        box-shadow: 2px 0 12px rgba(0,0,0,0.05);
        padding-top: 2rem;
    }
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
    .stSlider, .stNumberInput, .stTextInput, .stSelectbox {
        background-color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        margin-bottom: 8px;
    }
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
다양한 변인통제 실험 데이터를 바탕으로 수식을 도출하고 미래를 유추하는 수학·과학·데이터 분석 융합 교육 도구입니다.
""")

# 중력 가속도 상수 및 기본 각도 고정 안내 추가
G = 9.8
ANGLE = 45  

st.sidebar.header("🛠️ 기본 시뮬레이션 설정")
st.sidebar.info(f"💡 **현재 기본 발사 각도는 {ANGLE}°로 고정**되어 있습니다. 현실에서는 공기 저항과 낙하 특성으로 인해 이론값과 차이가 발생하며, 이는 하단의 심화 탐구 섹션에서 다룹니다.")
water_vol = st.sidebar.slider("물로켓 속 물의 양 (L)", min_value=0.10, max_value=0.70, value=0.40, step=0.05, format="%.2f")

if 'prev_traj' not in st.session_state:
    st.session_state['prev_traj'] = None  
if 'curr_params' not in st.session_state:
    st.session_state['curr_params'] = {'water_vol': water_vol, 'x': [], 'y': []}

# --- 기능 1: 기본 궤적 계산 ---
theoretical_r = 40 - 200 * ((water_vol - 0.4) ** 2)
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
        name=f"이전 궤적 ({prev['water_vol']:.2f}L)", 
        line=dict(color='#94a3b8', width=2, dash='dash'), opacity=0.6
    ))

fig.add_trace(go.Scatter(
    x=x_coords, y=y_coords, mode='lines', 
    name=f"현재 궤적 ({water_vol:.2f}L)", line=dict(color='#2563eb', width=4)
))

fig.update_layout(
    title=f"<b>공간 속 비행 궤적 비교</b> (발사각: {ANGLE}° 고정)",
    xaxis_title="<b>수평 거리 (m)</b>", yaxis_title="<b>높이 (m)</b>",
    yaxis=dict(range=[0, 15], gridcolor='#e2e8f0'), xaxis=dict(range=[0, 45], gridcolor='#e2e8f0'),
    template="plotly_white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#f8fafc',
    margin=dict(l=40, r=40, t=60, b=40),
    legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99, bgcolor="rgba(255,255,255,0.8)")
)

col1, col2 = st.columns([2.2, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader("📊 궤적 역학 지표")
    st.metric(label="🎯 최종 사거리 (R)", value=f"{max_range:.2f} m")
    st.metric(label="🔝 최고 도달 높이 (H)", value=f"{max_height:.2f} m")
    st.metric(label="⏱️ 총 비행 시간", value=f"{t_flight:.2f} 초")

st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

# --- 기능 2: 가상 데이터셋 생성 ---
st.subheader("📈 통계 분석용 실험 데이터셋 생성 (변인: 물의 양)")
st.write("발사각을 고정하고, **물의 양(0.10L ~ 0.70L)**을 변화시키며 반복 실험한 실제 측정 데이터를 수집합니다.")

if st.button("🎲 물의 양 기준 새로운 실험 데이터 생성하기"):
    water_volumes = np.repeat(np.arange(0.10, 0.71, 0.05), 5)
    results = []
    for idx, water in enumerate(water_volumes):
        theoretical_r = 40 - 200 * ((water - 0.4) ** 2)
        noise = np.random.normal(0, 1.5)
        actual_r = max(0, theoretical_r + noise)
        actual_h = max(0, (actual_r / 4) + np.random.normal(0, 0.4)) 
        
        results.append({
            "실험 번호": idx + 1,
            "물의 양 (L)": round(water, 2),
            "실제 측정 사거리 (m)": round(actual_r, 2),
            "실제 최고 높이 (m)": round(actual_h, 2)
        })
    st.session_state['rocket_data'] = pd.DataFrame(results)

if 'rocket_data' in st.session_state:
    df_display = st.session_state['rocket_data']
    
    col_df, col_down = st.columns([2.2, 1])
    with col_df:
        st.dataframe(df_display, use_container_width=True, height=200)
    with col_down:
        st.info("📂 **데이터 수집 완료**\n\n아래의 탐구 활동 및 심화 과정으로 이동하여 분석을 고도화하세요.")
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
    col_an1, col_an2 = st.columns([1.8, 1.2])
    with col_an1:
        st.markdown("##### ✏️ 1단계: 전체 데이터를 대표하는 회귀 모델 설계")
        w1, w2, w3 = st.columns(3)
        with w1: fit_h = st.number_input("최적 물의 양 (꼭짓점 h, L):", value=0.35, step=0.01, format="%.2f")
        with w2: fit_k = st.number_input("최대 사거리 (꼭짓점 k, m):", value=35.0, step=0.5)
        with w3: fit_a = st.number_input("방향/폭 계수 (a):", value=-100.0, step=1.0, format="%.1f")

        st.markdown("##### 🔮 2단계: 미지의 데이터 예측하기")
        predict_w = st.slider("예측해볼 미지의 물의 양 (L):", min_value=0.05, max_value=0.90, value=0.45, step=0.05, format="%.2f")
        student_pred_r = fit_a * ((predict_w - fit_h) ** 2) + fit_k

    with col_an2:
        st.markdown("##### 🎯 내 공식 예측 결과")
        st.markdown("<div style='background-color:#f8fafc; padding:10px; border-radius:8px; border:1px solid #e2e8f0; margin-bottom:15px; text-align:center;'>", unsafe_allow_html=True)
        st.markdown("**내가 완성한 이차함수 모델식**")
        st.latex(f"R = {fit_a:.1f}(W - {fit_h:.2f})^2 + {fit_k:g}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.metric(label=f"💡 {predict_w:.2f}L 입력 시 예측 거리", value=f"{student_pred_r:.2f} m")
        err = abs(fit_h - 0.4)
        if err < 0.03 and abs(fit_k - 40) < 2: st.success("🎯 완벽한 최적화 방정식을 찾았습니다.")
        elif err < 0.07: st.info("💡 정점의 위치를 조금 더 튜닝해보세요.")
        else: st.warning("⚠️ 실제 데이터 흐름과 차이가 큽니다.")

    w_axis = np.linspace(0.05, 0.85, 200)
    student_curve_r = fit_a * ((w_axis - fit_h) ** 2) + fit_k
    
    fig_a = go.Figure()
    fig_a.add_trace(go.Scatter(x=df_display["물의 양 (L)"], y=df_display["실제 측정 사거리 (m)"], mode='markers', name='실험 데이터', marker=dict(color='rgba(37, 99, 235, 0.5)', size=10)))
    fig_a.add_trace(go.Scatter(x=w_axis, y=student_curve_r, mode='lines', name='내 예측 방정식 선', line=dict(color='#ef4444', width=3)))
    fig_a.add_trace(go.Scatter(x=[predict_w], y=[student_pred_r], mode='markers+text', name='🎯 예측 지점', text=[f"{student_pred_r:.1f}m"], textposition="top center", marker=dict(color='#f59e0b', size=15, symbol='star')))
    fig_a.update_layout(title="<b>물의 양(통제 변인) vs 수평 사거리 관계 차트</b>", xaxis_title="<b>넣은 물의 양 (L)</b>", yaxis_title="<b>수평 사거리 (m)</b>", xaxis=dict(range=[0, 0.95], gridcolor='#e2e8f0'), yaxis=dict(range=[0, 55], gridcolor='#e2e8f0'), template="plotly_white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#f8fafc')
    st.plotly_chart(fig_a, use_container_width=True)

st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

# =====================================================================
# 🔥 [신규 추가] 심화 활동 3: 발사 각도 변형 실험 (공기저항 최적각 탐구)
# =====================================================================
st.subheader("🧪 [심화 탐구 3] 공기 저항 환경에서의 발사 각도(변수) vs 사거리 분석")
st.markdown("""
진짜 야외 환경에서는 **공기 저항 및 낙하 역학** 때문에 이론상 완벽한 $45^\circ$보다 **조금 더 낮은 각도**에서 최대 사거리가 관측되곤 합니다.
* **통제 변인**: 물의 양 $0.40\\text{L}$ 고정 
* **독립 변인**: 발사 각도 (도)
* **목표**: 각도에 따른 분포 데이터를 보고 실제 최대 사거리를 만드는 **현실적인 최적 발사각**을 유추해 보세요.
""")

if st.button("🎲 발사 각도 기준 새로운 심화 실험 데이터 생성하기"):
    # 15도부터 75도까지 5도 간격으로 3회씩 반복 실험 데이터 구성
    angle_tests = np.repeat(np.arange(15, 76, 5), 3)
    adv_results = []
    
    for idx, ang in enumerate(angle_tests):
        # 💡 공기 저항 모델 시뮬레이션: 꼭짓점이 40도일 때 최대 사거리 38m가 나오도록 유도
        # 수식: R = 38 - 0.035 * (angle - 40)^2
        theo_ang_r = 38 - 0.035 * ((ang - 40) ** 2)
        ang_noise = np.random.normal(0, 1.0)
        act_ang_r = max(0, theo_ang_r + ang_noise)
        
        adv_results.append({
            "실험 번호": idx + 1,
            "발사 각도 (도)": ang,
            "실제 측정 사거리 (m)": round(act_ang_r, 2)
        })
    st.session_state['angle_data'] = pd.DataFrame(adv_results)

if 'angle_data' in st.session_state:
    df_ang = st.session_state['angle_data']
    col_ang_l, col_ang_r = st.columns([1.8, 1.2])
    
    with col_ang_l:
        st.markdown("##### ✏️ 각도-사거리 이차함수 모델 설계 및 꼭짓점 도출")
        st.caption("아래 입력창에 수치를 대입해 점들을 감싸는 포물선 추세선 식 $R = a(\\theta - h)^2 + k$를 피팅하세요.")
        
        ang_h = st.number_input("데이터 기준 현실적인 최적 발사각(꼭짓점 h, 도):", value=45.0, step=1.0)
        ang_k = st.number_input("최대 도달 사거리 예측(꼭짓점 k, m):", value=35.0, step=0.5)
        ang_a = st.number_input("방향 및 폭 계수 (a):", value=-0.030, step=0.005, format="%.3f")
        
    with col_ang_r:
        st.markdown("##### 🎯 모델 분석 리포트")
        st.markdown("<div style='background-color:#f8fafc; padding:10px; border-radius:8px; border:1px solid #e2e8f0; margin-bottom:15px; text-align:center;'>", unsafe_allow_html=True)
        st.markdown("**현실 필드 각도 모델 방정식**")
        st.latex(f"R = {ang_a:.3f}(\\theta - {ang_h:g})^2 + {ang_k:g}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if abs(ang_h - 40) <= 2 and abs(ang_k - 38) <= 1.5:
            st.success(f"🎉 **탐구 대성공!** 공기 저항이 존재할 때의 최적 발사각이 약 **{ang_h:g}°** 부근이라는 과학적 사실을 수학적으로 완벽히 증명했습니다!")
        else:
            st.info("💡 45도 근처와 40도 근처 데이터의 미세한 사거리 차이를 비교하며 꼭짓점을 다시 조정해 보세요.")
            
    # 시각화
    a_axis = np.linspace(10, 80, 200)
    student_curve_ang = ang_a * ((a_axis - ang_h) ** 2) + ang_k
    
    fig_ang = go.Figure()
    fig_ang.add_trace(go.Scatter(x=df_ang["발사 각도 (도)"], y=df_ang["실제 측정 사거리 (m)"], mode='markers', name='각도 변형 실험 데이터', marker=dict(color='rgba(16, 185, 129, 0.6)', size=10)))
    fig_ang.add_trace(go.Scatter(x=a_axis, y=student_curve_ang, mode='lines', name='내가 유도한 각도 추세선', line=dict(color='purple', width=3)))
    fig_ang.update_layout(title="<b>발사 각도(독립 변인) vs 수평 사거리 분포 매칭</b>", xaxis_title="<b>발사 각도 (도)</b>", yaxis_title="<b>수평 사거리 (m)</b>", xaxis=dict(range=[5, 85], gridcolor='#e2e8f0'), yaxis=dict(range=[0, 50], gridcolor='#e2e8f0'), template="plotly_white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#f8fafc')
    st.plotly_chart(fig_ang, use_container_width=True)

st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

# =====================================================================
# 🔥 [신규 추가] 추추가 심화활동 4: 포물선 운동의 벡터(Vector) 표현
# =====================================================================
st.subheader("📐 [최상위 심화 탐구 4] 고등 수학 기하 연계: 포물선 운동의 벡터 성분 분해")
st.markdown("""
이차함수의 움직임은 시간에 따른 **수평 위치 성분 벡터($\\vec{x}$)와 수직 위치 성분 벡터($\\vec{y}$)**의 결합인 **'평면 벡터'**로 완벽하게 표현할 수 있습니다.
* 사이드바에 설정된 물의 양 기준 초기 속도($v_0 = {v0:.2f}\\text{ m/s}$, 발사각 $45^\\circ$)를 토대로 미분 및 벡터 성분을 실시간 추적합니다.
""").markdown(r"""
$$\text{위치 벡터 } \vec{r}(t) = \left( v_0 \cos\theta \cdot t \right)\hat{i} + \left( v_0 \sin\theta \cdot t - \frac{1}{2}gt^2 \right)\hat{j}$$
$$\text{속도 벡터 } \vec{v}(t) = \frac{d\vec{r}}{dt} = \left( v_0 \cos\theta \right)\hat{i} + \left( v_0 \sin\theta - gt \right)\hat{j}$$
""")

# 실시간 시간(t) 흐름 슬라이더 배치하여 벡터 변화 관찰
t_slider = st.slider("⏱️ 발사 후 시간 흐름에 따른 벡터 변화 추적 (초):", min_value=0.0, max_value=float(t_flight), value=float(t_flight*0.3), step=0.05, format="%.2f")

# 해당 시간에서의 물리 벡터 계산
vx_current = v0 * np.cos(rad)
vy_current = v0 * np.sin(rad) - G * t_slider
x_current = vx_current * t_slider
y_current = (v0 * np.sin(rad) * t_slider) - (0.5 * G * (t_slider**2))

v_quad1, v_quad2 = st.columns(2)
with v_quad1:
    st.markdown("##### 🧭 실시간 속도 벡터 기하 성분")
    st.latex(r"\vec{{v}}({:.2f}\text{{초}}) = {:.2f}\hat{{i}} + {:.2f}\hat{{j}}".format(t_slider, vx_current, vy_current))
with v_quad2:
    st.markdown("##### 📍 현재 위치 벡터 좌표")
    st.latex(r"\vec{{r}}({:.2f}\text{{초}}) = \left( {:.2f}, {:.2f} \right)".format(t_slider, x_current, y_current))

# 실시간 벡터 드로잉 그래프 구성
fig_vec = go.Figure()
# 1. 전체 비행 안착선 (기본 궤적)
fig_vec.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='lines', name='전체 이동 경로', line=dict(color='#cbd5e1', width=2)))
# 2. 현재 물로켓 위치 점
fig_vec.add_trace(go.Scatter(x=[x_current], y=[y_current], mode='markers', name='현재 로켓 위치', marker=dict(color='#2563eb', size=12)))

# 3. 💡 수평, 수직, 합성 속도 벡터 화살표(화살표 어노테이션 기법 기하 구현)
# 합성 벡터 화살표 (파란색)
fig_vec.add_annotation(x=x_current + vx_current*0.3, y=y_current + vy_current*0.3, ax=x_current, ay=y_current, xref="x", yref="y", axref="x", ayref="y", text="", showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=4, arrowcolor="#2563eb")
# 수평 벡터 화살표 (오렌지색 - 등속 운동 표현)
fig_vec.add_annotation(x=x_current + vx_current*0.3, y=y_current, ax=x_current, ay=y_current, xref="x", yref="y", axref="x", ayref="y", text="", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2.5, arrowcolor="#f59e0b")
# 수직 벡터 화살표 (빨간색 - 연직 투하 중력 가속도 변화 표현)
fig_vec.add_annotation(x=x_current, y=y_current + vy_current*0.3, ax=x_current, ay=y_current, xref="x", yref="y", axref="x", ayref="y", text="", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2.5, arrowcolor="#ef4444")

fig_vec.update_layout(
    title=f"<b>시간 $t = {t_slider:.2f}$초에서의 속도 벡터 분해 시각화</b> (🟨 수평등속성분, 🟥 수직가속성분, 🟦 합성속도벡터)",
    xaxis_title="수평 위치 (m)", yaxis_title="높이 (m)",
    yaxis=dict(range=[0, 15], gridcolor='#e2e8f0'), xaxis=dict(range=[0, 45], gridcolor='#e2e8f0'),
    template="plotly_white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#f8fafc', showlegend=False
)
st.plotly_chart(fig_vec, use_container_width=True)
st.caption("※ 슬라이더를 움직여보세요! 최고 높이(꼭짓점)에 도달했을 때 🟥 수직 속도 벡터 성분의 크기가 정확히 0이 되는 기하학적 대칭 원리를 시각적으로 관찰할 수 있습니다.")
