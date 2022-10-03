import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):
    """
    - This function reads files saved in data folders. 
    - loads the read data (single file for the project scope) into data frames. 
    - select the columns of interest for each table(song and artist).
    - apply the insert statement (from sql_queries.py file) for song and artist tables.
      INPUT :
    - cur for statement executions.
    - filepath from which we extract data.
    
    """
    # open song file
    
    #song_files = get_files(filepath)

    df = pd.read_json(filepath,lines= True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']]
    song_data = song_data.values.tolist()[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']]
    artist_data=artist_data.values[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    - This function reads files saved in data folders.
    - (filtering) select certain rows based of the page column.
      value to only select the 'NextSong'.
    - convert the type of start time coulmn to data time to be 
      able to extract other coulmns(day , month , hour ,....) from it.
    - loads the read data into data frames. 
    - changes the name of the column ts to a more descriptive one 
      that is start_time .
    - select the columns of interest for each table(time and users).
    - generates needed columns and extract their data from 
      start time column in log_data file.
    - apply the insert statement (from sql_queries.py file)for time
      and artist tables.
      INPUT :
    - cur for statement executions.
    - filepath from which we extract data.
    
    """
    # open log file
    #log_files = get_files(filepath)
    df = pd.read_json(filepath,lines=True)

    # filter by NextSong action
    df =df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'],unit ='ms')
    t=pd.DataFrame(t)
    # renaming the column ts to a more descriptive name that is start_time
    t=t.rename(columns={"ts":"start_time"})
    #extracting the hour,day,week,month,year , and week_day from the start_time column and putting them in their own columns
    t['hour'] = t['start_time'].dt.hour
    t['day'] = t['start_time'].dt.day
    t['week'] = t['start_time'].dt.week
    t['month'] = t['start_time'].dt.month
    t['year'] = t['start_time'].dt.year
    t['week_day'] = t['start_time'].dt.weekday
    # insert time data records
    time_data = (t['start_time'].dt.hour,
                 t['start_time'].dt.day,
                 t['start_time'].dt.week,
                 t['start_time'].dt.month,
                t['start_time'].dt.year,
                 t['start_time'].dt.weekday)
    ###column_labels = ['hour','day','week','month','year','weekday']
    time_df = t
    
   

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]
    user_df = user_df.drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts,unit='ms'),
                         row.userId,
                         row.level,
                         songid,
                         artistid,
                         row.sessionId,
                         row.location,
                         row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    - This function gets the files' complete paths 
      to allow for them to be read by the the past two functions.
    - prints the number of files found in a certain directory.
    - prints the percent of filed processed to know where we are in
      the reading process and to seek for error if they were existed 
      as we would know we this function stopped.
      INPUT
    - cur : that is the cursor for process execution and result status.
    - conn : connection to start the connection to the sparkify database.
    - filepath : directory in which we search for files to extract data from.
    - func : to pass the function that will do the etl process for a 
      certain directory and load the data into certain tables.
    
    - 
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - this is the main function from which we call the last three functions 
    to complete the etl process.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    
    main()