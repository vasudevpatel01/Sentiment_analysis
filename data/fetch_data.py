import requests
import pandas as pd
import sys
sys.path.append(r'C:\Users\SHWETA\Sentiment_analysis')
from config.api_config import API_CONFIG
from requests.exceptions import RequestException
from logs.logger_config import setup_logger
from langdetect import detect
from googletrans import Translator

logger = setup_logger(__name__)


class Fetch_data():
    def __init__(self,entity,start_Date,sortBy='popularity'):
        self.entity = entity
        self.url = (f"{API_CONFIG['base_url']}"
                    f"q={entity}&"
                    f"from={start_Date}&"
                    f"sortBy={sortBy}&"
                    f"pageSize=100&"
                    f"page=1&"
                    f"apiKey={API_CONFIG['api_key']}")

    
    def get_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()
            logger.info("Data fetched successfully")
            return data
               
        except RequestException as e:
            logger.exception(f"Error in fetching data {e} for {self.entity}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occured")
            return None
        
        
            
    def create_dataframe(self,data):
        try:
            if data and 'articles' in data:
                article = []
                for art in data.get('articles'):
                    article.append({
                        'entity' : self.entity,
                        'title' : art.get('title'),
                        'description' : art.get('description'),
                        'date' : art.get('publishedAt')[:10],
                        'content' : art.get('content')

                    })

                df = pd.DataFrame(article)
                logger.info(f"DataFrame created with {len(df)} rows")
                return df
            else:
                logger.warning("No articles found in data")
                return pd.DataFrame()
        except Exception as e:
            logger.exception(f"Error while creating DataFrame: {e}")
            return pd.DataFrame()
        
    
    def get_translated_df(self,data):
        df = self.create_dataframe(data)
        translator = Translator()
        title_translated = []

        for i, text in enumerate(df['title']):
            try:
                text = str(text)
                lang = detect(text)
                if lang != 'en' and text.strip() != '':
                    text_en = translator.translate(text,dest='en').text
                else:
                    text_en = text
            except Exception as e:
                text_en = text
                logger.exception(f"Title Translation failed at {i} index : {e}")
                
            title_translated.append(text_en)
        
        df['title_en'] = title_translated
        logger.info("Titles Translated Succsessfully")
        
        
        description_translated = []


        for i, text in enumerate(df['description']):
            text = str(text)
            try:
                lang = detect(text)
                if lang != 'en' and text.strip() != '':
                    text_en = translator.translate(text,dest='en').text
                else:
                    text_en =text
            except Exception as e:
                text_en = text
                print(f"Description Translation failed at {i}th index : {e}")

            description_translated.append(text_en)

        df['description_en'] = description_translated
        logger.info("Descriptions Translated Succesfully")

        logger.info("DataFrame created successfully!")
        return df







