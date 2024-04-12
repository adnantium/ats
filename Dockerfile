# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
WORKDIR /usr/src/ats/
COPY ./ats/ats/ .

# CMD ["ls -la"]

# CMD ["django-admin ", "loaddata", "groups.json"]

# # run server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
