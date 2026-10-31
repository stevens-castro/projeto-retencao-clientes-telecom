# Resumo do que foi escrito em cada MD

Projeto: **Retenção de clientes Telecom** · situação em 30/10/2026 (notebooks 00 a 03 concluídos)

---

## 1. `index.md` — Descrição do projeto

- **Assunto:** uma operadora de telefone e internet perde clientes todo mês (o chamado
  *churn*). Manter um cliente custa menos do que conquistar outro.
- **Dados:** base pública *Telco Customer Churn* (IBM), com 7.043 clientes fictícios e 21
  colunas.
- **Objetivo:** dividir os clientes em **grupos parecidos** (segmentos) usando aprendizado
  **não supervisionado**, em que o algoritmo não sabe quem cancelou. Assim a área de
  retenção pode criar ações diferentes para cada grupo.
- **Tipo do projeto:** análise exploratória + modelo de agrupamento.
- **Acesso:** público (os dados são abertos e fictícios).
- **Equipe:** Stevens Castro, Tevin e Thierry Pereira Canoco.
- **Falta preencher:** o nome do professor.

---

## 2. `status.md` — Status do projeto

- ✅ **Fase 1 – Ambiente:** repositório no GitHub criado e ferramentas instaladas.
- ⬜ **Fase 2 – Entendimento de negócio:** ainda em aberto.
- ✅ **Fase 3 – Entendimento dos dados:** dicionário (nb 00), qualidade e análise
  exploratória (nb 01).
- ✅ **Fase 4 – Preparação:** correção dos dados (nb 02) e preparação para o modelo (nb 03).
- ⬜ **Fases 5, 6 e 7 – Modelagem, avaliação e implantação:** ainda não feitas.

---

## 3. `entendimento-negocio.md` — Entendimento de negócio (preenchido em parte)

- **Marcos:** fases 1, 3 e 4 marcadas como concluídas.
- **Equipe:** os três integrantes do grupo.
- **Necessidade de negócio:** 1 em cada 4 clientes cancelou (26,5%). A área de retenção
  precisa conhecer os tipos de cliente para agir de forma diferente com cada um, por
  exemplo oferecendo contrato anual a quem está no mensal.
- **Ferramentas:** GitHub, uv, Python 3.12, Jupyter e bibliotecas (pandas, numpy,
  matplotlib, seaborn, scipy, prince, circlify, scikit-learn, umap-learn, mlxtend).
- **Requisitos de dados:** uma linha por cliente com perfil, serviços, contrato/pagamento e
  valores. A base atende a tudo isso, mas não tem datas, dados de uso nem de atendimento.
- **Mineração de dados:** explica as 4 etapas (dicionário → exploração → ajustes →
  preparação), uma por notebook.
- **Ficou em branco:** especialistas, recursos financeiros, requisitos funcionais e
  custo-benefício.

---

## 4. `fonte-dados.md` — Fonte dos dados

- **Origem:** um único arquivo CSV da IBM, salvo em `data/raw/` sem nenhuma alteração.
- **Tamanho:** 7.043 linhas, 21 colunas, cerca de 1 MB, sem datas (é uma "foto" de um
  único momento).
- **Cada linha = um cliente** (`customerID`).
- **Lista das 21 colunas** com uma explicação simples de cada uma.
- **Valores que podem ser somados:** `MonthlyCharges` (mensalidade) e `TotalCharges` (total
  já pago).
- **Caminho dos dados:** original → sem ID e sem Churn (nb 01) → base corrigida (nb 02) →
  base em números de 0 a 1 (nb 03) → segmentação (nb 04).
- **Como refazer:** `uv sync` e rodar os notebooks 00 a 03 em ordem.

---

## 5. `entendimento-dados.md` — Entendimento dos dados

- **Grupos de colunas:** perfil, telefone, internet, conta/contrato, valores e o rótulo
  `Churn`.
