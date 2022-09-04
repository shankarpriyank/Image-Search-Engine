FROM python:3.7.3-alpine3.9
WORKDIR /app
COPY requirements.txt .
RUN apk add git
RUN pip install -r requirements.txt
# RUN pip install pandas
COPY . .
RUN python ./src/caption.py
RUN python ./src/search.py
CMD ["python", "app.py"]