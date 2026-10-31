# Entendimento dos dados

Esta página responde a três perguntas sobre o conjunto de dados: **o que existe**, **em que
qualidade** e **o que isso impede ou permite** dentro dos objetivos do projeto.

## Dados iniciais

Os dados vêm do arquivo `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv` (veja
[Fonte dos dados](fonte-dados.md)). A descrição das colunas foi feita no notebook
`00-dicionario-dados.ipynb` e a análise de qualidade e a exploração no notebook
`01-analise-exploratoria.ipynb`.

## Descrição dos dados

### Grão

Cada linha é um **cliente** (`customerID`). Não há cliente repetido: os 7.043 códigos são
todos diferentes.

A tabela é **achatada**: tudo sobre o cliente está numa linha só, sem tabelas auxiliares.
Dentro dela existem quatro grupos de informação (perfil, serviços, conta e valores), mais o
rótulo `Churn`.

### Grupos de colunas

| Dimensão | Exemplos de colunas |
|:---|:---|
| Perfil do cliente | `gender`, `SeniorCitizen`, `Partner`, `Dependents` |
| Serviços de telefone | `PhoneService`, `MultipleLines` |
| Serviços de internet | `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies` |
| Conta e contrato | `tenure`, `Contract`, `PaperlessBilling`, `PaymentMethod` |
| Métricas (valores) | `MonthlyCharges`, `TotalCharges` |
| Rótulo (fora do modelo) | `Churn` |

Por tipo, o dicionário classificou as colunas assim: **17 nominais** (categorias sem
ordem, como `Yes/No`), **2 discretas** (números inteiros: `SeniorCitizen` e `tenure`) e
**2 contínuas** (valores com casas decimais: `MonthlyCharges` e `TotalCharges`). Não há
colunas de data nem colunas ordinais (categorias com ordem, como "baixo/médio/alto").

### Cobertura frente aos critérios de sucesso

<span style="color:red">**Preencher depois que os objetivos forem definidos em
[Critérios de sucesso](criterios-sucesso.md).**</span> Adiantando o que já se sabe: os dados
**permitem** descrever o perfil, os serviços e o contrato de cada cliente (base para a
segmentação), mas **não permitem** acompanhar o cliente ao longo do tempo (veja
[Limitações](#limitacoes)).

## Qualidade dos dados

No geral a base está bem limpa: quase não há células vazias, nenhum cliente repetido e
nenhum valor absurdo. Os pontos de atenção estão abaixo.

### Valores sentinela

"Sentinela" é um valor que **parece** um dado, mas na verdade quer dizer "sem informação"
ou "não se aplica". Nesta base, aparecem três casos:

| Sentinela | Significado |
|:---|:---|
| `" "` (espaço em branco) em `TotalCharges` | cliente que ainda não recebeu nenhuma cobrança (11 clientes, todos com `tenure = 0`) |
| `No internet service` nos 6 serviços de internet | o cliente não tem internet; repete o que `InternetService = "No"` já diz (1.526 clientes) |
| `No phone service` em `MultipleLines` | o cliente não tem telefone; repete o que `PhoneService = "No"` já diz (682 clientes) |

As correções estão no notebook `02-ajustes-dados.ipynb`: o espaço em branco virou `0` e as
duas categorias "No ... service" viraram `No`. Nenhuma informação se perde, porque a
ausência do serviço continua registrada em `InternetService` e `PhoneService`.

### Achados que mudam a análise

1. **`TotalCharges` chegou como texto e com 11 vazios.** Os 11 clientes vazios têm
   `tenure = 0`: entraram no mês da extração e ainda não pagaram nada. Por isso a correção
   é colocar **0**, e não apagar a linha nem usar a média. (A conta confirma:
   `TotalCharges` ≈ `tenure` × `MonthlyCharges`, com razão mediana de 1,00.)
2. **`TotalCharges` repete informação.** Como ela é praticamente tempo de casa ×
   mensalidade, tem correlação de 0,89 com `tenure` (Spearman). Se entrasse no modelo, o
   tempo de casa seria contado duas vezes. Por isso ela **fica fora** da segmentação.
3. **Categorias repetidas nos serviços.** `No internet service` aparece em 6 colunas e
   `No phone service` em uma. Sem correção, a mesma informação ("não tem internet")
   entraria 7 vezes e deixaria os serviços artificialmente parecidos entre si.
4. **`SeniorCitizen` é o único "Sim/Não" guardado como número (0/1).** Por isso a análise
   de valores discrepantes o apontou como "outlier", o que é falso: só 16% dos clientes são
   idosos. Ele foi convertido para `Yes/No`, como as outras colunas.
5. **Linhas iguais não são erro.** Sem o `customerID`, 40 linhas repetem outra (73 linhas
   envolvidas). Todas são de clientes com 1 mês de casa e o mesmo pacote básico: são
   clientes **diferentes** com o mesmo perfil, então **nada foi apagado**.
6. **`gender` não se relaciona com nada.** A associação com as outras colunas é
   praticamente zero (V de Cramér máximo de 0,02). Ela **fica fora** da segmentação para
   não criar grupos de "homens" e "mulheres" que não diferem em mais nada.
7. **Valores extremos: nenhum.** `tenure`, `MonthlyCharges` e `TotalCharges` não têm nenhum
   valor fora dos limites do critério IQR (veja [Análise exploratória](analise-exploratoria.md)).

## Dimensões-chave

Duas dimensões novas foram criadas na preparação (notebook 03), a partir das colunas
existentes. Elas não usam `Churn` em nenhum momento.

**`ServicosProtecao`**: os quatro serviços de proteção (segurança online, backup, proteção
do aparelho e suporte técnico) andam juntos — quem contrata um costuma contratar outro.
Em vez de quatro colunas, o modelo recebe **uma** contagem de quantos o cliente tem.

| Valor | Descrição | Regra de derivação |
|:---|:---|:---|
| `0` a `4` | quantos serviços de proteção o cliente contrata | soma dos `Yes` em `OnlineSecurity`, `OnlineBackup`, `DeviceProtection` e `TechSupport` |

**`PaymentMethod` agrupada**: as duas formas automáticas de pagamento têm perfis
praticamente iguais (tempo de casa mediano de 48 e 47 meses, mensalidade mediana de 73),
então viraram uma categoria só.

| Valor | Descrição | Regra de derivação |
|:---|:---|:---|
| `Automatic` | o cliente não precisa fazer nada para pagar | `Bank transfer (automatic)` ou `Credit card (automatic)` |
| `Electronic check` | paga por cheque eletrônico | sem mudança |
| `Mailed check` | paga por cheque pelo correio | sem mudança |

## Limitações

O que os dados **não** permitem responder:

- **Não há data.** A base é uma "foto" de um único momento. Não dá para saber quando o
  cliente cancelou, nem ver se o comportamento mudou com o tempo. O único dado de tempo é
  `tenure` (meses de casa).
- **Não há dados de uso nem de atendimento.** Não sabemos quanto o cliente usa a internet,
  quantas vezes ligou reclamando ou se recebeu alguma oferta. Esses são motivos comuns de
  cancelamento que ficam de fora.
- **Os dados são fictícios.** Servem para aprender o método, mas os números não
  representam uma operadora real.
- **Uso do `Churn` em aberto.** Pela decisão atual do grupo, `Churn` foi retirada da base
  ao final do notebook 01 e não participa de nenhuma etapa seguinte. Isso impede, por
  enquanto, de responder "qual segmento cancela mais?". A discussão está registrada em
  [decisão sobre o Churn](informacoes_complementares/decisao-churn.md).
