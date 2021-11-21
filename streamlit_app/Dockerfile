FROM python:3.8

EXPOSE 8501

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit","run" , "main.py"]


