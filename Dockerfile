FROM python:3.9-slim
WORKDIR /flask_app
COPY . /flask_app
RUN pip install -r requirements.txt
EXPOSE 80
ENV NAME World
CMD ["python", "test.py"]