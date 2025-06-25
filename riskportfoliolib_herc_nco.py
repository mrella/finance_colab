import numpy as np
import pandas as pd
import yfinance as yf
import warnings
warnings.filterwarnings("ignore")
import riskfolio as rp
import seaborn as sns
sns.set_theme(style="darkgrid", palette="muted", font_scale=1.1)
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')



def generar_graficos(path_riskfolio, assets):
        
    #yf.pdr_override()
    #pd.options.display.float_format = '{:.4%}'.format

    start = f"{datetime.now().year-2}-01-01"
    end = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    

    assets.sort()
    # Downloading data
    data = yf.download(assets, start = start, end = end)
    data = data.loc[:,('Close', slice(None))]
    data.columns = assets
    # Calculating returns
    Y = data[assets].pct_change().dropna()

    #display(Y.head())
    port = rp.HCPortfolio(returns=Y)

    #import riskfolio.PlotFunctions as plf


    # Plotting Assets Clusters
    ax = rp.plot_clusters(returns=Y,
                        #correlation='pearson',
                        linkage='ward',
                        k=None,
                        max_k=10,
                        leaf_order=True,
                        dendrogram=True,
                        linecolor='tab:purple',
                        ax=None)
    plt.savefig(path_riskfolio + "clusters.png")
    plt.close()

    # Risk Measures available:
    #
    # 'vol': Standard Deviation.
    # 'MV': Variance.
    # 'MAD': Mean Absolute Deviation.
    # 'MSV': Semi Standard Deviation.
    # 'FLPM': First Lower Partial Moment (Omega Ratio).
    # 'SLPM': Second Lower Partial Moment (Sortino Ratio).
    # 'VaR': Conditional Value at Risk.
    # 'CVaR': Conditional Value at Risk.
    # 'EVaR': Entropic Value at Risk.
    # 'WR': Worst Realization (Minimax)
    # 'MDD': Maximum Drawdown of uncompounded cumulative returns (Calmar Ratio).
    # 'ADD': Average Drawdown of uncompounded cumulative returns.
    # 'DaR': Drawdown at Risk of uncompounded cumulative returns.
    # 'CDaR': Conditional Drawdown at Risk of uncompounded cumulative returns.
    # 'EDaR': Entropic Drawdown at Risk of uncompounded cumulative returns.
    # 'UCI': Ulcer Index of uncompounded cumulative returns.
    # 'MDD_Rel': Maximum Drawdown of compounded cumulative returns (Calmar Ratio).
    # 'ADD_Rel': Average Drawdown of compounded cumulative returns.
    # 'DaR_Rel': Drawdown at Risk of compounded cumulative returns.
    # 'CDaR_Rel': Conditional Drawdown at Risk of compounded cumulative returns.
    # 'EDaR_Rel': Entropic Drawdown at Risk of compounded cumulative returns.
    # 'UCI_Rel': Ulcer Index of compounded cumulative returns.

    rms = ['MV', 'MAD', 'MSV', 'FLPM', 'SLPM',
        'CVaR', 'EVaR', 'WR', 'MDD', 'ADD',
            'CDaR', 'UCI']

    rms = ['vol', 'MV', 'MAD', 'MSV', 'FLPM', 'SLPM',
        'VaR','CVaR', 'EVaR', 'WR', 'MDD', 'ADD',
        'DaR', 'CDaR', 'EDaR', 'UCI', 'MDD_Rel', 'ADD_Rel',
        'DaR_Rel', 'CDaR_Rel', 'EDaR_Rel', 'UCI_Rel']

    w_s = pd.DataFrame([])

    model = 'HERC'
    rf = 0 # Risk free rate
    linkage = 'ward' # Linkage method used to build clusters
    max_k = 10 # Max number of clusters used in two difference gap statistic
    leaf_order = True # Consider optimal order of leafs in dendrogram

    for i in rms:

        w = port.optimization(model=model,
                            #correlation=correlation,
                            rm=i,
                            rf=rf,
                            linkage=linkage,
                            max_k=max_k,
                            obj='Sharpe',  # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
                            leaf_order=leaf_order)


        #ax = rp.plot_pie(w=w,
        #            title='HERC Naive Risk Parity: risk model: ' + i,
        #            others=0.05,
        #            nrow=25,
        #            cmap="tab20",
        #            height=5,
        #            width=6,
        #            ax=None)
        #plt.show()

        #ax = rp.plot_drawdown(returns=Y,
        #                w=w,
        #                alpha=0.05,
        #                height=8,
        #                width=10,
        #                ax=None)

        #plt.show()


        #x = rp.plot_table(returns=Y,
        #            w=w,
        #            MAR=0,
        #            alpha=0.05,
        #            ax=None)


        #plt.show()

        w_s = pd.concat([w_s, w], axis=1)


    w_s.columns = rms
    w_s = w_s.replace('%', '', regex=True).astype(float) / 100
    w_s['MEAN'] = w_s.mean(axis=1)
    w_s.style.format("{:.2%}").background_gradient(cmap='YlGn')


    ##MEAN

    mean_values = w_s['MEAN']*100
    #print(mean_values)

    # array de NumPy
    mean_array = mean_values.to_numpy()
    weights = pd.Series(mean_array, index=assets)

    # estimar retornos y covarianza
    portafolio = rp.Portfolio(returns=Y)
    portafolio.weights = weights

    ax = rp.plot_pie(w=portafolio.weights,
                    title='HERC Naive Risk Parity',
                    others=0.05,
                    nrow=25,
                    cmap="tab20",
                    height=5,
                    width=6,
                    ax=None)
    
    for text in ax.texts:
        text.set_color('white')  # texto blanco
        text.set_bbox(dict(facecolor='black', edgecolor='none', boxstyle='round,pad=0.3'))

    plt.savefig(path_riskfolio + "herc_pie.png")
    plt.close()

    ax = rp.plot_drawdown(returns=Y,
                        w=portafolio.weights,
                        alpha=0.05,
                        height=8,
                        width=10,
                        ax=None)
    plt.savefig(path_riskfolio + "herc_drawdown.png")
    plt.close()


    ax = rp.plot_table(returns=Y,
                    w=w,
                    MAR=0,
                    alpha=0.05,
                    ax=None)


    plt.savefig(path_riskfolio + "herc_table.png")
    plt.close()


    ################################## NCO #####################################

    # Risk Measures available:
    #
    # 'vol': Standard Deviation.
    # 'MV': Variance.
    # 'MAD': Mean Absolute Deviation.
    # 'MSV': Semi Standard Deviation.
    # 'FLPM': First Lower Partial Moment (Omega Ratio).
    # 'SLPM': Second Lower Partial Moment (Sortino Ratio).
    # 'VaR': Conditional Value at Risk.
    # 'CVaR': Conditional Value at Risk.
    # 'EVaR': Entropic Value at Risk.
    # 'WR': Worst Realization (Minimax)
    # 'MDD': Maximum Drawdown of uncompounded cumulative returns (Calmar Ratio).
    # 'ADD': Average Drawdown of uncompounded cumulative returns.
    # 'DaR': Drawdown at Risk of uncompounded cumulative returns.
    # 'CDaR': Conditional Drawdown at Risk of uncompounded cumulative returns.
    # 'EDaR': Entropic Drawdown at Risk of uncompounded cumulative returns.
    # 'UCI': Ulcer Index of uncompounded cumulative returns.
    # 'MDD_Rel': Maximum Drawdown of compounded cumulative returns (Calmar Ratio).
    # 'ADD_Rel': Average Drawdown of compounded cumulative returns.
    # 'DaR_Rel': Drawdown at Risk of compounded cumulative returns.
    # 'CDaR_Rel': Conditional Drawdown at Risk of compounded cumulative returns.
    # 'EDaR_Rel': Entropic Drawdown at Risk of compounded cumulative returns.
    # 'UCI_Rel': Ulcer Index of compounded cumulative returns.

    rms = ['vol', 'MV', 'MAD', 'MSV', 'FLPM', 'SLPM',
        'VaR','CVaR', 'EVaR', 'WR', 'MDD', 'ADD',
        'DaR', 'CDaR', 'EDaR', 'UCI', 'MDD_Rel', 'ADD_Rel',
        'DaR_Rel', 'CDaR_Rel', 'EDaR_Rel', 'UCI_Rel']


    rms = ['MV', 'MAD', 'MSV', 'FLPM', 'SLPM',
        'CVaR', 'EVaR', 'WR', 'MDD', 'ADD',
            'CDaR', 'UCI']


    w_s = pd.DataFrame([])

    model = 'NCO'
    rf = 0 # Risk free rate
    linkage = 'ward' # Linkage method used to build clusters
    max_k = 10 # Max number of clusters used in two difference gap statistic
    leaf_order = True # Consider optimal order of leafs in dendrogram


    for i in rms:

        w = port.optimization(model=model,
                            #correlation=correlation,
                            rm=i,
                            rf=rf,
                            linkage=linkage,
                            max_k=max_k,
                            obj='Sharpe',  # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
                            leaf_order=leaf_order)


        #ax = rp.plot_pie(w=w,
        #            title='HERC Naive Risk Parity: risk model: ' + i,
        #            others=0.05,
        #            nrow=25,
        #            cmap="tab20",
        #            height=5,
        #            width=6,
        #            ax=None)
        #plt.show()

        #ax = rp.plot_drawdown(returns=Y,
        #                w=w,
        #                alpha=0.05,
        #                height=8,
        #                width=10,
        #                ax=None)

        #plt.show()


        #x = rp.plot_table(returns=Y,
        #            w=w,
        #            MAR=0,
        #            alpha=0.05,
        #            ax=None)


        #plt.show()

        w_s = pd.concat([w_s, w], axis=1)


    w_s.columns = rms
    w_s = w_s.replace('%', '', regex=True).astype(float) / 100
    w_s['MEAN'] = w_s.mean(axis=1)
    w_s.style.format("{:.2%}").background_gradient(cmap='YlGn')

    ##MEAN

    mean_values = w_s['MEAN']*100
    #print(mean_values)

    # array de NumPy
    mean_array = mean_values.to_numpy()
    weights = pd.Series(mean_array, index=assets)

    # estimar retornos y covarianza
    portafolio = rp.Portfolio(returns=Y)
    portafolio.weights = weights

    ax = rp.plot_pie(w=portafolio.weights,
                    title='NCO',
                    others=0.05,
                    nrow=25,
                    cmap="tab20",
                    height=5,
                    width=6,
                    ax=None)
    for text in ax.texts:
        text.set_color('white')  # texto blanco
        text.set_bbox(dict(facecolor='black', edgecolor='none', boxstyle='round,pad=0.3'))
    
    
    plt.savefig(path_riskfolio + "nco_pie.png")
    plt.close()

    ax = rp.plot_drawdown(returns=Y,
                        w=portafolio.weights,
                        alpha=0.05,
                        height=8,
                        width=10,
                        ax=None)
    plt.savefig(path_riskfolio + "nco_drawdown.png")
    plt.close()


    ax = rp.plot_table(returns=Y,
                    w=w,
                    MAR=0,
                    alpha=0.05,
                    ax=None)
    plt.savefig(path_riskfolio + "nco_table.png")
    plt.close()



