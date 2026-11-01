"""Dicionário de dados: nomes, tipos semânticos e escalas ordinais.

Este módulo é a **fonte única da verdade** sobre o significado de cada coluna.
A base original (WA_Fn-UseC_-Telco-Customer-Churn, De Cock 2011) usa nomes em inglês sem espaço no
meio (``SeniorCitizen``, ``PhoneService``) e categorias em código (``Month-to-month``, ``Electronic check``);
a camada curada renomeia as colunas para `snake_case` em português e traduz as
categorias, porque o resultado é lido por gente de negócio.

Três decisões registradas aqui, e não no código de análise:

1. **`preco_venda` é rótulo reservado.** Não entra em nenhuma etapa de
   modelagem — só na avaliação *a posteriori*. Usá-lo antes descaracterizaria o
   problema não supervisionado.

2. **`bairro` também fica de fora da modelagem.** Localização é o principal
   determinante de preço no mercado imobiliário: incluí-la faria o algoritmo
   redescobrir o preço por caminho indireto. Fica reservada para validação
   externa dos segmentos.
   
3. **Atributos da transação** (mês, ano, tipo e condição de venda) descrevem o
   *negócio*, não o *produto*. Ficam na base curada para a análise temporal,
   fora da matriz de modelagem.
"""

from __future__ import annotations


# --------------------------------------------------------------------------- #
# Renomeação para a camada curada
# --------------------------------------------------------------------------- #

RENOMEAR: dict[str, str] = {
       "customerID": "clienteId",
       "gender": "genero",
       "SeniorCitizen": "cidadao_idoso?",
       "Partner": "tem_parceiro",
       "Dependents": "dependentes",
       "tenure": "permanencia",
       "PhoneService": "servico_telefonia",
       "MultipleLines": "multiplas_linhas",
       "InternetService": "servico_internet",
       "OnlineSecurity": "seguranca_online",
       "OnlineBackup": "backup_online",
       "DeviceProtection": "protecao_dispositivo",
       "TechSupport": "suporte_tecnico",
       "StreamingTV": "stream_tv",
       "StreamingMovies": "stream_filmes",
       "Contract": "tipo_contrato",
       "PaperlessBilling": "fatura_digital",
       "PaymentMethod": "tipo_pagamento",
       "MonthlyCharges": "valor_mensal",
       "TotalCharges": "valor_total",
       "Churn": "servico_cancelado",
}

# --------------------------------------------------------------------------- #
# Tradução das categorias para a camada curada
# --------------------------------------------------------------------------- #



# --------------------------------------------------------------------------- #
# Espaço de atributos da modelagem
# --------------------------------------------------------------------------- #

#: Numéricas contínuas e discretas. Descrevem tamanho, idade e contagem.
NUMERICAS = [    
    "tenure",
    "MonthlyCharges",
    "TotalCharges",

]



#: Nominais: sem ordem. Entram por Gower ou por *one-hot*, nunca como inteiro.
NOMINAIS = [
    "customerId",
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]

#: Binárias derivadas, usadas no espaço euclidiano enxuto.
BINARIAS = ["SeniorCitizen"]


#: Limiar de assimetria a partir do qual a transformação se justifica. O valor
#: 0,75 é a convenção usual; abaixo dele o ganho não compensa a perda de
#: legibilidade da unidade original.
LIMIAR_ASSIMETRIA = 0.75

#: Variáveis contínuas cuja assimetria **na base curada** supera o limiar e que,
#: por isso, recebem `log1p` antes da padronização.
#: Medições: varandas 0,974 · área habitável 0,747 · terreno 0,417 · porão 0,296.
#:
#: A lista encolheu quando a depuração da carteira entrou em cena, e as duas
#: mudanças estão medidas, não estimadas:
#:
#: * **área do terreno** marcava 13,20 na base bruta e caiu para 0,417. O que
#:   parecia forma da distribuição era um punhado de lotes acima de 200.000
#:   pés², removidos como valores extremos. Transformá-la agora seria hábito;
#: * **área habitável** ficou em 0,747, logo abaixo do limiar de 0,75. Fica de
#:   fora pelo critério declarado — mudar o limiar para acomodar a variável
#:   inverteria a ordem entre regra e resultado.
#:
#: Só entram contínuas. As ordinais `qualidade_externa` (0,81) e
#: `qualidade_porao` (−1,38) também passam do limiar, mas `log1p` sobre nota de
#: 0 a 5 destrói o passo constante que dá sentido à escala.
ASSIMETRICAS = ["area_varandas"]

