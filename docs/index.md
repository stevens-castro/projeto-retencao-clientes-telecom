# Retenção de clientes Telecom

## Introdução

Empresas de telefonia e internet perdem clientes todos os meses. Quando um cliente cancela
o contrato, chamamos isso de **churn** (cancelamento). Conquistar um cliente novo costuma
custar bem mais caro do que manter quem já está na base, então entender **quem são os
clientes** e **quais perfis têm mais chance de sair** ajuda a empresa a agir antes do
cancelamento.

Este projeto usa a base pública *Telco Customer Churn* (7.043 clientes de uma operadora
fictícia) para **dividir os clientes em grupos parecidos** (segmentos). A ideia é que cada
grupo tenha um perfil claro (tipo de contrato, serviços contratados, forma de pagamento,
tempo de casa), para que a área de retenção possa criar ações diferentes para cada um.

## Dados do projeto

A base tem **uma linha por cliente** e 21 colunas: dados pessoais simples (idoso, tem
parceiro, tem dependentes), serviços contratados (telefone, internet, segurança online,
streaming etc.), informações do contrato (tempo de casa, tipo de contrato, forma de
pagamento) e valores cobrados (mensalidade e total já pago). Também traz a coluna `Churn`,
que diz se o cliente cancelou ou não.

Detalhes em [Fonte dos dados](fonte-dados.md) e [Entendimento dos dados](entendimento-dados.md).

### Levantamento inicial

!!! info "Tipo do projeto"
    - [x] Análise exploratória
    - [ ] Modelo preditivo
    - [ ] Modelo de classificação
    - [x] Modelo de agrupamento
    - [ ] Detecção de anomalias

### Nível de acesso

!!! warning "Confidencialidade"
    - [x] Público
    - [ ] Interno (toda a organização)
    - [ ] Restrito (apenas a área requisitante)

    A base é pública (disponibilizada pela IBM como exemplo) e não identifica pessoas reais.

### Objetivos de negócio

!!! quote ""
    Separar a carteira de clientes em **segmentos com perfis diferentes**, usando
    aprendizado **não supervisionado** (o algoritmo encontra os grupos sozinho, sem saber
    quem cancelou), para que a área de retenção consiga entender cada grupo e planejar
    ações específicas para os perfis com maior risco de cancelamento.

## Sobre o projeto

### Histórico do documento

| Data       | Versão | Descrição                                                        | Autor             |
| :--------- | :----- | :--------------------------------------------------------------- | :---------------- |
| 30/10/2026 | 1.0    | Preenchimento com o que foi consolidado nos notebooks 00 a 03     | Equipe do projeto |

### Dados do solicitante

``` mermaid
flowchart TD
    id1[MBA em Dados] --o id2[Disciplina de Aprendizado de Máquina Não Supervisionado]
```

| Nome                                                   | Cargo / Função          | E-mail |
| :----------------------------------------------------- | :---------------------- | :----- |
| <span style="color:red">**Nome do professor**</span>   | Professor da disciplina | —      |

### Dados da equipe técnica

| Nome                   | Cargo / Função      | E-mail |
| :--------------------- | :------------------ | :----- |
| Stevens Castro         | Integrante do grupo | —      |
| Tevin                  | Integrante do grupo | —      |
| Thierry Pereira Canoco | Integrante do grupo | —      |
