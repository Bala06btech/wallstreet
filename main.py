import pandas as pd
from tabulate import tabulate
import datetime

sourceDf = pd.read_csv('MutualFunds.csv')
workSelectDF = sourceDf[['fund_symbol','top10_holdings']]
workSplitStocksDF = pd.concat([workSelectDF[['fund_symbol']],
                               workSelectDF['top10_holdings'].str.split(', ', expand=True).add_prefix('Stocks')], axis=1)
#print(workSplitStocksDF.head(5))
workPivotStocksDf = (workSplitStocksDF.melt(['fund_symbol'],
             var_name='Stock',
             value_name='StockNamePercent')
        .query("StockNamePercent.notnull()")).drop(columns=['Stock'])

#print(workPivotStocksDf.head(5))
workStockPercentDF = pd.concat([workPivotStocksDf[['fund_symbol']], workPivotStocksDf['StockNamePercent'].
                                    str.split(':', expand=True).
                                    add_prefix('A')], axis=1).drop(columns=['A2','A3'])

workStockPercentDF.rename({'A0':'StockName', 'A1':'Percent'}, axis='columns',inplace=True)
#print(workStockPercentDF.head(5))

#Get Total distinct funds.
print("Total Funds ==> " )
#print(workStockPercentDF['fund_symbol'].nunique())
#print("***********")

#print(workStockPercentDF.query('fund_symbol == "AAAAX"'))
Top10StocksDF = workStockPercentDF['StockName'].value_counts().head(10)

#Now we have top stocks invested by more number of index. Duh!
print("Top 10 Stocks ")
#print(Top10StocksDF)
#print(workStockPercentDF['StockName'].value_counts(normalize=True))
#print(tabulate(workStockPercentCleanDF.head(5)))

#Now get the best fund names.
sizeList = ['Large','Medium']
workGetBestFundsDF = sourceDf[(sourceDf['inception_date'] < '2010-01-01')].\
    query("rating == 5 and return_rating == 5 and risk_rating == 5").\
    query('size_type in @sizeList').\
    query('fund_return_ytd > 10.0 and fund_return_1year > 10.0').\
    query('fund_return_3years > 10.0 and fund_return_5years > 10.0'). \
    query('fund_return_10years > 10.0').\
    query('years_down < 5')

BestFundsDF = workGetBestFundsDF [['fund_symbol','fund_extended_name','fund_family']]
#print(tabulate(BestFundsDF))
workGemStocksDF = pd.concat([workGetBestFundsDF['top10_holdings'].str.split(', ', expand=True).add_prefix('Stocks')], axis=1)

workGemStocksPivotDf = (workGemStocksDF.melt(
             var_name='Stock',
             value_name='StockNamePercent')
        .query("StockNamePercent.notnull()")).drop(columns=['Stock'])

workGemStocksPercentDf = workGemStocksPivotDf['StockNamePercent'].\
                                    str.split(':', expand=True).\
                                    add_prefix('A')

workGemStocksPercentDf.rename({'A0':'StockName', 'A1':'Percent'}, axis='columns',inplace=True)

#Remove well known stocks
TopGemStocksDF = workGemStocksPercentDf['StockName'].drop_duplicates()

#df3 = Top10GemStocksDF.merge(Top10StocksDF, on=['StockName'], how='inner')
print("TopGemStocksDF - But filter out pending")
#print(TopGemStocksDF)
