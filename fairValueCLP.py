# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 21:08:10 2021

@author: gerar
"""
import os
FOLDER = 'D:/python/'
os.chdir(FOLDER)

from datetime import date
import chileanCalendar as ccl
import dateFormulas as dtf
import dataFromBbg as bbg

import pandas as pd

# llamo calendarios para ocupar formulas
cal = ccl.CLTradingCalendar()
bday_cl = ccl.CustomBusinessDay(calendar=cal)

# ============================================================================
# canasta latam

latam = ['clp', 'mxn', 'brl', 'cop', 'pen']
add = ' Curncy'
latam = list(map(lambda x: x+add, latam))


# data from bbg
desde = dtf.ytd(cal, bday_cl, date.today())
df = bbg.BBG(latam, 'PX_LAST', start=desde)

df["return"] = df.groupby(['security', 'field'])["value"]\
                 .pct_change(1).fillna(0)

# prices
px = pd.pivot_table(df, values='value',
                    index='date', columns='security')\
       .ffill()
px.columns = [x.replace(add, '') for x in px.columns]

# returns and correlations matrix
rt = pd.pivot_table(df, values='return',
                    index='date', columns='security')\
       .ffill()
rt.columns = [x.replace(add, '') for x in rt.columns]
matCorr = rt.corr()

# indicador con promedio simple de canasta xCLP
sumRt = (rt.sum(axis=1, skipna=True) - rt.clp)/(len(latam)-1) + 1
start = px.clp[0]
sumRt[0] = start
newClp = sumRt.cumprod()
clp = px.clp

clp.to_frame().join(newClp.to_frame()).plot()

valorHoy = clp.tail(1).item()
newHoy = round(newClp.tail(1).item(), 2)


print(f'CLP de hoy es {valorHoy} y segun canasta latam debiese ser {newHoy}')


'''
# veo si clp esta explicado con desfase por alguna de las ccy de latam
cor = {}  # corr with lag
cor[0] = {i:rt['clp'].corr(rt[i]) for i in rt.columns if i != 'clp'}
cor[1] = {i:rt['clp'].corr(rt[i].shift()) for i in rt.columns if i != 'clp'}
cor[2] = {i:rt['clp'].corr(rt[i].shift(2)) for i in rt.columns if i != 'clp'}
cor = pd.DataFrame.from_dict(cor)
'''

# ============================================================================
# canasta emm xlatam

eem = ['clp', 'zar', 'hkd', 'twd']
add = ' Curncy'
eem = list(map(lambda x: x+add, eem))


# data from bbg
desde = dtf.ytd(cal, bday_cl, date.today())
df = bbg.BBG(eem, 'PX_LAST', start=desde)

df["return"] = df.groupby(['security', 'field'])["value"]\
                 .pct_change(1).fillna(0)

# prices
px = pd.pivot_table(df, values='value',
                    index='date', columns='security')\
       .ffill()
px.columns = [x.replace(add, '') for x in px.columns]

# returns and correlations matrix
rt = pd.pivot_table(df, values='return',
                    index='date', columns='security')\
       .ffill()
rt.columns = [x.replace(add, '') for x in rt.columns]
matCorr = rt.corr()

# indicador con promedio simple de canasta xCLP
sumRt = (rt.sum(axis=1, skipna=True) - rt.clp)/(len(eem)-1) + 1
start = px.clp[0]
sumRt[0] = start
newClp = sumRt.cumprod()
clp = px.clp

clp.to_frame().join(newClp.to_frame()).plot()

valorHoy = clp.tail(1).item()
newHoy = round(newClp.tail(1).item(), 2)

print(f'CLP de hoy es {valorHoy} y segun canasta eem debiese ser {newHoy}')