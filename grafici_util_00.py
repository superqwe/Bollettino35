# 12.02.17

"""
nomencalura
a__b__c

a: parametro
    t-temperatura
    tm-temperatura minima
    tM-teperatura massima

b: intervallo di tempo
    a-anno

c: tabella fonte dati
    g-giornaliero
"""

import db_02 as DB


def t_tm_tM__a__g(db, anno):
    cmd = """
SELECT data, t, tmin, tmax
FROM Giornaliero
WHERE strftime('%Y') = '{}'
    """.format(anno)

    dati = db.cur.execute(cmd).fetchall()

    ldate = []
    lt = []
    ltm = []
    ltM = []
    for data, t, tm , tM in dati:
        ldate.append(data)
        lt.append(t)
        ltm.append(tm)
        ltM.append(tM)

    return ldate, lt, ltm, ltM


if __name__ == '__main__':
    db = DB.DB()
    db.crea_db()

    t_tm_tM__a__g(db, 2017)
