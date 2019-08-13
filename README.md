# Python + Jenkins 

Design and code a simple "Hello World" application that exposes the following HTTP-based APIs: 

Description: Saves/updates the given user's name and date of birth in the database. 
Request: PUT /hello/<username> ( "dateOfBirth": "YYYY-MM-DD" ) 
Response: 204 No Content
 
Note:
<usemame> must contains only letters. 
YYYY-MM-DD must be a date before the today date. 

Description: Returns hello birthday message for the given user 
Request: Get /hello/<username> 
Response: 200 OK 

Response Examples: 
A. If username's birthday is in N days: ( "message": "Hello, <username>! Your birthday is in N day(s)" } 
B. If username's birthday is today: ( "message": "Hello, <username>! Happy birthday!" } 

Note: Use storage/database of your choice. The code should have at least one unit test. 


# Prerequisites

## OSX

```bash
brew update
brew install python
export PATH=/usr/local/opt/python/libexec/bin:$PATH
pip install -U pytest
pytest --version

pip freeze > requirements.txt

pip install -r requirements.txt
pip3 install requests
```