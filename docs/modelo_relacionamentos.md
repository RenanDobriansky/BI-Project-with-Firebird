# Modelo de Relacionamentos Proposto

Este documento resume hipoteses de relacionamento entre as tabelas candidatas de vendas, itens de venda, clientes e produtos com base em:

- nomes das colunas em `exports/colunas.csv`
- amostras em `exports/preview_*.csv`
- contagens e dicionario ja construidos

Importante:

- as relacoes abaixo sao inferidas por nome e padrao de dados
- o banco pode nao expor chaves estrangeiras declaradas
- o nivel de confianca indica o quanto o relacionamento parece consistente pelo inventario

## Sinais Encontrados

Ao procurar campos como `IDVENDA`, `CODVENDA`, `IDCLIENTE`, `CODCLIENTE`, `IDPRODUTO`, `CODPRODUTO`, `IDEMPRESA`, `DATA`, `NUMERO` e `DOCUMENTO`, o padrao observado foi:

- nao apareceu um padrao unico de `IDVENDA`
- vendas parecem ser identificadas por tabelas diferentes conforme o processo:
  - `NFSAIDA.ID`
  - `PEDIDO.ID`
  - `CAIXAVENDAMOV.ID`
  - `CUPOMFISCAL.ID`
- cliente aparece quase sempre como `CLIENTE` nas fatos, em formato compativel com `CLIENTE.CODIGO`
- produto aparece quase sempre como `IDPRODUTO` nas fatos, em formato compativel com `PRODUTO.ID`
- empresa aparece como `EMPRESA`, normalmente `VARCHAR(3)`
- documentos comerciais aparecem em campos como:
  - `NOTAFISCAL`
  - `NUMPEDIDO`
  - `NUMERO`
  - `CODCUPOMFISCAL`
  - `DOCUMENTO`

## Hipoteses de Chave por Tabela

## Clientes

- `CLIENTE.ID`: chave tecnica candidata
- `CLIENTE.CODIGO`: chave de negocio mais provavel para relacionar com fatos
- `CLIENTE.CGCCPF`: chave natural auxiliar, nao recomendada como principal

## Produtos

- `PRODUTO.ID`: chave tecnica candidata
- `PRODUTO.CODIGO`: chave de negocio candidata

## Vendas

- `NFSAIDA.ID`: chave tecnica do cabecalho de nota
- `PEDIDO.ID`: chave tecnica do cabecalho de pedido
- `CAIXAVENDAMOV.ID`: chave tecnica do movimento de venda no PDV
- `CUPOMFISCAL.ID`: chave tecnica do cupom fiscal

## Itens

- `NFSAIITE.ID`: chave tecnica do item
- `PEDITE.ID`: chave tecnica do item do pedido
- `CAIXAVENDAITENS.ID`: chave tecnica do item do PDV
- `CUPOMITEM.ID`: chave tecnica do item do cupom

## Relacionamentos com Alta Confianca

### 1. Nota fiscal de saida -> itens da nota

- Relacao: `NFSAIITE.IDNFSAIDA` -> `NFSAIDA.ID`
- Confianca: `Alta`
- Motivo: padrao classico cabecalho-item; nomes e tipos sao compativeis

### 2. Pedido -> itens do pedido

- Relacao: `PEDITE.IDPEDIDO` -> `PEDIDO.ID`
- Confianca: `Alta`
- Motivo: padrao classico cabecalho-item; nomes e tipos sao compativeis

### 3. Movimento PDV -> itens do PDV

- Relacao: `CAIXAVENDAITENS.IDCAIXAMOVIMENTO` -> `CAIXAVENDAMOV.ID`
- Confianca: `Alta`
- Motivo: nome da coluna e semantica indicam item vinculado ao movimento do caixa

### 4. Movimento PDV -> recebimentos do PDV

- Relacao: `CAIXAVENDARECEB.IDCAIXAVENDAMOV` -> `CAIXAVENDAMOV.ID`
- Confianca: `Alta`
- Motivo: coluna explicita de referencia ao movimento de venda

### 5. Cupom fiscal -> itens do cupom

- Relacao: `CUPOMITEM.IDCUPOMFISCAL` -> `CUPOMFISCAL.ID`
- Confianca: `Alta`
- Motivo: padrao classico cabecalho-item e nomes identicos

### 6. Itens de nota -> produto

- Relacao: `NFSAIITE.IDPRODUTO` -> `PRODUTO.ID`
- Confianca: `Alta`
- Motivo: `IDPRODUTO` aparece como inteiro nas fatos e `PRODUTO.ID` e inteiro tecnico

### 7. Itens de pedido -> produto

