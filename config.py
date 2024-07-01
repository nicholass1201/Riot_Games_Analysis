import os
from dotenv import load_dotenv

load_dotenv()

riot_api_key = os.getenv('RIOT_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
