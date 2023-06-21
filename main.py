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

pagina_atual = [str("https://www.kabum.com.br/hardware/processadores?page_number={}&page_size=100&facet_filters=&sort=offer_price").format(i) for i in range(1, 9)]

# pagina_atual = [str("https://www.kabum.com.br/hardware/placa-de-video-vga?page_number={}&page_size=100&facet_filters=&sort=offer_price").format(i) for i in range(1, 15)]

product_link = []
product_name = []
product_price = []

for link in pagina_atual:
    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    products = soup.find_all(class_='productCard')

    for product in products:
        product_path = (product.find('a'))['href']
        match = re.search(r'(/produto/\d+)', product_path) #retornar apenas o numero dos produtos
        if match:
            product_path = match.group(1)
        product_link.append(f"https://www.kabum.com.br{product_path}")

        name = product.find(class_='nameCard')
        product_name.append(name.text.strip())

        price = product.find(class_='priceCard')
        price_text = price.text.strip()

        if price_text == "R$ ---":
            product_price.append(None) # retorna nan caso o produto esteja esgotado (algo deu errado, revisar)
        else:
            product_price.append(price_text)  # Mantém o preço como string

# Criando DataFrame
df = pd.DataFrame({"Link": product_link, "Nome": product_name, "Preço": product_price}, columns=["Link", "Nome", "Preço"])

# CSV
df.to_csv('processadores.csv')

