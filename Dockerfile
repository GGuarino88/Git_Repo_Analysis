## Updated Image based on the requirement
FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

## Installing the Dependencies for project
RUN apt-get update && apt-get install -y python3 python3-pip tzdata git
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

## Copying the latest code
RUN git clone -b production https://github.com/GGuarino88/Git_Repo_Analysis.git /Git_Repo_Analysis

## Copy the .env file
COPY .env /Git_Repo_Analysis/RepoAnalysis/.env

## Setting up the Env
WORKDIR /Git_Repo_Analysis/RepoAnalysis

## Install the required modules
RUN pip3 install -r requirements.txt

## Run Migration
RUN python3 manage.py migrate

## Start the Project
CMD ["sh", "-c", "python3 manage.py runsslserver 0.0.0.0:443 2>&1 | tee runserver.log"]