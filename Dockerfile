FROM python:latest

COPY requirements.txt requirements.txt

RUN pip3 install cmake -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

RUN pip3 install dlib -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

RUN pip3 --default-timeout=100 install -r ./requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

COPY app.py app.py

EXPOSE 5000

CMD [ "python3", "/app.py" ]