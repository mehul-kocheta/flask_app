FROM python:3.9-slim
WORKDIR /flask_app
COPY . /flask_app
RUN pip install -r requirements.txt
EXPOSE 5000
ENV NAME World
CMD ["python", "server.py"]