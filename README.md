#Repository for Final Year Project on Automatic Text Summarization  

###Contributors  
Ajinkya Zadbuke  
Sahil Pimenta  
Deepen Padwal  

###Description  
Summ-It is an application that fetches summarized news articles from sources such as CNN, Reuters etc.  
It uses Python for fetching, parsing and implementing summarization techniques, and MeteorJS as the  
web-application server.  

###Screenshot  
![alt tag](https://raw.githubusercontent.com/AjinkyaZ/FYProject/master/fypscr1.png)

###Folder Structure  
FYProject/  
-----> feeds_test.py   ... (fetches data from RSS feeds)  
-----> db_test.py      ... (displays data stored in DB)  
-----> parser.py      ... (implements parsing article html for content)   
-----> textrank.py    ... (summarization algorithm)  
-----> fyproject-meteor/  
------------------> fyproject-meteor.html  
------------------> fyproject-meteor.css  
------------------> fyproject-meteor.js  
------------------> public/   ... (directory for public files, images etc)  
------------------> libs/     ... (files in here loaded first)  

###Python Package Requirements  
NLTK (with Punkt tokenization module included)  
Scikit-learn  
Stemming  
NetworkX  
Matplotlib (optional)  
PyMongo  
FeedParser  
BeautifulSoup4  
Requests (previously urllib2)   

###Procedure for running application  
1. Run mongod instance in separate terminal  
   FYProject$ mongod --port 3001 --dbpath fyproject-meteor/.meteor/local/db

2. In another terminal run Python scripts  
   FYProject$ python <filename goes here>  
   a. feeds_test.py   (fetch data, summaries)  
   b. db_test.py    (display fetched data)  <optional, just for verification>  

3. Run Meteor application, specifying dbpath used previously  
   FYProject/fyproject-meteor$ MONGO_URL="mongodb://localhost:3001/feeds_database" meteor run --port 3005

###Most Recent Changes  
---Sort articles based on timestamp.  
---Replaced urllib2 with Requests.   
---Separate Date and Time fields.  
---Check for duplicate articles based on hash of Title.  
---Stemming for better quality summaries.  
---Textrank and Parser both use trained tokenization data (most edge cases handled).  
---Parser tokenization gives better article text.  
---Compression data processed while fetching, stored with article in db.  
---Added article fetch counts.  
---Added Compression ratio to db_test.py (not anymore, see above)  
---Summary should be more 200 chars in length, less than 1200 chars.    
---Article Size must be more than 10, not 13  
---Fixed Image Fetching for both CNN, Reuters.  
---gen_summary() call in db_test replaced by summary property of article loaded from db (faster)  

###NOTES:  
1. Default database name is "feeds_database", consisting of a single "articles" collection.  
   Create this database prior to any operations if running for the first time.   
2. Summary generation call is made from feeds_test to textrank.py.  
   Run textrank.py separately to test summarization without affecting data in DB.  
