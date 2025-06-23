import markov_hidden_lstm_regimen_mercado as markov 
import best_stocks_morningstar as best_stocks
import drawdown_medio_tickers as drawdown
import lppl_sobrecompra_sobreventa as lppl
import telegram as t
import os 

#### VARIABLES
path_base       = "C:/users/mrella/OneDrive - Consorci Administració Oberta de Catalunya/Inversion/FinanceMR/"
path_base       = "./"


#### MARKOV HIDDEN 
path_markov     = path_base + "markov/"
os.makedirs(path_markov, exist_ok=True)
markov.generar_graficos(path_markov)
t.send_img(path_markov+"markov_return.png",caption="Hidden Markov Returns Analysis")
t.send_img(path_markov+"markov_atr.png",caption="Hidden Markov ATR Analysis")

exit()

#### LPPL SOBRECOMPRA Y SOBREVENTA
path_lppl = path_base + "lppl/"
os.makedirs(path_lppl, exist_ok=True)
lppl.generar_graficos(path_lppl)
t.send_img(path_lppl+"lppl_spy_sobre.png",caption="LPPL sobrecompra sobreventa SPY")
t.send_img(path_lppl+"lppl_qqq_sobre.png",caption="LPPL sobrecompra sobreventa QQQ")

#### DRAWDOWN MEDIO TICKERS
path_drawdown_medio = path_base + "drawdown_medio/"
os.makedirs(path_drawdown_medio, exist_ok=True)
drawdown.generar_graficos_video(path_drawdown_medio)
t.send_video(path_drawdown_medio+"spy_drawdown.mp4",caption="Mean drawdown SPY animation")
t.send_video(path_drawdown_medio+"qqq_drawdown.mp4",caption="Mean drawdown QQQ animation")  

#### BEST STOCKS MORNINGSTAR
path_best_stocks = path_base + "best_stocks/"
os.makedirs(path_best_stocks, exist_ok=True)
best_stocks.generar_graficos(path_best_stocks)
t.send_img(path_best_stocks+"best_stocks.png",caption="Core best stocks more repeated (x-axis) at the most profitable funds at morningstar")

#t.send_img(path_lppl+"lppl_spy.png",caption="LPPL sobre SPY")
#t.send_img(path_lppl+"lppl_qqq.png",caption="LPPL sobre QQQ")
#t.send_img(path_drawdown_medio+"spy_drawdown.png",caption="Mean drawdown SPY")
#t.send_img(path_drawdown_medio+"qqq_drawdown.png",caption="Mean drawdown QQQ")  
#drawdown.generar_graficos(path_drawdown_medio)
