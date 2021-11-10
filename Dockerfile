FROM python:3.9

WORKDIR /usr/src/app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]