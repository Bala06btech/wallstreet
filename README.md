# Wallstreet

## Let's follow the money
My friend and I always wanted to play around with Wallstreet data and see if we can get some insights, ok as usual started googling for dataset and as usual ended up getting from Kaggle. As we all know Kaggle will pretty cleaned up data than real world production scenario. Lets go with this data for now. Specifically we wanted understand which stocks were popular among fund managers. 

### Total Funds
After quick clean up and initial data parsing end up with total number of funds, a whopping **23355** funds are available in our dataset.

### Top 20 Stocks
Now comes to the initial question which stocks are loved by the all the fund managers irrespective of their fund status. 

![image](https://user-images.githubusercontent.com/19653585/139564370-56580aea-1d32-4bda-ae1e-7e8c13d224cc.png)

Duh !! Looks like familiar names which are mostly familiar among us. 

### Top 20 Funds
Time to focus on Funds and find the successfull funds from them. Time to filter out gem of gem from 23000+ available funds. See which ones are successfull over the years and provided to get good return consistently and didn't have so many down years and finally ended up with **20 Funds** 

![image](https://user-images.githubusercontent.com/19653585/139563981-1e9b775e-8df8-410a-ad8d-6012d3d72444.png)

### Gem Stocks from Top funds

![image](https://user-images.githubusercontent.com/19653585/139565806-1a3cd53f-d02e-4658-976f-b11e663a294b.png)

### Worst Performing Funds

![image](https://user-images.githubusercontent.com/19653585/139591372-d68414db-12e4-4401-bdb7-5bb58bc8a93a.png)


## Resources
https://www.kaggle.com/stefanoleone992/mutual-funds-and-etfs
https://www.nasdaq.com/market-activity/stocks/screener


## Work In Progress
1. Parsing all stocks and percentage into different columns from "top10_holdings" can be function.
2. Analysing individual stocks 
