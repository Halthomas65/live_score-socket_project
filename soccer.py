from tkinter import messagebox as ms
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sqlite3   
from sqlite3 import Error


# def create_connection(db_file):
#     """ create a database connection to a SQLite database """
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()
def create_table():
    with sqlite3.connect('Soccer.db') as db:
        c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS match (ID TEXT NOT NULL PRIMARY KEY,Time DATETIME NOT NULL, Team1 TEXT NOT NULL, Team2 TEXT NOT NULL, Score TEXT NOT NULL);')
    c.execute('CREATE TABLE IF NOT EXISTS detail (ID_M TEXT NOT NULL, ID_D TEXT NOT NULL, TEAM TEXT NOT NULL, TIME_IN_MACTH TEXT NOT NULL, ID_SCORE TEXT, ID_YC TEXT, ID_RC, PRIMARY KEY(ID_M, ID_D), FOREIGN KEY (ID_M) REFERENCES match (ID), FOREIGN KEY (ID_SCORE) REFERENCES score (ID_SCORE), FOREIGN KEY (ID_YC) REFERENCES yellow_card (ID_YC),  FOREIGN KEY (ID_RC) REFERENCES red_card (ID_RC));')
    c.execute('CREATE TABLE IF NOT EXISTS score (ID_SCORE TEXT NOT NULL PRIMARY KEY, PLAYER_NAME TEXT NOT NULL);')
    c.execute('CREATE TABLE IF NOT EXISTS yellow_card (ID_YC TEXT NOT NULL PRIMARY KEY, PLAYER_NAME TEXT);')
    c.execute('CREATE TABLE IF NOT EXISTS red_card (ID_RC TEXT NOT NULL PRIMARY KEY, PLAYER_NAME TEXT);')
    db.commit()
    db.close()
def insert(id, time, team1, team2, score, id_score, player_name, id_yc, id_rc, id_d, time_in_match):
    with sqlite3.connect('Soccer.db') as db:
        c = db.cursor()
    c.execute('INSERT INTO match(ID, time, team1, team2, score) VALUES(?,?,?,?,?)',[id, time, team1, team2, score])
    c.execute('INSERT INTO score(ID_SCORE, PLAYER_NAME) VALUES(?,?)', [id_score, player_name])
    c.execute('INSERT INTO yellow_card(ID_YC, PLAYER_NAME) VALUES(?,?)', [id_yc, player_name])
    c.execute('INSERT INTO red_card(ID_RC, PLAYER_NAME) VALUES(?,?)', [id_rc, player_name])
    c.execute('INSERT INTO detail(ID_M, ID_D, TEAM, TIME_IN_MACTH, ID_SCORE, ID_YC, ID_RC) VALUES(?,?,?,?,?,?,?)', [id, id_d, team1, time_in_match, id_score, id_yc, id_rc])
    db.commit()
    db.close()
def insert2(id, team, id_score, player_name, id_d, time_in_match):
    with sqlite3.connect('Soccer.db') as db:
        c = db.cursor()
    
    c.execute('INSERT INTO detail(ID_M, ID_D, TEAM, TIME_IN_MACTH, ID_SCORE, ID_YC, ID_RC) VALUES(?,?,?,?,?,?,?)', [id, id_d, team, time_in_match, id_score, 'NULL', 'NULL'])
    c.execute('INSERT INTO score(ID_SCORE, PLAYER_NAME) VALUES(?,?)', [id_score, player_name])
    db.commit()
    db.close()

if __name__ == '__main__':
    # create_connection(r"C:\Soccer.db")
    #create_table()
    # insert("M1", "FT", "VietNam", "ThaiLand", "3-0", "S1", "Long", "Y1", "R1","D1","5'")
    # insert2("M1", "VietNam", "S3", "Hao","D3","45'")

