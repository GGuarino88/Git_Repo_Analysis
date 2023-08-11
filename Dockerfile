## Updated Image based on the requirement
FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

## Installing the Dependencies for project
RUN apt-get update && apt-get install -y python3 python3-pip tzdata git # openssl
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

## Copying the latest code
RUN git clone -b production https://github.com/GGuarino88/Git_Repo_Analysis.git /Git_Repo_Analysis

## Copy the .env file
COPY .env /Git_Repo_Analysis/RepoAnalysis/.env

## Setting up the Env
WORKDIR /Git_Repo_Analysis/RepoAnalysis

## Install the required modules
RUN pip3 install -r requirements.txt

## Expose port 80 for HTTP
EXPOSE 8000

## Collect Static Files
RUN python3 manage.py collectstatic

## Start the Project with SSL support
CMD ["sh", "-c", "python3 manage.py runserver 0.0.0.0:8000 2>&1 | tee runserver.log"]