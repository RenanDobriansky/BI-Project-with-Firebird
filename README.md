# Silo Firebird BI

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Firebird](https://img.shields.io/badge/Firebird-ODBC-E54D2E)
![Power BI](https://img.shields.io/badge/Power%20BI-Modelagem%20Comercial-F2C811?logo=powerbi&logoColor=black)
![Status](https://img.shields.io/badge/Status-Em%20Evolucao-0A7E8C)

Exploracao de um ERP em Firebird com foco em BI, modelagem estrela e preparacao de dados para Power BI, incluindo uma camada inicial de frete a partir de planilha operacional.

## Visao Geral

Este repositorio organiza o trabalho de descoberta do banco, validacao de relacionamentos e montagem das primeiras estruturas analiticas para uso comercial.

Hoje o projeto cobre:

- conexao com Firebird via ODBC
- inventario tecnico do banco
- exportacao de tabelas e consultas para CSV
- classificacao de tabelas por assunto
- hipoteses de relacionamento entre entidades
- queries iniciais de `fVendas`, `fPedidos`, `dClientes` e `dProdutos`
- camada de frete manual no Power BI com `fFrete`, `fFrete_base` e `fFreteExcecoes`
- medidas DAX iniciais para vendas e frete

Repositorio GitHub:

- <https://github.com/RenanDobriansky/BI-Project-with-Firebird>

## Objetivo

Construir uma base inicial para um modelo estrela no Power BI, priorizando o dashboard comercial.

Escopo atual:

- `fVendas`
- `fPedidos`
- `dClientes`
- `dProdutos`
- `dCalendario` no Power BI
- `fFrete` a partir de planilha manual de transportes

## Estrutura do Projeto

```text
silo-firebird-bi/
|-- README.md
|-- requirements.txt
|-- env.example
|-- docs/
|   |-- dicionario_tabelas.md
|   |-- inventario_banco.md
|   |-- modelo_relacionamentos.md
|   `-- frete.txt
|-- powerbi/
|   |-- fFrete_base.m
|   |-- fFrete.m
|   |-- fFreteExcecoes.m
|   |-- medidas_iniciais.dax
|   `-- medidas_frete.dax
|-- queries/
|   |-- 01_listar_tabelas.sql
|   |-- 02_listar_colunas.sql
|   |-- 03_preview_vendas.sql
|   |-- 04_preview_produtos.sql
|   |-- bi/
|   `-- exploracao/
|-- scripts/
|   |-- conectar_firebird.py
|   |-- exportar_bi.py
|   |-- exportar_tabelas.py
|   `-- inventario_banco.py
`-- exports/
```

## Fluxo do Projeto

1. Conectar no Firebird via ODBC.
2. Gerar inventario de tabelas, colunas e volume.
3. Identificar tabelas candidatas para vendas, clientes, produtos, estoque e financeiro.
4. Validar relacionamentos mais provaveis.
5. Montar queries iniciais das fatos e dimensoes.
6. Exportar datasets para testes no Power BI.
7. Estruturar o frete manual em Power Query para cruzamento com `fVendas`.

## Quick Start

### 1. Requisitos

- Python 3.10 ou superior
- Driver ODBC do Firebird instalado no Windows
- `pyodbc`

### 2. Instalar dependencias

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se preferir instalar direto no Python que executa os scripts:

```powershell
"C:\Users\renan\AppData\Local\Programs\Python\Python312\python.exe" -m pip install -r requirements.txt
```

### 3. Configurar variaveis de ambiente

Voce pode configurar as variaveis direto no PowerShell:

```powershell
$env:FIREBIRD_HOST="127.0.0.1"
$env:FIREBIRD_PORT="3050"
$env:FIREBIRD_DATABASE="C:\dados\ERP.FDB"
$env:FIREBIRD_USER="SYSDBA"
$env:FIREBIRD_PASSWORD="masterkey"
$env:FIREBIRD_CHARSET="UTF8"
```

Ou criar um arquivo `.env` na raiz do projeto:

```text
FIREBIRD_HOST=127.0.0.1
FIREBIRD_PORT=3050
FIREBIRD_DATABASE=C:\dados\ERP.FDB
FIREBIRD_USER=SYSDBA
FIREBIRD_PASSWORD=masterkey
FIREBIRD_CHARSET=UTF8
```

Use [env.example](env.example) como modelo.

### 4. Testar a conexao

```powershell
python .\scripts\conectar_firebird.py
```

### 5. Gerar inventario do banco

```powershell
python .\scripts\inventario_banco.py
```

Arquivos gerados:

- `exports/tabelas.csv`
- `exports/colunas.csv`
- `exports/contagem_linhas.csv`
- `exports/preview_*.csv`

### 6. Exportar tabelas brutas

```powershell
python .\scripts\exportar_tabelas.py --limit 1000
```

### 7. Exportar datasets de BI

```powershell
python .\scripts\exportar_bi.py
```

Exportacoes padrao:

- `exports/fVendas.csv`
- `exports/fPedidos.csv`
- `exports/dClientes.csv`
- `exports/dProdutos.csv`

## Consultas de BI Atuais

### Fatos

- [queries/bi/fVendas.sql](queries/bi/fVendas.sql)
- [queries/bi/fPedidos.sql](queries/bi/fPedidos.sql)

### Dimensoes

- [queries/bi/dClientes.sql](queries/bi/dClientes.sql)
- [queries/bi/dProdutos.sql](queries/bi/dProdutos.sql)

### Validacoes

- [queries/bi/validacao_nfsaida_pedido.sql](queries/bi/validacao_nfsaida_pedido.sql)
- [queries/bi/validacao_nfsaida_cliente.sql](queries/bi/validacao_nfsaida_cliente.sql)
- [queries/bi/validacao_nfsaiite_produto.sql](queries/bi/validacao_nfsaiite_produto.sql)
- [queries/bi/validacao_fvendas_qualidade.sql](queries/bi/validacao_fvendas_qualidade.sql)
- [queries/bi/validacao_fpedidos_qualidade.sql](queries/bi/validacao_fpedidos_qualidade.sql)

## Camada de Frete no Power BI

A primeira versao de frete foi estruturada a partir da planilha manual `CONTROLE TRANSPORTADORA.xlsx`, usando a aba `CONHECIMENTOSILO`.

Arquivos principais:

- [powerbi/fFrete_base.m](powerbi/fFrete_base.m)
- [powerbi/fFrete.m](powerbi/fFrete.m)
- [powerbi/fFreteExcecoes.m](powerbi/fFreteExcecoes.m)
- [powerbi/medidas_frete.dax](powerbi/medidas_frete.dax)

O que essa camada faz:

- trata colunas manuais de frete cotado e frete emitido
- extrai `NUMERO_NF`, `DATA_NF`, `NUMERO_CTE` e `DATA_CTE`
- consolida a fato de frete no grao de NF
- separa excecoes com multiplos conhecimentos ou inconsistencias
- prepara medidas para analise de frete realizado x cotado

### Relacoes esperadas no modelo

- `dCalendario[Data] -> fFrete[DATA_NF]`
- `fFrete` deve se relacionar com `fVendas` por numero da NF

Observacao importante:

- como a planilha manual pode trazer NFs sem zeros a esquerda e a `fVendas` pode trazer a nota com mascara como `000024504`, o ideal e criar uma chave auxiliar sem zeros a esquerda nas duas tabelas antes do relacionamento no modelo

## Medidas DAX

Arquivos atuais:

- [powerbi/medidas_iniciais.dax](powerbi/medidas_iniciais.dax)
- [powerbi/medidas_frete.dax](powerbi/medidas_frete.dax)

As medidas atuais cobrem:

- faturamento, quantidade, custo, lucro e margem
- contagem de notas, pedidos, clientes e produtos
- inteligencia temporal basica
- frete emitido, frete cotado, diferenca de frete e frete percentual sobre a NF

## Documentacao

- [Dicionario de tabelas](docs/dicionario_tabelas.md)
- [Inventario do banco](docs/inventario_banco.md)
- [Hipoteses de relacionamento](docs/modelo_relacionamentos.md)
- [Metricas DAX iniciais](docs/metricas_dax_iniciais.md)
- [Release notes iniciais](docs/release_notes_v1.md)
- [Descricoes para portfolio e LinkedIn](docs/portfolio_descricao.md)
- [Notas da camada de frete](docs/frete.txt)

## Tabelas Prioritarias para Dashboard Comercial

Ordem recomendada de investigacao:

1. `NFSAIITE`
2. `NFSAIDA`
3. `CLIENTE`
4. `PRODUTO`
5. `TITRECEB`
6. `PEDITE`
7. `PEDIDO`
8. `CAIXAVENDAMOV`
9. `CAIXAVENDAITENS`
10. `CAIXAVENDARECEB`

## Direcao Atual do Modelo

Hipotese atual do modelo comercial:

- `fVendas` baseada em `NFSAIDA + NFSAIITE`
- `fPedidos` baseada em `PEDIDO + PEDITE`
- `dClientes` baseada em `CLIENTE`
- `dProdutos` baseada em `PRODUTO + PRODUTOEMPRESA`
- `dCalendario` criada no Power BI
- `fFrete` baseada em planilha manual consolidada no grao de NF

## Publicacao no GitHub

### Descricao curta para o campo About

Use esta sugestao no GitHub:

`Exploracao de ERP Firebird para BI com inventario automatizado, modelagem comercial e camada de frete para Power BI.`

### Topicos sugeridos

Sugestao de tags para o repositorio:

- `firebird`
- `odbc`
- `python`
- `power-bi`
- `business-intelligence`
- `data-modeling`
- `sql`
- `etl`

Antes de publicar:

- nao versionar `.env`
- nao subir CSVs com dados sensiveis
- revisar se `exports/` deve ficar fora do repositorio
- manter apenas exemplos ficticios em configuracoes

## Boas Praticas

- Use variaveis de ambiente para credenciais.
- Trate os CSVs exportados como dados potencialmente sensiveis.
- Valide relacionamentos antes de consolidar as fatos no Power BI.
- Prefira exportacoes pequenas no inicio, como `--limit 1000`, para acelerar os testes.
- Em tabelas manuais, preserve uma camada base e uma camada consolidada para auditoria.

## Proximos Passos

- padronizar a chave de NF entre `fVendas` e `fFrete`
- validar cobertura de relacionamento entre venda e frete
- evoluir as medidas de margem considerando frete
- criar pagina de auditoria no Power BI para `fFreteExcecoes`
