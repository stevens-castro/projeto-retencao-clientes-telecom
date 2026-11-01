# Critérios de sucesso

O sucesso do projeto é dado à completude dos objetivos de negócio definidos a seguir. Cada
objetivo está descrito no formato de história de usuário (**Como** / **Quero** / **Para** /
**Objetivo**), acompanhado dos respectivos critérios de aceite.

## Visão geral

| # | Objetivo de negócio | Solicitante (papel) | Entrega principal |
|:-:|:---|:---|:---|
| 1 | Segmentação de clientes (até 5 grupos) | Diretor Comercial | Tabela de clientes com o segmento atribuído e o perfil de cada segmento (serviços, contrato, pagamento, tempo de casa e mensalidade) |
| 2 | Definição da verba de retenção por segmento | Gerente Financeiro | Tabela de alocação da verba por segmento, com a regra de priorização |
| 3 | Modelo treinado que atribui o segmento a cada cliente | Diretor Comercial | Modelo serializado, pronto para o piloto, e script de classificação de novos clientes |
| 4 | Plano de ações de retenção por segmento | Gerente Comercial | Lista de ações sugeridas por segmento, com o cliente-alvo de cada uma |
| 5 | Retorno esperado e desenho do piloto | Gerente Financeiro / Diretor Comercial | Estimativa de retorno e plano de piloto com grupo de controle |
| 6 | Operação, monitoramento e prazo | Líder de Infraestrutura | Rotina de atualização, monitoramento do modelo e relatório final dentro dos 60 dias |

---

## 1. Segmentação de clientes

???+ success "Segmentação de clientes"
    **Como** Diretor Comercial<br>
    **Quero** conhecer os tipos de cliente da carteira, em no máximo 5 grupos, com o perfil
    de cada um<br>
    **Para** planejar ações de retenção diferentes por grupo, em vez de tratar todos os
    clientes do mesmo jeito<br>
    **Objetivo** substituir a abordagem genérica por grupos de clientes parecidos, que
    caibam na verba de retenção

    **Critérios de aceite:**

    - [ ] Todos os 7.043 clientes recebem exatamente um segmento, e o número de segmentos
      é de no máximo 5
    - [ ] Cada segmento é descrito por serviços contratados, tipo de contrato, forma de
      pagamento, tempo de casa e mensalidade média
    - [ ] Nenhum segmento representa menos de 5% da base (tamanho mínimo para uma ação
      de retenção valer a pena)
    - [ ] O `Churn` não é usado como variável de entrada do agrupamento; é usado apenas
      para descrever o risco de cada segmento

    **Entrega:** tabela de clientes por segmento e perfil dos segmentos
    (`reports/05-clientes-por-segmento.csv` e `reports/05-perfil-segmentos.csv`), gerados
    pelos notebooks 04 e 05.

## 2. Definição da verba de retenção por segmento

???+ success "Definição da verba de retenção por segmento"
    **Como** Gerente Financeiro<br>
    **Quero** saber para quais segmentos a verba de retenção deve ir e em que proporção<br>
    **Para** aprovar o orçamento de retenção com base no risco e no valor de cada grupo<br>
    **Objetivo** direcionar a verba apenas aos grupos de maior risco, sem desperdiçar
    desconto em clientes que não precisam

    **Critérios de aceite:**

    - [ ] Cada segmento tem a taxa de churn observada, a mensalidade média e o número de
      clientes
    - [ ] Os segmentos estão ordenados por prioridade, com a regra de priorização escrita
      (por exemplo, churn × mensalidade média × tamanho)
    - [ ] O segmento prioritário e o de menor prioridade diferem em pelo menos 15 pontos
      percentuais na taxa de churn (se não diferirem, a segmentação não ajuda a
      decidir a verba)
    - [ ] A divisão da verba respeita o limite de 5 grupos; qualquer excedente fica
      explicitamente fora do plano

    **Entrega:** tabela de alocação da verba por segmento, em `reports/` (a partir dos
    notebooks 05 e 06), e seção correspondente da [Avaliação](avaliacao.md).

    !!! warning "Ressalva"
        O **valor em reais** da verba de retenção e o custo de cada oferta **não constam**
        na documentação nem na base. Sem eles, o projeto entrega a **ordem de prioridade
        e a proporção** entre segmentos, não o valor absoluto. Ver Pendências de dados.


