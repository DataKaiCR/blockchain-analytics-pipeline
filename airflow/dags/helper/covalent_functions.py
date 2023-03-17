import os
import json
from dotenv import load_dotenv

load_dotenv()
dotenvpath = os.path.join(os.path.dirname(__file__), 'config')
load_dotenv(dotenvpath)

# API_KEY = os.getenv('COVALENT_API_KEY')
API_KEY = 'ckey_8e5235567a2b47ad937b2a86eba'

def get_transactions_for_address_v2_url(chain, address, page_number, page_size):

    endpoint = f'{chain}/address/{address}/transactions_v2/'
    url = f'https://api.covalenthq.com/v1/{endpoint}?key={API_KEY}'
    url_extended = f'{url}&page-number={page_number}&page-size={page_size}'

    return url_extended

async def get_results(session, url):
    pass
    # async with session.get(url) as response:
    #     result = await response.json()
    #     return result