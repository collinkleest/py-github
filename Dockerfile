FROM python:3

ADD src/* /src/

RUN pip install requests PyInquirer logzero logzero

CMD ["python", "./src/App.py"]