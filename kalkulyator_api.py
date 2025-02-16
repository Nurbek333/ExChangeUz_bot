import requests

API_KEY = 'e60f1dfbf1e1110fd527af5b91f1e97a79cff8bfa7686bf61d126c7a69c29580'

def get_crypto_price(crypto, currency="USD"):
    url = 'https://min-api.cryptocompare.com/data/pricemulti'
    parameters = {
        'fsyms': crypto,
        'tsyms': currency
    }
    headers = {
        'Authorization': f'Apikey {API_KEY}'
    }
    
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    if crypto in data and currency in data[crypto]:
        return data[crypto][currency]
    else:
        return None


def get_usd_to_uzs():
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        for currency in data:
            if currency["Ccy"] == "USD":
                return float(currency["Rate"])
    
    return None
