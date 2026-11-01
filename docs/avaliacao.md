# Avaliação dos resultados

Enquanto a avaliação feita em [Modelagem dos dados](modelagem.md) é **técnica**, esta página
olha para o **projeto como um todo**: os resultados atendem aos objetivos de negócio, o
processo foi conduzido corretamente, e o que fazer em seguida.

!!! note "Base desta avaliação"
    Cada critério dos [critérios de sucesso](criterios-sucesso.md) foi confrontado com os
    artefatos do repositório: `reports/05-avaliacao.json`, `reports/05-perfil-segmentos.csv`,
    `reports/05-clientes-por-segmento.csv`, `reports/06-lista-acao-retencao.csv`,
    `data/processed/segmentos.csv` e os notebooks 05 e 06. 

## Confronto com os critérios de aceite

Cada critério de aceite comparado com o que foi efetivamente entregue.

| Obj. | Critério de aceite | Situação | Evidência |
|:-:|:---|:-:|:---|
| 1 | Todos os 7.043 clientes com exatamente um segmento, no máximo 5 segmentos | parcial | 3 segmentos, mas **24 clientes (0,3%) ficam "Sem segmento"** (ruído do DBSCAN): 99,7% de cobertura (`05-avaliacao.json`) |
| 1 | Cada segmento descrito por serviços, contrato, pagamento, tempo de casa e mensalidade | atendido | `05-perfil-segmentos.csv`: proteção, fibra, contrato mensal, cheque eletrônico, idoso, tempo de casa e mensalidade (mediana) |
| 1 | Nenhum segmento abaixo de 5% da base | atendido | menor segmento: 21,7% (Segmento A) |
| 1 | `Churn` fora da entrada do agrupamento e usado só para descrever o risco | atendido | `Churn` sai no notebook 01 e não entra no 03, 04 nem 05; o risco por segmento foi calculado só nesta avaliação (ver "Leitura consolidada") |
| 2 | Cada segmento com taxa de churn, mensalidade média e nº de clientes | parcial | nº de clientes e mensalidade (mediana) estão no perfil; a **taxa de churn não está gravada** em nenhum relatório |
| 2 | Segmentos ordenados por prioridade, com a regra escrita | atendido | regra do notebook 05: maior fatia em contrato mensal, desempate pela receita mensal; prioridade alta, média e baixa em `06-lista-acao-retencao.csv` |
| 2 | Prioritário e menos prioritário diferem em pelo menos 15 p.p. de churn | atendido | Segmento C 42,0% × Segmento A 7,4% = **34,6 p.p.** (calculado a partir da base bruta, não gravado) |
| 2 | Divisão da verba respeita o limite de 5 grupos e o excedente fica fora | não atendido | não existe tabela de alocação da verba por segmento; o valor da verba não foi informado |
| 3 | Modelo salvo e carregado em script que devolve o segmento de cada cliente | parcial | `models/model_telecom_dbscan.joblib` e a função `segmentar` do notebook 06; `src/model/` está vazio e `src/deployment/app.py` ainda é o modelo em branco |
| 3 | Cliente novo recebe segmento sem erro | atendido | acurácia de **100%** em validação cruzada (random forest) no 05 e função `segmentar` com validação de entrada no 06 |
| 3 | Qualidade medida e comparada entre pelo menos dois algoritmos, escolha justificada | atendido | 11 algoritmos, silhueta e Davies-Bouldin; justificativa em [Modelagem](modelagem.md) |
| 3 | Mesma base e mesma semente produzem os mesmos segmentos | não verificado | as sementes estão fixas (`random_state=42`), mas ninguém rodou o processo duas vezes para comparar; o ARI de 0,994 do 05 mede **estabilidade em reamostragem**, não reprodutibilidade |
| 4 | Cada segmento com ação sugerida e a característica que a justifica | atendido | A: fidelidade e renovação antecipada; B: migração para contrato anual; C: pacote de proteção por 3 meses (fibra com pouca proteção); "Sem segmento": análise individual |
| 4 | Cada ação com público-alvo e responsável pela execução | parcial | público-alvo definido (segmento e prioridade); responsável é genérico ("equipe de retenção") no plano do 06 |
| 4 | Lista nominal de clientes ordenada por prioridade | atendido | `reports/06-lista-acao-retencao.csv`: 7.043 clientes com segmento, prioridade e ação |
| 5 | Estimativa de retorno com premissas explícitas | parcial | 3 cenários no 05 (receita protegida de 2%, 5% e 8%; US$ 15 por contato; US$ 50 mil de implantação; US$ 20 mil por ano), mas **sem taxa de aceitação e sem custo separado da oferta**, e em **US$** |
| 5 | Piloto com grupo de controle | atendido | plano do notebook 06: grupo de controle aleatório em cada segmento; ainda **não está em** [Implementação](implementacao.md) |
| 5 | Indicador de sucesso e meta definidos antes da execução | não atendido | o 06 cita "cancelamentos evitados", mas sem meta numérica |
| 6 | Modelo funcionando em até 60 dias | não verificado | não há datas de início nem de entrega registradas no repositório |
| 6 | Rotina de atualização 2 vezes ao dia desenhada | não atendido | o plano do 06 prevê **lote mensal** da carteira e clientes novos no cadastro, e não as 2 atualizações diárias da premissa de infraestrutura |
| 6 | Monitoramento do perfil dos segmentos e gatilho de retreino | atendido | monitoramento por PSI no 06; retreino semestral ou PSI > 0,25 |
| 6 | Investimento dentro do teto de R$ 270 mil | não verificado | o teto é o orçamento planejado; não há custo realizado registrado (o US$ 116 mil do 05 é o custo da campanha, não o do projeto) |
| 6 | Dados tratados conforme a LGPD | parcial | `customerID` não entra no modelo e os dados são fictícios; falta a avaliação sobre a base real da operadora |


