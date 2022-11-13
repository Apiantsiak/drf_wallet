# drf_wallet_project

[![Python Version](https://img.shields.io/badge/python-3.10-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-4.1.2-brightgreen.svg)](https://djangoproject.com)
[![Django Rest Framework Version](https://img.shields.io/badge/djangorestframework-3.14.0-brightgreen.svg)](https://www.django-rest-framework.org/)
[![Docker Version](https://img.shields.io/badge/docker-latest-brightgreen.svg)](https://docs.docker.com/)

This is a simple Django REST project of the transactions service.

## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/Apiantsiak/drf_wallet.git
```

In the root folder using docker-compose.yml file run docker containers:

```bash
docker-compose up -d --build
```

The API endpoints will be available at:
 - for users [http://127.0.0.1:8000/api/auth/](http://127.0.0.1:8000/api/auth/)
 - for wallets [http://127.0.0.1:8000/api/wallets/](http://127.0.0.1:8000/api/wallets/)
 - for transaction [http://127.0.0.1:8000/api/wallets/transactions/](http://127.0.0.1:8000/api/wallets/transactions/)

For testing API endpoints import drf_wallet.postman_collection.json file into Postman app.
