# Welcome to Jobboard documentation

<b><a href="https://erfan-karimii.github.io/jobboard/">full documentation</a></b>

## About

Jobboard is an online recruiting platform API designed to streamline the hiring process. Its primary goal is to simplify recruitment while handling high traffic loads efficiently. The platform is engineered to manage high-pressure situations by maintaining optimal performance with minimal response times, ensuring a smooth and responsive experience for both recruiters and job seekers. [Learn more about how we achieve this.](https://erfan-karimii.github.io/jobboard/high-pressure/)


## Installation

    git clone https://github.com/erfan-karimii/jobboard
    cd jobboard
    docker compose -f docker-compose-dev.yaml up

Note: Ensure that ports 5000, 25, and 143 are open, as they are required for SMTP4Dev.

## Why This Project Stands Out

* [use locust to handel high load pressure](https://erfan-karimii.github.io/jobboard/high-pressure/)
* [use celery for handling background processing and task scheduling](https://erfan-karimii.github.io/jobboard/celery/)
* [cash strategies](https://erfan-karimii.github.io/jobboard/cash/)
