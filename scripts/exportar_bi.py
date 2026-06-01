import argparse
import csv
from pathlib import Path
from typing import Dict, List, Optional

try:
    from conectar_firebird import connect
except SystemExit:
    raise


PROJECT_DIR = Path(__file__).resolve().parents[1]
QUERIES_DIR = PROJECT_DIR / "queries" / "bi"
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "exports"

QUERY_CONFIGS: List[Dict[str, Optional[str]]] = [
    {
        "name": "fVendas",
        "sql_file": "fVendas.sql",
        "order_by": "DATA_VENDA DESC, NOTA_FISCAL DESC, ITEM_VENDA DESC",
        "output_file": "fVendas.csv",
    },
    {
        "name": "fPedidos",
        "sql_file": "fPedidos.sql",
        "order_by": "DATA_PEDIDO DESC, CODIGO_PEDIDO DESC, ID_PEDITE DESC",
        "output_file": "fPedidos.csv",
    },
    {
        "name": "dClientes",
        "sql_file": "dClientes.sql",
        "order_by": "CODIGO_CLIENTE DESC",
        "output_file": "dClientes.csv",
    },
    {
        "name": "dProdutos",
        "sql_file": "dProdutos.sql",
        "order_by": "CODIGO_PRODUTO DESC",
        "output_file": "dProdutos.csv",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa queries de BI e exporta os resultados em CSV."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=1000,
        help="Quantidade maxima de registros por query. Padrao: 1000.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Diretorio de saida para os CSVs.",
    )
    parser.add_argument(
        "--queries",
        nargs="+",
        choices=[config["name"] for config in QUERY_CONFIGS],
        help="Lista opcional de queries para exportar.",
    )
    return parser.parse_args()


def load_sql(sql_path: Path) -> str:
    sql = sql_path.read_text(encoding="utf-8")
    return sql.strip().rstrip(";")


def build_limited_query(base_sql: str, limit: int, order_by: Optional[str]) -> str:
    wrapped_query = [
        "SELECT FIRST {limit} *".format(limit=limit),
        "FROM (",
        base_sql,
        ") q",
    ]

    if order_by:
        wrapped_query.append(f"ORDER BY {order_by}")

    return "\n".join(wrapped_query)


def export_query(cursor, query_sql: str, output_path: Path) -> int:
    cursor.execute(query_sql)
    columns = [column[0].strip() if column[0] else "" for column in cursor.description]

    with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(columns)

        row_count = 0
        for row in cursor:
            writer.writerow(list(row))
            row_count += 1

    return row_count


def filter_configs(selected_queries: Optional[List[str]]) -> List[Dict[str, Optional[str]]]:
    if not selected_queries:
        return QUERY_CONFIGS

    selected = {name.strip() for name in selected_queries}
    return [config for config in QUERY_CONFIGS if config["name"] in selected]


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    query_configs = filter_configs(args.queries)

    with connect() as conn:
        cursor = conn.cursor()

        for config in query_configs:
            sql_path = QUERIES_DIR / str(config["sql_file"])
            output_path = output_dir / str(config["output_file"])

            try:
                base_sql = load_sql(sql_path)
                query_sql = build_limited_query(
                    base_sql=base_sql,
                    limit=args.limit,
                    order_by=config.get("order_by"),
                )
                row_count = export_query(cursor, query_sql, output_path)
                print(
                    f"{config['name']}: {row_count} linhas exportadas para {output_path}"
                )
            except Exception as exc:
                print(f"{config['name']}: erro na exportacao -> {exc}")


if __name__ == "__main__":
    main()
