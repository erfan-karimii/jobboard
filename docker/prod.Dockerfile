FROM docker.arvancloud.ir/python:3.11.1-slim


ENV PYTHONUNBUFFERED 1


ADD requirements/ requirements/
RUN pip install --upgrade pip -i https://mirror-pypi.runflare.com/simple \ 
    && pip install -i https://mirror-pypi.runflare.com/simple -r requirements/prod.txt

# Get the django project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./core/ /app/

COPY ./scripts/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh