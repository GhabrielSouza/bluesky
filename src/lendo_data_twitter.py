import pandas as pd
from fast_langdetect import detect_language
from datetime import datetime
import os

arquivoDeOrigem = "./data_twitter/PRESERVACAOAMBIENTAL_x_data_exported_2024-09-10-2024-12-04.csv"

dataFrame_ArquivoOrigem = pd.read_csv(arquivoDeOrigem)


# Criar os arquivos csv para cada tema e filtrar com o detect na 
# lingua pt e depois juntar tudo em um arquivo só csv

dataFrame_filtrado = dataFrame_ArquivoOrigem[
    dataFrame_ArquivoOrigem['Tweet Text'].apply(detect_language) == 'PT'
]

ArquivoDestino = f"./data_twitterFiltrado/{"PRESERVACAOAMBIENTAL"}_arquivo_filtrado_{datetime.now().strftime('%Y-%m-%d')}.csv"

dataFrame_filtrado.to_csv(ArquivoDestino, index=False, encoding="utf-8")

