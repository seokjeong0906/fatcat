import streamlit as st
import json
import os
import datetime

# 카테고리와 배너 이미지 매핑
category_config = {
    "성우": {"key": "seongwoo", "image": "seongwoo.png"},
    "음식": {"key": "food", "image": "pizza.png"},
    "나라": {"key": "country", "image": "korea.png"}
}

# 상태 초기화
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""
if "score" not in st.session_state:
    st.session_state.score = 0
if "likes" not in st.session_state:
    st.session_state.likes = {}

st.set_page_config(page_title="퀴즈월드", layout="wide")

st.title("🎯 사진 보고 맞추기 퀴즈")

# 댓글 저장 및 로드
comment_file = "comments.json"
def load_comments():
    if os.path.exists(comment_file):
        with open(comment_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_comment(nickname, comment):
    all_comments = load_comments()
    all_comments.append({
        "nickname": nickname,
        "comment": comment,
        "timestamp": datetime.datetime.now().isoformat(),
        "likes": 0
    })
    with open(comment_file, "w", encoding="utf-8") as f:
        json.dump(all_comments, f, ensure_ascii=False, indent=2)

# ✅ 메인 페이지 (카테고리 선택 전)
if st.session_state.selected_category is None:
    st.subheader("카테고리를 선택하세요")
    cols = st.columns(len(category_config))

    for idx, (label, config) in enumerate(category_config.items()):
        with cols[idx]:
            st.image(f"https://raw.githubusercontent.com/seokjeong0906/fatcat/main/images/banner/{config['image']}", width=250)
            if st.button(label):
                st.session_state.selected_category = config["key"]
                st.session_state.current_index = 0
                st.session_state.show_result = False
                st.session_state.user_answer = ""
                st.session_state.score = 0
                st.rerun()

# ✅ 문제 풀이 화면
else:
    cat_key = st.session_state.selected_category
    data_path = f"data/{cat_key}.json"

    if not os.path.exists(data_path):
        st.error(f"❌ 데이터 파일이 없습니다: {data_path}")
    else:
        with open(data_path, "r", encoding="utf-8") as f:
            quiz_data = json.load(f)

        index = st.session_state.current_index

        if index >= len(quiz_data):
            total = len(quiz_data)
            correct = st.session_state.score
            rate = round((correct / total) * 100)

            st.success(f"🎉 모든 문제 완료!")
            st.markdown(f"**총 {total}문제 중 {correct}문제 정답!**")
            st.markdown(f"**정답률: {rate}%**")

            st.markdown("---")
            st.markdown("💬 **퀴즈 어땠나요? 한마디 남겨주세요!**")
            nickname = st.text_input("닉네임 입력", key="nickname_input")
            comment = st.text_input("댓글 입력", key="comment_input")
            if st.button("댓글 남기기"):
                if nickname.strip() and comment.strip():
                    save_comment(nickname.strip(), comment.strip())
                    st.success("댓글이 등록되었습니다!")
                    st.rerun()

            # 댓글 리스트 출력
            all_comments = load_comments()
            if all_comments:
                st.markdown("#### 📣 댓글 모음")
                for i, c in enumerate(reversed(all_comments)):
                    col1, col2 = st.columns([8, 1])
                    with col1:
                        st.markdown(f"**{c['nickname']}**: {c['comment']}")
                    with col2:
                        if st.button("👍", key=f"like_{i}"):
                            c['likes'] += 1
                            with open(comment_file, "w", encoding="utf-8") as f:
                                json.dump(all_comments, f, ensure_ascii=False, indent=2)
                            st.rerun()
                        st.write(c['likes'])

            st.markdown("---")
            if st.button("🏠 메인으로"):
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()

        else:
            question = quiz_data[index]
            image_url = f"https://raw.githubusercontent.com/seokjeong0906/fatcat/main/images/{cat_key}/{question['image']}"

            # 문제 이미지 (25% 정도 크기로)
            st.image(image_url, caption="누구일까요?", width=250)

            if not st.session_state.show_result:
                answer = st.text_input("정답을 입력하세요", key=f"input_{index}")
                if st.button("제출", key=f"submit_{index}"):
                    st.session_state.user_answer = answer.strip().lower()
                    st.session_state.show_result = True
                    correct = question["answer"].strip().lower()
                    if st.session_state.user_answer == correct:
                        st.session_state.score += 1
                    st.rerun()
            else:
                correct_answer = question["answer"]
                is_correct = st.session_state.user_answer == correct_answer.strip().lower()

                st.markdown(f"#### {'✅ 정답!' if is_correct else '❌ 땡!'}")
                st.markdown(f"**정답은: {correct_answer}**")

                if st.button("➡ 다음 문제"):
                    st.session_state.current_index += 1
                    st.session_state.show_result = False
                    st.rerun()
