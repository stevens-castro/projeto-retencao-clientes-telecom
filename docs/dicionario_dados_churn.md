# Dicionário de Dados: Churn de Clientes (21 features)

| # | Feature | Descrição |
|---|---|---|
| 1 | **customerID** | Identificador único de cada cliente. |
| 2 | **gender** | Gênero do cliente: Male (Masculino), Female (Feminino). |
| 3 | **SeniorCitizen** | Indica se o cliente tem 65 anos ou mais: 1 (Sim), 0 (Não). |
| 4 | **Partner** | Indica se o cliente possui cônjuge ou companheiro(a): Yes, No. |
| 5 | **Dependents** | Indica se o cliente mora com algum dependente (filhos, pais, avós etc.): Yes, No. |
| 6 | **tenure** | Quantidade total de meses que o cliente permanece na empresa. |
| 7 | **PhoneService** | Indica se o cliente assina o serviço de telefone residencial da empresa: Yes, No. |
| 8 | **MultipleLines** | Indica se o cliente assina múltiplas linhas telefônicas com a empresa: Yes, No, No phone service (sem serviço de telefone). |
| 9 | **InternetService** | Tipo de serviço de internet assinado com a empresa: DSL, Fiber optic (Fibra Óptica), No (Não possui). |
| 10 | **OnlineSecurity** | Indica se o cliente assina um serviço adicional de segurança online oferecido pela empresa: Yes, No, No internet service (sem internet). |
| 11 | **OnlineBackup** | Indica se o cliente assina um serviço adicional de backup online oferecido pela empresa: Yes, No, No internet service. |
| 12 | **DeviceProtection** | Indica se o cliente assina um plano adicional de proteção para seus equipamentos de internet: Yes, No, No internet service. |
| 13 | **TechSupport** | Indica se o cliente assina um plano adicional de suporte técnico com tempo de espera reduzido: Yes, No, No internet service. |
| 14 | **StreamingTV** | Indica se o cliente usa a internet para assistir programas de TV por streaming de um provedor terceiro: Yes, No, No internet service. A empresa não cobra taxa adicional por isso. |
| 15 | **StreamingMovies** | Indica se o cliente usa a internet para assistir filmes por streaming de um provedor terceiro: Yes, No, No internet service. A empresa não cobra taxa adicional por isso. |
| 16 | **Contract** | Tipo de contrato atual do cliente: Month-to-month (Mensal), One year (Um ano), Two year (Dois anos). |
| 17 | **PaperlessBilling** | Indica se o cliente optou pela fatura digital (sem papel): Yes, No. |
| 18 | **PaymentMethod** | Forma de pagamento do cliente: Electronic check (Cheque eletrônico), Mailed check (Cheque via correio), Bank transfer (automatic) (Transferência bancária automática), Credit card (automatic) (Cartão de crédito automático). |
| 19 | **MonthlyCharges** | Valor mensal total atual cobrado do cliente por todos os serviços contratados. |
| 20 | **TotalCharges** | Valor total já cobrado do cliente durante todo o período como cliente. |
| 21 | **Churn** | Variável alvo. Indica se o cliente deixou a empresa no último mês: Yes, No. |
