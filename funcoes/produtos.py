import pandas as pd

class Item:
    def __init__(self, nome, pix, prazo, frase) -> None:
        self.nome = nome,
        self.pix = float(pix),
        self.prazo = float(prazo),
        self.frase = frase,
        self.df = None,

    def cria_df(self, df=None):
        dicionario = {'nome': self.nome,
                      'pix': self.pix,
                      'prazo': self.prazo,
                      'frase': self.frase
                      }
        if df is None:
            self.df = pd.DataFrame(dicionario)
            #self.df.to_excel('teste.xlsx')
            return self.df

def junta_dataframes(df_antigo, df_novo):

    # Verifica se o DataFrame antigo está vazio
    if df_antigo is None or df_antigo.empty:
        # Se estiver vazio, retorna o DataFrame novo

        return df_novo
    else:
        # Se o DataFrame antigo não estiver vazio, concatena os dois DataFrames
        df_resultado = pd.concat([df_antigo, df_novo], ignore_index=True)
        return df_resultado



def rs_element_to_float(numero_elemento, pos=1,splitter=' '):
    numero_com_virgula_sem_rs = numero_elemento.text.split(splitter)[pos]
    numero_com_ponto_sem_rs = numero_com_virgula_sem_rs.replace('.', '')
    numero_com_ponto_sem_rs = numero_com_ponto_sem_rs.replace(',', '.')

    return float(numero_com_ponto_sem_rs)


def a_prazo(texto):
    texto = texto.split()
    valor = float(texto[9].replace(',', '.'))
    parcelas = float(texto[6].replace('x', ''))
    return valor*parcelas

if __name__=='__main__':
    num = '1.384,64'
    num = num.replace('.', '')
    num = num.replace(',', '.')
    print(float(num))
