#Repository for Final Year Project on Automatic Text Summarization

###Contributors:
Ajinkya Zadbuke  
Sahil Pimenta  
Deepen Padwal  

###Description:  
<to-do>

###Folder Structure  
FYProject/  
-----> feeds_test.py   ... (fetches data from RSS feeds)  
-----> db_test.py      ... (displays data stored in DB)  
-----> textrank.py    ... (summarization algorithm) <to-do>  
-----> fyproject-meteor/  
------------------> fyproject-meteor.html  
------------------> fyproject-meteor.css  
------------------> fyproject-meteor.js  
------------------> public/   ... (dir for public files, images etc)  
------------------> libs/     ... (files in here loaded first)  
------------------> journal/  

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
---Added Compression ratio to db_test.py  
---Summary should be >200 chars in length  
---Article Size must be >10, not 13  
---Fixed Image Fetching for both CNN, Reuters.  
---gen_summary() call in db_test replaced by summary property of article loaded from db (faster)  

###NOTES:  
1. Default database name is "feeds_database", consisting of a single "articles" collection.  
   Create this database prior to any operations if running for the first time.   
2. Default num. of articles fetched from each source is 6 (for now)  
3. Summary generation call is made from feeds_test to textrank.py.  
   Run textrank.py separately to test summarization without affecting articles in DB.