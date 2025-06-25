import graficador_markov
import best_stocks_morningstar as best_stocks
import drawdown_medio_tickers as drawdown
import graficador_lppl
import riskportfoliolib_herc_nco as riskfolio
import gappers
import cruces
import graficador_ma
import tg as t
import pandas as pd
import os
import seaborn as sns
import tickers
sns.set_theme(style="darkgrid", palette="muted", font_scale=1.1)
from matplotlib import style
import matplotlib

matplotlib.use('Agg')
import time
style.use('dark_background')


#### VARIABLES DE FICHEROS
path_base       = "./"
#path_base       = "C:/users/mrella/OneDrive - Consorci Administració Oberta de Catalunya/Inversion/FinanceMR/"
path_tickers    = path_base + "tickers/"
os.makedirs(path_tickers, exist_ok=True)


#### MARKOV HIDDEN 
print("MARKOV ..........................................................")

graficador_markov.generar_graficos(['SPY','QQQ'], path_tickers,'5y')
for ticker in ['SPY','QQQ']:
    t.send_img(f"{path_tickers}{ticker}_markov_return.png",caption=f"Hidden MARKOV Returns Analysis {ticker}")
    t.send_img(f"{path_tickers}{ticker}_markov_atr.png",caption=f"Hidden MARKOV ATR Analysis {ticker}")
t.send("Explicación MARKOV: https://chatgpt.com/share/6859c35f-9130-8002-8cff-f15e677bd165)")


#### LPPL SOBRECOMPRA Y SOBREVENTA
print("LPPL .................................................................")

graficador_lppl.generar_graficos(['SPY','QQQ'], path_tickers)
for ticker in ['SPY','QQQ']:
    t.send_img(f"{path_tickers}{ticker}_lppl.png",caption=f"LPPL sobrecompra sobreventa {ticker}")
    

#### DRAWDOWN MEDIO TICKERS
print("DRAWDOWN MEDIO........................................................")
path_drawdown_medio = path_base + "drawdown_medio/"
os.makedirs(path_drawdown_medio, exist_ok=True)
#drawdown.generar_graficos(path_drawdown_medio)
drawdown.generar_graficos_video(path_drawdown_medio)
#t.send_img(path_drawdown_medio+"spy_drawdown.png",caption="Mean drawdown SPY")
t.send_video(path_drawdown_medio+"spy_drawdown.mp4",caption="Mean drawdown SPY animation")
#t.send_img(path_drawdown_medio+"qqq_drawdown.png",caption="Mean drawdown QQQ")
t.send_video(path_drawdown_medio+"qqq_drawdown.mp4",caption="Mean drawdown QQQ animation")


#### RISKPORTFOLIOLIB HERC NCO
print("RISKFOLIO............................................................")
path_riskfolio = path_base + "riskfolio/"
os.makedirs(path_riskfolio, exist_ok=True)
assets = ["XLK", "TLT", "GOLD", "BILL", "SPY", "IWM", "IWO", "KWEB"]
riskfolio.generar_graficos(path_riskfolio, assets)
t.send_img(path_riskfolio+"clusters.png",caption="Optimización sharpe riskfoliolib HERC clusters assets diversificados")
t.send_img(path_riskfolio+"herc_pie.png",caption="HERC optimizacion ajustada a riesgo")
t.send_img(path_riskfolio+"herc_drawdown.png",caption="HERC drawdown")
t.send_img(path_riskfolio+"herc_table.png",caption="HERC detalle")
t.send("Optimización sharpe riskfoliolib NCO:")
t.send_img(path_riskfolio+"nco_pie.png",caption="NCO optimizacion más agresiva")
t.send_img(path_riskfolio+"nco_drawdown.png",caption="NCO drawdown")
t.send_img(path_riskfolio+"nco_table.png",caption="NCO detalle")


#### BEST STOCKS MORNINGSTAR
print("BEST STOCKS..........................................................")
path_best_stocks = path_base + "best_stocks/"
os.makedirs(path_best_stocks, exist_ok=True)
best_stocks.generar_graficos(path_best_stocks)
t.send_img(path_best_stocks+"best_stocks.png",caption="Core best stocks more repeated (x-axis) at the most profitable funds at morningstar")


#### GAPPERS
print("GAPPERS..........................................................")
gappers_str, num_gappers, last_gappers = gappers.get_gappers(tickers.tickers_spy_qqq)
t.send(f"Large caps >4% gappers last 30 days ({num_gappers}): \n\n  {gappers_str}")
#last_gappers = ['ALB','TSLA']
graficador_lppl.generar_graficos(last_gappers, path_tickers)
graficador_markov.generar_graficos(last_gappers, path_tickers,'2y')
graficador_ma.generar_graficos(last_gappers, path_tickers)


for ticker in last_gappers:
    t.send_img(f"{path_tickers}{ticker}_ma.png",caption=f"MA gapper {ticker}")
    time.sleep(2)
    t.send_img(f"{path_tickers}{ticker}_lppl.png",caption=f"LPPL gapper {ticker}")
    time.sleep(2)
    t.send_img(f"{path_tickers}{ticker}_markov_return.png",caption=f"MARKOV return gapper {ticker}")
    time.sleep(2)
    t.send_img(f"{path_tickers}{ticker}_markov_atr.png",caption=f"MARKOV atr gapper {ticker}")
    time.sleep(2)


#### CRUCES
print("CRUCES...........................................................")
#last_cruces = cruces.get_cruces(tickers.tickers_spy_qqq)
last_cruces = ['TECH']
t.send(f"Last crosses MA20/50: {last_cruces}") 
print("markov...........................................................")
graficador_markov.generar_graficos(last_cruces, path_tickers,'2y')
print("lppl.............................................................")
graficador_lppl.generar_graficos(last_cruces, path_tickers)
print("ma...............................................................")
graficador_ma.generar_graficos(last_cruces, path_tickers)

for ticker in last_cruces:
    t.send_img(f"{path_tickers}{ticker}_ma.png",caption=f"MA cruce {ticker}")
    time.sleep(2)
    t.send_img(f"{path_tickers}{ticker}_lppl.png",caption=f"LPPL cruce {ticker}")
    time.sleep(2)
    t.send_img(f"{path_tickers}{ticker}_markov_return.png",caption=f"MARKOV cruce  {ticker}")
    time.sleep(2)
    t.send_img(f"{path_tickers}{ticker}_markov_atr.png",caption=f"MARKOV atr cruce {ticker}")
    time.sleep(2)

exit()


#path_base       = "C:/users/mrella/OneDrive - Consorci Administració Oberta de Catalunya/Inversion/FinanceMR/"
#t.send_img(path_lppl+"lppl_spy.png",caption="LPPL sobre SPY")
#t.send_img(path_lppl+"lppl_qqq.png",caption="LPPL sobre QQQ")
#drawdown.generar_graficos(path_drawdown_medio)
