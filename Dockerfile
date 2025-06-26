FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# This is the fix: expose the port Render provides
ENV PORT 10000
EXPOSE $PORT

CMD ["uvicorn", "bot:app", "--host", "0.0.0.0", "--port", "10000"]
