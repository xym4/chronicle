FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 80

CMD ["python3", "communications-db-api.py"]
