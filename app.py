import streamlit as st
import datetime
import time

# ========================================================
# 🎨 [색상 커스텀 구간] 원하는 색상의 헥스코드로 변경하세요!
# ========================================================
PRIMARY_COLOR = "#FF4B4B"       # 포인트 색상 (타이머 글자, 추가 버튼 등)
BACKGROUND_COLOR = "#F8F9FA"    # 메인 화면 배경색 (연한 회색/흰색 톤)
CARD_BG_COLOR = "#FFFFFF"       # 과목 카드의 배경색 (하얀색 상자)
TEXT_COLOR = "#212529"          # 기본 글자 색상
BORDER_COLOR = "#DEE2E6"        # 테두리 선 색상

# CSS 스타일 주입 (기존 기능과 모습을 유지하며 색상만 강제 지정)
st.markdown(
    f"""
    <style>
        /* 메인 화면 배경색 및 글자색 */
        .stApp {{
            background-color: {BACKGROUND_COLOR} !important;
            color: {TEXT_COLOR} !important;
        }}
        
        /* 스톱워치/타이머 강조 글자 색상 */
        .big-font {{
            font-size: 50px !important;
            font-weight: bold !important;
            color: {PRIMARY_COLOR} !important;
            text-align: center;
            margin-bottom: 20px;
        }}
        
        /* 과목 박스(카드) 테두리 및 배경색 */
        .subject-card {{
            background-color: {CARD_BG_COLOR};
            border: 1px solid {BORDER_COLOR};
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
        }}
        
        /* 입력창 및 기본 위젯 글자색 고정 */
        .stTextInput input {{
            color: {TEXT_COLOR} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ========================================================
# ⚙️ [앱 기능 로직] 기존 StudyMate Lite의 핵심 기능 그대로 유지
# ========================================================

st.title("📚 StudyMate Lite")
st.subheader("오늘의 공부 시간을 기록하고 관리해보세요!")

# 세션 상태(Session State) 초기화 (과목 및 타이머 정보 저장)
if "subjects" not in st.session_state:
    st.session_state.subjects = {"국어": 0, "수학": 0, "영어": 0}
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "current_subject" not in st.session_state:
    st.session_state.current_subject = "국어"

# ---- 1. 과목 추가 기능 ----
st.write("### ➕ 새로운 과목 추가")
col1, col2 = st.columns([3, 1])
with col1:
    new_subject = st.text_input("추가할 과목 이름을 입력하세요", placeholder="예: 과학, 한국사", label_visibility="collapsed")
with col2:
    if st.button("과목 추가", use_container_width=True):
        if new_subject.strip() and new_subject not in st.session_state.subjects:
            st.session_state.subjects[new_subject.strip()] = 0
            st.success(f"'{new_subject}' 과목이 추가되었습니다!")
            time.sleep(0.5)
            st.rerun()

# ---- 2. 공부 타이머 기능 ----
st.write("### ⏱️ 공부 타이머")
selected_subject = st.selectbox("현재 공부할 과목을 선택하세요", list(st.session_state.subjects.keys()))

# 타이머 상태 변화 계산
if st.session_state.timer_running:
    elapsed = int(time.time() - st.session_state.start_time)
    current_time_str = str(datetime.timedelta(seconds=elapsed))
else:
    current_time_str = "0:00:00"

# 화면에 타이머 표시 (위에서 설정한 포인트 색상 적용)
st.markdown(f'<div class="big-font">{current_time_str}</div>', unsafe_allow_html=True)

t_col1, t_col2 = st.columns(2)
with t_col1:
    if not st.session_state.timer_running:
        if st.button("🚀 공부 시작", type="primary", use_container_width=True):
            st.session_state.timer_running = True
            st.session_state.start_time = time.time()
            st.session_state.current_subject = selected_subject
            st.rerun()
    else:
        st.button("🚀 공부 중...", disabled=True, use_container_width=True)

with t_col2:
    if st.session_state.timer_running:
        if st.button("🛑 공부 종료 (기록)", use_container_width=True):
            total_elapsed = int(time.time() - st.session_state.start_time)
            st.session_state.subjects[st.session_state.current_subject] += total_elapsed
            st.session_state.timer_running = False
            st.session_state.start_time = None
            st.success(f"{st.session_state.current_subject} 공부 시간이 {datetime.timedelta(seconds=total_elapsed)} 만큼 추가되었습니다!")
            time.sleep(1)
            st.rerun()
    else:
        st.button("🛑 대기 중", disabled=True, use_container_width=True)

# 실시간 타이머 작동용 화면 갱신 트리거
if st.session_state.timer_running:
    time.sleep(1)
    st.rerun()

# ---- 3. 학습 결과 및 누적 시간 현황 ----
st.write("### 📊 오늘 과목별 학습 현황")

total_study_time = sum(st.session_state.subjects.values())

for subj, secs in st.session_state.subjects.items():
    time_formatted = str(datetime.timedelta(seconds=secs))
    st.markdown(
        f"""
        <div class="subject-card">
            <span style="font-weight: bold; font-size: 16px;">{subj}</span> : 
            <span style="color: {PRIMARY_COLOR}; font-weight: bold;">{time_formatted}</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

st.write(f"**총 누적 공부 시간:** {str(datetime.timedelta(seconds=total_study_time))}")

# ---- 4. 데이터 초기화 기능 ----
st.write("---")
if st.button("♻️ 전체 기록 초기화", help="모든 과목의 공부 시간 기록을 0으로 되돌립니다."):
    st.session_state.subjects = {"국어": 0, "수학": 0, "영어": 0}
    st.session_state.timer_running = False
    st.session_state.start_time = None
    st.toast("모든 기록이 초기화되었습니다.")
    time.sleep(0.5)
    st.rerun()