### Leitura consolidada

De 23 critérios: **11 atendidos, 6 parciais, 3 não atendidos e 3 não verificados.**

| Objetivo | Atendidos | Parciais | Não atendidos | Não verificados |
|:---|:-:|:-:|:-:|:-:|
| 1. Segmentação | 3 | 1 | 0 | 0 |
| 2. Verba por segmento | 2 | 1 | 1 | 0 |
| 3. Modelo que atribui o segmento | 2 | 1 | 0 | 1 |
| 4. Plano de ações | 2 | 1 | 0 | 0 |
| 5. Retorno e piloto | 1 | 1 | 1 | 0 |
| 6. Operação e prazo | 1 | 1 | 1 | 2 |
| **Total** | **11** | **6** | **3** | **3** |

**Para o negócio:** a segmentação existe, cabe nos 5 grupos, tem perfis e uma lista nominal
de ação para os 7.043 clientes. O que **falta é financeiro e operacional**: valor da verba,
alocação por segmento, meta do piloto e rotina de atualização.

**Churn observado por segmento** (calculado nesta avaliação, só para descrever):

| Segmento | Clientes | Churn | Contrato mensal | Mensalidade mediana |
|:---|--:|--:|--:|--:|
| A | 1.525 | 7,4% | 34% | US$ 20,15 |
| B | 2.410 | 19,0% | 51% | US$ 56,15 |
| C | 3.084 | 42,0% | 69% | US$ 91,65 |
| Sem segmento | 24 | 12,5% (3 clientes) | 4% | US$ 81,53 |

A ordem de risco **confirma** a regra de prioridade do notebook 05 (contrato mensal): quanto
maior a fatia em contrato mensal, maior o churn. O Segmento C concentra 43,8% da carteira, e
42% dele cancelou.


!!! warning "Achado crítico: os segmentos repetem a variável `InternetService`"
    O critério técnico "segmentos além de uma variável" do 05 falhou com ARI de **1,000**
    contra `InternetService`: os três segmentos são, na prática, o **tipo de internet**.
    O perfil confirma: o Segmento A tem mensalidade de US$ 20 e proteção 0 (sem internet), o
    B tem fibra 0% (DSL) e o C tem fibra 100%. Ou seja, **um filtro simples por tipo de
    internet entregaria os mesmos grupos**, e o modelo não acrescenta nada além disso. O
    churn por segmento (7,4%, 19,0% e 42,0%) é o churn conhecido por tipo de internet.

    
