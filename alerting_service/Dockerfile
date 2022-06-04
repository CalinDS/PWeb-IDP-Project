FROM alpine:edge
 
RUN apk add --update py3-pip
 
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY . .

RUN chmod +x startup.sh

CMD ["sh", "./startup.sh"]