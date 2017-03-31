# IPL Prediction Analysis #

## Synopsis ##

Please go through **Project_Report.pdf** to read the entire synopsis of this project.
This is a Big Data based project where we had to process 700 MB worth of match data
obtained from various sources using several frameworks such as Hadoop, Hive and Spark.
Once we obtain cluster probabilites for various batsman-bowler pairs using various
Big Data techniques (by processing scraped data of course), we then proceeded to simulate 
a match using these cluster probabilities.

## Procedure ##

* Create a spreadsheet to denote a particular IPL match. This is the input given to our program.
* This must have two columns, one for the lineup of the first team and other for the second team
* Populate the columns with players accordingly.
* Check out the **members** folder for sample lineups.
* Execute **demo.py** and give the recent spreadsheet you gave as input.
* An **output.html** file is generated, and opens automatically.

## Working ##

![alt tag](Image_Demo.gif)