import yfinance as yf
import sys
sys.path.append(r"C:\Users\SHWETA\Sentiment_analysis")
from logs.logger_config import setup_logger

logger = setup_logger(__name__)

def stock_prices(ticker_symbol,start_date,end_date):
    try:
        data = yf.download(ticker_symbol,start=start_date,end=end_date)
        logger.info(f"Stocks data generated for {ticker_symbol}")
        return data
    except Exception as e:
        logger.exception(f"Can't generate stock data for {ticker_symbol} :{e}")