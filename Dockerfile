FROM python:3.9-slim
COPY . /flask_app
RUN pip install -r requirements.txt
EXPOSE 80
ENV NAME World
CMD ["python", "test.py"]