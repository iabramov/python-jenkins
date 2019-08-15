# Python + Jenkins 

## Problem specification

```
Design and code a simple "Hello World" application that exposes the following HTTP-based APIs: 

Description: Saves/updates the given user's name and date of birth in the database. 
Request: PUT /hello/<username> { "dateOfBirth": "YYYY-MM-DD" }
Response: 204 No Content
 
Note:
<usemame> must contains only letters. 
YYYY-MM-DD must be a date before the today date. 

Description: Returns hello birthday message for the given user 
Request: Get /hello/<username> 
Response: 200 OK 

Response Examples: 
A. If username's birthday is in N days: { "message": "Hello, <username>! Your birthday is in N day(s)" } 
B. If username's birthday is today: { "message": "Hello, <username>! Happy birthday!" } 

Note: Use storage/database of your choice. The code should have at least one unit test. 
```

## Tools, repos and deloyments 

- Jenkins jobs [http://68.183.67.246:8080/job/python-jenkins/](http://68.183.67.246:8080/job/python-jenkins/)
- Deployed example [http://68.183.67.246:8081](http://68.183.67.246:8081)
- DockerHub repo [https://hub.docker.com/r/iabramov/python-test](https://hub.docker.com/r/iabramov/python-test)

## How to run and test locally

- Run server ```python main.py``` 
- Run test without logging ```pytest -q``` 
- Run test without logging ```pytest -q -c pytest_logs.ini``` 

Logs can be found in "logs" directory.

You may test server manually, following link [http://localhost:8080/hello/Basil](http://localhost:8080/hello/Basil)

## How to run and test via docker-compose
```bash
docker-compose up test_server
docker-compose up run_server
```

## Prerequisites
```bash
pip install -r requirements.txt
```
## OSX

```bash
brew update
brew install python
pip install -U pytest
pytest --version
pip install -r requirements.txt
echo 'export PATH=/usr/local/opt/python/libexec/bin:/Users/Ivan/Library/Python/3.7/bin:$PATH' >> ~/.bash_profile
```