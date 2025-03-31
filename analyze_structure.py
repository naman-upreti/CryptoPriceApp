import requests
from bs4 import BeautifulSoup
import json

try:
    print('Fetching data from CoinMarketCap...')
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')
    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    if data:
        print('Found __NEXT_DATA__ script tag')
        coin_data = json.loads(data.contents[0])
        print('\nJSON Structure:')
        for key in coin_data.keys():
            print(f'- {key}')
        
        if 'props' in coin_data:
            print('\nProps Structure:')
            for key in coin_data['props'].keys():
                print(f'- {key}')
            
            if 'initialState' in coin_data['props']:
                print('\nInitialState Structure:')
                for key in coin_data['props']['initialState'].keys():
                    print(f'- {key}')
                
                if 'cryptocurrency' in coin_data['props']['initialState']:
                    print('\nCryptocurrency Structure:')
                    for key in coin_data['props']['initialState']['cryptocurrency'].keys():
                        print(f'- {key}')
                    
                    # Check if listingLatest exists and its structure
                    if 'listingLatest' in coin_data['props']['initialState']['cryptocurrency']:
                        print('\nListingLatest Structure:')
                        for key in coin_data['props']['initialState']['cryptocurrency']['listingLatest'].keys():
                            print(f'- {key}')
                            
                        # Check the data structure inside listingLatest
                        if 'data' in coin_data['props']['initialState']['cryptocurrency']['listingLatest']:
                            print('\nData exists in listingLatest')
                            print(f"Data type: {type(coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data'])}")
                            if isinstance(coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data'], list):
                                print(f"Data length: {len(coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data'])}")
                                if len(coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']) > 0:
                                    print('\nSample coin structure:')
                                    sample_coin = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data'][0]
                                    for key in sample_coin.keys():
                                        print(f'- {key}')
                            else:
                                print('Data is not a list. Showing keys:')
                                for key in coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data'].keys():
                                    print(f'- {key}')
    else:
        print('Could not find __NEXT_DATA__ script tag')
except Exception as e:
    print(f'Error: {str(e)}')