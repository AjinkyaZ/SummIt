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
-----> db_test.py      ... (displays data stored in dB)
-----> summ_test.py    ... (summarization algorithm) <to-do>
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

2. Run Python scripts
   FYProject$ python <filename>
   a. feeds_test.py   (fetch data)
   b. db_test.py    (display fetched data)
   c. summ_test.py   (run summarization algorithm) <skip for now>
  
3. Run Meteor application, specifying dbpath used previously
   FYProject/fyproject-meteor$ MONGO_URL="mongodb://localhost:3001/<dbname>" meteor run --port 3005

NOTES:
<to-do>
