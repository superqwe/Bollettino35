# 11.12.16: 00
# 13.12.16
# 29.01.17
# 30.01.17 DB.elabora_orario2
# 01.02.17
# 02.02.17

import datetime
import os
import sqlite3 as lite

from pprint import pprint as pp

import leggi_csv_00 as leggi_csv
import util_00 as util
from util_00 import direzione_vento_orario

NOME_DB = 'test.sqlite'
ANNI_DAL = 2012
ANNI_AL = 2016


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
                                      vvel FLOAT,
                                      vdir INT
                                     )"""
            self.cur.execute(cmd)
            self.db.commit()
        except lite.OperationalError:
            print('tabella esistente: Raw')

        tabelle = ('Orario', 'Giornaliero', 'Mensile', 'Annuale')

        for tabella in tabelle:
            try:
                cmd = """CREATE TABLE %s(data TIMESTAMP NOT NULL,
                                          t FLOAT,
                                          tmin FLOAT,
                                          tmax FLOAT,
                                          pres FLOAT,
                                          mm FLOAT,
                                          vvel FLOAT,
                                          vdir TEXT
                                         )""" % tabella
                self.cur.execute(cmd)
                self.db.commit()
            except lite.OperationalError:
                print('tabella esistente: ', tabella)

    def inserisci_raw(self, fin):
        dati = leggi_csv.leggi_csv(fin)

        ldati = []
        for row in dati:
            record = row.get()
            ldati.append(record)

        cmd = "INSERT INTO Raw VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        self.cur.executemany(cmd, ldati)
        self.db.commit()

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

    def interroga2(self, tabella, dal, al=None, campi=[], solo_orari=True, senza_data=False, somma=False):
        if campi:
            campi = list(campi)

            if not senza_data:
                campi.insert(0, 'data')

            campi = ', '.join(campi)
        else:
            campi = '*'

        if not al:
            al = datetime.datetime(dal.year, dal.month, dal.day, 23, 59, 59)

        if solo_orari:
            solo_orari = """AND ( strftime('%M', data) = '00' OR
                                  strftime('%M', data) = '59')"""
        else:
            solo_orari = ''

        if somma:
            cmd = """
                  SELECT sum({campi})
                  FROM {tabella}
                  WHERE data
                  BETWEEN '{dal}' AND '{al}'
                  {solo_orari}
                  """.format(campi=campi,
                             tabella=tabella,
                             dal=dal,
                             al=al,
                             solo_orari=solo_orari)
        else:
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
            db.elabora_orario2(anno)
            # db.elabora_giornaliero(anno)

    def elabora_orario(self, anno):
        dal = datetime.date(anno, 1, 1)
        al = datetime.date(anno, 12, 31)

        dati = db.interroga('raw', dal, al).fetchall()
        ldati = []

        for n, rec in enumerate(dati):
            if not n % 100: print((n))
            vento = direzione_vento_orario(self, rec)
            rec2 = list(rec[:-2])
            rec2.extend(vento)
            ldati.append(rec2[:])

        print('commit')

        # cmd = "INSERT INTO Orario VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        # self.cur.executemany(cmd, ldati)
        # self.db.commit()

    def elabora_orario2(self, anno):
        ora = datetime.datetime(anno, 1, 1, 0, 0)
        al = datetime.datetime(anno, 12, 31, 23, 59)
        dt_ora = datetime.timedelta(1.0 / 24.0)  # 1 ora
        dt_minuti = datetime.timedelta(1.0 / 24.0 / 60.0)  # 1 minuto

        ldati = []
        while ora <= al:
            dati = db.interroga2('raw', ora + dt_minuti, ora + dt_ora, campi=['t', 'tmin', 'tmax', 'pres']).fetchall()

            mm = db.interroga2('raw', ora + dt_minuti, ora + dt_ora, campi=['mm'], solo_orari=False,
                               senza_data=True, somma=True).fetchone()[0]

            vento = db.interroga2('raw', ora + dt_minuti, ora + dt_ora, campi=['vvel', 'vdir'],
                                  solo_orari=False, senza_data=True).fetchall()
            velocita, direzione = util.vento_analisi(vento)

            ora += dt_ora

            dati.extend([mm, velocita, direzione])
            ldati.append(dati)

        print('commit')

        cmd = "INSERT INTO Orario VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        self.cur.executemany(cmd, ldati)
        self.db.commit()

    def elabora_giornaliero(self, anno):
        dal = datetime.date(anno, 1, 1)
        al = datetime.date(anno, 12, 31)

        ldati = db.interroga('raw', dal).fetchall()
        pp(ldati)
        #
        # cmd = "INSERT INTO Orario VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        # self.cur.executemany(cmd, ldati)
        # self.db.commit()


if __name__ == '__main__':
    db = DB()
    # db.crea_db()
    db.ricrea_db()

# ---
# db.inserisci_raw('2012a.TXT')
# db.inserisci_raw('2013a.TXT')
# db.inserisci_raw('2014a.TXT')
# db.inserisci_raw('2015a.TXT')
# db.inserisci_raw('2016a.TXT')

# ---
# dal = datetime.date(2015, 12, 12)
# al = datetime.date(2015, 12, 13)
#
# a = db.interroga('raw', dal, al, campi=['tmin', 'tmax'])
#
# for x in a:
#     print(x)
