import os
import yfinance as yf
import time as time
import pandas as pd
import glob
import numpy as np
import shutil
import logging

def downloadStockData() :
    
    indir = './dir/stage'
    
    tickerFile = 'Ticker.csv'
    
    tickerDf = pd.read_csv(os.path.join(indir, tickerFile), delimiter= "|")
    
    logging.info(tickerDf.head())
    
    for i,tick in tickerDf.iterrows():

        ticker = tick['Ticker']
        tickData = yf.download(ticker)
        
        logging.info(tickData.head())
        
        tickData['Ticker'] = tick['Ticker']

        timestr = time.strftime("%Y%m%d-%H%M%S")

        outname = f"{ticker}_{timestr}.csv"
        outdir = './dir/download'
    
        if not os.path.exists(outdir):
            os.mkdir(outdir)

        fullname = os.path.join(outdir, outname)  
        
        logging.info('Ticker stock data path: ' + fullname)  

        tickData.to_csv(fullname)
        
        
def rma(x, n):
    """Running moving average"""
    a = np.full_like(x, np.nan)
    a[n] = x[1:n+1].mean()
    for i in range(n+1, len(x)):
        a[i] = (a[i-1] * (n - 1) + x[i]) / n
    return a
        
        
def stockDataAgg() :
    indir = './dir/download/*.csv'
    outdir = "./dir/agg"
    
    stockDataAggDf = pd.DataFrame()
    
    for fname in glob.glob(indir):
        
        logging.info('Ticker stock data agg path: ' + fname)  
        
        stockDatafileDf = pd.read_csv(fname, delimiter= ",")
        
        cols = stockDatafileDf.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        stockDatafileDf = stockDatafileDf[cols]
        
        stockDatafileDf['change'] = stockDatafileDf['Close'].diff()
        stockDatafileDf['gain'] = stockDatafileDf.change.mask(stockDatafileDf.change < 0, 0.0)
        stockDatafileDf['loss'] = -stockDatafileDf.change.mask(stockDatafileDf.change > 0, -0.0)

        stockDatafileDf['avg_gain'] = rma(stockDatafileDf.gain.to_numpy(), 14)
        stockDatafileDf['avg_loss'] = rma(stockDatafileDf.loss.to_numpy(), 14)

        stockDatafileDf['rs'] = stockDatafileDf.avg_gain / stockDatafileDf.avg_loss
        stockDatafileDf['rsi'] = 100 - (100 / (1 + stockDatafileDf.rs))
        
        stockDataAggDf = pd.concat([stockDataAggDf,stockDatafileDf],ignore_index=True)
        
    stockDataAggDf = stockDataAggDf.drop_duplicates()
    
    
    timestr = time.strftime("%Y%m%d-%H%M%S")

    outname = f"stockDataResults_{timestr}.csv"
    
    
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    fullname = os.path.join(outdir, outname)    
    
    
    logging.info('stock agg results path: ' + fullname)  

    stockDataAggDf.to_csv(fullname)
    
    
    
def clearDownloadDir():
    dir = './dir/download'
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
#downloadStockData()
#stockDataAgg()
#clearDownloadDir()