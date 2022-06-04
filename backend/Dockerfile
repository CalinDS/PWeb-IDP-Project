# FROM alpine:edge
 
FROM python:3.10

# RUN apk add --update py3-pip
 
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY ./ /usr/src/app/


EXPOSE 5000
EXPOSE 8005
 
CMD ["python3", "-u", "/usr/src/app/app.py"]