## 3. Modelo treinado que atribui o segmento a cada cliente

???+ success "Modelo treinado que atribui o segmento a cada cliente"
    **Como** Diretor Comercial<br>
    **Quero** um modelo que classifique qualquer cliente (novo ou existente) em um dos
    segmentos<br>
    **Para** iniciar o piloto de retenção sem refazer a análise a cada rodada<br>
    **Objetivo** ter um modelo pronto para uso, estável e explicável

    **Critérios de aceite:**

    - [ ] O modelo está salvo e é carregado em um script que recebe a base de clientes e
      devolve o segmento de cada um
    - [ ] O modelo aplicado a um cliente **novo** (fora da base de treino) atribui um
      segmento sem erro
    - [ ] A qualidade do agrupamento é medida (silhueta, entre outras) e comparada entre
      pelo menos dois algoritmos, com a escolha justificada por escrito
    - [ ] Rodar o processo duas vezes com a mesma base e a mesma semente produz os mesmos
      segmentos (reprodutibilidade)

    **Entrega:** `models/` (modelo e pré-processador), `src/` (script de classificação),
    notebooks 04 e 05, e [Modelagem](modelagem.md).

    !!! warning "Ressalva"
        A silhueta do modelo selecionado hoje (DBSCAN, 3 grupos) é de **0,187**, valor
        baixo (grupos pouco separados). O critério pede que a qualidade seja medida e
        justificada, **não** que atinja um valor mágico, para não ajustar o critério ao
        resultado.


## 4. Plano de ações de retenção por segmento

???+ success "Plano de ações de retenção por segmento"
    **Como** Gerente Comercial<br>
    **Quero** uma ação de retenção sugerida para cada segmento, ligada às características
    do grupo<br>
    **Para** aprovar o uso da verba e orientar a equipe de retenção<br>
    **Objetivo** transformar a segmentação em ofertas concretas e aprováveis

    **Critérios de aceite:**

    - [ ] Cada segmento tem pelo menos uma ação sugerida, com a característica do grupo
      que a justifica (ex.: contrato mensal → oferta de contrato anual)
    - [ ] Cada ação tem o público-alvo definido (quais clientes do segmento) e o
      responsável pela execução
    - [ ] Existe uma lista nominal de clientes a abordar, ordenada por prioridade

    **Entrega:** lista de ações de retenção (`reports/06-lista-acao-retencao.csv`) e
    seção correspondente de [Implementação](implementacao.md).

## 5. Retorno esperado e desenho do piloto

???+ success "Retorno esperado e desenho do piloto"
    **Como** Gerente Financeiro e Diretor Comercial<br>
    **Quero** uma estimativa do retorno da campanha e um plano para comprovar o efeito em
    pequena escala<br>
    **Para** decidir se amplia a campanha depois do piloto<br>
    **Objetivo** medir se a retenção aumenta e se a verba é bem aplicada

    **Critérios de aceite:**

    - [ ] A estimativa de retorno está registrada, com premissas explícitas (clientes
      abordados, taxa de aceitação, custo da oferta, mensalidade preservada)
    - [ ] O piloto prevê um **grupo de controle** (clientes do mesmo segmento que não
      recebem a oferta)
    - [ ] O indicador de sucesso do piloto e a meta estão definidos antes da execução
      (ex.: redução da taxa de churn do segmento tratado em relação ao controle)

    **Entrega:** seção de retorno e piloto da [Avaliação](avaliacao.md) e plano de piloto
    em [Implementação](implementacao.md).

    !!! warning "Ressalva"
        Não há como **comprovar** a redução de cancelamentos com esta base (é uma foto de
        um único momento, sem datas e sem histórico de campanhas). O projeto entrega a
        **estimativa** e o **desenho do piloto**; o resultado real só existe depois do
        piloto.

