FROM python:3.11.9

ENV PYTHONUNBUFFERED 1

WORKDIR /SCV

COPY . /SCV/


RUN pip install -r requirements.txt

#RUN python manage.py collectstatic --noinput\

RUN source venv/bin/activate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "scv.wsgi:application"]