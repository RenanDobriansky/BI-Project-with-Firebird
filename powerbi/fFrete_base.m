let
    WorkbookPath = FreteWorkbookPath,
    SheetName = "CONHECIMENTOSILO",
    MinValidYear = 2016,
    MaxValidYear = 2026,

    NormalizeText = (value as any, optional forceUpper as nullable logical) as nullable text =>
        let
            rawText = try Text.Trim(Text.From(value)) otherwise null,
            cleanText =
                if rawText = null or rawText = "" then
                    null
                else if forceUpper = true then
                    Text.Upper(rawText)
                else
                    rawText
        in
            cleanText,

    IsDateInRange = (value as nullable date) as logical =>
        value <> null and Date.Year(value) >= MinValidYear and Date.Year(value) <= MaxValidYear,

    ParseDateValue = (value as any) as nullable date =>
        let
            parsed =
                if value = null then
                    null
                else if Value.Is(value, type date) then
                    value
                else if Value.Is(value, type datetime) then
                    Date.From(value)
                else
                    let
                        rawText = NormalizeText(value, false),
                        numericValue = try Number.From(value) otherwise null,
                        textNumber = if rawText <> null then try Number.FromText(rawText, "en-US") otherwise null else null,
                        fromNumber =
                            if numericValue <> null then
                                Date.AddDays(#date(1899, 12, 30), Number.RoundDown(numericValue))
                            else if textNumber <> null then
                                Date.AddDays(#date(1899, 12, 30), Number.RoundDown(textNumber))
                            else
                                null,
                        fromText =
                            if rawText <> null then
                                let
                                    ptDate = try Date.FromText(rawText, "pt-BR") otherwise null,
                                    enDate = if ptDate = null then try Date.FromText(rawText, "en-US") otherwise null else ptDate
                                in
                                    enDate
                            else
                                null
                    in
                        if fromText <> null then fromText else fromNumber,
            validDate = if IsDateInRange(parsed) then parsed else null
        in
            validDate,

    ExtractBetween = (value as any, startDelimiter as text, endDelimiter as text) as nullable text =>
        let
            txt = NormalizeText(value, true),
            extracted = if txt = null then null else try Text.BetweenDelimiters(txt, startDelimiter, endDelimiter, 0, 0) otherwise null,
            cleaned = NormalizeText(extracted, false)
        in
            cleaned,

    ExtractBefore = (value as any, delimiter as text) as nullable text =>
        let
            txt = NormalizeText(value, true),
            extracted = if txt = null then null else try Text.BeforeDelimiter(txt, delimiter, 0) otherwise null,
            cleaned = NormalizeText(extracted, false)
        in
            cleaned,

    ExtractAfter = (value as any, delimiter as text) as nullable text =>
        let
            txt = NormalizeText(value, true),
            extracted = if txt = null then null else try Text.AfterDelimiter(txt, delimiter, 0) otherwise null,
            cleaned = NormalizeText(extracted, false)
        in
            cleaned,

    GetDigitTokens = (value as any) as list =>
        let
            txt = NormalizeText(value, true),
            chars = if txt = null then {} else Text.ToList(txt),
            maskedChars = List.Transform(chars, each if _ >= "0" and _ <= "9" then _ else "|"),
            joined = Text.Combine(maskedChars, ""),
            tokens = List.Select(Text.Split(joined, "|"), each _ <> "")
        in
            tokens,

    GetTextBeforeDe = (value as any) as nullable text =>
        let
            txt = NormalizeText(value, true),
            semPrefixo = if txt <> null and Text.StartsWith(txt, "NF ") then Text.Range(txt, 3) else txt,
            beforeDe =
                if semPrefixo = null then
                    null
                else if Text.Contains(semPrefixo, " DE ") then
                    Text.BeforeDelimiter(semPrefixo, " DE ")
                else if Text.Contains(semPrefixo, "DE ") then
                    Text.BeforeDelimiter(semPrefixo, "DE ")
                else
                    semPrefixo
        in
            NormalizeText(beforeDe, true),

    ExtractDateAfterDe = (value as any) as nullable date =>
        let
            txt = NormalizeText(value, true),
            afterDe =
                if txt = null then
                    null
                else if Text.Contains(txt, " DE ") then
                    ExtractAfter(txt, " DE ")
                else if Text.Contains(txt, "DE ") then
                    ExtractAfter(txt, "DE ")
                else
                    null
        in
            ParseDateValue(afterDe),

    ExtractNumeroNF = (value as any) as nullable text =>
        let
            tokens = GetDigitTokens(GetTextBeforeDe(value))
        in
            if List.Count(tokens) = 0 then null else List.First(tokens),

    ExtractDataNF = (value as any) as nullable date => ExtractDateAfterDe(value),

    ExtractNumeroCTE = (value as any) as nullable text =>
        let
            tokens = GetDigitTokens(GetTextBeforeDe(value))
        in
            if List.Count(tokens) = 0 then null else List.First(tokens),

    ExtractDataCTE = (value as any) as nullable date => ExtractDateAfterDe(value),

    ToNumber = (value as any) as nullable number =>
        let
            parsed =
                if value = null then
                    null
                else if Value.Is(value, type number) then
                    value
                else
                    let
                        rawText = NormalizeText(value, false),
                        enNumber = if rawText <> null then try Number.FromText(rawText, "en-US") otherwise null else null,
                        ptNumber = if enNumber = null and rawText <> null then try Number.FromText(rawText, "pt-BR") otherwise null else enNumber
                    in
                        ptNumber
        in
            parsed,

    Source = Excel.Workbook(File.Contents(WorkbookPath), null, true),
    RawSheet = Source{[Item = SheetName, Kind = "Sheet"]}[Data],
    PromotedHeaders = Table.PromoteHeaders(RawSheet, [PromoteAllScalars = true]),
    ReplacedExcelErrors = Table.ReplaceErrorValues(
        PromotedHeaders,
        List.Transform(Table.ColumnNames(PromotedHeaders), each {_, null})
    ),
    RenamedColumns = Table.RenameColumns(
        ReplacedExcelErrors,
        {
            {"VALOR", "VALOR_FRETE_CTE"},
            {"Column3", "VALOR_FRETE_COTADO"},
            {"% DE FRETE", "PCT_FRETE_CTE"},
            {"Column8", "PCT_FRETE_COTADO"},
            {"N? NOTA ", "TEXTO_NOTA"},
            {"CONHECIMENTO DE TRANSPORTE", "TEXTO_CTE"},
            {"VALOR NF", "VALOR_NF"},
            {"COLETADO ", "COLETADO_RAW"},
            {"CHEGADA", "CHEGADA_RAW"},
            {"DATA VENCIMENTO", "DATA_VENCIMENTO_RAW"},
            {"N?COLETA", "NUMERO_COLETA"},
            {"SITUA??O", "SITUACAO"}
        },
        MissingField.Ignore
    ),
    NotaColumnFixed =
        if Table.HasColumns(RenamedColumns, "TEXTO_NOTA") then
            RenamedColumns
        else if Table.HasColumns(RenamedColumns, "N° NOTA ") then
            Table.RenameColumns(RenamedColumns, {{"N° NOTA ", "TEXTO_NOTA"}}, MissingField.Ignore)
        else if Table.HasColumns(RenamedColumns, "N° NOTA") then
            Table.RenameColumns(RenamedColumns, {{"N° NOTA", "TEXTO_NOTA"}}, MissingField.Ignore)
        else if Table.HasColumns(RenamedColumns, "Nº NOTA ") then
            Table.RenameColumns(RenamedColumns, {{"Nº NOTA ", "TEXTO_NOTA"}}, MissingField.Ignore)
        else if Table.HasColumns(RenamedColumns, "Nº NOTA") then
            Table.RenameColumns(RenamedColumns, {{"Nº NOTA", "TEXTO_NOTA"}}, MissingField.Ignore)
        else
            RenamedColumns,
    AddedRowId = Table.AddIndexColumn(NotaColumnFixed, "ID_LINHA_ORIGEM", 1, 1, Int64.Type),
    FilteredRows = Table.SelectRows(AddedRowId, each List.NonNullCount(List.RemoveMatchingItems(Record.FieldValues(_), {"", null})) > 0),
    CleanedTextColumns = Table.TransformColumns(
        FilteredRows,
        {
            {"TRANSPORTADORA", each NormalizeText(_, true), type nullable text},
            {"DESTINO", each NormalizeText(_, true), type nullable text},
            {"UNID", each NormalizeText(_, true), type nullable text},
            {"REGIONAL", each NormalizeText(_, true), type nullable text},
            {"SITUACAO", each NormalizeText(_, true), type nullable text},
            {"TEXTO_NOTA", each NormalizeText(_, true), type nullable text},
            {"TEXTO_CTE", each NormalizeText(_, true), type nullable text},
            {"NUMERO_COLETA", each NormalizeText(_, false), type nullable text},
            {"DIAS", each NormalizeText(_, false), type nullable text}
        },
        null,
        MissingField.Ignore
    ),
    TypedNumbers = Table.TransformColumns(
        CleanedTextColumns,
        {
            {"VALOR_FRETE_CTE", each ToNumber(_), type nullable number},
            {"VALOR_FRETE_COTADO", each ToNumber(_), type nullable number},
            {"VALOR_NF", each ToNumber(_), type nullable number},
            {"PCT_FRETE_CTE", each ToNumber(_), Percentage.Type},
            {"PCT_FRETE_COTADO", each ToNumber(_), Percentage.Type},
            {"VOLUME", each ToNumber(_), type nullable number},
            {"PESO", each ToNumber(_), type nullable number}
        },
        null,
        MissingField.Ignore
    ),
    AddedColetado = Table.AddColumn(TypedNumbers, "COLETADO", each ParseDateValue([COLETADO_RAW]), type nullable date),
    AddedChegada = Table.AddColumn(AddedColetado, "CHEGADA", each ParseDateValue([CHEGADA_RAW]), type nullable date),
    AddedVencimento = Table.AddColumn(AddedChegada, "DATA_VENCIMENTO", each ParseDateValue([DATA_VENCIMENTO_RAW]), type nullable date),
    AddedNumeroNF = Table.AddColumn(AddedVencimento, "NUMERO_NF", each ExtractNumeroNF([TEXTO_NOTA]), type nullable text),
    AddedDataNF = Table.AddColumn(AddedNumeroNF, "DATA_NF", each ExtractDataNF([TEXTO_NOTA]), type nullable date),
    AddedNumeroCTE = Table.AddColumn(AddedDataNF, "NUMERO_CTE", each ExtractNumeroCTE([TEXTO_CTE]), type nullable text),
    AddedDataCTE = Table.AddColumn(AddedNumeroCTE, "DATA_CTE", each ExtractDataCTE([TEXTO_CTE]), type nullable date),
    AddedFlagNFInvalida = Table.AddColumn(AddedDataCTE, "FLAG_NF_INVALIDA", each [NUMERO_NF] = null or [DATA_NF] = null, type logical),
    AddedFlagCTEInvalido = Table.AddColumn(AddedFlagNFInvalida, "FLAG_CTE_INVALIDO", each [NUMERO_CTE] = null or [DATA_CTE] = null, type logical),
    AddedFlagDataColetaInvalida = Table.AddColumn(AddedFlagCTEInvalido, "FLAG_DATA_COLETA_INVALIDA", each [COLETADO] = null and NormalizeText([COLETADO_RAW], false) <> null, type logical),
    AddedFlagDataChegadaInvalida = Table.AddColumn(AddedFlagDataColetaInvalida, "FLAG_DATA_CHEGADA_INVALIDA", each [CHEGADA] = null and NormalizeText([CHEGADA_RAW], false) <> null, type logical),
    AddedFlagDataVencimentoInvalida = Table.AddColumn(AddedFlagDataChegadaInvalida, "FLAG_DATA_VENCIMENTO_INVALIDA", each [DATA_VENCIMENTO] = null and NormalizeText([DATA_VENCIMENTO_RAW], false) <> null, type logical)
in
    AddedFlagDataVencimentoInvalida


