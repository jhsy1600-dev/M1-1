import os
import pandas as pd
import matplotlib.pyplot as plt

# 폴더 생성
os.makedirs("data", exist_ok=True)
os.makedirs("images", exist_ok=True)

# 한글 폰트 설정, 윈도우 기준
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 1. 데이터 불러오기
file_path = "data/samsung_2023_2024.csv"
df = pd.read_csv(file_path)

# 2. 날짜 형식 변환 및 정렬
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# 3. 종가 기준 분석
price_col = "Close"

# 4. 이동평균 계산
df["MA20"] = df[price_col].rolling(window=20).mean()
df["MA60"] = df[price_col].rolling(window=60).mean()

# 5. 일별 수익률 계산
df["Daily_Return"] = df[price_col].pct_change() * 100

# 6. 월별 수익률 계산
monthly_price = df.set_index("Date")[price_col].resample("ME").last()
monthly_return = monthly_price.pct_change() * 100

# 7. 정제된 데이터 저장
df.to_csv("data/samsung_cleaned.csv", index=False, encoding="utf-8-sig")

print("데이터 정제 완료!")
print(df.head())
print()
print("기본 통계:")
print(df[[price_col, "MA20", "MA60", "Daily_Return"]].describe())

# =========================
# 그래프 1. 종가 추세
# =========================
plt.figure(figsize=(12, 6))
plt.plot(df["Date"], df[price_col], label="종가", color="blue")
plt.title("삼성전자 종가 추세, 2023~2024")
plt.xlabel("날짜")
plt.ylabel("주가, 원")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("images/close_trend.png")
plt.close()

# =========================
# 그래프 2. 이동평균선
# =========================
plt.figure(figsize=(12, 6))
plt.plot(df["Date"], df[price_col], label="종가", color="gray", alpha=0.7)
plt.plot(df["Date"], df["MA20"], label="20일 이동평균", color="orange")
plt.plot(df["Date"], df["MA60"], label="60일 이동평균", color="red")
plt.title("삼성전자 종가와 이동평균선")
plt.xlabel("날짜")
plt.ylabel("주가, 원")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("images/moving_average.png")
plt.close()

# =========================
# 그래프 3. 월별 수익률
# =========================
colors = ["red" if value < 0 else "green" for value in monthly_return]

plt.figure(figsize=(12, 6))
monthly_return.plot(kind="bar", color=colors)
plt.title("삼성전자 월별 수익률, 2023~2024")
plt.xlabel("월")
plt.ylabel("수익률, %")
plt.axhline(0, color="black", linewidth=1)
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("images/monthly_return.png")
plt.close()

# 월별 수익률 저장
monthly_return_df = monthly_return.reset_index()
monthly_return_df.columns = ["Date", "Monthly_Return"]
monthly_return_df.to_csv("data/monthly_return.csv", index=False, encoding="utf-8-sig")

print()
print("그래프 저장 완료!")
print("1. images/close_trend.png")
print("2. images/moving_average.png")
print("3. images/monthly_return.png")
print()
print("월별 수익률 저장 완료: data/monthly_return.csv")