- **Tipos:** 17 colunas de categoria, 2 de números inteiros e 2 de valores com decimais.
- **Qualidade:** a base está bem limpa. Os pontos de atenção foram:
  1. `TotalCharges` tinha 11 vazios, todos de clientes novos (0 meses) → virou **0**;
  2. `TotalCharges` repete tempo de casa × mensalidade → **fica fora** do modelo;
  3. `No internet service` / `No phone service` repetem informação → viraram **No**;
  4. `SeniorCitizen` estava como 0/1 e parecia "outlier" → virou **Yes/No**;
  5. linhas iguais são clientes novos diferentes com o mesmo pacote → **mantidas**;
  6. `gender` não tem relação com nada → **fica fora**;
  7. nenhum valor extremo nas colunas numéricas.
- **Variáveis criadas:** `ServicosProtecao` (quantos dos 4 serviços de proteção o cliente
  tem, de 0 a 4) e `PaymentMethod` com os dois pagamentos automáticos juntos em `Automatic`.
- **Limitações:** não há datas, não há dados de uso nem de atendimento, os dados são
  fictícios e o uso do `Churn` ainda está em discussão no grupo.
- **Falta preencher:** a tabela de cobertura dos critérios de sucesso.

---

## 6. `analise-exploratoria.md` — Análise exploratória

- **Notebooks:** 00 (dicionário) e 01 (exploração).
- **Etapas feitas:** valores ausentes, análise de uma variável por vez, outliers (critério
  IQR), duas variáveis juntas, várias variáveis juntas (V de Cramér e análise de
  correspondência) e correlação. Não houve análise ao longo do tempo porque a base não tem
  datas.
- **Glossário simples:** o que é IQR, V de Cramér e análise de correspondência.
- **Principais achados:**
  - 26,5% dos clientes cancelaram;
  - contrato mensal: 42,7% de cancelamento (anual 11,3%, dois anos 2,8%);
  - clientes com até 6 meses: 53% cancelam;
  - fibra óptica: 41,9% de cancelamento;
  - quem tem segurança e suporte cancela bem menos (15% contra 41–42%);
  - cheque eletrônico: 45,3% contra 16% no pagamento automático;
  - mensal + fibra + cheque eletrônico: 60,4% de cancelamento, forte candidato a grupo de
    alto risco;
  - `gender` não faz diferença.
- **Decisões e motivos:** `Churn` foi usada só para descrever e não para decidir; usamos o
  V de Cramér em vez do p-valor; tratamos as categorias repetidas; investigamos os vazios
  antes de corrigir; comparamos percentuais em vez de quantidades.
- **Onde estão os resultados:** figuras em `docs/imagens/eda/` e tabelas em `docs/tabelas/`.
- **Pendente:** os gráficos de uma e de duas variáveis ainda não têm tabela salva junto.

---

## 7. `preparacao.md` — Preparação dos dados

- **Camadas:** original → selecionada → curada (nb 02) → pré-processada (nb 03). Todas
  mantêm as 7.043 linhas na mesma ordem.
- **Correções do notebook 02:** retirar o ID e o Churn, manter as linhas repetidas,
  trocar vazio por 0, passar `SeniorCitizen` para Yes/No e as categorias repetidas para No.
- **Preparação do notebook 03 (para o algoritmo K-Means):**
  - retirar `TotalCharges` e `gender`;
  - criar `ServicosProtecao` e juntar os pagamentos automáticos;
  - Yes/No → uma coluna 0/1;
  - colunas de 3 categorias → uma coluna 0/1 para cada categoria (*one-hot*);
  - números → escala de 0 a 1, para nenhuma coluna pesar mais que as outras.
- **Resultado:** 7.043 clientes × 20 colunas, tudo entre 0 e 1. O pré-processador foi salvo
  em `models/preprocessador.joblib` para ser reutilizado.
- **Conferências:** nenhuma linha perdida, nenhum vazio, todos os valores entre 0 e 1 e
  proporções iguais às da EDA.
- **Outliers:** não houve nenhum a tratar.

---

## Arquivos que não foram alterados

| Arquivo | Por quê |
|:---|:---|
| `criterios-sucesso.md` | os objetivos e critérios de aceite precisam ser definidos pelo grupo |
| `modelagem.md` | depende dos notebooks 04 |
| `avaliacao.md` | depende do notebook 05 |
| `implementacao.md` | depende do notebook 06 |
