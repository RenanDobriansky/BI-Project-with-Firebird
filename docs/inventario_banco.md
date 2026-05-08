# Inventario do Banco Firebird

Este processo gera um inventario estrutural do banco via ODBC e salva os resultados em CSV dentro de `exports/`.

O fluxo atual foi pensado para bases grandes:

- gera `tabelas.csv` e `colunas.csv` primeiro
- gera os previews das tabelas relevantes antes da contagem
- grava `contagem_linhas.csv` de forma incremental, tabela por tabela

## Arquivos Gerados

- [exports/tabelas.csv](/c:/Users/renan/Desktop/Projetos%20BI/Silo%20Miotto/silo-firebird-bi/exports/tabelas.csv): lista de tabelas de usuario encontradas no banco
- [exports/colunas.csv](/c:/Users/renan/Desktop/Projetos%20BI/Silo%20Miotto/silo-firebird-bi/exports/colunas.csv): colunas, tipos, tamanho e nulabilidade
- [exports/contagem_linhas.csv](/c:/Users/renan/Desktop/Projetos%20BI/Silo%20Miotto/silo-firebird-bi/exports/contagem_linhas.csv): contagem por tabela

Tambem sao gerados previews das tabelas mais relevantes, em arquivos como:

- `exports/preview_CLIENTE.csv`
- `exports/preview_PRODUTO.csv`
- `exports/preview_PEDIDO.csv`
- `exports/preview_VENDAS.csv`
- `exports/preview_CAIXAVENDA.csv`
- `exports/preview_CAIXAVENDAITENS.csv`

## Campos do Inventario

### `tabelas.csv`

- `tabela`: nome da tabela

### `colunas.csv`

- `tabela`: nome da tabela
- `coluna`: nome da coluna
- `tipo_dado`: tipo derivado do catalogo Firebird
- `tamanho`: comprimento ou tamanho interno do campo
- `aceita_nulo`: `SIM` ou `NAO`

### `contagem_linhas.csv`

- `tabela`: nome da tabela
- `contagem_linhas_aproximada`: total atual retornado pela consulta
- `metodo`: forma usada para a contagem

Observacao:

- apesar do nome do arquivo usar "aproximada", a implementacao atual tenta `COUNT(*)` em cada tabela
- isso foi escolhido porque a exposicao de estatisticas aproximadas por SQL varia bastante entre versoes e drivers do Firebird

## Script Responsavel

O inventario e gerado por:

- [scripts/inventario_banco.py](/c:/Users/renan/Desktop/Projetos%20BI/Silo%20Miotto/silo-firebird-bi/scripts/inventario_banco.py)

## Como Executar

Com o `.env` ja configurado:

```powershell
C:\Users\renan\AppData\Local\Programs\Python\Python312\python.exe .\silo-firebird-bi\scripts\inventario_banco.py
```

Se a contagem demorar muito, voce pode:

```powershell
C:\Users\renan\AppData\Local\Programs\Python\Python312\python.exe .\silo-firebird-bi\scripts\inventario_banco.py --skip-counts
```

E depois retomar apenas as contagens:

```powershell
C:\Users\renan\AppData\Local\Programs\Python\Python312\python.exe .\silo-firebird-bi\scripts\inventario_banco.py --resume-counts
```

## Escopo dos Previews

As tabelas atualmente consideradas mais relevantes para preview sao:

- `CLIENTE`
- `PRODUTO`
- `PRODUTOEMPRESA`
- `PEDIDO`
- `VENDAS`
- `CAIXAVENDA`
- `CAIXAVENDAITENS`
- `NFSAIDA`
- `NFSAIITE`
- `PRODUTOMOVIMENTACAO`
- `TITRECEB`
- `TITPAGAR`
- `FORNEC`
- `NFENTRAD`
- `NFENTITE`

## Uso Recomendado

Depois de gerar o inventario:

1. revise `tabelas.csv` para entender a cobertura funcional do ERP
2. use `colunas.csv` para localizar chaves, datas e valores
3. use `contagem_linhas.csv` para priorizar tabelas com maior volume
4. valide os previews antes de puxar tabelas completas para o Power BI
