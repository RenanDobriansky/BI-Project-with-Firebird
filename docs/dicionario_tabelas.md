# Dicionario de Tabelas para BI Comercial

Este dicionario foi atualizado com base no inventario gerado do banco:

- `exports/tabelas.csv`
- `exports/colunas.csv`
- `exports/contagem_linhas.csv`
- previews das tabelas mais relevantes em `exports/preview_*.csv`

O foco aqui e identificar quais tabelas devem entrar primeiro na exploracao para um dashboard comercial no Power BI.

## Resumo Executivo

As tabelas mais promissoras para vendas realizadas sao:

- `NFSAIDA`: cabecalho fiscal da venda faturada
- `NFSAIITE`: item da nota fiscal de saida
- `CLIENTE`: dimensao de cliente
- `PRODUTO`: dimensao de produto
- `TITRECEB`: financeiro originado da venda

As tabelas mais promissoras para carteira, pedidos e acompanhamento comercial sao:

- `PEDIDO`: cabecalho do pedido
- `PEDITE`: item do pedido
- `PEDIDO_STATUS`: status do pedido

As tabelas mais promissoras para PDV e balcao sao:

- `CAIXAVENDAMOV`: movimento de venda do caixa
- `CAIXAVENDAITENS`: itens vendidos no caixa
- `CAIXAVENDARECEB`: detalhamento do recebimento

Observacoes importantes do inventario:

- `VENDAS` tem `0` linhas e nao deve ser prioridade no primeiro ciclo.
- `CAIXAVENDA` parece representar abertura e fechamento de caixa, nao a venda em si.
- `PRODUTOMOVIMENTACAO` e muito volumosa e parece mais adequada para estoque do que para comercial.

## Classificacao por Assunto Provavel

## Vendas

- `NFSAIDA`: cabecalho fiscal da venda faturada
- `PEDIDO`: cabecalho comercial do pedido
- `CAIXAVENDAMOV`: movimento de venda no PDV
- `CUPOMFISCAL`: cabecalho de cupom fiscal
- `FATURA`: faturamento ou consolidacao de venda
- `FATURA_NF`: relacao entre faturamento e nota
- `LIBERACAOVENDA`: etapa operacional da venda
- `TIPOVENDANFE`: tipo de venda vinculado a NFe
- `PEDIDO_STATUS`: situacao do pedido
- `PREVISAOFATURAMENTO`: previsao comercial

## Itens de Venda

- `NFSAIITE`: item da nota fiscal de saida
- `PEDITE`: item do pedido
- `CAIXAVENDAITENS`: item vendido no PDV
- `CUPOMITEM`: item do cupom fiscal
- `PEDITECOMPL`: complemento do item do pedido
- `PEDITELOTE`: lote do item do pedido
- `NFSAIITECOMPL`: complemento do item de nota
- `NFSAIITELOTE`: lote do item de nota
- `CAIXAVENDAITENSCOMPL`: complemento do item do caixa
- `CAIXAVENDAITENSLOTE`: lote do item do caixa

## Clientes

- `CLIENTE`: cadastro principal
- `CONTATO`: contatos complementares
- `CLIENTE_TRIBUTO`: dados fiscais
- `CLIENTE_ORIGEM`: origem do cliente
- `CLIENTE_PONTUACAO`: programa de relacionamento
- `CLIENTEDEBITO`: saldo ou situacao financeira
- `VENDEDOR_CLIENTE`: relacionamento vendedor x cliente
- `CLIENTE_FIEL`: fidelidade
- `WEBCLIENTE`: integracao digital
- `MERCOS_CLIENTES`: integracao externa

## Produtos