# --------------------------------------------------------------------------- #
# Descrição de negócio, para o dicionário publicado e para a aplicação
# --------------------------------------------------------------------------- #

DESCRICOES: dict[str, str] = {
    "area_habitavel": "Área construída acima do solo, em pés quadrados",
    "area_porao": "Área total do porão, em pés quadrados (0 = sem porão)",
    "area_terreno": "Área do lote, em pés quadrados",
    "area_garagem": "Área da garagem, em pés quadrados (0 = sem garagem)",
    "area_varandas": "Soma de deck, varandas aberta, fechada, de tela e de três estações",
    "banheiros_total": "Banheiros equivalentes: completos + metade dos lavabos, incluindo porão",
    "comodos": "Cômodos acima do solo, exceto banheiros",
    "dormitorios": "Dormitórios acima do solo",
    "lareiras": "Número de lareiras",
    "idade_imovel": "Anos entre a construção e a venda",
    "anos_desde_reforma": "Anos entre a última reforma (ou a construção) e a venda",
    "qualidade_geral": "Qualidade geral de material e acabamento (1 a 10)",
    "conservacao_geral": "Estado geral de conservação (1 a 10)",
    "qualidade_externa": "Qualidade do revestimento externo (0 a 5)",
    "qualidade_cozinha": "Qualidade da cozinha (0 a 5)",
    "qualidade_porao": "Altura e qualidade do porão (0 = sem porão, 5 = excelente)",
    "acabamento_garagem": "Acabamento interno da garagem (0 = sem garagem, 3 = acabada)",
    "zoneamento": "Classificação de zoneamento urbano",
    "tipo_construcao": "Tipo de construção (isolada, geminada, sobreposta)",
    "estilo": "Estilo e número de pavimentos",
    "tipo_garagem": "Posição da garagem em relação à casa",
    "ar_central": "Possui ar-condicionado central",
    "tem_porao": "Possui porão",
    "tem_garagem": "Possui garagem",
    "tem_lareira": "Possui ao menos uma lareira",
    "tem_segundo_pavimento": "Possui pavimento superior",
    "bairro": "Bairro de Ames (reservado para validação externa)",
    "preco_venda": "Preço de venda em dólares (rótulo reservado)",
    "ano_venda": "Ano da transação",
    "mes_venda": "Mês da transação",
    "tipo_venda": "Modalidade da venda",
    "condicao_venda": "Condição da venda (normal, parcial, familiar, execução…)",
}

#: Rótulos curtos para gráficos e para a aplicação.
ROTULOS_CURTOS: dict[str, str] = {
    "area_habitavel": "Área habitável",
    "area_porao": "Área do porão",
    "area_terreno": "Área do terreno",
    "area_garagem": "Área da garagem",
    "area_varandas": "Área de varandas",
    "banheiros_total": "Banheiros",
    "comodos": "Cômodos",
    "dormitorios": "Dormitórios",
    "lareiras": "Lareiras",
    "idade_imovel": "Idade do imóvel",
    "anos_desde_reforma": "Anos desde a reforma",
    "qualidade_geral": "Qualidade geral",
    "conservacao_geral": "Conservação",
    "qualidade_externa": "Qualidade externa",
    "qualidade_cozinha": "Qualidade da cozinha",
    "qualidade_porao": "Qualidade do porão",
    "acabamento_garagem": "Acabamento da garagem",
    "zoneamento": "Zoneamento",
    "tipo_construcao": "Tipo de construção",
    "estilo": "Estilo",
    "tipo_garagem": "Tipo de garagem",
    "ar_central": "Ar central",
    "tem_porao": "Tem porão",
    "tem_garagem": "Tem garagem",
    "tem_lareira": "Tem lareira",
    "tem_segundo_pavimento": "Tem 2º pavimento",
}


def rotulo(coluna: str) -> str:
    """Devolve o rótulo curto de uma coluna, ou o próprio nome se não houver."""
    return ROTULOS_CURTOS.get(coluna, coluna.replace("_", " ").capitalize())
