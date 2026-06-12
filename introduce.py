import streamlit as st

# 페이지 제목 및 탭 아이콘 설정
st.set_page_config(page_title="팀 수화물 소개", page_icon="🧪", layout="wide")

# =====================================================================
# 🎨 CSS 커스텀 스타일링 (math 페이지와 완벽히 일치하는 웹앱 UI)
# =====================================================================
st.markdown("""
<style>
    /* 기본 폰트 적용 (Pretendard) */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif !important;
    }
    
    /* 상단 기본 헤더 숨김 및 여백 조정 */
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* 앱 메인 배경색 (살짝 시원한 톤의 밝은 회색) */
    [data-testid="stAppViewContainer"] {
        background-color: #f1f5f9;
    }
    
    /* 주요 대제목 스타일 (강조된 파란색 밑줄) */
    h1 {
        color: #1e3a8a !important;
        font-weight: 800 !important;
        border-bottom: 3px solid #0ea5e9;
        padding-bottom: 10px;
        margin-bottom: 25px;
    }
    h2, h3, h4 {
        color: #334155 !important;
        font-weight: 700 !important;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    
    /* 본문 인용구(Blockquote) 스타일 커스텀 */
    blockquote {
        background-color: #e0f2fe !important;
        border-left: 5px solid #0ea5e9 !important;
        color: #0369a1 !important;
        padding: 15px 20px !important;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 500;
    }
    
    /* 둥근 테두리와 그림자가 들어간 흰색 카드 섹션 */
    .info-card {
        background-color: white;
        padding: 25px 30px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }
    
    /* 테이블 스타일 세련되게 변경 */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }
    th {
        background-color: #f8fafc;
        color: #1e3a8a;
        font-weight: 700;
        padding: 12px;
        border-bottom: 2px solid #cbd5e1;
    }
    td {
        padding: 12px;
        border-bottom: 1px solid #e2e8f0;
        color: #475569;
    }
</style>
""", unsafe_allow_html=True)
# =====================================================================

# 상단 대제목
st.title("🧪➗🧲 팀 수화물 (Suhwamul) 공간")

# 좌우 2단 레이아웃 분할로 깔끔한 대시보드 느낌 연출
col_left, col_right = st.columns([1.4, 1.6])

with col_left:
    # 카드 1: 팀 슬로건 및 의미
    st.markdown("""
    <div class="info-card">
        <h3>💡 팀명 정의</h3>
        <blockquote>
            <b>수</b>학, <b>화</b>학, <b>물</b>리가 서로 단단히 결합하여 새로운 가치를 만드는 융합 프로젝트 공간입니다.<br>
            화학의 '수화물(Hydrate)'처럼, 세 가지 학문의 정수를 모아 하나의 아름다운 결합체를 이룹니다.
        </blockquote>
    </div>
    """, unsafe_allow_html=True)
    
    # 카드 2: 팀원 정보 및 역할 배치
    st.markdown("""
    <div class="info-card">
        <h3>👥 융합 연구 팀원 소개</h3>
        <table>
            <thead>
                <tr>
                    <th style="text-align:center;">이름</th>
                    <th style="text-align:center;">역할</th>
                    <th style="text-align:center;">담당 분야</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="text-align:center;"><b>팀원1</b></td>
                    <td style="text-align:center;">팀장 / 개발</td>
                    <td>수학 모델링 및 메인 시스템 구현</td>
                </tr>
                <tr>
                    <td style="text-align:center;"><b>팀원2</b></td>
                    <td style="text-align:center;">팀원 / 리서치</td>
                    <td>화학 데이터 분석 및 실험 검증</td>
                </tr>
                <tr>
                    <td style="text-align:center;"><b>팀원3</b></td>
                    <td style="text-align:center;">팀원 / 시각화</td>
                    <td>물리 엔진 적용 및 대시보드 UI 디자인</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    # 카드 3: 귀여운 메인 비주얼 일러스트 구역
    st.markdown('<div class="info-card" style="text-align:center; padding: 20px;">', unsafe_allow_html=True)
    
    # 🧪 과학/실험실 느낌의 귀엽고 정제된 무료 플랫 일러스트 연동
    st.image(
        "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&q=80&w=600",
        caption="수학·화학·물리 데이터가 융합되는 랩실 비주얼",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 카드 4: 주요 프로젝트 안내 및 Tech Stack
    st.markdown("""
    <div class="info-card">
        <h3>📌 융합 프로젝트 핵심 연구</h3>
        <ul style="color: #475569; line-height: 1.7; padding-left: 20px;">
            <li><b>보일의 법칙 연계</b>: 기체의 압력과 부피 관계를 통한 초기 추진력 역학 해석</li>
            <li><b>이차함수 모델 수식화</b>: 실시간 실험 데이터(Noise)기반 통계 회귀분석 및 미래 데이터 예측</li>
            <li><b>평면 벡터 성분 분해</b>: 시간에 따른 수평·수직 속도 변화 기하학적 매칭</li>
        </ul>
        <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;">
        <span style="font-size: 13px; color: #94a3b8;"><b>Tech Stack:</b> Python, Streamlit, Plotly, GlowScript, NumPy, Pandas</span>
    </div>
    """, unsafe_allow_html=True)

# 하단 캡션 저작권 표기
st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 팀 수화물. Powered by 수학·화학·물리 융합 프로젝트.")
