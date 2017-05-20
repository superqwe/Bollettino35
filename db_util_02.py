# 13.12.16: 00
# 29.01.17:
# 02.01.17: 01 spostati da db 'interroga2', 'popola_orario', 'popola_raw'
#           popola_giornaliero
# 03.01.17: popola_orario2 ok,
#           popola_giornaliero
# 05.02.17: popola_giornaliero ok,
#           popola_mensile, popola_annuale, inserisci_mese (da rivedere i dati dell'anno)
# 08.02.17: fix dati anno del 05.02.17
#           popola_tabella
# 09.02.17: popola_tabella da verificare i valori, da verificare con la tabella annuale
#         : fix tabella annuale
# 10.02.17: 02 aggiornamento a seguito di db_02
#           popola effemridi

import calendar
import datetime

from pprint import pprint as pp

import db_02 as DB
import leggi_csv_01 as leggi_csv
import util_00 as util

from costanti_01 import CMD_db_util_popola_tabella as CMD

ANNI_DAL = 2012
ANNI_AL = 2016

###############################################################################
# obsoleti
###############################################################################

def popola_orario2(db, dal=None, al=None):
    """obsoleto"""

    if dal:
        cmd = '''SELECT data, avg(t), min(tmin), max(tmax), avg(pres), sum(mm)
                FROM Raw
                WHERE data BETWEEN '{}' AND '{}'
                GROUP BY strftime('%Y-%m-%d %H', data, '-10 minutes')
                '''.format(dal, al)
    else:
        cmd = '''SELECT data, avg(t), min(tmin), max(tmax), avg(pres), sum(mm)
                FROM Raw
                GROUP BY strftime('%Y-%m-%d %H', data, '-10 minutes')
            '''
    dati = db.cur.execute(cmd)

    ldati = []
    for row in dati:
        rec = list(row)
        rec.extend((None, None))
        ldati.append(rec)

    cmd = "INSERT INTO Orario VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    db.cur.executemany(cmd, ldati)
    #
    # db.db.commit()

    if dal:
        cmd = '''SELECT data
                FROM Orario
                WHERE data BETWEEN '{}' AND '{}'
                GROUP BY strftime('%Y-%m-%d %H', data, '-10 minutes')
                '''.format(dal, al)
    else:
        cmd = '''SELECT data
                FROM Orario
                GROUP BY strftime('%Y-%m-%d %H', data, '-10 minutes')
                '''
    ldate = db.cur.execute(cmd).fetchall()

    for data in ldate:
        d = data[0].strip()
        print(d)

        cmd = '''SELECT vvel, vdir
                FROM Raw
                WHERE (data BETWEEN datetime('{0}', '-55 minutes')
                               AND datetime('{0}'))
                        AND vvel IS NOT NULL
                '''.format(d)

        dati = db.cur.execute(cmd).fetchall()

        if dati:
            vvel, vdir = util.vento_analisi(dati)

            cmd = """UPDATE Orario
                    SET vvel = {1},
                        vdir = '{2}'
                    WHERE data = '{0}'
                    """.format(d, vvel, vdir)

            db.cur.execute(cmd)

    db.db.commit()


def popola_giornaliero2(db, dal=None, al=None):
    """obsoleto"""

    if dal:
        cmd = '''SELECT date(data), avg(t), min(tmin), max(tmax), avg(pres), sum(mm)
            FROM Orario
            WHERE data BETWEEN '{}' AND '{}'
            GROUP BY strftime('%Y-%m-%d', data)
            '''.format(dal, al)
    else:
        cmd = '''SELECT date(data), avg(t), min(tmin), max(tmax), avg(pres), sum(mm)
            FROM Orario
            GROUP BY strftime('%Y-%m-%d', data)
            '''

    dati = db.cur.execute(cmd)

    ldati = []
    for row in dati:

        if row[0]:
            rec = list(row)
            rec.extend((None, None))
            ldati.append(rec)

    cmd = "INSERT INTO Giornaliero VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    db.cur.executemany(cmd, ldati)
    #
    # db.db.commit()

    if dal:
        cmd = '''SELECT date(data)
            FROM Orario
            WHERE data BETWEEN '{}' AND '{}'
            GROUP BY strftime('%Y-%m-%d', data)
            '''.format(dal, al)
    else:
        cmd = '''SELECT date(data)
                FROM Orario
                GROUP BY strftime('%Y-%m-%d', data)
                '''
    ldate = db.cur.execute(cmd).fetchall()

    for data in ldate:
        d = data[0]
        if d:
            print(d)

            cmd = '''SELECT vvel, vdir
                    FROM Raw
                    WHERE date(data) = date('{0}') AND
                          vvel IS NOT NULL
                    '''.format(d)

            # print(cmd)

            dati = db.cur.execute(cmd).fetchall()

            if dati:
                vvel, vdir = util.vento_analisi(dati)

                cmd = """UPDATE Giornaliero
                        SET vvel = {1},
                            vdir = '{2}'
                        WHERE data = '{0}'
                        """.format(d, vvel, vdir)

                db.cur.execute(cmd)

    db.db.commit()


