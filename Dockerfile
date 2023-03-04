FROM python:3.9
ADD . /login-api
WORKDIR /login-api
RUN pip install -r requirements.txt
CMD python -m login_api.app