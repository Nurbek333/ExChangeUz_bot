import requests

# API kalitni sozlash
API_KEY = 'e60f1dfbf1e1110fd527af5b91f1e97a79cff8bfa7686bf61d126c7a69c29580'

# Kriptovalyuta narxlarini olish funksiyasi
def get_crypto_prices():
    url = 'https://min-api.cryptocompare.com/data/pricemulti'
    parameters = {
        'fsyms': 'BTC,ETH,USDT,BNB,SOL,XRP,USDC,DOGE,TON,ADA,SHIB,AVAX,TRX,DOT,LTC,MATIC',
        'tsyms': 'USD'
    }
    headers = {
        'Authorization': f'Apikey {API_KEY}'
    }
    response = requests.get(url, headers=headers, params=parameters)
    return response.json()


