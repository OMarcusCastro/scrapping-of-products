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
LINK = 'https://www.americanas.com.br/'

with open(INPUT_PATH, 'r') as file:
    lista_de_produtos = file.readlines()

lista_de_produtos =list(map(lambda x: x.replace('\n',' olist'), lista_de_produtos))
# print('produtos:', lista_de_produtos)


# driver=create_driver()
driver=create_undetected_driver()

itens_df = pd.DataFrame(columns=['nome', 'pix', 'frase', 'link'])

for produto_input in lista_de_produtos:
    try:
        lista_lojas=[]

        driver.get(LINK)
        time.sleep(1)


        print('Pesquisando: ', produto_input)
        
        barra_pesquisa = driver.find_element(By.CSS_SELECTOR, "input[class='search__InputUI-sc-1wvs0c1-2 dRQgOV']")
        barra_pesquisa.send_keys(produto_input)
        time.sleep(1)
        barra_pesquisa.send_keys(Keys.ENTER)
        time.sleep(2)

        # =============================================================================
        while True:
            try:
                
                select_elemento = espera_elemento_presente(By.CSS_SELECTOR,'div[class="aggregation__ContainerAggregation-sc-1m8iglp-0 dDWUqi"]',driver)
                lista_selects = select_elemento\
                    .find_elements(By.TAG_NAME, 'a')
                
                #print(lista_selects)
                for select in lista_selects:
                    if 'olist' in select.text.lower() and not select.text in lista_lojas:
                        print('select:', select.text)
                        lista_lojas.append(select.text)
                        select.click()
                        break
                else:
                    break

                time.sleep(2)
            except:
                
                break
        
        
        r=list(filter(lambda x:"olist" in x.text,lista_selects))
        if len(r)==0:
            continue

    # print("testee:  " ,r)


        produto_input = produto_input.split()
        produto_input = produto_input.pop()


        produto_lista_pagina=driver.find_elements(By.XPATH, 
                                                '//*[@id="rsyswpsdk"]/div/main/div/div[3]/div[3]')

        # print('produto_lista_pagina:', produto_lista_pagina)
        for produto_pesquisado in produto_lista_pagina:
            
            print('produto_pesquisado:', produto_pesquisado)	
            
            titulo_produto=espera_elemento_presente(By.CSS_SELECTOR,
                                                    'div[class="product-info__Wrapper-sc-1or28up-2 iKCquI"]',produto_pesquisado)
            titulo_produto=titulo_produto.find_element(By.CSS_SELECTOR, 'h3[class="product-name__Name-sc-1shovj0-0 gUjFDF"]').text

            titulo_filtrado = list(filter(lambda x: x.lower() in titulo_produto.lower(), produto_input))
            not_complete_name_in_title = len(titulo_filtrado) < 0.8*len(produto_input)

            if not_complete_name_in_title: 
                continue
            else:
                break


        preco_elemento = produto_pesquisado.find_element(By.CSS_SELECTOR, 'div[class="price-info__Wrapper-sc-1xm1xzb-0 clqFWq inStockCard__PriceInfoUI-sc-1ngt5zo-3 ciWwot"]')
        preco = preco_elemento.find_element(By.CSS_SELECTOR, 'span[class="src__Text-sc-154pg0p-0 price__PromotionalPrice-sc-h6xgft-1 ctBJlj price-info__ListPriceWithMargin-sc-1xm1xzb-2 liXDNM"]')\
                            
        preco_float = rs_element_to_float(preco)
        frase = preco_elemento.find_element(By.CSS_SELECTOR, 'span[class="installment__InstallmentUI-sc-1g296bd-0 fNXtFB"]').text
        link_produto = produto_pesquisado.find_element(By.CSS_SELECTOR, 'div[class="inStockCard__Wrapper-sc-1ngt5zo-0 iRvjrG"]')\
            .find_element(By.TAG_NAME, 'a')\
            .get_attribute('href')
        
        
        print('titulo_produto:', titulo_produto)
        print('preco:', preco_float)
        print('frase:', frase)
        print('link:', link_produto)

        itens_df = pd.concat([itens_df, pd.DataFrame([{
        'nome': titulo_produto,
        'pix': preco_float,
        'frase': frase,
        'link': link_produto
    }])], ignore_index=True)
    except:
        print('Erro ao buscar o produto')
        continue



itens_df.to_excel(FILE_PATH/ 'resultados'/ 'americanas.xlsx')
input('Enter para finalizar')
driver.quit()
    #input('Pressione ENTER para continuar... Selecionando o produto...')
    # =============================================================================
    #     # =============================================================================
    #     #     # =============================================================================
    #     #     #     # =============================================================================
    #     #     #     # =============================================================================
