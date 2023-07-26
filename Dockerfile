FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3 python3-pip tzdata git
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata
RUN git clone https://github.com/GGuarino88/Git_Repo_Analysis /Git_Repo_Analysis
COPY .env /Git_Repo_Analysis/RepoAnalysis/.env
WORKDIR /Git_Repo_Analysis/RepoAnalysis
RUN pip3 install -r requirements.txt
RUN python3 manage.py migrate
CMD ["sh", "-c", "python3 manage.py runserver 0.0.0.0:8000 2>&1 | tee runserver.log"]