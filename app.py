import streamlit as st
import json
import os

st.set_page_config(page_title="맞추기 퀴즈", layout="centered")
st.title("🧠 사진 보고 맞추기 퀴즈!")

# 카테고리 한글로 표시
category_label = st.selectbox("카테고리를 선택하세요", ["성우"])
category = "seongwoo"  # 내부 파일명은 영어로 처리

# JSON 데이터 파일 경로
data_path = f"data/{category}.json"

# JSON 파일이 존재하는지 먼저 확인
if not os.path.exists(data_path):
    st.error(f"❌ 데이터 파일이 없습니다: {data_path}")
else:
    with open(data_path, "r", encoding="utf-8") as f:
        quiz_data = json.load(f)

    # 문제 선택 (첫 번째 문제 고정)
    question = quiz_data[0]
    image_path = os.path.join("images", category, question["image"])

    # 이미지 표시
    st.image(image_path, caption="이 사진은 누구일까요?", use_column_width=True)

    # 사용자 입력
    user_answer = st.text_input("정답을 입력하세요")

    # 제출 버튼
    if st.button("제출"):
        if user_answer.strip().lower() == question["answer"].lower():
            st.success("✅ 정답입니다!")
        else:
            st.error("❌ 오답입니다.")