#path_base       = "C:/users/mrella/OneDrive - Consorci Administració Oberta de Catalunya/Inversion/FinanceMR/"
#path_riskfolio = path_base + "riskfolio/"
#assets = ["XLK", "TLT", "GOLD", "BILL", "SPY", "IWM", "IWO", "KWEB"]
#generar_graficos(path_riskfolio, assets)


# Tickers of assets
    #assets = ['JCI', 'TGT', 'CMCSA', 'CPB', 'MO', 'APA', 'MMC', 'JPM',
    #        'ZION', 'PSA', 'BAX', 'BMY', 'LUV', 'PCAR', 'TXT', 'TMO',
    #        'DE', 'MSFT', 'HPQ', 'SEE', 'VZ', 'CNP', 'NI', 'T', 'BA']
    #assets = ["IWM", "VWO","SPY", "MOAT"]
    #assets = ["XLE", "XLK","SPY", "MOAT","IWM", "VWO"]
    #assets = ["SPY", "REIT","IWM", "TLT", "VWO"]
    #assets = ["XLK","SPY", "BABA", "JD","IWM", "VWO", "NGD", "KWEB", "MOAT", "GOOGL", "META"]
    #assets = ["XLK","SPY", "IWM", "VWO", "GOLD", "KWEB"]


    #assets = [
    #    "AAPL","ABNB","ADBE","ADI","ADP","ADSK","AEP","AMAT","AMD","AMGN",
    #    "AMZN","ANSS","APP","ARM","ASML","AVGO","AXON","AZN","BIIB","BKNG",
    #    "BKR","CCEP","CDNS","CDW","CEG","CHTR","CMCSA","COST","CPRT","CRWD",
    #    "CSCO","CSGP","CSX","CTAS","CTSH","DASH","DDOG","DXCM","EA","EXC",
    #    "FANG","FAST","FTNT","GEHC","GFS","GILD","GOOG","GOOGL","HON","IDXX",
    #    "INTC","INTU","ISRG","KDP","KHC","KLAC","LIN","LRCX","LULU","MAR",
    #    "MCHP","MDLZ","MELI","META","MNST","MRVL","MSFT","MSTR","MU","NFLX",
    #    "NVDA","NXPI","ODFL","ON","ORLY","PANW","PAYX","PCAR","PDD","PEP",
    #    "PLTR","PYPL","QCOM","REGN","ROP","ROST","SBUX","SHOP","SNPS","TEAM",
    #    "TMUS","TSLA","TTD","TTWO","TXN","VRSK","VRTX","WBD","WDAY","XEL","ZS"
    #]





