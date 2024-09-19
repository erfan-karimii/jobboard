# Welcome to Jobboard documentation

## About

Jobboard is an online recruiting platform API designed to streamline the hiring process. Its primary goal is to simplify recruitment while handling high traffic loads efficiently. The platform is engineered to manage high-pressure situations by maintaining optimal performance with minimal response times, ensuring a smooth and responsive experience for both recruiters and job seekers. [Learn more about how we achieve this.](high-pressure.md)


## Installation

    git clone https://github.com/erfan-karimii/jobboard
    cd jobboard
    docker compose -f docker-compose-dev.yaml up

Note: Ensure that ports 5000, 25, and 143 are open, as they are required for SMTP4Dev.

## Why This Project Stands Out

* [use locust to handel high load pressure](high-pressure.md)
* [use celery for handling background processing and task scheduling](celery.md)
* [cash strategies](cash.md)

<div class="custom-box">
    <h4>Hardware configuration</h4>
    <div class="custom-box-detail">
    <p>Ram: 8GB single channel</p>
    <p>hard: 128GB SSD</p>
    <p>cpu: 8core</p>
    <p>os: ubuntu server</p>
    </div>
</div>