### Critérios técnicos do notebook 05

O notebook 05 tem uma lista própria de 7 critérios, que mede se o modelo serve à retenção.
Resultado: **4 de 7 atendidos, nenhum crítico falhou.**

| Critério | Meta | Obtido | Atende | Crítico |
|:---|:---|:---|:-:|:-:|
| Segmentos operáveis | 2 a 5 | 3 | sim | sim |
| Menor segmento | ≥ 10% da carteira | 21,7% | sim | sim |
| Cliente novo classificável | acurácia ≥ 85% | 100% | sim | sim |
| Segmentos estáveis | ARI ≥ 0,8 | 0,994 | sim | sim |
| Separação dos grupos | silhueta ≥ 0,25 | 0,187 (Davies-Bouldin 2,05) | **não** | não |
| Segmentos além de uma variável | ARI < 0,9 com qualquer variável | 1,000 (`InternetService`) | **não** | não |
| Cobertura da carteira | 100% com segmento | 99,7% | **não** | não |

**Cenários financeiros do ano 1** (segmento prioritário: C, 3.084 clientes, receita anual de
US$ 3,39 milhões):

| Cenário | Receita protegida | Ganho | Custo da campanha | Resultado do ano 1 | ROI |
|:---|--:|--:|--:|--:|--:|
| Pessimista | 2% | US$ 67.722 | US$ 46.260 | **−US$ 48.538** | −42% |
| Base | 5% | US$ 169.304 | US$ 46.260 | **US$ 53.044** | 46% |
| Otimista | 8% | US$ 270.887 | US$ 46.260 | US$ 154.627 | 133% |



### Critérios não atendidos

| Critério | Causa | Natureza |
|:---|:---|:---|
| Alocação da verba por segmento (obj. 2) | o valor da verba de retenção e o custo de cada oferta nunca foram informados | dado indisponível |
| Meta numérica do piloto (obj. 5) | a meta de redução de churn não foi definida pelo negócio | dado indisponível / decisão pendente |
| Atualização 2 vezes ao dia (obj. 6) | o desenho do 06 foi feito para lote mensal; a premissa de infraestrutura não foi considerada | decisão de condução |
| Cobertura de 100% (obj. 1, parcial) | o DBSCAN rotula 24 clientes como ruído e não foi feita a atribuição ao grupo mais próximo | restrição técnica |
| Retorno com todas as premissas (obj. 5, parcial) | faltam taxa de aceitação e custo da oferta | dado indisponível |

- **Verba e custo das ofertas:** destrava com o **Gerente Financeiro** (valor da verba) e o
  **Gerente Comercial** (custo e aceitação de cada oferta).
- **Meta do piloto:** depende do **Diretor Comercial** e do Gerente Financeiro.
- **Atualização 2×/dia:** depende de decisão do **Líder de Infraestrutura** com a equipe de
  dados; é refazer o desenho do 06 (não é limitação de dado).
- **Cobertura:** depende só da equipe de dados (atribuir o ruído ao vizinho mais próximo ou
  adotar o K-Means, que rotula todos).


## Revisão do processo

Retrospectiva da condução, independente do resultado.

- **O que funcionou**
    - cadeia de notebooks (00 a 06) com artefatos gravados e lidos pelo passo seguinte
      (`selecionado.json`, `05-avaliacao.json`), o que permite refazer o fluxo;
    - regras de escolha declaradas **antes** de olhar o resultado (04-0 e 05), em vez de
      escolher o modelo pela aparência;
    - conferências de alinhamento entre bases (`assert` de tamanho e ordem das linhas);
    - `Churn` mantido fora da modelagem, coerente com o projeto não supervisionado;
    - o 05 já registra uma tabela de lacunas e erros, o que acelerou esta revisão.
