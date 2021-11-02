import pandas as pd
from tabulate import tabulate

# create source dataframe from raw data
sourceFundsDf = pd.read_csv('MutualFunds.csv')

# get only required columns for the top 20 stock data process.
workSelectDF = sourceFundsDf[['fund_symbol','top10_holdings']]

# split the stocks from one column to 10 columns
workSplitStocksDF = pd.concat([workSelectDF[['fund_symbol']],
                               workSelectDF['top10_holdings'].str.split(r'[0-9],', expand=True).add_prefix('Stocks')], axis=1)

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

# Get Top 20 stocks from all funds
Top10StocksDF = workStockPercentDF['StockName'].\
    value_counts().rename_axis('StockName').\
    reset_index(name='NoOfPresence').head(20)

# Top 20 stocks (all funds)
print(tabulate(Top10StocksDF,headers=['Stock Name','No of Presence']))

# Now Let's get the best fund names.
sizeList = ['Large','Medium']
workGetBestFundsDF = sourceFundsDf[(sourceFundsDf['inception_date'] < '2010-01-01')].\
    query("rating == 5 and return_rating == 5 and risk_rating == 5").\
    query('size_type in @sizeList').\
    query('fund_return_ytd > 10.0 and fund_return_1year > 10.0').\
    query('fund_return_3years > 10.0 and fund_return_5years > 10.0'). \
    query('fund_return_10years > 10.0').\
    query('years_down < 5').\
    sort_values(by=['fund_return_10years'], ascending=False).head(20)

# Print best performing funds
BestFundsDF = workGetBestFundsDF [['fund_symbol','fund_extended_name','fund_family']]
print(tabulate(BestFundsDF,headers=BestFundsDF.columns))

# Focus on Gem stocks from best funds
workGemStocksDF = pd.concat([workGetBestFundsDF['top10_holdings'].str.split(', ', expand=True).
                            add_prefix('Stocks')], axis=1)

workGemStocksPivotDf = (workGemStocksDF.melt(
             var_name='Stock',
             value_name='StockNamePercent')
        .query("StockNamePercent.notnull()")).drop(columns=['Stock'])

workGemStocksPercentDf = workGemStocksPivotDf['StockNamePercent'].\
                                    str.split(':', expand=True).\
                                    add_prefix('A')

workGemStocksPercentDf.rename({'A0':'StockName', 'A1':'Percent'}, axis='columns',inplace=True)

# Get Top 20 stocks from best funds and exclude from our Top20 stock(all) list
# Remove well known stocks
print("TopGemStocksDF - But filter out pending")
TopGemStocksDF = workGemStocksPercentDf['StockName'].\
    value_counts().rename_axis('StockName').\
    reset_index(name='NoOfPresence')

TopGemStocksExclDF = TopGemStocksDF[~(TopGemStocksDF['StockName'].isin(Top10StocksDF['StockName']))].head(20)
print(tabulate(TopGemStocksExclDF,headers=['Stock Name','No of Presence']))

# Now Let's get the worst performing fund names.
sizeList = ['Large','Medium']
workGetWorstFundsDF = sourceFundsDf[(sourceFundsDf['inception_date'] < '2010-01-01')].\
    query('size_type in @sizeList'). \
    query('fund_return_10years < 0.0'). \
    query('fund_return_3years < 0.0 and fund_return_5years < 0.0'). \
    sort_values(by=['fund_return_10years'], ascending=True)

print(tabulate(workGetWorstFundsDF[['fund_extended_name','fund_return_10years']].head(20),
               headers=['Stock Name','10 Year Return %']))

sourceTickerDf = pd.read_csv('NASDAQ_Ticker_info.csv')
workTickerDf = sourceTickerDf[(sourceTickerDf['Country'] == 'United States')]
workTickerDf = workTickerDf[['Symbol','Name']]
workTickerDf['Name'] = workTickerDf['Name'].str.replace(' Common Stock', '')

#print(workTickerDf)
