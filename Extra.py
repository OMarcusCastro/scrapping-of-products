#%%
import time
import os

import pandas as pd

from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from driver.driver_init import create_driver,create_undetected_driver, espera_elemento_presente
from funcoes.produtos import Item, junta_dataframes
from funcoes.produtos import rs_element_to_float, a_prazo

#%%
# =============================================================================

FILE_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = FILE_PATH /'lista_produtos.txt'
LINK = 'https://www.extra.com.br/'

with open(INPUT_PATH, 'r') as file:
    lista_de_produtos = file.readlines()


# driver=create_driver()
driver=create_undetected_driver()
itens_df = pd.DataFrame(columns=['nome', 'pix', 'prazo', 'frase'])

driver.get(LINK)

for produto in lista_de_produtos:

    time.sleep(1)
    print('link: ', driver.current_url)

    # try:
    barra_de_pesquisa = espera_elemento_presente(
        By.ID, 'search-form-input',driver)

    produto = produto.replace('\n', '')
    produto = produto + ' olist '
    nome = produto
    for caractere in produto:
        barra_de_pesquisa.send_keys(caractere)
        time.sleep(0.03)  # Atraso de 0.3 segundos entre cada caractere

    time.sleep(2)
    barra_de_pesquisa.send_keys(Keys.ENTER)

    if '_erro' in driver.current_url:
        driver.back()
        # input('Erro ao carregar a página. Pressione ENTER para continuar...')
        time.sleep(3)
        continue
    time.sleep(3)
    # input('Pressione ENTER para continuar... Selecionando o produto...')
    elemento_divgrid = espera_elemento_presente(
        By.CSS_SELECTOR, 'div[data-cy="divGridProducts"]',driver)

    # input('Pressione ENTER para continuar... Selecionando o produto...')
    time.sleep(2)
    produto = elemento_divgrid.find_element(
        By.CSS_SELECTOR, 'div[data-testid="product-card-desktop"]')

    texto_produto = produto.find_element(By.TAG_NAME, 'h3').text
    print('Produto: ', texto_produto)
    time.sleep(2)
    precos = produto.find_element(
        By.CSS_SELECTOR, 'div[data-testid="product-card-installment"]')
    # input('Pressione ENTER para continuar... Achando precos...')
    time.sleep(1)
    preco_avista = rs_element_to_float(precos.find_element(By.TAG_NAME, 'b'))
    preco_aprazo = precos.find_element(By.TAG_NAME, 'span').text
    a_prazo(preco_aprazo)
    print('Preço à vista: ', preco_avista)

    print('Preço a prazo: ', preco_aprazo)
    print('Preço a prazo total: ', a_prazo(preco_aprazo))

    item = Item(nome, pix=preco_avista, prazo=a_prazo(
        preco_aprazo), frase=preco_aprazo)
    item.cria_df()
    itens_df = junta_dataframes(itens_df, item.df)

    # limpa_dados()
    time.sleep(2)

itens_df.to_excel(FILE_PATH/ 'resultados'/ 'extra.xlsx')


# %%
