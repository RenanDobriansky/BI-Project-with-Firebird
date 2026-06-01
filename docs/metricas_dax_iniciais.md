# Metricas DAX Iniciais

As queries finais da primeira analise passaram a usar:

- `fVendas`
- `dClientes`
- `dProdutos`
- `dCalendario` no Power BI

## Relacionamentos esperados no Power BI

- `dCalendario[Data] -> fVendas[DATA_VENDA]`
- `dClientes[CODIGO_CLIENTE] -> fVendas[CODIGO_CLIENTE]`
- `dProdutos[CODIGO_PRODUTO] -> fVendas[CODIGO_PRODUTO]`

## Arquivo de medidas

As medidas iniciais foram salvas em:

- [powerbi/medidas_iniciais.dax](../powerbi/medidas_iniciais.dax)

## Primeiro bloco de indicadores

- faturamento
- quantidade vendida
- custo total
- lucro bruto
- margem bruta percentual
- quantidade de notas fiscais
- quantidade de pedidos
- quantidade de clientes
- quantidade de produtos vendidos
- ticket medio
- preco medio unitario
- custo medio unitario

## Inteligencia temporal inicial

- faturamento MTD
- faturamento YTD
- faturamento ano anterior
- variacao absoluta vs ano anterior
- variacao percentual vs ano anterior
- lucro bruto MTD
- lucro bruto YTD
- margem bruta percentual YTD

## Observacao

Se a sua tabela calendario usar outro nome de coluna de data, ajuste as medidas que referenciam `dCalendario[Data]`.
