let
    Fonte = fFrete_base,
    LinhasValidas = Table.SelectRows(Fonte, each [NUMERO_NF] <> null and Text.Trim([NUMERO_NF]) <> ""),
    Agrupado = Table.Group(
        LinhasValidas,
        {"NUMERO_NF"},
        {
            {"DATA_NF", each List.Min(List.RemoveNulls([DATA_NF])), type nullable date},
            {"TRANSPORTADORA", each List.First(List.RemoveNulls([TRANSPORTADORA])), type nullable text},
            {"DESTINO", each List.First(List.RemoveNulls([DESTINO])), type nullable text},
            {"VALOR_FRETE_CTE", each List.Sum(List.RemoveNulls([VALOR_FRETE_CTE])), type nullable number}
        }
    )
in
    Agrupado
