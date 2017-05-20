# 09.02.17: 00
# 10.02.17: mensile in corso
# 11.02.17: pioggia da correggere la fine pioggia alle 23.59.00

import datetime
import time

from pprint import pprint as pp

import db_02 as DB


MESE = '2017-03'
DH_MIN = datetime.timedelta(1.0 / 24 / 60 * 30)  # intervallo di tempo minimo tra la fine di una pioggia e
                                                # l'inizio di un'altra


def pioggia(db, mese):
    dm = datetime.timedelta(1.0/24/6)  # 10 minuti

    cmd = """SELECT data, mm
            FROM Raw
            WHERE (strftime('%Y-%m', data) = '{}') AND
                  mm > 0
            """.format(mese)

    dati = db.cur.execute(cmd).fetchall()

    al = datetime.datetime.strptime(dati[0][0], '%Y-%m-%d %H:%M:%S')
    dal = al - dm
    giorno = al.day
    mm = dati[0][1]

    rigo = '{:02d}\t{:%H:%M:%S}\t{:%H:%M:%S}\t{:.1f}'.format(giorno, dal, al, mm)

    print(rigo)

    for row in dati[1:]:
        al = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        dal = al - dm
        g = al.day
        mm = row[1]

        if giorno == g:
            rigo = '  \t{:%H:%M:%S}\t{:%H:%M:%S}\t{:.1f}'.format(dal, al, mm)
        else:
            rigo = '{:02d}\t{:%H:%M:%S}\t{:%H:%M:%S}\t{:.1f}'.format(g, dal, al, mm)
            giorno = g

        print(rigo)


def pioggia2(db, mese):
    print('\nPIOGGIA')
    dm = datetime.timedelta(1.0/24/6)  # 10 minuti

    cmd = """SELECT data, mm
            FROM Raw
            WHERE (strftime('%Y-%m', data) = '{}') AND
                  mm > 0
            """.format(mese)

    dati = db.cur.execute(cmd).fetchall()

    al0 = datetime.datetime.strptime(dati[0][0], '%Y-%m-%d %H:%M:%S')
    dal0 = al0 - dm
    g0 = al0.day
    mm0 = dati[0][1]

    lpioggia = []
    for row in dati[1:]:
        al = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        dal = al - dm
        g = al.day
        mm = row[1]

        if g == g0 and (dal-al0) < DH_MIN:
            al0 = al
            mm0 += mm
        else:
            rigo = '{:02d}\t{:%H:%M:%S}\t{:%H:%M:%S}\t{:.1f}'.format(g0, dal0, al0, mm0)
            print(rigo)
            rec = (g0, dal0, al0, mm0, '%s' % (al0 - dal0))
            lpioggia.append(rec)

            g0 = g
            dal0 = dal
            al0 = al
            mm0 = mm


    rigo = '{:02d}\t{:%H:%M:%S}\t{:%H:%M:%S}\t{:.1f}'.format(g0, dal0, al0, mm0)
    print(rigo)
    rec = (g0, dal0, al0, mm0, '%s' % (al0 - dal0))
    lpioggia.append(rec)

    cmd = """INSERT INTO Pioggia
            VALUES (?, time(?), time(?), ?, ?)"""
    db.cur.executemany(cmd, lpioggia)
    db.db.commit()

    cmd = """SELECT *
            FROM Pioggia
            """
    dati = db.cur.execute(cmd).fetchall()
    return dati


def mensile(db, mese):
    print('\nMENSILE')
    cmd = """
SELECT Giornaliero.data, Giornaliero.pres, Giornaliero.t, Giornaliero.tmin, Giornaliero.tmax, Giornaliero.ur,
       Giornaliero.vdir, Giornaliero.vvel, Giornaliero.eliof / Effemeridi.effe, Giornaliero.mm
FROM Giornaliero
INNER JOIN Effemeridi
ON strftime('%m-%d', Giornaliero.data)  = strftime('%m-%d', Effemeridi.data)
WHERE (strftime('%Y-%m', Giornaliero.data) = '{}')
""".format(mese)

    dati = db.cur.execute(cmd).fetchall()

    for row in dati:
        data = row[0][-2:]
        pres = int(row[1])
        t = row[2]
        tmin = row[3]
        tmax = row[4]
        ur = row[5]
        vdir = row[6]
        vvel = row[7]

        cielo = row[8]
        if cielo > 0.8:
            cielo = 'sereno'
        elif cielo > 0.6:
            cielo = 'poco nuvoloso'
        elif cielo > 0.4:
            cielo = 'nuvoloso'
        elif cielo > 0.2:
            cielo = 'molto nuvoloso'
        else:
            cielo = 'coperto'

        cmd = """
SELECT mm, durata
FROM Pioggia
WHERE data = '{}'
        """.format(data)

        dati = db.cur.execute(cmd).fetchall()

        mm = 0
        dmm = datetime.timedelta(minutes=0)
        for xmm, ymm in dati:

            mm += xmm
            minuti = int(ymm.split(':')[0]) * 60 + int(ymm.split(':')[1])
            dmm+= datetime.timedelta(minutes=minuti)

        ddati = {'data': data, 'pres': pres, 't': t, 'tmin': tmin, 'tmax': tmax, 'ur': ur, 'vdir': vdir, 'vvel': vvel,
                 'cielo': cielo, 'mm': mm, 'dmm': str(dmm).zfill(8)}

        rigo = '{data} {pres:4.0f} {t:5.1f} {tmin:5.1f} {tmax:5.1f} {ur:2.0f} {vdir:2s} {vvel:4.1f} {cielo:14s} ' \
               '{mm:5.1f} {dmm}'.format(**ddati)
        print(rigo)


if __name__ == '__main__':
    db = DB.DB()
    db.crea_db()

    # pioggia2(db, MESE)
    mensile(db, MESE)
