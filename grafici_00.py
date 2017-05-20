# 12.02.17

import matplotlib.pyplot as plt
from pprint import pprint as pp

import db_02 as DB
import grafici_util_00 as grafici


def t_tm_tM__a__g(db, anno):
    dati = grafici.t_tm_tM__a__g(db, anno)

    for x in dati:
        print(x)

    plt.plot(dati[1])
    plt.plot(dati[2])
    plt.plot(dati[3])
    plt.ylabel('some numbers')
    plt.show()


if __name__ == '__main__':
    db = DB.DB()
    db.crea_db()

    t_tm_tM__a__g(db, 2017)