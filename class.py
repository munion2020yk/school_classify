import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 1. 시도 횟수를 기억하는 세션 상태 초기화 및 증가 함수
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

def add_attempt():
    st.session_state.attempts += 1

st.set_page_config(page_title="수동 AI: 분류 모델", layout="centered")
st.title("수동 인공지능: 두 그룹 분류하기")

# 시도 횟수 화면 출력
st.markdown(f"### 🔄 현재 시도 횟수: **{st.session_state.attempts}회**")
st.write("직선의 방정식 $y = ax + b$의 기울기(a)와 y절편(b)을 조절하여 파란색 점과 빨간색 점을 완벽히 나누는 선을 찾아보세요!")

# 2. 사용자 입력 (슬라이더 조작 시 add_attempt 함수 실행)
col1, col2 = st.columns(2)
with col1:
    a = st.slider("기울기 (a)", min_value=-5.0, max_value=5.0, value=0.0, step=0.1, on_change=add_attempt)
with col2:
    b = st.slider("y절편 (b)", min_value=-150, max_value=150, value=0, step=5, on_change=add_attempt)

# 3. 그룹 데이터 정의
group1_x, group1_y = [-100, -50, -20, 30, 80, 10], [100, 60, 120, 80, 40, 20]
group2_x, group2_y = [100, 50, 20, -30, -80, -10, -30], [-100, -60, -120, -80, -40, 10,15]

# 4. 그래프 시각화 설정
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(group1_x, group1_y, color='blue', label='Group 1 (위쪽)')
ax.scatter(group2_x, group2_y, color='red', label='Group 2 (아래쪽)')

x_vals = np.array([-150, 150])
y_vals = a * x_vals + b
ax.plot(x_vals, y_vals, color='green', linestyle='--', linewidth=2, label=f'y = {a}x + {b}')

ax.set_xlim(-150, 150)
ax.set_ylim(-150, 150)
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)
ax.grid(color='gray', linestyle=':', linewidth=0.5)
ax.legend()

st.pyplot(fig)

# 5. 분류 성공 여부 검증
success = True
for x, y in zip(group1_x, group1_y):
    if y <= a * x + b:
        success = False

for x, y in zip(group2_x, group2_y):
    if y >= a * x + b:
        success = False

# 6. 결과 피드백 출력
if success:
    st.success(f"🎉 분류 성공! 총 {st.session_state.attempts}번의 시도 끝에 두 그룹을 완벽하게 나누었습니다.")
    st.balloons()
else:
    st.error("❌ 분류 실패! 선이 두 그룹을 정확히 나누지 못했습니다. a와 b를 다시 조절해 보세요.")
