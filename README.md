<p align="center">
  <img src="assets/capa-firebird.png" alt="Business Intelligence com Firebird e Power BI" width="100%">
</p>

<h1 align="center">Business Intelligence com Firebird e Power BI</h1>

<p align="center">
  Exploração de um ERP Firebird, construção de consultas SQL, modelagem analítica e desenvolvimento de indicadores comerciais para Power BI.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Firebird-ODBC-E34F26?style=for-the-badge" alt="Firebird">
  <img src="https://img.shields.io/badge/SQL-Consultas%20Anal%C3%ADticas-336791?style=for-the-badge" alt="SQL">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Power%20BI-DAX%20e%20Power%20Query-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI">
  <img src="https://img.shields.io/badge/Status-Em%20evolu%C3%A7%C3%A3o-0A7E8C?style=for-the-badge" alt="Status">
</p>

## Visão geral

Este projeto organiza a construção de uma solução de Business Intelligence conectada a um ERP com banco de dados Firebird.

O trabalho parte da descoberta de um banco legado, passa pelo inventário de tabelas e relacionamentos, estrutura consultas SQL para fatos e dimensões e prepara os dados para consumo no Power BI.

Além da camada comercial, o projeto inclui uma primeira integração de informações de frete provenientes de uma planilha operacional, permitindo comparar valores cotados, realizados e associados às notas fiscais.

## Problema de negócio

Bancos de dados de ERPs legados costumam possuir grande quantidade de tabelas, nomenclaturas pouco intuitivas e relacionamentos sem documentação acessível.

Para transformar esses dados em indicadores confiáveis, foi necessário resolver desafios como:

- identificar as tabelas corretas de vendas, pedidos, clientes e produtos;
- compreender chaves e relacionamentos entre cabeçalhos e itens;
- tratar notas canceladas e registros inconsistentes;
- padronizar datas, códigos e valores financeiros;
- evitar duplicidade na consolidação das vendas;
- integrar dados comerciais com uma base manual de frete;
- preparar um modelo adequado para análise no Power BI.

## Solução desenvolvida

```text
ERP Firebird
     ↓
Conexão ODBC
     ↓
Inventário técnico do banco
     ↓
Exploração e validação das tabelas
     ↓
Consultas SQL de fatos e dimensões
     ↓
Exportação e tratamento dos dados
     ↓
Power Query e modelagem estrela
     ↓
Medidas DAX e indicadores comerciais
     ↓
Dashboard no Power BI
```

## Principais entregas

| Etapa | Entrega |
|---|---|
| Conexão | Integração com o Firebird por meio de ODBC e `pyodbc` |
| Descoberta | Inventário de tabelas, colunas, volumes e amostras |
| Documentação | Dicionário de tabelas e hipóteses de relacionamento |
| SQL | Consultas para fatos, dimensões e validações de qualidade |
| Modelagem | Estrutura inicial em modelo estrela para o Power BI |
| Power Query | Tratamento da base manual de frete com Linguagem M |
| DAX | Medidas comerciais, financeiras e logísticas |
| Auditoria | Consultas para validar cobertura, chaves e consistência |

## Modelo analítico

A direção atual do modelo comercial utiliza as seguintes estruturas:

### Tabelas fato

- `fVendas` — vendas faturadas, itens, quantidades, receitas e custos;
- `fPedidos` — pedidos comerciais e seus respectivos itens;
- `fFrete` — valores de frete consolidados no nível da nota fiscal;
- `fFreteExcecoes` — notas que exigem auditoria por inconsistência ou multiplicidade de registros.

### Tabelas dimensão

- `dClientes` — cadastro e atributos dos clientes;
- `dProdutos` — cadastro e classificação dos produtos;
- `dCalendario` — calendário analítico criado no Power BI.

### Principais origens no ERP

| Estrutura analítica | Tabelas de origem |
|---|---|
| `fVendas` | `NFSAIDA` e `NFSAIITE` |
| `fPedidos` | `PEDIDO` e `PEDITE` |
| `dClientes` | `CLIENTE` |
| `dProdutos` | `PRODUTO` e `PRODUTOEMPRESA` |
| `fFrete` | Planilha operacional de transportadoras |

