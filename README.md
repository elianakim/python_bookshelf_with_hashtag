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

## Descriptions

### Search Function
User can find a book by 1) title only, 2) title and year, or 3) hashtag. <br/>
![alt text](https://github.com/elianakim/python_bookshelf/blob/master/images/1_searchform.PNG) <br/>

If the user enters the word in title input and press search button, the web application searches all the books whose title contains that word. For example, if the title input is "database", "Database Systems: The Complete Book" and "Fundamentals of Database Systems" are queried and shown to the result page. For this functionality, search() in crud.py, search list(title, year, limit, cursor) in model cloudsql.py, search list.html were newly implemented and added to the path.<br/>
**<Example: search by title only>**<br/>
![alt text](https://github.com/elianakim/python_bookshelf/blob/master/images/2_bytitle.PNG) <br/>
**<Example: searched result>**<br/>
![alt text](https://github.com/elianakim/python_bookshelf/blob/master/images/3_bytitle_result.PNG)<br/>
User can search a book by both title and year as well. This procedure is quiet straightforward, so I just leave the screenshots that describes the result.<br/>
**<Example: search by title and year>**<br/>
![alt text](https://github.com/elianakim/python_bookshelf/blob/master/images/4_bytitleandyear.PNG)<br/>
**<Example: search result>**<br/>
![alt text](https://github.com/elianakim/python_bookshelf/blob/master/images/5_bytitleandyearresult.PNG)<br/>

Users are also able to search books by a hashtag. I implemented the application so that user can describe the book using 3 hashtags in review page (will be described later). Therefore, when an user enters the word in hashtag input form and press search button, web application will query books that has similar hashtags with the input. For example, if the user enters 'engineer', the result shows the book with the hashtag 'engineering', 'engineer', 'engineers', and so on. For this functionality, hsearch() in crud.py, hashtag(id) and search hash(hashtag, limit, cursor) in model cloudsql.py, search hash.html were newly implemented and added to path. * I intended to search books that have 'similar' hashtags, but there is a known bug: if I enter 'engineer', the system queries all books with hashtag 'engineer' and 'engineering', but if I enter 'engineering', the system only queries books with hashtag 'engineering'.<br/>
**<Example: search by hashtag>**<br/>
![alt text](https://github.com/elianakim/python_bookshelf/blob/master/images/6_byhashtag.PNG)<br/>
**<Example: search result>**<br/>
![alt text](https://github.com/elianakim/python_bookshelf/blob/master/images/7_hashtag_result.PNG)<br/>

### Review Function
I revised "view.html" to enable user to review books. At the path "/books/<id>", if the user enters "review book" button, the application returns review.html which is newly implemented.<br/>
**<view.html>**<br/>
![alt text](https://github.com/elianakim/python_bookshelf/blob/master/images/8_reviews.PNG)
**<review.html>**<br/>
![alt text](https://github.com/elianakim/python_bookshelf/blob/master/images/9_reviewform.PNG)<br/>
  
In this format, users are required to type username, rate the book from 1 to 5, (step = 0.5) and write comment (reviews). Also, they need to fill out 3 hashtag forms to explain the book in simple words. When users submit the form, data is saved to "reviews" table. In the view page, average rate and number of raters are displayed, along with basic information of the book. Also, reviews that users wrote are displayed. For hashtags, since it is not efficient to display all of them, (imagine, if 100 users write 3 different hashtags, up to 300 different words need to be displayed in one page!) I implemented hashtag(id) function in model cloudsql.py to query 5 tags that are most frequently submitted. In addition, if the user click on the hashtag button, web application immediately returns the search result page with corresponding hashtag input.<br/>
To make examples, I distributed the url of this page and asked my friends to add books and rate them. The results are as follows:<br/>
![alt text]()
![alt text]()
![alt text]()
![alt text]()
![alt text]()
![alt text]()
![alt text]()
![alt text]()
