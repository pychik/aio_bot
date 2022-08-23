FROM python:3.9


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh


COPY . .
ENTRYPOINT ["./entrypoint.sh"]