- Relacao: `PEDITE.IDPRODUTO` -> `PRODUTO.ID`
- Confianca: `Alta`
- Motivo: mesmo padrao de chave tecnica por produto

### 8. Itens do PDV -> produto

- Relacao: `CAIXAVENDAITENS.IDPRODUTO` -> `PRODUTO.ID`
- Confianca: `Alta`
- Motivo: mesmo padrao de chave tecnica por produto

### 9. Itens do cupom -> produto

- Relacao: `CUPOMITEM.IDPRODUTO` -> `PRODUTO.ID`
- Confianca: `Alta`
- Motivo: mesmo padrao de chave tecnica por produto

### 10. Produto por empresa -> produto

- Relacao: `PRODUTOEMPRESA.IDPRODUTO` -> `PRODUTO.ID`
- Confianca: `Alta`
- Motivo: nome da coluna e cardinalidade esperada produto x empresa

### 11. Historico de preco -> produto

- Relacao: `PRODUTO_PRECO.IDPRODUTO` -> `PRODUTO.ID`
- Confianca: `Alta`
- Motivo: tabela enxuta com `IDPRODUTO`, `DATA`, `PRECO`

### 12. Nota fiscal -> cliente

- Relacao: `NFSAIDA.CLIENTE` -> `CLIENTE.CODIGO`
- Confianca: `Alta`
- Motivo: preview mostra `CLIENTE` como codigo textual de 6 posicoes, aderente a `CLIENTE.CODIGO`

### 13. Pedido -> cliente

- Relacao: `PEDIDO.CLIENTE` -> `CLIENTE.CODIGO`
- Confianca: `Alta`
- Motivo: mesmo padrao de codigo de cliente usado no cabecalho do pedido

### 14. Movimento PDV -> cliente

- Relacao: `CAIXAVENDAMOV.CLIENTE` -> `CLIENTE.CODIGO`
- Confianca: `Alta`
- Motivo: coluna textual de cliente com mesma semantica encontrada nas demais vendas

### 15. Cupom fiscal -> cliente

- Relacao: `CUPOMFISCAL.CLIENTE` -> `CLIENTE.CODIGO`
- Confianca: `Alta`
- Motivo: mesmo padrao textual de codigo do cliente

### 16. Titulo a receber -> cliente

- Relacao: `TITRECEB.CLIENTE` -> `CLIENTE.CODIGO`
- Confianca: `Alta`
- Motivo: preview de `TITRECEB` mostra o mesmo formato de codigo do cliente

## Relacionamentos com Media Confianca

### 17. Itens do PDV -> cliente

- Relacao: `CAIXAVENDAITENS.CLIENTE` -> `CLIENTE.CODIGO`
- Confianca: `Media`
- Motivo: a coluna existe, mas em algumas vendas de PDV o cliente pode estar vazio ou ser herdado do cabecalho

### 18. Itens do cupom -> cliente

- Relacao: `CUPOMITEM.CLIENTE` -> `CLIENTE.CODIGO`
- Confianca: `Media`
- Motivo: existe no item, mas pode ser redundante em relacao ao cabecalho

### 19. Nota fiscal -> titulo a receber

- Relacao: `TITRECEB.IDORIGEM` -> `NFSAIDA.ID`, quando `TITRECEB.ORIGEM = 'NFSAID'`
- Confianca: `Media`
- Motivo: o preview mostra `ORIGEM = NFSAID` e `IDORIGEM` coerente com IDs de nota

### 20. Movimento PDV -> titulo a receber

- Relacao: `CAIXAVENDAMOV.IDTITRECEB` -> `TITRECEB.ID`
- Confianca: `Media`
- Motivo: a coluna sugere integracao entre venda no caixa e financeiro, mas precisa validacao com amostras

### 21. Movimento PDV -> nota fiscal

- Relacao: `CAIXAVENDAMOV.IDNFSAIDA` -> `NFSAIDA.ID`
- Confianca: `Media`
- Motivo: nome explicito e coerente com faturamento posterior do caixa

### 22. Movimento PDV -> cupom fiscal

- Relacao: `CAIXAVENDAMOV.CODCUPOMFISCAL` -> `CUPOMFISCAL.NUMERO`
- Confianca: `Media`
- Motivo: sem coluna `IDCUPOMFISCAL`, o vinculo parece ser por numero do cupom

### 23. Movimento PDV -> pedido

- Relacao: `CAIXAVENDAMOV.NUMEROORIGEM` -> `PEDIDO.NUMPEDIDO` ou `PEDIDO.ID`, dependendo do processo
- Confianca: `Media`
- Motivo: `NUMEROORIGEM` sugere documento de origem, mas precisa checagem em dados reais

