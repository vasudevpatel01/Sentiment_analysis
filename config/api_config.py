from dotenv import load_dotenv
import os
load_dotenv()



API_CONFIG = {
    "base_url" : r"https://newsapi.org/v2/everything?",
    "api_key" : os.getenv("NEWS_API_KEY")
}
