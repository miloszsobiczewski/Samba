FROM python:3-onbuild
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app
EXPOSE 8000