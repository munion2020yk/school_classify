import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="수동 AI: 회귀 모델", layout="centered")
st.title("수동 인공지능: 데이터 추세선 찾기 📈")
st.write("슬라이더를 움직여 $y = ax + b$ 직선을 만들고, 점들과 직선 사이의 **오차(회색 점선)**를 최소로 줄여보세요!")

# 2. 가상의 데이터 생성 (고정된 난수로 일정한 패턴 생성)
np.random.seed(42)
x_data = np.linspace(10, 90, 20)
# 실제 정답에 가까운 식은 y = 1.5x + 20 수준이며 여기에 노이즈(오차)를 추가함
y_data = 1.5 * x_data + 20 + np.random.normal(0, 15, len(x_data)) 

# 3. 사용자 입력 UI
col1, col2 = st.columns(2)
with col1:
    a = st.slider("기울기 (a)", min_value=-3.0, max_value=5.0, value=0.0, step=0.1)
with col2:
    b = st.slider("y절편 (b)", min_value=-50, max_value=100, value=0, step=5)

# 4. 사용자의 선에 대한 오차(MSE) 계산
y_pred = a * x_data + b
# 평균 제곱 오차 (Mean Squared Error)
mse = np.mean((y_data - y_pred)**2) 

# 가장 완벽한 정답(AI가 수학적으로 찾은 최적의 선) 계산
best_a, best_b = np.polyfit(x_data, y_data, 1)
best_mse = np.mean((y_data - (best_a * x_data + best_b))**2)

# 5. 그래프 시각화
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x_data, y_data, color='blue', label='Data Points', zorder=3)
# 사용자가 만든 선 그리기
x_line = np.array([0, 100])
y_line = a * x_line + b
ax.plot(x_line, y_line, color='red', linewidth=2, label=f'Line: y = {a}x + {b}', zorder=2)

# 오차 시각화 (점과 선 사이의 거리)
for x, y, p in zip(x_data, y_data, y_pred):
    ax.plot([x, x], [y, p], color='gray', linestyle=':', alpha=0.6, zorder=1)

ax.set_xlim(0, 100)
ax.set_ylim(0, 180)
ax.grid(color='lightgray', linestyle='-', linewidth=0.5)
ax.legend(loc='upper left')

st.pyplot(fig)

# 6. 피드백 및 점수판 UI
st.subheader("📊 현재 나의 모델 성능")
metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.metric(label="현재 오차 (작을수록 좋음)", value=f"{mse:,.0f}")
with metric_col2:
    # 정답 힌트 보기 토글
    show_hint = st.checkbox("AI가 찾은 정답 선 보기 (힌트)")

if show_hint:
    st.info(f"💡 AI가 계산한 최적의 식은 약 **y = {best_a:.1f}x + {best_b:.0f}** 이며, 이때의 최소 오차는 **{best_mse:,.0f}** 입니다.")

# 성공 판정 (최적의 오차 범위에 15% 이내로 근접했을 때)
if mse <= best_mse * 1.15:
    st.success("🎉 완벽합니다! 점들의 추세를 아주 잘 설명하는 최적의 선을 찾으셨습니다!")
    st.balloons()
else:
    st.warning("회색 점선(오차)의 길이가 전체적으로 가장 짧아지도록 기울기와 절편을 조절해보세요.")