## 6. Operação, monitoramento e prazo

???+ success "Operação, monitoramento e prazo"
    **Como** Líder de Infraestrutura<br>
    **Quero** saber como o modelo roda, é atualizado e é monitorado no ambiente da
    empresa<br>
    **Para** operá-lo com segurança depois da entrega<br>
    **Objetivo** manter o modelo confiável e entregá-lo dentro do prazo e do orçamento

    **Critérios de aceite:**

    - [ ] O modelo funcionando é entregue em até 60 dias, a partir da base de testes
      disponibilizada
    - [ ] A rotina de atualização (2 vezes ao dia, conforme a premissa de infraestrutura)
      está desenhada e documentada
    - [ ] Há indicadores de monitoramento (tamanho e perfil dos segmentos ao longo do
      tempo) e um gatilho para retreinar o modelo
    - [ ] O investimento fica dentro do teto de R$ 270 mil
    - [ ] Dados dos clientes tratados conforme a LGPD (sem `customerID` real no modelo e
      sem dado pessoal além do necessário)

    **Entrega:** [Implementação](implementacao.md), `src/deployment/` e relatório final do
    projeto.

---

## Consolidado dos critérios de aceite

| Objetivo | Critérios de aceite | Concluídos | Observação |
|:---|:-:|:-:|:---|
| 1. Segmentação de clientes | 4 | 0 | Tratar o ruído do DBSCAN |
| 2. Verba de retenção por segmento | 4 | 0 | Valor em R$ pendente |
| 3. Modelo que atribui o segmento | 4 | 0 | DBSCAN sem `predict` |
| 4. Plano de ações de retenção | 3 | 0 | Custo das ações pendente |
| 5. Retorno e piloto | 3 | 0 | Só estimativa, sem comprovação |
| 6. Operação, monitoramento e prazo | 5 | 0 | LGPD vale para dados reais |
| **Total** | **23** | **0** | |

## Pendências de dados

Critérios em aberto que **não dependem de análise**, e sim de dado que não veio na origem.
Registre aqui para que a conversa com a área provedora tenha uma lista objetiva.

| # | Pendência | Destrava |
|:-:|:---|:---|
| 1 | Valor total (R$) da verba de retenção | Objetivo 2 (valor absoluto por segmento) |
| 2 | Custo unitário e taxa de aceitação esperada de cada oferta | Objetivos 4 e 5 (ações e retorno) |
| 3 | Margem ou valor do cliente ao longo da vida (CLV) | Objetivos 2 e 5 (priorização por valor e retorno) |
| 4 | Histórico de campanhas de retenção anteriores e datas de cancelamento | Objetivo 5 (comprovar efeito e calibrar a meta do piloto) |
| 5 | Meta de redução de churn definida pelo negócio | Objetivo 5 (indicador de sucesso do piloto) |
| 6 | Dados de uso e de atendimento (ausentes na base) | Melhoria da segmentação (fora do escopo atual) |
| 7 | Confirmação dos solicitantes e aprovação deste documento | Todos os objetivos |


!!! info "Fonte"
    Rascunho inicial dos objetivos 1 a 3 (grupo do projeto) e requisitos funcionais,
    recursos financeiros e análise custo-benefício de
    [Entendimento de negócio](entendimento-negocio.md). Objetivos 4 a 6 propostos pelo gerente de projetos, **pendentes de aprovação**. Não há ata ou termo de abertura formal;
    **[DECIDIR]** qual documento será citado como fonte oficial (versão 0.2, 31/10/2026).
