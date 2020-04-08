def get_recom(df):
    recom = ''

    if df['temp'][0] > 20:
        recom += 'Сегодня можно надеть футболку.\n'
    elif df['temp'][0] > 8:
        recom += 'Лёгкая куртка не помешает.\n'
    else:
        recom += 'Нужно одеться потеплее.\n'

    if df['precip'] > 40:
        if (df['wind'] < 5) and (df['temp'] > 0):
            recom += 'Зонт не помешает.\n'
        else:
            recom += 'Капюшон не помешает.\n'

    if df['uv'] > 5:
        recom += 'Стоит взять солнцезащитные очки.\n'

    return recom