def popola_mensile(db, dal=None, al=None):
    """obsoleto"""

    if dal:
        cmd = '''SELECT date(data), avg(t), min(tmin), max(tmax), avg(pres), sum(mm)
                FROM Giornaliero
                WHERE data BETWEEN '{}' AND '{}'
                GROUP BY strftime('%Y-%m', data)
                '''.format(dal, al)
    else:
        cmd = '''SELECT date(data), avg(t), min(tmin), max(tmax), avg(pres), sum(mm)
                FROM Giornaliero
                GROUP BY strftime('%Y-%m', data)
                '''

    dati = db.cur.execute(cmd)

    ldati = []
    for row in dati:

        if row[0]:
            rec = list(row)
            rec.extend((None, None))
            ldati.append(rec)

    cmd = "INSERT INTO Mensile VALUES (date(?,'start of month') , ?, ?, ?, ?, ?, ?, ?)"
    db.cur.executemany(cmd, ldati)
    #
    # db.db.commit()

    if dal:
        cmd = '''SELECT date(data)
                FROM Giornaliero
                WHERE data BETWEEN '{}' AND '{}'
                GROUP BY strftime('%Y-%m', data)
                '''.format(dal, al)
    else:
        cmd = '''SELECT date(data)
                FROM Giornaliero
                GROUP BY strftime('%Y-%m', data)
                '''
    ldate = db.cur.execute(cmd).fetchall()

    for data in ldate:
        d = data[0]
        if d:
            print(d)

            cmd = '''SELECT vvel, vdir
                    FROM Raw
                    WHERE strftime('%Y-%m', data) = strftime('%Y-%m','{0}') AND
                          vvel IS NOT NULL
                    '''.format(d)

            # print(cmd)
            dati = db.cur.execute(cmd).fetchall()
            # pp(dati)

            if dati:
                vvel, vdir = util.vento_analisi(dati)

                cmd = """UPDATE Mensile
                        SET vvel = {1},
                            vdir = '{2}'
                        WHERE data = date('{0}', 'start of month')
                        """.format(d, vvel, vdir)

                # print(cmd)
                db.cur.execute(cmd)

    db.db.commit()


def popola_annuale(db, dal=None, al=None):
    """obsoleto"""

    if dal:
        cmd = '''SELECT date(data), avg(t), min(tmin), max(tmax), avg(pres), sum(mm)
            FROM Mensile
            WHERE data BETWEEN date('{}') AND date('{}')
            GROUP BY strftime('%Y', data)
            '''.format(dal, al)
    else:
        cmd = '''SELECT date(data), avg(t), min(tmin), max(tmax), avg(pres), sum(mm)
            FROM Mensile
            GROUP BY strftime('%Y', data)
            '''

    dati = db.cur.execute(cmd)

    ldati = []
    for row in dati:

        if row[0]:
            rec = list(row)
            rec.extend((None, None))
            ldati.append(rec)

    cmd = "INSERT INTO Annuale VALUES (strftime('%Y', ?) , ?, ?, ?, ?, ?, ?, ?)"
    db.cur.executemany(cmd, ldati)
    #
    # db.db.commit()

    if dal:
        cmd = '''SELECT date(data)
            FROM Mensile
            WHERE data BETWEEN date('{}') AND date('{}')
            GROUP BY strftime('%Y', data)
            '''.format(dal, al)
    else:
        cmd = '''SELECT date(data)
            FROM Mensile
            GROUP BY strftime('%Y', data)
            '''

    ldate = db.cur.execute(cmd).fetchall()

    for data in ldate:
        d = data[0]
        if d:
            print(d)

            cmd = '''SELECT vvel, vdir
                    FROM Raw
                    WHERE strftime('%Y', data) = strftime('%Y','{0}') AND
                          vvel IS NOT NULL
                    '''.format(d)

            # print(cmd)
            dati = db.cur.execute(cmd).fetchall()
            # pp(dati)

            if dati:
                vvel, vdir = util.vento_analisi(dati)

                cmd = """UPDATE Annuale
                        SET vvel = {1},
                            vdir = '{2}'
                        WHERE data = strftime('%Y','{0}')
                        """.format(d, vvel, vdir)

                # print(cmd)
                db.cur.execute(cmd)

    db.db.commit()


