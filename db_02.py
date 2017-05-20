# 11.12.16: 00
# 13.12.16
# 29.01.17
# 30.01.17 DB.elabora_orario2
# 01.02.17
# 02.01.17: 01 spostato a db_util 'interroga2', 'elabora_orario2', 'inserisci_raw'
# 03.01.17: modificate tabelle 'Giornaliero', 'Mensile', 'Annuale'
# 03.01.17: modificate tabella 'Annuale'
# 10.02.17: 02 inseriti i campo ur, eliof, pir
#           aggiunta tabella effemeridi
# 11.02.17: tabella pioggia

import datetime
import os
import sqlite3 as lite

from pprint import pprint as pp

import leggi_csv_01 as leggi_csv

from util_00 import direzione_vento_orario

NOME_DB = 'test.sqlite'

class DB(object):
    def __init__(self):
        self.db = lite.connect(NOME_DB)
        self.cur = self.db.cursor()

    def crea_db(self):
        try:
            cmd = """CREATE TABLE Raw(data TIMESTAMP NOT NULL,
                                      t FLOAT,
                                      tmin FLOAT,
                                      tmax FLOAT,
                                      pres FLOAT,
                                      mm FLOAT,
                                      ur FLOAT,
                                      eliof FLOAT,
                                      pir FLOAT,
                                      vvel FLOAT,
                                      vdir INT
                                     )"""
            self.cur.execute(cmd)
            self.db.commit()
        except lite.OperationalError:
            print('tabella esistente: Raw')

        try:
            cmd = """CREATE TABLE Orario(data TIMESTAMP NOT NULL,
                                       t FLOAT,
                                       tmin FLOAT,
                                       tmax FLOAT,
                                       pres FLOAT,
                                       mm FLOAT,
                                      ur FLOAT,
                                      eliof FLOAT,
                                      pir FLOAT,
                                       vvel FLOAT,
                                       vdir TEXT
                                     )"""
            self.cur.execute(cmd)
            self.db.commit()
        except lite.OperationalError:
            print('tabella esistente: Orario',)

        tabelle = ('Giornaliero', 'Mensile')

        for tabella in tabelle:
            try:
                cmd = """CREATE TABLE %s(data DATE NOT NULL,
                                          t FLOAT,
                                          tmin FLOAT,
                                          tmax FLOAT,
                                          pres FLOAT,
                                          mm FLOAT,
                                      ur FLOAT,
                                      eliof FLOAT,
                                      pir FLOAT,
                                          vvel FLOAT,
                                          vdir TEXT
                                          )""" % tabella
                self.cur.execute(cmd)
                self.db.commit()
            except lite.OperationalError:
                print('tabella esistente:', tabella)

        try:
            cmd = """CREATE TABLE Annuale(data INT NOT NULL,
                                      t FLOAT,
                                      tmin FLOAT,
                                      tmax FLOAT,
                                      pres FLOAT,
                                      mm FLOAT,
                                                                           ur FLOAT,
                                      eliof FLOAT,
                                      pir FLOAT,
                                      vvel FLOAT,
                                      vdir TEXT
                                     )"""
            self.cur.execute(cmd)
            self.db.commit()
        except lite.OperationalError:
            print('tabella esistente: Annuale')

        try:
            cmd = """CREATE TABLE Effemeridi(data DATE NOT NULL,
                                      effe INT
                                     )"""
            self.cur.execute(cmd)
            self.db.commit()
            print('tabella creata: Effemeridi')
        except lite.OperationalError:
            print('tabella esistente: Effemeridi')

        try:
            cmd = """CREATE  TABLE Pioggia(data DATE NOT NULL,
                                                    dal TIME,
                                                    al TIME,
                                                    mm FLOAT,
                                                    durata TIME)"""
            self.cur.execute(cmd)
            self.db.commit()
            print('tabella creata: Pioggia')
        except lite.OperationalError:
            print('problemi su tabella: Pioggia')



    def interroga(self, tabella, dal, al=None, campi=[], solo_orari=True):
        if campi:
            campi = list(campi)
            campi.insert(0, 'data')
            campi = ', '.join(campi)
        else:
            campi = '*'

        if al:
            al = datetime.datetime(al.year, al.month, al.day, 23, 59, 59)
        else:
            al = datetime.datetime(dal.year, dal.month, dal.day, 23, 59, 59)

        if solo_orari:
            solo_orari = """AND ( strftime('%M', data) = '00' OR
                                  strftime('%M', data) = '59')"""
        else:
            solo_orari = ''

        cmd = """
                 SELECT {campi}
                 FROM {tabella}
                 WHERE data
                 BETWEEN '{dal}' AND '{al}'
                 {solo_orari}
              """.format(campi=campi,
                         tabella=tabella,
                         dal=dal,
                         al=al,
                         solo_orari=solo_orari)

        return self.cur.execute(cmd)

    def ricrea_db(self):
        # self.db.close()
        # os.remove(NOME_DB)
        # self.__init__()
        # self.crea_db()

        for anno in range(ANNI_DAL, ANNI_AL + 1):
            print(anno)
            # db.inserisci_raw('%sa.TXT' % anno)
            # db.elabora_orario2(anno)
            # db.elabora_giornaliero(anno)

if __name__ == '__main__':
    db = DB()
    db.crea_db()
    # db.ricrea_db()


