# Análise exploratória

Esta página resume **como** a análise exploratória (EDA) foi feita: quais notebooks existem,
o que cada um responde e as decisões que valem para todos. Os resultados ficam nas figuras
de `docs/imagens/eda/` e nas tabelas de `docs/tabelas/`.

## Mapa dos notebooks

| Notebook | Objetivo | Recorte | Saída principal |
|:---|:-:|:---|:---|
| `00-dicionario-dados.ipynb` | — | base bruta completa (7.043 × 21) | `data/processed/dicionario.csv` (nome, descrição, exemplos e tipo de cada coluna) |
| `01-analise-exploratoria.ipynb` | — | base bruta sem `customerID` (7.043 × 20) | figuras em `docs/imagens/eda/`, tabelas em `docs/tabelas/` e `data/processed/Telcon-Customer-Churn_columns_selected.csv` |

A coluna **Objetivo** referencia a numeração dos [critérios de sucesso](criterios-sucesso.md),
que ainda serão definidos.

## Desenho da EDA

O notebook 01 segue o roteiro de oito etapas da metodologia (figura abaixo) e é aplicado a
todas as 20 colunas da base, exceto o `customerID`. O tipo de cada coluna (nominal,
discreta ou contínua) vem do dicionário do notebook 00 e define qual gráfico é feito.

| Seção | Técnica | O que responde |
|:---|:---|:---|
| Valores ausentes | contagem de células preenchidas por coluna (`valores-ausentes.png` e `.csv`) | a ausência é aleatória ou tem um motivo? |
| Univariada | barras de frequência (nominais); mínimo/máximo, dispersão e caixa (numéricas) | como cada variável se distribui? |
| Outliers | critério IQR: valor abaixo de Q1 − 1,5×IQR ou acima de Q3 + 1,5×IQR | há valor fora do normal? |
| Bivariada | média de cada variável numérica para cada categoria (`bivariada-*.png`) | quais variáveis andam juntas? |
| Multivariada | V de Cramér para todos os pares de categóricas e análise de correspondência (`acc-*.png`) | que estrutura existe no conjunto? |
| Correlação | correlação entre as numéricas (`correlacao.png`) e matriz de V de Cramér (`Correlacao_v_cramer.png`) | quais variáveis repetem informação? |
| Temporal | não se aplica | a base não tem nenhuma coluna de data |

![](imagens/eda-steps.png)

Alguns termos usados acima, de forma simples:

- **IQR** (intervalo interquartil): a faixa onde ficam os 50% "do meio" dos valores. O que
  passa muito dessa faixa é considerado discrepante.
- **V de Cramér**: um número de 0 a 1 que mede o quanto duas colunas de categorias andam
  juntas. 0 = nenhuma relação; perto de 1 = uma praticamente determina a outra.
- **Análise de correspondência**: um gráfico que coloca as categorias de duas colunas num
  mesmo "mapa", para ver quais aparecem juntas com frequência.

### Principais achados

A lista completa está em `docs/tabelas/insights.csv`. Em resumo:

- 26,5% dos clientes cancelaram (1.869 de 7.043), cerca de 1 em cada 4.
- O **contrato mensal** é o que mais separa quem sai de quem fica: 42,7% de cancelamento,
  contra 11,3% no anual e 2,8% no de dois anos.
- O cancelamento se concentra no **começo do relacionamento**: 53% de quem tem até 6 meses
  sai, contra 9,5% de quem passa de 48 meses.
- **Fibra óptica** é o maior foco de perda: 41,9% de cancelamento e 69% de todas as saídas.
- Quem tem **segurança online e suporte técnico** cancela bem menos (15% contra 41–42%).
- Quem paga por **cheque eletrônico** cancela 45,3%, contra 16,0% no pagamento automático.
- A combinação **contrato mensal + fibra + cheque eletrônico** reúne 18,6% dos clientes,
  60,4% de cancelamento e 42% de todas as saídas: forte candidata a um segmento de alto
  risco.
- `gender` não faz diferença (26,9% × 26,2%); idade, parceiro e dependentes fazem.
- Pares quase repetidos: `StreamingTV` × `StreamingMovies` (V = 0,53), `Partner` ×
  `Dependents` (0,45), `PhoneService` × `InternetService` (0,45).

### Escolhas metodológicas

- **`Churn` só para descrever, nunca para decidir.** Na EDA, `Churn` foi usada apenas para
  entender a base. Ela foi retirada ao final do notebook 01 e nenhuma decisão de preparação
  se apoia nela. *Por quê:* o projeto é não supervisionado; se o rótulo guiasse as
  escolhas, o modelo deixaria de ser "às cegas". A discussão está em
  [decisão sobre o Churn](informacoes_complementares/decisao-churn.md).
- **Associação entre categorias pelo V de Cramér, e não pelo p-valor.** *Por quê:* com
  7 mil clientes, quase qualquer teste dá "significativo" (p < 0,05). O V de Cramér mede o
  **tamanho** da relação; usamos V ≥ 0,10 como corte para levar um par à análise de
  correspondência.
- **"No internet service" e "No phone service" tratados como "No" na multivariada.**
  *Por quê:* essas categorias só repetem o que `InternetService` e `PhoneService` já dizem
  e inflariam a associação entre os serviços.
- **Ausência explicada antes de corrigida.** Os 11 vazios de `TotalCharges` foram
  investigados (todos com `tenure = 0`) antes de decidir o que fazer. *Por quê:* apagar as
  linhas ou usar a média esconderia que são clientes novos.
- **Percentual em vez de quantidade** ao comparar grupos (por exemplo, taxa de
  cancelamento por tipo de contrato). *Por quê:* os grupos têm tamanhos muito diferentes, e
  a quantidade absoluta mede o tamanho do grupo, não o comportamento.

## Reprodução

```bash
uv sync           # instala o ambiente
uv run invoke lab # abre o JupyterLab; executar os notebooks 00 e 01, nessa ordem
```

Os notebooks são salvos no git **sem as saídas** (o `pre-commit` roda o `nbstripout`). Por
isso toda figura e tabela importante é gravada em disco: figuras em `docs/imagens/eda/` e
tabelas em `docs/tabelas/`.

## Dados por trás de cada gráfico

As tabelas são gravadas em `docs/tabelas/`, em CSV com separador vírgula (`,`) e ponto
como separador decimal:

| Tabela | Conteúdo |
|:---|:---|
| `valores-ausentes.csv` | células preenchidas e percentual por coluna |
| `outliers.csv` | limites do IQR e valores discrepantes encontrados |
| `multivariada-associacao-dos-pares.csv` | qui-quadrado, p-valor e V de Cramér de cada par de categóricas |
| `multivariada-inercia-dos-pares.csv` | quanto da relação de cada par cabe no gráfico da análise de correspondência |
| `insights.csv` | resumo escrito dos achados da EDA |

<span style="color:red">**Pendente:** as figuras univariadas e bivariadas ainda não têm uma
tabela gravada ao lado. Não existe uma função única que grave figura e tabela juntas; cada
seção do notebook grava as suas.</span>
