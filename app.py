import streamlit as st
import json
import os

# 카테고리 딕셔너리
categories = {
    "성우": "seongwoo",
    "음식": "food",
    "나라": "country"
}

# 세션 상태 초기화
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

st.set_page_config(page_title="맞추기 퀴즈", layout="centered")
st.title("🧠 사진 보고 맞추기 퀴즈!")

# 카테고리 선택
if st.session_state.selected_category is None:
    category_label = st.selectbox("카테고리를 선택하세요", list(categories.keys()))
    if st.button("시작하기"):
        st.session_state.selected_category = categories[category_label]
        st.session_state.current_index = 0
        st.session_state.show_result = False
        st.rerun()
else:
    category = st.session_state.selected_category
    data_path = f"data/{category}.json"

    if not os.path.exists(data_path):
        st.error(f"❌ 퀴즈 데이터 파일이 없습니다: {data_path}")
    else:
        with open(data_path, "r", encoding="utf-8") as f:
            quiz_data = json.load(f)

        questions = quiz_data
        if st.session_state.current_index >= len(questions):
            st.success("🎉 모든 문제를 풀었습니다!")
            if st.button("처음으로"):
                st.session_state.selected_category = None
                st.rerun()
        else:
            current_question = questions[st.session_state.current_index]
            image_url = f"https://raw.githubusercontent.com/seokjeong0906/fatcat/main/images/{category}/{current_question['image']}"
            st.image(image_url, caption="이 사진은 무엇일까요?", use_container_width=True)

            if not st.session_state.show_result:
                answer = st.text_input("정답을 입력하세요")
                if st.button("제출"):
                    st.session_state.show_result = True
                    st.session_state.user_answer = answer
                    st.rerun()
            else:
                user = st.session_state.user_answer.strip().lower()
                correct = current_question["answer"].strip().lower()

                if user == correct:
                    st.markdown("##### ✅ 정답!")
                else:
                    st.markdown("##### ❌ 땡!")

                st.markdown(f"**정답은: {current_question['answer']}**")

                if st.button("➡ 다음 문제"):
                    st.session_state.current_index += 1
                    st.session_state.show_result = False
                    st.rerun()
