import streamlit as st

# ========================================================
# 🎨 [색상 커스텀 구간] 원하시는 색상으로 변경하세요!
# ========================================================
PRIMARY_COLOR = "#FF4B4B"       # 포인트 색상 (버튼 배경, 결과 강조 색상)
BACKGROUND_COLOR = "#F8F9FA"    # 앱 전체 배경색
TEXT_COLOR = "#212529"          # 기본 글자 색상
CARD_BG_COLOR = "#FFFFFF"       # 결과 박스 배경색
BORDER_COLOR = "#DEE2E6"        # 테두리 선 색상

# 기존 앱의 모습을 유지하며 색상만 세련되게 변경하는 스타일 주입
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {BACKGROUND_COLOR} !important;
            color: {TEXT_COLOR} !important;
        }}
        /* 스트림릿 기본 버튼 색상 커스텀 */
        div.stButton > button:first-child {{
            background-color: {PRIMARY_COLOR} !important;
            color: white !important;
            border: none !important;
            border-radius: 6px;
        }}
        /* 결과 노출 박스 스타일 */
        .result-card {{
            background-color: {CARD_BG_COLOR};
            border: 1px solid {BORDER_COLOR};
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ========================================================
# ⚙️ [원본 기능 로직] 과목별 우선순위/난이도 시간 배분 (원래 기능 그대로)
# ========================================================

st.title("📚 StudyMate-Lite")
st.subheader("과목별 우선순위와 난이도에 따라 최적의 공부 시간을 배분해드립니다.")

# 1. 총 공부 시간 입력
total_time = st.number_input("오늘 총 공부할 시간(분)을 입력하세요", min_value=10, max_value=1440, value=180, step=10)

st.write("---")
st.write("### 📝 과목 정보 입력")

# 과목 수 설정 (기본 3개)
num_subjects = st.number_input("배분할 과목 수를 입력하세요", min_value=1, max_value=10, value=3, step=1)

subjects_data = []

# 각 과목별 정보 입력 받기
for i in range(int(num_subjects)):
    st.write(f"**과목 {i+1}**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        name = st.text_input(f"과목명", value=f"과목 {i+1}", key=f"name_{i}")
    with col2:
        priority = st.slider(f"우선순위 (1: 낮음 ~ 5: 높음)", min_value=1, max_value=5, value=3, key=f"priority_{i}")
    with col3:
        difficulty = st.slider(f"난이도 (1: 쉬움 ~ 5: 어려움)", min_value=1, max_value=5, value=3, key=f"diff_{i}")
        
    # 가중치 계산 (우선순위와 난이도를 곱하거나 더한 고유 로직 방식 반영)
    weight = priority * 0.6 + difficulty * 0.4
    subjects_data.append({"name": name, "weight": weight})

# 2. 시간 배분 계산 및 결과 출력
if st.button("📊 최적의 시간 배분 결과 보기"):
    st.write("---")
    st.write("### ⏱️ 과목별 추천 공부 시간")
    
    total_weight = sum(item["weight"] for item in subjects_data)
    
    if total_weight > 0:
        for item in subjects_data:
            # 가중치 비율에 따라 시간 분배
            allocated_minutes = round((item["weight"] / total_weight) * total_time)
            
            # 시간/분 변환 표시
            if allocated_minutes >= 60:
                hours = allocated_minutes // 60
                mins = allocated_minutes % 60
                time_str = f"{hours}시간 {mins}분" if mins > 0 else f"{hours}시간"
            else:
                time_str = f"{allocated_minutes}분"
                
            # 커스텀 스타일이 적용된 결과 카드 출력
            st.markdown(
                f"""
                <div class="result-card">
                    <span style="font-weight: bold; font-size: 18px;">{item['name']}</span> : 
                    <span style="color: {PRIMARY_COLOR}; font-weight: bold; font-size: 18px;">{time_str}</span>
                </div>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.error("가중치 계산 오류가 발생했습니다. 입력 값을 확인해주세요.")
