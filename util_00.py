# 29.01.17: 0
# 30.01.17: direzione_vento_orario
# 31.01.17: vento_analisi

import datetime
import math
from pprint import pprint as pp

def direzione_vento_G2PC(velocita, direzione):
    '''converte la direzione del vento da gradi a punto cardinale'''
    if velocita *3.6 <= 5.0:
        direzione = 'C'

    else:
        if 360.0 - 22.5 < direzione or 0 <= direzione < 0.0 + 22.5:
            direzione = 'N'
        elif 45.0-22.5 < direzione < 45.0+22.5:
            direzione = 'NE'
        elif 90.0 - 22.5 < direzione < 90.0 + 22.5:
            direzione = 'E'
        elif 135.0 - 22.5 < direzione < 135.0 + 22.5:
            direzione = 'SE'
        elif 180.0 - 22.5 < direzione < 180.0 + 22.5:
            direzione = 'S'
        elif 225.0 - 22.5 < direzione < 225.0 + 22.5:
            direzione = 'SO'
        elif 270.0 - 22.5 < direzione < 270.0 + 22.5:
            direzione = 'O'
        elif 315.0 - 22.5 < direzione < 315.0 + 22.5:
            direzione = 'NO'

    return direzione

def direzione_vento_orario(db, dati):
    al = datetime.datetime.strptime(dati[0], '%Y-%m-%d %H:%M:%S')
    dal = al - datetime.timedelta(55 * 1.0 / 24 / 60)

    # direzione = util.direzione_vento_G2PC(rec[-2], rec[-1])
    #
    odati = db.interroga2('raw', dal, al, campi=['vvel', 'vdir'], solo_orari=False).fetchall()
    try:
        odati = [(x[1], direzione_vento_G2PC(x[1], x[2])) for x in odati if x[1]]
    except:
        pp(odati)

    velocita = [x[0] for x in odati]
    velocita = math.fsum(velocita) / len(velocita)

    if velocita * 3.6 <= 5.0:
        direzione = 'C'
    else:
        direzioni = [x[1] for x in odati]
        direzione = direzione_dominante(direzioni)

    return  velocita, direzione

def direzione_dominante(direzioni):
    punti_cardinali = ('N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO')
    ddirezioni = {}

    for d in punti_cardinali:
        ddirezioni[d] = direzioni.count(d)

    dominante = [(ddirezioni[x], x) for x in ddirezioni]
    dominante.sort(reverse=True)

    if dominante[0][0] == dominante[1][0]:
        dominante = 'V'
    else:
        dominante = dominante[0][1]

    return dominante

def vento_analisi(dati):
    """[(v1, d1), (v2, d2), ...] --> velocita_media, direzione_dominate"""
    lvelocita = []
    ldirezioni = []

    for velocita, gradi in dati:
        lvelocita.append(velocita)

        direzione = direzione_vento_G2PC(velocita, gradi)
        ldirezioni.append(direzione)

    try:
        velocita = sum(lvelocita) / len(lvelocita)
    except ZeroDivisionError:
        return None, None

    direzione = direzione_dominante(ldirezioni)

    return velocita, direzione

if __name__ == '__main__':
    pass

