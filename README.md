# python_bookshelf
Application of GoogldCloudPlatform/getting-started-python
https://github.com/GoogleCloudPlatform/getting-started-python/tree/steps

## Getting Started
To connect Google Cloud SQL to local host and deploy the Bookshelf application, follow the instructions in https://cloud.google.com/python. 
After completing the initial setup, you can deploy the web application via command 'gcloud app deploy'.

## About the Code
I modified the code to enable a user searching for books and rating them. 
Modified codes are in the directory '2-structured-data/bookshelf'

### Prerequisites
Flask, a microframework for Python based Web developing. http://flask.pocoo.org/docs/1.0/
SQLAlchemy, the Python SQL toolkit and Object Relational Mapper https://www.sqlalchemy.org

## How it looks like
User can find a book by 1) title only, 2) title and year, or 3) hashtag. 
