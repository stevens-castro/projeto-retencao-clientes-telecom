# Resumo dos notebooks

Projeto de segmentação não supervisionada da base Telco Customer Churn (7.043 clientes), para orientar ações de retenção. O `Churn` foi retirado no notebook 01 e não é usado em nenhuma etapa.

| Notebook | O que foi feito |
|---|---|
| **00 · Dicionário de dados** | Carrega a base bruta, converte `TotalCharges` de texto para número e monta o dicionário com tipo, valores e descrição de negócio de cada coluna (`dicionario.csv`). |
| **01 · Análise exploratória** | Faz as análises univariada, bivariada e multivariada das variáveis, sem `customerID` e sem `Churn`. Grava a base com as colunas selecionadas para a próxima etapa. |
| **02 · Ajustes nos dados** | Mantém os duplicados (são clientes novos com o mesmo perfil), preenche com 0 o `TotalCharges` vazio de quem tem `tenure` 0, padroniza `SeniorCitizen` para No/Yes e troca "No internet/phone service" por "No". Grava a base curada (`_tratado.csv`) na mesma ordem da base bruta. |
| **03 · Preparação** | Retira `TotalCharges` (redundante com tenure × mensalidade) e `gender` (sem relação com as demais variáveis). Cria `ServicosProtecao` (0 a 4 serviços), junta os dois pagamentos automáticos, aplica MinMax e one-hot (20 features) e salva a base pré-processada e o `preprocessador.joblib`. |
| **04-0 · Modelagem (agrupamento)** | Compara 11 algoritmos de agrupamento com suas grades de hiperparâmetros, todos pela mesma métrica (silhueta euclidiana). Salva o vencedor, `segmentos.csv` e `selecionado.json`. No resultado atual vence o DBSCAN com 3 segmentos (silhueta 0,187), em empate técnico com o K-Means. |
| **04-1 · Cotovelo** | Para cada algoritmo, traça a curva de custo (cotovelo) e a de silhueta por número de grupos. O cotovelo fica em 3 ou 4 grupos, e a silhueta baixa em todos (≤ 0,19) mostra que os perfis formam um contínuo, sem grupos bem separados. |
| **04-2 · Redução de dimensionalidade** | Aplica PCA (11 componentes, 90% da variância) e UMAP e mede quais variáveis mais pesam em cada um. `InternetService`, `Contract` e `PaymentMethod` dominam as duas reduções. |
| **04-3 · Regras de associação** | Roda Apriori, Eclat e FP-Growth, que encontram os mesmos 191 conjuntos frequentes, e gera 168 regras fortes (confiança ≥ 60% e lift ≥ 1,2), como "fibra + streaming → mensalidade alta". |
| **05 · Avaliação** | Avalia os segmentos contra os critérios de sucesso: número e tamanho dos segmentos, classificação de clientes novos, estabilidade, silhueta e redundância com uma única variável. Também estima o impacto financeiro, registra a decisão de implantação e lista lacunas e próximos passos. O modelo foi aprovado com ressalvas: os segmentos praticamente repetem `InternetService`. |
| **06 · Implantação** | Aplica o mesmo pré-processamento do 03 a clientes novos (validando a entrada) e atribui o segmento, a prioridade e a ação de retenção sugerida. Gera a lista de ação da carteira inteira por `customerID` e inclui um monitoramento (PSI) que indica quando re-treinar. |
