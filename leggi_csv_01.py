# 11.12.16: 00
# 10.02.17: 01 per aggiornamento tabelle db
#            leggi_effemeridi, leggi_effemeridi2

import csv
import datetime

from pprint import pprint as pp 


class Record(object):
    def __init__(self, data):
        self.data = data
        self.t = None

    def __repr__(self):
        return '%s' % self.data

    def get(self):
        dati = (self.data, self.t, self.tmin, self.tmax, self.pres, self.mm,
                self.ur, self.eliof, self.pir, self.vvel, self.vdir)

        ldati = []
        for d in dati:
            ldati.append(d if d else None)

        return ldati
    

def leggi_csv(fin):
    with open(fin) as f:
        reader = csv.DictReader(f, delimiter=';')
        dati = []
        
        for row in reader:
            giorno = row['GIORNO']
            ora = '23.59' if row['ORA'] == '24.00' else row['ORA']

            data = '%s %s' % (giorno, ora)
            try:
                data = datetime.datetime.strptime(data, '%d/%m/%Y %H.%M')
            except ValueError:
                if __name__ == '__main__':
                    print('dato mancante', row['GIORNO'], row['ORA'])

            dato = Record(data)
            dato.t = row['TARANTO T Aria 2m (MED) °C'] 
            dato.tmin = row['TARANTO T Aria 2m (MIN) °C']
            dato.tmax = row['TARANTO T Aria 2m (MAX) °C']
            dato.pres = row['TARANTO PR 2m (MED) hPa']
            dato.mm = row['TARANTO PLUV (MED) mm']
            dato.vvel = row['TARANTO VEL V 10m (MED) m/s']
            dato.vdir = row['TARANTO DIR V 10m (MED) GN']
            dato.ur = row['TARANTO UM 2m (MED) %']
            dato.eliof = row['TARANTO ELIOF (MED) min']
            dato.pir = row['TARANTO PIR (MED) W/m2']

            dati.append(dato)

    return dati
            

def leggi_effemeridi(fin):
    """obsoleto"""
    with open(fin) as f:
        dati = f.readlines()

        durata_di = []
        for row in dati:

            if row.startswith('<script type="text/javaSCRIPT">function frmSubmit()'):
                dal = row.find('Declin.')

                for tr in (row[dal:].split('<tr>')[1:]):

                    rigo = tr.split('<td class="n12" align="center">')
                    giorno = (rigo[1][:-8])
                    sorge = (rigo[2][:-6]).split('h')
                    sorge = int(sorge[0]) * 60 + int(sorge[1])
                    tramonta = (rigo[6][:-6]).split('h')
                    tramonta = int(tramonta[0]) * 60 + int(tramonta[1])

                    durata_di.append([giorno, tramonta-sorge])

    return durata_di


def leggi_effemeridi2():
    effemeridi = []
    for nmese in range(1, 13):
        fin = '{:02d} effe.txt'.format(nmese)

        with open(fin) as f:
            dati = f.read()
            dati = dati[dati.find('\n01'):]
            dati = dati[:dati.find('\n\n')]

            for rigo in dati.split('\n')[1:]:
                rigo = rigo.split()

                data = datetime.date(2000, nmese, int(rigo[0]))
                sorge = int(rigo[2][:2]) * 60 + int(rigo[2][-3:-1])
                tramonta = int(rigo[6][:2]) * 60 + int(rigo[6][-3:-1])
                durata_di = tramonta - sorge

                effemeridi.append([data, durata_di])

    return effemeridi


if __name__ == '__main__':
    # leggi_csv('2012a.TXT')
    # leggi_effemeridi('01 effe.htm')
    leggi_effemeridi2()
