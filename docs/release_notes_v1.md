# Release Notes v0.1.0

## Titulo sugerido

`v0.1.0 - Estrutura inicial de exploracao Firebird para BI`

## Resumo

Primeira versao publica do projeto de exploracao de um ERP com banco Firebird, com foco em inventario tecnico, descoberta de relacionamentos e preparacao de datasets iniciais para Power BI.

## Entregas desta versao

- conexao com Firebird via ODBC usando Python
- configuracao por variaveis de ambiente
- inventario automatizado do banco
- exportacao de tabelas e consultas para CSV
- classificacao de tabelas por assunto de negocio
- documentacao inicial de relacionamento entre entidades
- queries iniciais para `fVendas`, `fPedidos`, `dClientes` e `dProdutos`
- queries de validacao para cobertura de cliente, produto, pedido e qualidade das fatos

## Principais arquivos

- `scripts/conectar_firebird.py`
- `scripts/inventario_banco.py`
- `scripts/exportar_tabelas.py`
- `scripts/exportar_bi.py`
- `queries/bi/fVendas.sql`
- `queries/bi/fPedidos.sql`
- `queries/bi/dClientes.sql`
- `queries/bi/dProdutos.sql`

## Valor entregue

Esta versao organiza a fase mais critica de um projeto de BI sobre ERP legado: transformar um banco pouco documentado em uma base exploravel, validada e pronta para evoluir para modelo estrela e dashboards comerciais.

## Proximos passos

- criar `dCalendario`
- refinar regras de cancelamento e status comercial
- cruzar vendas com financeiro em `TITRECEB`
- consolidar a primeira versao do modelo estrela no Power BI
- publicar exemplos visuais do dashboard
