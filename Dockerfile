# 使用 Python 基底
FROM python:3.12-slim

# 安裝系統相依套件
RUN apt-get update && apt-get install -y build-essential

# 設定工作目錄
WORKDIR /app

# 先複製 requirements
COPY requirements.txt .

# 安裝套件
RUN pip install --no-cache-dir -r requirements.txt

# 再複製全部程式碼
COPY . .

# 讓 Uvicorn 在 Cloud Run 可監聽 0.0.0.0:$PORT
ENV PORT=8080

# 啟動 FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
