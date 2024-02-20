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
def preco_de_frase_arial(frase_arialabel):
    frase_arialabel = frase_arialabel.split()
    preco_int_list = list(filter(lambda x:x.isdigit(), frase_arialabel))
    preco_flaot = float('.'.join(preco_int_list))
    return preco_flaot



FILE_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = FILE_PATH /'lista_produtos.txt'
LINK = 'https://www.mercadolivre.com.br/'

with open(INPUT_PATH, 'r') as file:
    lista_de_produtos = file.readlines()

lista_de_produtos =list(map(lambda x: x.replace('\n',' olist'), lista_de_produtos))
print('produtos:', lista_de_produtos)


# driver=create_driver()
driver=create_undetected_driver()

itens_df = pd.DataFrame(columns=['nome', 'pix', 'prazo', 'frase', 'link'])


#driver.get(LINK)ui-search-item__group ui-search-item__group--title

for produto_input in lista_de_produtos:


    driver.get(LINK)
    time.sleep(1)


    print('Presquisando: ', produto_input)
    
    barra_pesquisa = driver.find_element(By.CSS_SELECTOR, "input[class='nav-search-input']")
    barra_pesquisa.send_keys(produto_input)
    time.sleep(1)
    barra_pesquisa.send_keys(Keys.ENTER)
    time.sleep(2)
    
    produto_input = produto_input.split()
    
    # input('Pressione ENTER para continuar... Selecionando o produto...')
    

    produto_lista_pagina = driver.find_elements(
        By.CSS_SELECTOR, 'li[class="ui-search-layout__item"]')

    if len(produto_lista_pagina)==0:
        produtos_lista = driver.find_element(By.CSS_SELECTOR, 'ol[class="ui-search-layout ui-search-layout--stack shops__layout"]')
        produto_lista_pagina = produtos_lista.find_elements(
        By.CSS_SELECTOR, 'li[class="ui-search-layout__item shops__layout-item ui-search-layout__stack"]')
    print(produto_lista_pagina)
    
# ui-search-item__group__element ui-search-link__title-card ui-search-link
    # errado = False

    time.sleep(1)

    for produto_pesquisado in produto_lista_pagina:

        
        # titulo_produto=espera_elemento_presente(By.CSS_SELECTOR,
        #                                         'div[class="ui-search-item__group ui-search-item__group--title"]', produto_pesquisado)
        
        titulo_produto = espera_elemento_presente(By.CSS_SELECTOR,
                                                   'a[class="ui-search-item__group__element ui-search-link__title-card ui-search-link"]',produto_pesquisado).text
        

        titulo_filtrado = list(filter(lambda x: x.lower() in titulo_produto.lower(), produto_input))

        not_complete_name_in_title = len(titulo_filtrado) != len(produto_input)
        
        if not_complete_name_in_title: 
            continue 
        else: 
            break
        # for palavra in produto_input:
        #     if not palavra.lower() in titulo_produto.lower():
        #         errado = True

        # if errado == True:
        #     errado = False
        #     continue

       
    


    preco_elemento = produto_pesquisado.find_element(By.CSS_SELECTOR,
                                    'span[class="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"]')
    preco_elemento=preco_elemento.get_attribute('aria-label')
    preco_flaot = preco_de_frase_arial(preco_elemento)

    preco_parcelado = produto_pesquisado.find_element(By.CSS_SELECTOR,
                                    'span[class="andes-money-amount ui-search-price__part ui-search-price__part--x-tiny andes-money-amount--cents-superscript andes-money-amount--compact"]')
    preco_parcelado=preco_parcelado.get_attribute('aria-label')
    preco_parcelado_flaot = preco_de_frase_arial(preco_parcelado)

    try:
        frase_parcelado = produto_pesquisado.find_element(By.CSS_SELECTOR,
                                    'span[class="ui-search-item__group__element ui-search-installments ui-search-color--BLACK"]').text
    except:
         frase_parcelado = produto_pesquisado.find_element(By.CSS_SELECTOR,
                                    'span[class="ui-search-item__group__element ui-search-installments ui-search-color--LIGHT_GREEN"]').text
    frase_parcelado=frase_parcelado.replace('\n',' ')
    vezes_parcelado = int(frase_parcelado.split()[1].replace('x',''))

    link_produto = produto_pesquisado.find_element(By.CSS_SELECTOR,
                                    'a[class="ui-search-item__group__element ui-search-link__title-card ui-search-link"]').get_attribute('href')

    print('titulo_produto:',titulo_produto)
    print('vezes_parcelado:',vezes_parcelado)
    print('Frase_parcelamento:',frase_parcelado)
    print('preco parcelado:  ',preco_parcelado_flaot)
    print('preco:  ',preco_flaot)
    print('link_produto:',link_produto)
    # input('Enter para continuar')
    preco = preco_elemento

    itens_df = pd.concat([itens_df, pd.DataFrame([{
    'nome': titulo_produto,
    'pix': preco_flaot,
    'prazo': float(f'{preco_parcelado_flaot*vezes_parcelado:.2f}'),
    'frase': preco_parcelado,
    'link': link_produto
}])], ignore_index=True)

#     itens_df = itens_df.append({
#         'nome': titulo_produto,
#         'pix': preco_flaot,
#         'prazo': float(f'{preco_parcelado_flaot*vezes_parcelado:.2f}'),
#         'frase': preco_parcelado,
#         'link': link_produto
#     }, ignore_index=True)
# 'nome', 'pix', 'prazo', 'frase','link'



    

   
# with open('produtos.txt', 'a+') as file:
#     file.write(f'Produto: {titulo_produto}-Preco:{preco} reais\n')
# # print(produto_pesquisado.text)
# print(titulo_produto, preco)

itens_df.to_excel(FILE_PATH/ 'resultados'/ 'mercadolivre.xlsx')
input('Enter para finalizar')
driver.quit()