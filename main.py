from data.fetch_data import Fetch_data
from data.fetch_stocks import stock_prices
from logs.logger_config import setup_logger
import yfinance as yf
import pickle
import datetime

logger = setup_logger(__name__)

Entities = {'Tesla': 'TSLA','Alphabet':'GOOGL','Moderna':'MRNA','Apple':'AAPL','Boeing':'BA'}


def run_workflow():
    entity_dfs = {}
    entity_stocks = {}

    for entity,ticker in Entities.items():
        logger.info(f"Workflow started for {entity}")    
        fetch_data_obj = Fetch_data(entity,'2025-08-24')

        data = fetch_data_obj.get_data()
        entity_dfs[entity] = fetch_data_obj.get_translated_df(data)
            
        entity_stocks[entity] = stock_prices(ticker,'2025-08-23','2025-09-24')

        logger.info(f"Workflow completed for {entity} succesfully!")

    return entity_dfs,entity_stocks
    

if __name__=="__main__":
     entity_dfs,entity_stocks = run_workflow()


# with open(r'notebook/entity_data.pkl','wb') as f:

#     try:
#         pickle.dump((entity_dfs,entity_stocks),f)
#         logger.info(f"Data saved to entity_data.pkl")
#     except Exception as e:
#         logger.exception(f"Error : {e}")
        


# Generate timestamped filename
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = fr'notebook/entity_data_{timestamp}.pkl'

with open(filename, 'wb') as f:
    try:
        pickle.dump((entity_dfs, entity_stocks), f)
        logger.info(f"Data saved to {filename}")
    except Exception as e:
        logger.exception(f"Error while saving data: {e}")