## Indicadores desenvolvidos

As medidas DAX e as consultas atuais apoiam análises como:

### Vendas

- faturamento;
- quantidade vendida;
- custo total;
- lucro e margem;
- quantidade de notas fiscais;
- quantidade de pedidos;
- clientes ativos;
- produtos vendidos;
- ticket médio;
- análises por período.

### Frete

- frete emitido;
- frete cotado;
- diferença entre cotado e realizado;
- frete percentual sobre a nota fiscal;
- cobertura de relacionamento entre vendas e fretes;
- identificação de exceções para auditoria.

## Camada de frete

A camada de frete foi criada a partir de uma planilha operacional e estruturada em três consultas no Power Query:

| Consulta | Responsabilidade |
|---|---|
| `fFrete_base.m` | Importação e padronização da planilha original |
| `fFrete.m` | Consolidação dos registros no nível da nota fiscal |
| `fFreteExcecoes.m` | Separação de inconsistências e casos com múltiplos conhecimentos |

Entre os tratamentos realizados estão:

- extração do número e da data da nota fiscal;
- extração do número e da data do conhecimento de transporte;
- padronização de campos manuais;
- comparação entre frete cotado e frete emitido;
- criação de uma camada auditável;
- preparação da chave de relacionamento com `fVendas`.

> Como os números das notas podem possuir máscaras e zeros à esquerda, o modelo utiliza uma chave auxiliar padronizada para melhorar o relacionamento entre vendas e frete.

## Consultas SQL

### Fatos e dimensões

- [`queries/bi/fVendas.sql`](queries/bi/fVendas.sql)
- [`queries/bi/fPedidos.sql`](queries/bi/fPedidos.sql)
- [`queries/bi/dClientes.sql`](queries/bi/dClientes.sql)
- [`queries/bi/dProdutos.sql`](queries/bi/dProdutos.sql)

### Validações

- [`queries/bi/validacao_nfsaida_pedido.sql`](queries/bi/validacao_nfsaida_pedido.sql)
- [`queries/bi/validacao_nfsaida_cliente.sql`](queries/bi/validacao_nfsaida_cliente.sql)
- [`queries/bi/validacao_nfsaiite_produto.sql`](queries/bi/validacao_nfsaiite_produto.sql)
- [`queries/bi/validacao_fvendas_qualidade.sql`](queries/bi/validacao_fvendas_qualidade.sql)
- [`queries/bi/validacao_fpedidos_qualidade.sql`](queries/bi/validacao_fpedidos_qualidade.sql)

## Tecnologias utilizadas

| Categoria | Tecnologia | Aplicação |
|---|---|---|
| Banco de dados | Firebird | Fonte de dados do ERP |
| Conectividade | ODBC | Comunicação entre o ambiente analítico e o banco |
| Linguagem | SQL | Exploração, validação e construção das consultas |
| Automação | Python | Inventário do banco e exportação dos datasets |
| Biblioteca | pyodbc | Conexão do Python com o Firebird |
| Business Intelligence | Power BI | Modelagem, indicadores e visualizações |
| Transformação | Power Query / Linguagem M | Limpeza e preparação das bases |
| Métricas | DAX | Indicadores e inteligência de tempo |
| Versionamento | Git e GitHub | Documentação e controle de versões |

## Estrutura do projeto

```text
silo-firebird-bi/
├── assets/
│   └── capa-firebird.png
├── docs/
│   ├── dicionario_tabelas.md
│   ├── inventario_banco.md
│   ├── modelo_relacionamentos.md
│   ├── metricas_dax_iniciais.md
│   ├── release_notes_v1.md
│   ├── portfolio_descricao.md
│   └── frete.txt
├── powerbi/
│   ├── fFrete_base.m
│   ├── fFrete.m
│   ├── fFreteExcecoes.m
│   ├── medidas_iniciais.dax
│   └── medidas_frete.dax
├── queries/
│   ├── 01_listar_tabelas.sql
│   ├── 02_listar_colunas.sql
│   ├── 03_preview_vendas.sql
│   ├── 04_preview_produtos.sql
│   ├── bi/
│   └── exploracao/
├── scripts/
│   ├── conectar_firebird.py
│   ├── exportar_bi.py
│   ├── exportar_tabelas.py
│   └── inventario_banco.py
├── exports/
├── env.example
├── requirements.txt
└── README.md
```

