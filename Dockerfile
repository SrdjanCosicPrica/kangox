FROM python:3
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE django_app.settings

COPY src /src

WORKDIR /src

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "django_app.asgi", "-w 4", "-k uvicorn.workers.UvicornWorker", "-b 0.0.0.0:8080"]
