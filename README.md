<> Summary of the project 
- in this project i was asked to design a database of sparkify
- this database contains five table (4 dimesional and one fact table)
- dimesion table are (users , song , artist ,and time )
- in the users the data of the user is user_id , first and last name , gender ,and the level
- in song table we store data about song_id , title , artist id , year , and duration of the song
- in artist table we store data about artist_id , name , location , latitude and logitude 
- in time table we store the start_time , hour , day , week , month , year , and week_day
- fact table is named songplays table in which we store sonplay_id , start_time , user_id , level , song_id , artist_id ,
session_id , location , and user_agent
- data was provided by two datasets the first was song_data from which we loaded data into song and artsit tables
- second dataset was log_data set from which we loaded data into the other tables
- No data any data manipulation was conducted
- data was never changed

<> how to run python scripts
    you want to open your terminal 
    check for directory 
        -- type in the teminal python sql_queries (optional)
    then type
        -- python create_table.py  
    to create database and its table after establishing connection and cursor allocation (after finishing it closes the cursor for deallocation)    
    then type
        -- python etl.py 
    this file allows for importing data from its json files and loading this data into their own tables


<> Files in the repository (final and data)
first folder (final)
1 - sql_queries.py  this file has all queries needed for creation , selection , and dropping tables
2 - create_table.py  this file is resposible for creation of the five table in the dataset 
3- etl.py after creation of tables we now want to load them with data which we extarct from json files 
saved in two folders (log_data and song_data) by a some function
second folder (data)
having to datasets saved in many files
1 - the first is song_data
2 - the second is log_data