- `PRODUTO`: cadastro principal
- `PRODUTOEMPRESA`: produto por empresa ou filial
- `PRODUTO_PRECO`: preco
- `PRODUTOGRADE`: grade ou variacao
- `PRODUTOGRADEPRECO`: preco por grade
- `PRODUTOCODIGOBARRAS`: codigos auxiliares
- `PRODUTOLOCAL`: local de estoque
- `PRODUTOLOCALIZACAO`: localizacao fisica
- `PRODUTOMODELO`: classificacao complementar
- `PRODUTO_HIERARQUIA`: hierarquia de produto
- `PRODUTOCLIENTE`: relacionamento produto x cliente
- `KIT_PRODUTO`: kits

## Estoque

- `PRODUTOMOVIMENTACAO`: movimentacao de estoque
- `PRODUTOMOVIMENTOATUALMES`: acumulado ou snapshot mensal
- `PRODUTOMOVIMENTACAOATUAL`: posicao atual
- `PRODUTOEMPRESA`: possivel saldo por empresa
- `PRODUTOINVENTARIO`: inventario
- `PRODUTOINVENTARIORATEIO`: rateio de inventario
- `PRODUTOLOTE`: controle por lote
- `PRODUTOLOTECONF`: configuracao de lote
- `LFSALDO`: saldo
- `ESTOQUEREGULADOR`: regulador de estoque
- `VARIAVELESTOQUE`: parametrizacao

## Financeiro

- `TITRECEB`: contas a receber
- `TITRECEB_ORIGEM`: origem do recebivel
- `TITPAGAR`: contas a pagar
- `COBTITULO`: titulo de cobranca
- `COBTITULOMOV`: movimento do titulo
- `CAIXAVENDARECEB`: recebimentos de venda no caixa
- `BANCO`: cadastro bancario
- `CAIXA`: cadastro de caixa
- `CONTARECDESP`: natureza ou conta financeira
- `TITULOMOVIMENTACAO`: movimentos de titulos
- `TITULOSITUACAO`: status financeiro
- `CONCILIACAOBANCO`: conciliacao

## Compras

- `NFENTRAD`: cabecalho de nota de entrada
- `NFENTITE`: item da nota de entrada
- `COTACAO`: cabecalho de cotacao
- `COTACAOITENS`: itens da cotacao
- `ORCCOMPRA`: cabecalho de orcamento de compra
- `ORCCOMPRAITENS`: itens do orcamento de compra
- `SOLICITCOMPRA`: solicitacao de compra
- `SOLICITCOMPRAITE`: item da solicitacao
- `NFENTPRAZO`: prazos da entrada
- `NFENTRADREFERENCIA`: referencias da entrada

## Fornecedores

- `FORNEC`: cadastro principal
- `FORNECGRUPO`: agrupamento de fornecedor
- `FORNECMARCA`: marcas do fornecedor
- `FORNEC_TRIBUTO`: dados fiscais
- `FORNECEMAIL`: contatos
- `FORNEC_FORMAPG2`: forma de pagamento
- `FORNEC_COTACAO`: relacionamento com cotacoes
- `FORNEC_CONTRATO`: contratos

## Tabelas Tecnicas

- `CONFIG`, `CONFIGCUSTO`, `CONFIGFIS`, `CONFIGURACOES`: configuracao
- `LOG`, `LOG_SISTEMA`, `PRODUTO_LOG`: logs
- `PROXIMOGENERATOR`: controle tecnico
- `CONTROLE_SINCRONIZACAO`: integracao
- `LOJA_INTEGRADA_PEDIDO_TEMP`: staging temporario
- `GSP_NUVEM_TITULO`, `NUVEM_TITULO`: integracoes
- `TMP_TITULO`, `TMPFATURA`: temporarias

## Prioridade para Dashboard Comercial

Ordem recomendada para investigacao no Power BI:

