# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users" 
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = (
                                                "CREATE TABLE songplays (songplay_id SERIAL PRIMARY KEY \
                                                ,start_time timestamp NOT NULL REFERENCES time(start_time)\
                                                ,user_id int NOT NULL REFERENCES users(user_id), level varchar(10) \
                                                ,song_id varchar(35) REFERENCES song(song_id) \
                                                ,artist_id varchar(35) REFERENCES artist(artist_id)\
                                                ,session_id int \
                                                ,location varchar(50) \
                                                ,user_agent varchar(300))"
                        )

user_table_create = (
                                                "CREATE TABLE users (user_id int PRIMARY KEY\
                                                ,first_name varchar(25)\
                                                ,last_name varchar(25)\
                                                ,gender varchar(1)\
                                                ,level varchar(10))"
                    )

song_table_create = (
                            "CREATE TABLE song (song_id varchar(35) PRIMARY KEY\
                            ,title varchar(5000) \
                            ,artist_id varchar(35) \
                            ,year int\
                            ,duration float)"
                    )

artist_table_create = (
    "CREATE TABLE artist (artist_id varchar(35) PRIMARY KEY\
    , name varchar(5000)\
    ,location varchar(50)\
    ,latitude float\
    ,longitude float)"
                       )

time_table_create = (
                                        "CREATE TABLE time (start_time timestamp PRIMARY KEY\
                                        , hour int , day varchar(20)\
                                        , week int \
                                        , month varchar(10)\
                                        ,year int \
                                        , weekday int)"
                    )

# INSERT RECORDS

songplay_table_insert = (
                            """INSERT INTO songplays (
                            start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
                            )
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s) 
                            ON CONFLICT(songplay_id) DO NOTHING
                            """)

user_table_insert = (
                            """INSERT INTO users 
                            (
                            user_id,first_name,last_name,gender,level
                            ) 
                            VALUES (%s,%s,%s,%s,%s)
                            ON CONFLICT(user_id) DO UPDATE SET level = EXCLUDED.level
                            """)

song_table_insert = (
                        """INSERT INTO song 
                        (
                        song_id,title,artist_id ,year,duration
                        )
                        VALUES (%s,%s,%s,%s,%s)
                        ON CONFLICT(song_id) DO NOTHING"""
                    )

artist_table_insert = ("""
                        INSERT INTO artist 
                        (
                        artist_id ,name ,location,latitude ,longitude
                        ) 
                        VALUES(%s,%s,%s,%s,%s)
                        ON CONFLICT(artist_id) DO NOTHING
                        """)


time_table_insert = ("""
    INSERT INTO time 
    (
    start_time,hour, day,week,month,year,weekday
    )
    VALUES(%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT(start_time) DO NOTHING
    """)

# FIND SONGS

song_select = ("""
                SELECT song_id ,artist.artist_id  
                FROM song, artist
                WHERE song.artist_id = artist.artist_id
                AND (song.title = %s AND
                artist.name = %s AND
                song.duration = %s)
                     
                    """)


# QUERY LISTS

create_table_queries = [user_table_create,
                        song_table_create,
                        artist_table_create,
                        time_table_create,
                        songplay_table_create]

drop_table_queries = [songplay_table_drop,
                      user_table_drop ,
                      song_table_drop,
                      artist_table_drop,
                      time_table_drop]