### 24. Itens do PDV -> origem comercial

- Relacao: `CAIXAVENDAITENS.IDORIGEM` -> tabela de origem variavel, possivelmente `PEDIDO`, `NFSAIDA` ou outra
- Confianca: `Media`
- Motivo: nome generico; depende do campo `TIPO` ou da regra de negocio

### 25. Produto -> grade

- Relacao: `PRODUTO.IDPRODUTOGRADE` -> `PRODUTOGRADE.ID`
- Confianca: `Media`
- Motivo: a tabela `PRODUTO` aponta para uma grade, mas `PRODUTOGRADE` tambem tem auto-relacao por `IDPRODUTOGRADE`

### 26. Itens -> grade

- Relacoes:
  - `NFSAIITE.IDPRODUTOGRADE` -> `PRODUTOGRADE.ID`
  - `PEDITE.IDPRODUTOGRADE` -> `PRODUTOGRADE.ID`
  - `CAIXAVENDAITENS.IDPRODUTOGRADE` -> `PRODUTOGRADE.ID`
  - `CUPOMITEM.IDPRODUTOGRADE` -> `PRODUTOGRADE.ID`
- Confianca: `Media`
- Motivo: nome consistente, mas a interpretacao da grade precisa validacao pela hierarquia da propria tabela

## Relacionamentos com Baixa Confianca

### 27. Nota fiscal -> pedido

- Relacao: `NFSAIDA.NUMEROORIGEM` -> `PEDIDO.NUMPEDIDO`
- Confianca: `Baixa`
- Motivo: pode existir em alguns cenarios, mas o nome `NUMEROORIGEM` e generico e pode apontar para outros documentos

### 28. Pedido -> financeiro

- Relacao: `TITRECEB.NUMPEDIDO` -> `PEDIDO.NUMPEDIDO`
- Confianca: `Baixa`
- Motivo: o campo existe em `TITRECEB`, mas pode nao estar preenchido de forma padronizada

### 29. Cupom fiscal -> nota fiscal

- Relacao: `CUPOMFISCAL.NUMERONF` -> `NFSAIDA.NOTAFISCAL`
- Confianca: `Baixa`
- Motivo: possivel conversao de cupom em nota, mas sem chave tecnica explicita no inventario

## Mapa Proposto para Modelo Comercial

## Fatos principais

- `fVendasFaturadas`: `NFSAIITE`
- `fPedidos`: `PEDITE`
- `fPdv`: `CAIXAVENDAITENS`
- `fRecebimentos`: `TITRECEB`

## Dimensoes principais

- `dCliente`: `CLIENTE`
- `dProduto`: `PRODUTO`
- `dProdutoEmpresa`: `PRODUTOEMPRESA`
- `dCalendario`: derivada no Power BI

## Juncoes mais seguras para comecar

- `NFSAIITE.IDNFSAIDA = NFSAIDA.ID`
- `NFSAIITE.IDPRODUTO = PRODUTO.ID`
- `NFSAIDA.CLIENTE = CLIENTE.CODIGO`
- `PEDITE.IDPEDIDO = PEDIDO.ID`
- `PEDITE.IDPRODUTO = PRODUTO.ID`
- `PEDIDO.CLIENTE = CLIENTE.CODIGO`
- `CAIXAVENDAITENS.IDCAIXAMOVIMENTO = CAIXAVENDAMOV.ID`
- `CAIXAVENDAITENS.IDPRODUTO = PRODUTO.ID`
- `CAIXAVENDAMOV.CLIENTE = CLIENTE.CODIGO`
- `CAIXAVENDARECEB.IDCAIXAVENDAMOV = CAIXAVENDAMOV.ID`
- `PRODUTOEMPRESA.IDPRODUTO = PRODUTO.ID`
- `PRODUTO_PRECO.IDPRODUTO = PRODUTO.ID`

## Proximos Testes Recomendados

1. Validar se todo `NFSAIITE.IDNFSAIDA` existe em `NFSAIDA.ID`.
2. Validar se todo `PEDITE.IDPEDIDO` existe em `PEDIDO.ID`.
3. Medir cobertura de `CLIENTE` nas fatos usando `CLIENTE.CODIGO`.
4. Medir cobertura de `IDPRODUTO` nas fatos usando `PRODUTO.ID`.
5. Testar se `TITRECEB.ORIGEM = 'NFSAID'` realmente fecha com `NFSAIDA.ID`.
6. Testar se `CAIXAVENDAMOV.IDNFSAIDA` e `CODCUPOMFISCAL` ajudam a reconciliar PDV com faturamento.