def interroga(tabella, dal, al, campi=[], dati_orari=True):
    '''obsoleto'''
    db = DB.DB()
    rec = db.interroga(tabella, dal, al, campi, dati_orari).fetchall()
    return rec

###############################################################################
# fine obsoleti
###############################################################################

def interroga2(db, tabella, dal, al=None, campi=[], solo_orari=True, senza_data=False, somma=False):
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

    return db.cur.execute(cmd)


def popola_raw(db, fin):
    dati = leggi_csv.leggi_csv(fin)

    ldati = []
    for row in dati:
        record = row.get()
        ldati.append(record)

    cmd = "INSERT INTO Raw VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    db.cur.executemany(cmd, ldati)
    db.db.commit()


def popola_tabella(db, tabella, dal=None, al=None):
    print('\n', tabella)

    if dal:
        cmd = '''SELECT data, avg(t), min(tmin), max(tmax), avg(pres), sum(mm), avg(ur), sum(eliof), avg(pir)
                FROM {from0}
                {where02}
                GROUP BY {group02}
                '''.format(**CMD[tabella]).format(dal, al)
    else:
        cmd = '''SELECT data, avg(t), min(tmin), max(tmax), avg(pres), sum(mm), avg(ur), sum(eliof), avg(pir)
                FROM {from0}
                GROUP BY {group02}
                '''.format(**CMD[tabella])
    dati = db.cur.execute(cmd)

    ldati = []
    for row in dati:
        rec = list(row)
        rec.extend((None, None))
        ldati.append(rec)

    cmd = """INSERT INTO {insert1}
            VALUES {values1}""".format(**CMD[tabella])

    db.cur.executemany(cmd, ldati)
    #
    # db.db.commit()

    if dal:
        cmd = '''SELECT {select2}
                FROM {from2}
                {where02}
                GROUP BY {group02}
                '''.format(**CMD[tabella]).format(dal, al)
    else:
        cmd = '''SELECT {select2}
                FROM {from2}
                GROUP BY {group02}
                '''.format(**CMD[tabella])
    # print(cmd)
    ldate = db.cur.execute(cmd).fetchall()

    for data in ldate:
        d = data[0].strip()
        print(d)

        cmd = '''SELECT vvel, vdir
                FROM Raw
                WHERE {where3} AND
                      vvel IS NOT NULL
                '''.format(**CMD[tabella]).format(d)

        dati = db.cur.execute(cmd).fetchall()

        if dati:
            vvel, vdir = util.vento_analisi(dati)

            cmd = """UPDATE {update4}
                    SET vvel = {0},
                        vdir = '{1}'
                    WHERE data = {where4}
                    """.format(vvel, vdir, **CMD[tabella]).format(d)

            db.cur.execute(cmd)

    db.db.commit()


def inserisci_mese(db, fin):
    anno = int('20%2s' % fin[:2])
    mese = int(fin[2:4])
    ngiorni = calendar.monthrange(anno, mese)[1]

    dal = datetime.datetime(anno, mese, 1)
    al = datetime.datetime(anno, mese, ngiorni, 23, 59, 59)

    adal = datetime.datetime(anno, 1, 1)
    aal = datetime.datetime(anno, 12, 31, 23, 59, 59)

    popola_raw(db, fin)
    popola_tabella(db, 'orario', dal, al)
    popola_tabella(db, 'giornaliero', dal, al)
    popola_tabella(db, 'mensile', dal, al)
    popola_tabella(db, 'annuale', adal, aal)


def popola_effemeridi():
    effemeridi = leggi_csv.leggi_effemeridi2()

    cmd = """INSERT INTO Effemeridi
            VALUES (?, ?)"""

    db.cur.executemany(cmd, effemeridi)
    db.db.commit()



if __name__ == '__main__':
    db = DB.DB()
    db.crea_db()

    dal = datetime.datetime(2016, 1, 1)
    al = datetime.datetime(2016, 12, 31, 23, 59, 59)

    #   popola raw
    #     for anno in range(ANNI_DAL, ANNI_AL+1):
    #         popola_raw(db, '%ia.txt' % anno)
    popola_raw(db, '1703m.TXT')

    # popola_orario2(db)

    # # popola_giornaliero2(db, dal, al)
    #
    # popola_mensile(db, dal, al)
    #
    # popola_annuale(db, dal, al)

    # inserisci_mese(db, '1701m.TXT')

    # popola_effemeridi()