1. `NFSAIITE` - melhor candidata para fato de vendas realizadas no grao item; volume `237386`.
2. `NFSAIDA` - cabecalho da venda faturada; conecta cliente, vendedor, datas, totais e situacao; volume `32088`.
3. `CLIENTE` - dimensao de cliente; volume `1355`.
4. `PRODUTO` - dimensao de produto; volume `5422`.
5. `TITRECEB` - essencial para indicadores de recebimento, prazo e inadimplencia; volume `29081`.
6. `PEDITE` - importante para carteira comercial e itens de pedido; volume `103653`.
7. `PEDIDO` - cabecalho do pedido; permite acompanhar orcamento, pedido, previsao e situacao; volume `11880`.
8. `CAIXAVENDAMOV` - melhor candidata para cabecalho de venda no canal PDV; volume `9587`.
9. `CAIXAVENDAITENS` - itens do PDV; volume `16688`.
10. `CAIXAVENDARECEB` - forma de recebimento do PDV; volume `10747`.
11. `PRODUTOEMPRESA` - complemento importante para sortimento, empresa e possiveis status por filial; volume `5422`.
12. `PEDIDO_STATUS` - apoio para leitura operacional do pedido.
13. `CUPOMITEM` - alternativa ou complemento ao PDV fiscal; volume `10388`.
14. `CUPOMFISCAL` - cabecalho do cupom; volume `3796`.
15. `VENDAS` - baixa prioridade no primeiro ciclo, porque no inventario aparece com `0` linhas.

## Interpretacao Recomendada

Para um dashboard comercial, a prioridade deve ser:

- `venda realizada`: `NFSAIDA` + `NFSAIITE`
- `carteira e pedido`: `PEDIDO` + `PEDITE`
- `pdv e balcao`: `CAIXAVENDAMOV` + `CAIXAVENDAITENS` + `CAIXAVENDARECEB`
- `cliente`: `CLIENTE`
- `produto`: `PRODUTO` + `PRODUTOEMPRESA`
- `financeiro da venda`: `TITRECEB`

## Proposta Inicial de Modelo Estrela Comercial

### Fato principal

- `fVendas`: comecar por `NFSAIITE`

### Chaves e tabelas de apoio

- `NFSAIITE.IDNFSAIDA` -> `NFSAIDA.ID`
- `NFSAIITE.IDPRODUTO` -> `PRODUTO.ID`
- `NFSAIDA.CLIENTE` -> `CLIENTE.CODIGO`
- `NFSAIDA.IDVENDEDOR` -> tabela de vendedor, se existir e for relevante

### Fatos complementares

- `fPedidos`: `PEDITE` + `PEDIDO`
- `fRecebimentos`: `TITRECEB`
- `fPdv`: `CAIXAVENDAITENS` + `CAIXAVENDAMOV` + `CAIXAVENDARECEB`

## Alertas Antes de Modelar

- `CAIXAVENDA` nao parece ser venda; o preview indica abertura e fechamento de caixa.
- `VENDAS` nao deve ser usada sem verificacao adicional, porque esta vazia.
- `PEDIDO` parece guardar cabecalho comercial e traz campos como `STATUS`, `SITUACAO`, `VALORBRUTO` e `VALORLIQUIDO`, mas a granularidade de item esta em `PEDITE`.
- `NFSAIDA` e `NFSAIITE` parecem mais confiaveis para analise de faturamento realizado.
- `TITRECEB` indica origem `NFSAID` em pelo menos parte dos registros, o que e muito bom para reconciliar comercial e financeiro.

## Proximo Passo Recomendado

Se a meta for acelerar a montagem do dashboard comercial, o proximo passo deve ser exportar e mapear estas tabelas em conjunto:

1. `NFSAIDA`
2. `NFSAIITE`
3. `CLIENTE`
4. `PRODUTO`
5. `TITRECEB`
6. `PEDIDO`
7. `PEDITE`
8. `CAIXAVENDAMOV`
9. `CAIXAVENDAITENS`
10. `CAIXAVENDARECEB`

Depois disso, vale desenhar:

- relacionamentos
- definicao do grao de cada fato
- calendario
- medidas DAX comerciais
