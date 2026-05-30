    st.subheader("과목별 추천 공부 시간 그래프")

    fig, ax = plt.subplots(figsize=(8, 5))

    # 변경 포인트: 정렬된 데이터프레임(df)의 '색상' 컬럼을 리스트로 변환하여 color 인자에 그대로 주입합니다.
    ax.bar(
        df["과목"],
        df["추천 공부 시간(분)"],
        color=df["색상"].tolist()  # 정렬된 순서대로 색상 리스트가 적용됩니다.
    )

    ax.set_xlabel("과목")
    ax.set_ylabel("추천 공부 시간(분)")
    ax.set_title("과목별 추천 공부 시간")

    # 그래프 격자 추가 (시각적 개선)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig)
