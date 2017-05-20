# 08.02.17: CMD_db_util_popola_tabella
# 09.02.17: CMD_db_util_popola_tabella riformulata
# 10.02.17: CMD_db_util_popola_tabella fix mensile values1 e where4, annuali where4
#         : 01 aggiornamento per db_02

CMD_db_util_popola_tabella = {
    'orario': {
        'from0': 'Raw',
        'where02': "WHERE data BETWEEN '{}' AND '{}'",
        'group02': "strftime('%Y-%m-%d %H', data, '-10 minutes')",
        'insert1': 'Orario',
        'values1': '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        'select2': 'data',
        'from2': 'Orario',
        'where3': "(data BETWEEN datetime('{0}', '-55 minutes') AND datetime('{0}'))",
        'update4': 'Orario',
        'where4': "'{0}'"
    },
    'giornaliero': {
        'from0': 'Orario',
        'where02': "WHERE data BETWEEN '{}' AND '{}'",
        'group02': "strftime('%Y-%m-%d', data)",
        'insert1': 'Giornaliero',
        'values1': '(date(?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        'select2': 'date(data)',
        'from2': 'Orario',
        'where3': """date(data) = date('{0}')""",
        'update4': 'Giornaliero',
        'where4': "'{0}'"
    },
    'mensile': {
        'from0': 'Giornaliero',
        'where02': "WHERE data BETWEEN '{}' AND '{}'",
        'group02': "strftime('%Y-%m', data)",
        'insert1': 'Mensile',
        'values1': "(date(?,'start of month') , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        'select2': 'date(data)',
        'from2': 'Giornaliero',
        'where3': "strftime('%Y-%m', data) = strftime('%Y-%m','{0}')",
        'update4': 'Mensile',
        'where4': "date('{0}', 'start of month')"
    },
    'annuale': {
        'from0': 'Mensile',
        'where02': "WHERE data BETWEEN date('{}') AND date('{}')",
        'group02': "strftime('%Y', data)",
        'insert1': 'Annuale',
        'values1': "(strftime('%Y', ?) , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        'select2': 'date(data)',
        'from2': 'Mensile',
        'where3': "strftime('%Y', data) = strftime('%Y','{0}')",
        'update4': 'Annuale',
        'where4': "strftime('%Y','{0}')"
    },
}