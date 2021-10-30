import pandas as pd
from tabulate import tabulate

# create source dataframe from raw data
sourceFundsDf = pd.read_csv('MutualFunds.csv')

# get only required columns for the top 10 stock data process.
workSelectDF = sourceFundsDf[['fund_symbol','top10_holdings']]

# split the stocks from one column to 10 columns
workSplitStocksDF = pd.concat([workSelectDF[['fund_symbol']],
                               workSelectDF['top10_holdings'].str.split(', ', expand=True).add_prefix('Stocks')], axis=1)

# Let's pivot the multiple Stocks column into one
workPivotStocksDf = (workSplitStocksDF.melt(['fund_symbol'],
             var_name='Stock',
             value_name='StockNamePercent')
        .query("StockNamePercent.notnull()")).drop(columns=['Stock'])

workStockPercentDF = pd.concat([workPivotStocksDf[['fund_symbol']], workPivotStocksDf['StockNamePercent'].
                                    str.split(':', expand=True).
                                    add_prefix('A')], axis=1).drop(columns=['A2','A3'])

workStockPercentDF.rename({'A0':'StockName', 'A1':'Percent'}, axis='columns',inplace=True)

# Get Total number of distinct funds.
print("Total Funds ==> " , workStockPercentDF['fund_symbol'].nunique() )

# Get Top 10 stocks from all funds
Top10StocksDF = workStockPercentDF['StockName'].value_counts().head(10)
#print("Top 10 Stocks ")
#print(Top10StocksDF)
#print(workStockPercentDF['StockName'].value_counts(normalize=True))
#print(tabulate(workStockPercentCleanDF.head(5)))

#Now get the best fund names.
sizeList = ['Large','Medium']
workGetBestFundsDF = sourceFundsDf[(sourceFundsDf['inception_date'] < '2010-01-01')].\
    query("rating == 5 and return_rating == 5 and risk_rating == 5").\
    query('size_type in @sizeList').\
    query('fund_return_ytd > 10.0 and fund_return_1year > 10.0').\
    query('fund_return_3years > 10.0 and fund_return_5years > 10.0'). \
    query('fund_return_10years > 10.0').\
    query('years_down < 5')

BestFundsDF = workGetBestFundsDF [['fund_symbol','fund_extended_name','fund_family']]
print(tabulate(BestFundsDF))
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

sourceTickerDf = pd.read_csv('NASDAQ_Ticker_info.csv')

workTickerDf = sourceTickerDf[(sourceTickerDf['Country'] == 'United States')]
workTickerDf = workTickerDf[['Symbol','Name']]
workTickerDf['Name'] = workTickerDf['Name'].str.replace(' Common Stock', '')

print(workTickerDf)
