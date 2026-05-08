import argparse
import csv
from pathlib import Path
from typing import Optional

try:
    from conectar_firebird import connect
except SystemExit:
    raise


DEFAULT_TABLES = [
    "CLIENTE",
    "PRODUTO",
    "PRODUTOEMPRESA",
    "PRODUTO_PRECO",
    "PRODUTOGRADE",
    "PEDIDO",
    "PEDIDO_STATUS",
    "VENDAS",
    "CAIXAVENDA",
    "CAIXAVENDAITENS",
    "NFSAIDA",
    "NFSAIITE",
    "PRODUTOMOVIMENTACAO",
    "PRODUTOMOVIMENTOATUALMES",
    "TITRECEB",
    "TITRECEB_ORIGEM",
    "TITPAGAR",
    "COBTITULO",
    "COBTITULOMOV",
    "CONTARECDESP",
    "BANCO",
    "CAIXA",
    "FORNEC",
    "NFENTRAD",
    "NFENTITE",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exporta tabelas do Firebird para arquivos CSV separados."
    )
    parser.add_argument(
        "--tables",
        nargs="+",
        help="Lista de tabelas para exportar. Se omitido, usa a lista padrao.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parents[1] / "exports"),
        help="Diretorio de saida para os CSVs.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limita a quantidade de linhas exportadas por tabela.",
    )
    return parser.parse_args()


def sanitize_table_name(table_name: str) -> str:
    return table_name.strip().upper()


def build_query(table_name: str, limit: Optional[int]) -> str:
    if limit is None:
        return f"SELECT * FROM {table_name}"
    return f"SELECT FIRST {limit} * FROM {table_name}"


def export_table(cursor, table_name: str, output_dir: Path, limit: Optional[int]) -> None:
    query = build_query(table_name, limit)
    cursor.execute(query)
    columns = [column[0].strip() if column[0] else "" for column in cursor.description]
    output_path = output_dir / f"{table_name}.csv"

    with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(columns)
        row_count = 0
        for row in cursor:
            writer.writerow(list(row))
            row_count += 1

    print(f"{table_name}: {row_count} linhas exportadas para {output_path}")


def main() -> None:
    args = parse_args()
    tables = args.tables or DEFAULT_TABLES
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    normalized_tables = [sanitize_table_name(table_name) for table_name in tables]

    with connect() as conn:
        cursor = conn.cursor()
        for table_name in normalized_tables:
            try:
                export_table(cursor, table_name, output_dir, args.limit)
            except Exception as exc:
                print(f"{table_name}: erro na exportacao -> {exc}")


if __name__ == "__main__":
    main()
