let
    Fonte = fFrete_base,
    LinhasValidas = Table.SelectRows(Fonte, each [NUMERO_NF] <> null and Text.Trim([NUMERO_NF]) <> ""),
    Agrupado = Table.Group(
        LinhasValidas,
        {"NUMERO_NF"},
        {
            {"DATA_NF", each List.Min(List.RemoveNulls([DATA_NF])), type nullable date},
            {
                "NUMERO_CTE_PRINCIPAL",
                each
                    let
                        ctes = List.Sort(List.Distinct(List.RemoveNulls([NUMERO_CTE])))
                    in
                        if List.Count(ctes) = 0 then null else Text.From(List.First(ctes)),
                type nullable text
            },
            {
                "NUMERO_CTE",
                each
                    let
                        ctes = List.Sort(List.Distinct(List.RemoveNulls([NUMERO_CTE])))
                    in
                        if List.Count(ctes) = 0 then null else Text.Combine(List.Transform(ctes, each Text.From(_)), " | "),
                type nullable text
            },
            {"TRANSPORTADORA", each try List.First(List.RemoveNulls([TRANSPORTADORA])) otherwise null, type nullable text},
            {"DESTINO", each try List.First(List.RemoveNulls([DESTINO])) otherwise null, type nullable text},
            {"UNID", each try List.First(List.RemoveNulls([UNID])) otherwise null, type nullable text},
            {"REGIONAL", each try List.First(List.RemoveNulls([REGIONAL])) otherwise null, type nullable text},
            {"SITUACAO", each try List.First(List.RemoveNulls([SITUACAO])) otherwise null, type nullable text},
            {"VALOR_FRETE_CTE", each List.Sum(List.RemoveNulls([VALOR_FRETE_CTE])), type nullable number},
            {"VALOR_FRETE_COTADO", each List.Sum(List.RemoveNulls([VALOR_FRETE_COTADO])), type nullable number},
            {"VALOR_NF", each List.Max(List.RemoveNulls([VALOR_NF])), type nullable number},
            {"VOLUME", each List.Sum(List.RemoveNulls([VOLUME])), type nullable number},
            {"PESO", each List.Sum(List.RemoveNulls([PESO])), type nullable number},
            {"DATA_COLETA_MIN", each List.Min(List.RemoveNulls([COLETADO])), type nullable date},
            {"DATA_CHEGADA_MAX", each List.Max(List.RemoveNulls([CHEGADA])), type nullable date},
            {"DATA_VENCIMENTO_MAX", each List.Max(List.RemoveNulls([DATA_VENCIMENTO])), type nullable date},
            {"QTD_CONHECIMENTOS", each List.Count(List.Distinct(List.RemoveNulls([NUMERO_CTE]))), Int64.Type},
            {"QTD_LINHAS_ORIGEM", each Table.RowCount(_), Int64.Type},
            {"FLAG_DIVERGENCIA_TRANSPORTADORA", each List.Count(List.Distinct(List.RemoveNulls([TRANSPORTADORA]))) > 1, type logical},
            {"FLAG_DIVERGENCIA_DESTINO", each List.Count(List.Distinct(List.RemoveNulls([DESTINO]))) > 1, type logical},
            {"FLAG_DIVERGENCIA_REGIONAL", each List.Count(List.Distinct(List.RemoveNulls([REGIONAL]))) > 1, type logical},
            {"FLAG_NF_INVALIDA", each List.AnyTrue(List.Transform(List.RemoveNulls([FLAG_NF_INVALIDA]), each _ = true)), type logical},
            {"FLAG_CTE_INVALIDO", each List.AnyTrue(List.Transform(List.RemoveNulls([FLAG_CTE_INVALIDO]), each _ = true)), type logical},
            {"FLAG_DATA_COLETA_INVALIDA", each List.AnyTrue(List.Transform(List.RemoveNulls([FLAG_DATA_COLETA_INVALIDA]), each _ = true)), type logical},
            {"FLAG_DATA_CHEGADA_INVALIDA", each List.AnyTrue(List.Transform(List.RemoveNulls([FLAG_DATA_CHEGADA_INVALIDA]), each _ = true)), type logical},
            {"FLAG_DATA_VENCIMENTO_INVALIDA", each List.AnyTrue(List.Transform(List.RemoveNulls([FLAG_DATA_VENCIMENTO_INVALIDA]), each _ = true)), type logical}
        }
    ),
    AddedFlagMultiplosCtes = Table.AddColumn(Agrupado, "FLAG_MULTIPLOS_CTES", each [QTD_CONHECIMENTOS] > 1, type logical),
    AddedPctFreteCte = Table.AddColumn(AddedFlagMultiplosCtes, "PCT_FRETE_CTE", each if [VALOR_NF] = null or [VALOR_NF] = 0 then null else [VALOR_FRETE_CTE] / [VALOR_NF], Percentage.Type),
    AddedPctFreteCotado = Table.AddColumn(AddedPctFreteCte, "PCT_FRETE_COTADO", each if [VALOR_NF] = null or [VALOR_NF] = 0 then null else [VALOR_FRETE_COTADO] / [VALOR_NF], Percentage.Type),
    AddedFlagQualidade = Table.AddColumn(AddedPctFreteCotado, "FLAG_EXCECAO_QUALIDADE", each [FLAG_MULTIPLOS_CTES] or [FLAG_DIVERGENCIA_TRANSPORTADORA] or [FLAG_DIVERGENCIA_DESTINO] or [FLAG_DIVERGENCIA_REGIONAL] or [FLAG_NF_INVALIDA] or [FLAG_CTE_INVALIDO] or [FLAG_DATA_COLETA_INVALIDA] or [FLAG_DATA_CHEGADA_INVALIDA] or [FLAG_DATA_VENCIMENTO_INVALIDA], type logical)
in
    AddedFlagQualidade


