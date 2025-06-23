import requests
import mstarpy
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import matplotlib.pyplot as plt2

import seaborn as sns
sns.set_theme(style="darkgrid", palette="muted", font_scale=1.1)

import warnings
warnings.filterwarnings('ignore')

def generar_graficos(path):

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
            */*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8,es-ES;q=0.5,es;q=0.3",
            "Cache-Control": "no-cache", "dnt": "1",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0)\
            Gecko/20100101 Firefox/93.0"}


    #OBTENCIÓN DE LOS DATOS DE FONDOS EN BRUTO
    secids = []
    names = []
    returns = []
    holdings = []
    for page in range(1, 3):
        url = 'https://lt.morningstar.com/api/rest.svc/klr5zyak8x/security/screener?page=' + str(page) + '&pageSize=50&sortOrder=ReturnM120%20desc&outputType=json&version=1&languageId=es-ES&currencyId=EUR&universeIds=FOESP%24%24ALL&securityDataPoints=SecId%7CName%7CPriceCurrency%7CTenforeId%7CLegalName%7CClosePrice%7CYield_M12%7CCategoryName%7CAnalystRatingScale%7CStarRatingM255%7CQuantitativeRating%7CSustainabilityRank%7CReturnD1%7CReturnW1%7CReturnM1%7CReturnM3%7CReturnM6%7CReturnM0%7CReturnM12%7CReturnM36%7CReturnM60%7CReturnM120%7CFeeLevel%7CManagerTenure%7CMaxDeferredLoad%7CInitialPurchase%7CFundTNAV%7CEquityStyleBox%7CBondStyleBox%7CAverageMarketCapital%7CAverageCreditQualityCode%7CEffectiveDuration%7CMorningstarRiskM255%7CAlphaM36%7CBetaM36%7CR2M36%7CStandardDeviationM36%7CSharpeM36%7CTrackRecordExtension&filters=&term=&subUniverseId='
        req = requests.get(url, headers=headers)
        funds_json = req.json()
        for row in funds_json['rows']:
            category = row['CategoryName']
            if 'RV' in category:
                secid = row['SecId']
                secids.append(secid)
                name = row['LegalName']
                names.append(name)
                return120 = row['ReturnM120']
                returns.append(return120)
                fund = mstarpy.Funds(term=secid)
                df = fund.holdings(holdingType="equity")
                df = df[df['country']=='United States']
                df = df.head(10)
                holdings.append(df['ticker'].tolist())

        df_funds = pd.DataFrame({'Id': secids, 'Fund': names, 'Return10A': returns, 'Stocks': holdings})
    #df_funds.head(5)


    #LIMPIADO DE DUPLICADOS DE FONDOS CON VARIAS CLASES
    funds_list = df_funds['Fund'].tolist()
    i = 0
    while i < len(funds_list):
        j = i + 1
        while j < len(funds_list):
            similarity_ratio = fuzz.ratio(funds_list[i], funds_list[j])
            if similarity_ratio > 85:
                del funds_list[j]
            else:
                j += 1
        i += 1
    df_funds = df_funds[df_funds['Fund'].isin(funds_list)]
    #df_funds.head(5)

    #LIMPIADO DE FONDOS SIN ACCIONES AMERICANAS
    df_funds['Stocks'] = np.where(df_funds['Stocks'].apply(len) > 0, df_funds['Stocks'], None)
    df_funds = df_funds.dropna()
    #df_funds.head(5)

    #OBTENCIÓN DE LA LISTA CON TODAS LAS APARICIONES
    stocks_list = df_funds['Stocks'].tolist()
    stocks_list = [element for sublist in stocks_list for element in sublist]

    #RECUENTO DE APARICIONES
    df_stocks = pd.DataFrame({'Stock': stocks_list})
    df_stocks = df_stocks['Stock'].value_counts().reset_index()
    df_stocks.columns = ['Stock', 'Appearances']
    #df_stocks.head(10)

    #VISUALIZACIÓN
    plt2.barh(df_stocks['Stock'].head(20), df_stocks['Appearances'].head(20), color='orange')
    plt2.gca().invert_yaxis()
    plt2.tight_layout()
    # Reducir tamaño de letra de los ejes
    plt2.yticks(fontsize=8)
    plt2.xticks(fontsize=8)
    plt2.savefig(path + 'best_stocks.png')


#generar_graficos("C:/users/mrella/OneDrive - Consorci Administració Oberta de Catalunya/Inversion/FinanceMR/best_stocks/best_stocks.png")