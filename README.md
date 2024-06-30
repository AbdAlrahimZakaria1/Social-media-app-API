# Social media app

This is a simple social media app, Users can create/update/delete posts & vote on them.

This app is deployed on:
1. Ubuntu server (Subscription is cancelled now).
2. Render free cloud hosting service: https://fastapi-9jxc.onrender.com/  (Please wait up to a minute for the website to start).
See the API docs here: https://fastapi-9jxc.onrender.com/docs

- The **API** logic and the PostgreSQL are seperately containerized using Docker, visible here: https://hub.docker.com/r/lypophrenia/fastapi
- **Docker compose** files are configured for both **DEV** & **PROD** to quickly instantiate a docker image.




# CI/CD:
A **CI/CD** pipeline is created using Github Actions to automatically do the following tasks upon pushing any commit to github:

A. **Build the image:**
  1. Set up python & update pip on VM.
  2. install requirements/dependencies.
  3. Create a testing PostgreSQL DB for pytest tests.
  4. Run pytest tests (~30 tests).
  5. Create a new Docker Image and upload it to Docker Hub. (https://hub.docker.com/r/lypophrenia/fastapi)

B. **Deployment:**
  1. Deploy on an Ubuntu Server
  2. Deploy on "Render" cloud hosting provider




# Features:
1. User authorization & authentication using JWT tokens.
2. Users, Posts & votes system.
3. Fully tested by unit-tests.
4. Resource authorization, No user can alter other users data.



# Technologies:
- Language: Python3.12
- Framework: Fastapi
- Database: PostgreSQL
- Database ORM: SQLAlchemy
- Database Migration: SQL Alembic
- CI/CD: Github Actions
- Containerization: Docker
- Hosting: Ubuntu server
- Testing: Pytest
  
Please make sure that you're logged-ing/authorized before using the requests that have "Lock" next to them.
