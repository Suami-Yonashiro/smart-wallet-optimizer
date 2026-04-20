# Smart Wallet Optimizer — Data-Driven Equity Valuation Engine.
## Otimizador de Carteira — Painel Valuation.

Ferramenta automatizada de análise de ações baseado em dados, projetada para identificar distorções entre preço de mercado e valor intrínseco na B3, combinando Python, SQL e Power BI.

Este projeto não constitui recomendação de investimento. Seu objetivo é estruturar um processo analítico escalável e orientado a dados para suporte à tomada de decisão.

---

## Contexto de negócio.

O mercado acionário brasileiro possui centenas de ativos listados, mas a identificação de oportunidades ainda é, em muitos casos, manual, subjetiva e pouco escalável.

Analisar individualmente ~1.000 ações exige:
- Tempo elevado.
- Padronização de critérios.
- Consistência analítica.
Sem automação, esse processo se torna inviável para análises recorrentes.

---

## Solução proposta. 

O Smart Wallet Optimizer automatiza o processo de triagem e avaliação de ações, aplicando critérios quantitativos inspirados no value investing para reduzir o universo analisado e destacar potenciais oportunidades.

Resultado prático:
Redução de ~997 → 168 ativos elegíveis.
Tempo de processamento: ~2 minutos.
Pipeline 100% reproduzível.

---

## Arquitetura da solução.

| Camada | Tecnologia | Função |
|---|---|---|
| Coleta | Python + fundamentus + yfinance | ETL de dados da B3 |
| Armazenamento | SQLite + SQLAlchemy | Banco de dados local |
| Processamento | Python + pandas | Limpeza, transformação e modelagem |
| Visualização | Power BI Desktop | Dashboard interativo |

---

## Metodologia.

### 1. Pipeline de dados (ETL).
Script para coleta de fundamentos via fundamentus e atualização de preços via yfinance. 
Cálculo de indicadores derivados para obter o LPA (lucro por ação) e VPA (valor patrimonial por ação). 

### 2. Filtro de elegibilidade (data-driven screening).
Apenas ações que passam nos três critérios entram no modelo:
- **P/L positivo** → empresa lucrativa.
- **ROE positivo** → eficiência sobre capital.
- **Liquidez mínima** → volume de R$ 1 milhão em 2 meses.

- Garante consistência estatística.
- Remove ruído do modelo.

### 3. Modelo de valuation (Graham).
Aplicação da fórmula.
**Preço Justo = √(22,5 × LPA × VPA)** 
**Margem de Segurança = ((Preço Justo - Cotação) / Preço Justo) × 100**

### 4. Classificação de ativos. 
- **COMPRAR** — margem de segurança acima de 25%.
- **AGUARDAR** — margem entre 0% e 25%.
- **EVITAR** — preço acima do valor justo.

---

## Camadas analíticas (Power BI).

O dashboard foi estruturado para suportar quatro diferentes níveis de decisão:

**1. Visão executiva.**
Snapshot do mercado.
Percentual (%) de ativos com margem positiva.
Indicador de “mercado caro vs barato”, >50% de forma generalizada, indica que o mercado está barato. 

**2. Visão metodológica.**
Funil de elegibilidade.
Transparência dos critérios aplicados, exclusão das 829 ações.

**3. Visão operacional.**
Barras com as principais oportunidades (filtro ≥ 59%).
Tabela com análise individual por ativo.

**4. Visão estratégica.**
Distribuição de recomendações.
Relação entre preço vs valor justo.
Identificação de padrões de mercado não evidentes nas visualizações anteriores.

---

## Diferenciais do projeto.
- Pipeline automatizado ponta a ponta.
- Integração entre múltiplas fontes de dados.
- Aplicação prática de modelo financeiro clássico.
- Estrutura escalável para novos modelos.
- Foco em tomada de decisão (não apenas visualização).

---

## Estrutura do projeto. 
```
smart-wallet-optimizer/
├── data/
│   ├── smart_wallet.db       # banco SQLite
│   └── smart_wallet.xlsx     # exportação para Power BI
├── scripts/
│   ├── salvar_banco.py       # ETL + modelo de Graham
│   ├── exportar_excel.py     # exportação para Power BI
│   └── explorar_dados.py     # análise exploratória
├── notebooks/                # exploração e testes
└── README.md
```

---

## Roadmap. Próximas evoluções.
- [ ] Análise de sentimento com notícias do mercado (NLP).
- [ ] Atualização automática via agendamento (Task Scheduler).
- [ ] Integração com APIs financeiras.
- [ ] Implementação de novos modelos (Magic Formula, múltiplos comparáveis).
- [ ] Sistema de alertas.

---

## Autor.
Projeto desenvolvido por Suami Yonashiro.
Foco em Analytics, BI e Data-Driven Strategy aplicada a negócios.