- **O que atrasou** (inferido das lacunas registradas; não há datas no repositório)
    - retrabalho de formato: o 03 gravava CSV com `;` e os notebooks 04 liam com `,`;
    - textos, nomes e exemplos herdados de um projeto imobiliário, que exigiram revisão
      dos notebooks 04;
    - **critérios de sucesso definidos depois da modelagem**: o 05 chegou a registrar que
      o documento ainda era o modelo em branco, e os critérios técnicos do notebook foram
      escritos sem o aval do negócio;
    - falta de dados do negócio (verba, custo das ofertas, meta de churn).
- **O que foi esquecido**
    - **a redundância com `InternetService` poderia ter sido vista na EDA**; só apareceu na
      avaliação, quando já havia modelo escolhido;
    - a taxa de churn por segmento não foi gravada em relatório;
    - o teste de reprodutibilidade (rodar duas vezes e comparar) não foi feito;
    - o código ficou nos notebooks: `src/model/` vazio e `src/deployment/app.py` ainda é o
      modelo em branco;
    - a documentação está desencontrada: [Entendimento de negócio](entendimento-negocio.md)
      e [Status](status.md) marcam todas as fases como concluídas, e
      [Implementação](implementacao.md) ainda é o modelo em branco;
    - o item 2 da tabela de lacunas do 05 diz que o desempate a favor do K-Means foi
      "declarado na regra do 04-0", mas o 04-0 **seleciona o DBSCAN**.

??? note "Perguntas que ajudam nesta revisão"
    - alguma conclusão está apoiada em dado que não foi conferido? **Sim:** o 100% de
      acurácia vem de segmentos que são função das mesmas variáveis (ver comentário);
    - as decisões metodológicas relevantes ficaram registradas? **Em grande parte**, nos
      notebooks e em [Modelagem](modelagem.md); falta o desempate DBSCAN × K-Means;
    - alguém que não participou consegue reproduzir os resultados? **Provavelmente**
      (`uv sync` e notebooks em ordem), mas sem teste de reprodutibilidade;
    - o tratamento de dados pessoais foi adequado? **Sim**, com dados fictícios; vale
      reavaliar com a base real.


## Próximas etapas

Decisão sobre o destino do projeto, com base nas duas seções anteriores.

!!! info "Decisão"
    - [ ] **Implantar** — seguir para [Implementação](implementacao.md)
    - [ ] **Iterar** — voltar a uma fase anterior; indique qual e por quê
    - [ ] **Encerrar** — registrar o aprendizado e não prosseguir

    
| Ação | Responsável | Prazo |
|:---|:---|:---|
| Gravar a taxa de churn por segmento no notebook 05 e em `reports/` | Cientista de Dados | antes da reunião de decisão |
| Atribuir os 24 clientes sem segmento ao grupo mais próximo, ou adotar o K-Means (que rotula todos e tem `predict`), e registrar o desempate | Cientista de Dados | na iteração |
| Subdividir o grupo de fibra (e o de contrato mensal) por contrato e pagamento, e reavaliar a redundância com `InternetService` | Cientista de Dados | na iteração |
| Rodar o processo duas vezes e comparar os segmentos (reprodutibilidade) | Cientista de Dados | na iteração |
| Informar o valor da verba, o custo e a aceitação de cada oferta, e a meta do piloto | Gerente Financeiro, Gerente Comercial, Diretor Comercial | antes do piloto |
| Converter as premissas financeiras do 05 para **R$** e para a verba real, e refazer os cenários | Cientista de Dados, com o Gerente Financeiro | após a resposta da linha anterior |
| Redesenhar a rotina de atualização para 2 vezes ao dia ou formalizar a exceção (lote mensal) | Cientista de Dados, com o Líder de Infraestrutura | antes da implantação |
| Mover a função `segmentar` e o modelo para `src/` e trocar o `app.py` em branco | Cientista de Dados | antes da implantação |
| Preencher [Implementação](implementacao.md) com o plano de piloto e atualizar [Status](status.md) | Gerente de Projetos | antes da entrega |
