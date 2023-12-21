FROM python:3.9.2-buster

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

COPY requirements.txt .
COPY app app
RUN pip install -r requirements.txt
WORKDIR /app
#EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081", "--reload"]