import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'www.kabum.com.br',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
}

# pagina_atual = [str("https://www.kabum.com.br/hardware/processadores?page_number={}&page_size=100&facet_filters=&sort=offer_price").format(i) for i in range(1, 9)]

pagina_atual = [str("https://www.kabum.com.br/hardware/placa-de-video-vga?page_number={}&page_size=100&facet_filters=&sort=offer_price").format(i) for i in range(1, 15)]

product_link = []
product_name = []
product_price = []

for link in pagina_atual:
    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    products = soup.find_all(class_='productCard')

    for product in products:
        product_path = (product.find('a'))['href']
        product_link.append(f"https://www.kabum.com.br{product_path}")

        name = product.find(class_='nameCard')
        product_name.append(name.text.strip())

        price = product.find(class_='priceCard')
        price_text = price.text.strip()
        price_digits = re.sub(r'[^0-9]', '', price_text)

        if price_digits:
            product_price.append(float(price_digits) / 100) # dividindo por 100 pra ajustar a representação em centavos
        else:
            product_price.append(None)  # Adiciona None se não houver preço válido

# Criando DataFrame
df = pd.DataFrame({"Link": product_link, "Nome": product_name, "Preço": product_price})

# CSV
df.to_csv('placa_de_video2.csv')