## Como executar

### Pré-requisitos

- Python 3.10 ou superior;
- Firebird ou acesso ao servidor do ERP;
- driver ODBC compatível com o Firebird;
- Power BI Desktop para consumo e modelagem dos dados;
- Git para clonar o projeto.

### 1. Clone o repositório

```bash
git clone https://github.com/RenanDobriansky/BI-Project-with-Firebird.git
cd BI-Project-with-Firebird
```

### 2. Crie e ative o ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` com base em [`env.example`](env.example):

```env
FIREBIRD_HOST=127.0.0.1
FIREBIRD_PORT=3050
FIREBIRD_DATABASE=C:\caminho\para\seu\banco.fdb
FIREBIRD_USER=SYSDBA
FIREBIRD_PASSWORD=sua_senha
FIREBIRD_CHARSET=UTF8
```

Nunca envie o arquivo `.env` ou credenciais reais para o GitHub.

### 5. Teste a conexão

```powershell
python .\scripts\conectar_firebird.py
```

### 6. Gere o inventário do banco

```powershell
python .\scripts\inventario_banco.py
```

Arquivos esperados:

```text
exports/tabelas.csv
exports/colunas.csv
exports/contagem_linhas.csv
exports/preview_*.csv
```

### 7. Exporte uma amostra das tabelas

```powershell
python .\scripts\exportar_tabelas.py --limit 1000
```

### 8. Exporte os datasets de BI

```powershell
python .\scripts\exportar_bi.py
```

Arquivos esperados:

```text
exports/fVendas.csv
exports/fPedidos.csv
exports/dClientes.csv
exports/dProdutos.csv
```

## Segurança e privacidade

Este projeto se conecta a um banco de dados empresarial. Por isso:

- credenciais devem permanecer apenas no arquivo `.env` local;
- o arquivo físico do banco Firebird não deve ser versionado;
- exportações com dados reais devem permanecer fora do repositório público;
- nomes, documentos e informações comerciais devem ser anonimizados em exemplos;
- somente consultas, estruturas e amostras fictícias devem ser publicadas.

## Documentação complementar

- [Dicionário de tabelas](docs/dicionario_tabelas.md)
- [Inventário do banco](docs/inventario_banco.md)
- [Hipóteses de relacionamento](docs/modelo_relacionamentos.md)
- [Métricas DAX iniciais](docs/metricas_dax_iniciais.md)
- [Notas da camada de frete](docs/frete.txt)
- [Descrição para portfólio e LinkedIn](docs/portfolio_descricao.md)

## Resultados esperados

- centralização das informações comerciais;
- redução do trabalho manual para preparar bases;
- indicadores confiáveis de vendas, margem e frete;
- maior rastreabilidade entre ERP, consultas e dashboard;
- identificação de inconsistências antes da publicação dos dados;
- base reutilizável para novas análises e páginas no Power BI.

## Próximos passos

- padronizar a chave de nota fiscal entre `fVendas` e `fFrete`;
- ampliar a validação de cobertura dos relacionamentos;
- evoluir as medidas de margem considerando o impacto do frete;
- criar uma página específica para auditoria das exceções;
- adicionar capturas anonimizadas do dashboard ao README;
- documentar o modelo estrela final;
- automatizar a atualização das exportações utilizadas no Power BI.

## Autor

**Renan Dobriansky**  
Analista de Dados | Power BI | SQL | Python | Business Intelligence

[LinkedIn](https://www.linkedin.com/in/renandobriansky/) • [GitHub](https://github.com/RenanDobriansky)

---

Projeto desenvolvido para fins de aprendizado, aplicação prática e portfólio profissional.