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
    c.execute('CREATE TABLE IF NOT EXISTS match (ID TEXT NOT NULL PRIMARY KEY,Time TEXT NOT NULL, Team1 TEXT NOT NULL, Team2 TEXT NOT NULL, Score TEXT NOT NULL, Date DATETIME NOT NULL);')
    c.execute('CREATE TABLE IF NOT EXISTS detail (ID_M TEXT NOT NULL, ID_D TEXT NOT NULL, TEAM TEXT NOT NULL, TIME_IN_MACTH TEXT NOT NULL, ID_SCORE TEXT, ID_YC TEXT, ID_RC, PRIMARY KEY(ID_M, ID_D), FOREIGN KEY (ID_M) REFERENCES match (ID), FOREIGN KEY (ID_SCORE) REFERENCES score (ID_SCORE), FOREIGN KEY (ID_YC) REFERENCES yellow_card (ID_YC),  FOREIGN KEY (ID_RC) REFERENCES red_card (ID_RC));')
    c.execute('CREATE TABLE IF NOT EXISTS score (ID_SCORE TEXT NOT NULL PRIMARY KEY, PLAYER_NAME TEXT NOT NULL, SCORE_CURRENT TEXT);')
    c.execute('CREATE TABLE IF NOT EXISTS yellow_card (ID_YC TEXT NOT NULL PRIMARY KEY, PLAYER_NAME TEXT, NOTE TEXT NOT NULL);')
    c.execute('CREATE TABLE IF NOT EXISTS red_card (ID_RC TEXT NOT NULL PRIMARY KEY, PLAYER_NAME TEXT, NOTE TEXT NOT NULL);')
    db.commit()
    db.close()
def insert(id, time, team1, team2, score, date, id_score, player_name, score_cur, id_yc, id_rc, id_d, time_in_match):
    with sqlite3.connect('Soccer.db') as db:
        c = db.cursor()
    c.execute('INSERT INTO match(ID, time, team1, team2, score, date) VALUES(?,?,?,?,?,?)',[id, time, team1, team2, score, date])
    c.execute('INSERT INTO score(ID_SCORE, PLAYER_NAME, SCORE_CURRENT) VALUES(?,?, ?)', [id_score, player_name, score_cur])
    c.execute('INSERT INTO yellow_card(ID_YC, PLAYER_NAME, NOTE) VALUES(?,?,?)', [id_yc, player_name, 'Yellow card'])
    c.execute('INSERT INTO red_card(ID_RC, PLAYER_NAME, NOTE) VALUES(?,?,?)', [id_rc, player_name, 'Red card'])
    c.execute('INSERT INTO detail(ID_M, ID_D, TEAM, TIME_IN_MACTH, ID_SCORE, ID_YC, ID_RC) VALUES(?,?,?,?,?,?,?)', [id, id_d, team1, time_in_match, id_score, id_yc, id_rc])
    db.commit()
    db.close()
def insert_match(id, time, team1, team2, score, date):
    with sqlite3.connect('Soccer.db') as db:
        c = db.cursor()
    c.execute('INSERT INTO match(ID, time, team1, team2, score, date) VALUES(?,?,?,?,?,?)',[id, time, team1, team2, score, date])
    db.commit()
    db.close()
def insert_score(id_score, player_name, score_cur):
    with sqlite3.connect('Soccer.db') as db:
        c = db.cursor()
    c.execute('INSERT INTO score(ID_SCORE, PLAYER_NAME, SCORE_CURRENT) VALUES(?,?, ?)', [id_score, player_name, score_cur])
    db.commit()
    db.close()

def insert_yc(id_yc, player_name):
    with sqlite3.connect('Soccer.db') as db:
        c = db.cursor()
    c.execute('INSERT INTO yellow_card(ID_YC, PLAYER_NAME, NOTE) VALUES(?,?,?)', [id_yc, player_name, 'Yellow card'])
    db.commit()
    db.close()   

def insert_rc(id_rc, player_name):
    with sqlite3.connect('Soccer.db') as db:
        c = db.cursor()
    c.execute('INSERT INTO red_card(ID_RC, PLAYER_NAME, NOTE) VALUES(?,?,?)', [id_rc, player_name, 'Red card'])
    db.commit()
    db.close()

def insert_detail(id, id_d, team, time_in_match, id_score, id_yc, id_rc):
    with sqlite3.connect('Soccer.db') as db:
        c = db.cursor()
    c.execute('INSERT INTO detail(ID_M, ID_D, TEAM, TIME_IN_MACTH, ID_SCORE, ID_YC, ID_RC) VALUES(?,?,?,?,?,?,?)', [id, id_d, team, time_in_match, id_score, id_yc, id_rc])
    db.commit()
    db.close()
if __name__ == '__main__':
    #create_table()
    #insert("M1", "FT", "VietNam", "ThaiLand", "1-0","23/04/2021", "S1", "Long", "1-0", "NULL", "NULL","D1","5'")

    #insert_match("M1", "FT", "VietNam", "ThaiLand", "1-0","23.04.2021")
    # insert_score("S1", "Long", "1-0")
    # insert_yc("YC1", "Long")
    # insert_rc("RC1", "Muya")
    insert_detail("M1", "D3", "ThaiLand", "80'", "NULL", "NULL", "RC1")