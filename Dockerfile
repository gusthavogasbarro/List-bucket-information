FROM python:3
COPY . /lambda
RUN pip3 install flask && pip3 install boto3
WORKDIR /lambda
CMD python3 lambda.py
EXPOSE 5000
