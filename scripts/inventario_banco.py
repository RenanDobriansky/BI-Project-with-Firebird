import argparse
import csv
from pathlib import Path
from typing import Iterable, List, Sequence, Set

from conectar_firebird import connect


RELEVANT_TABLES = [
    "CLIENTE",
    "PRODUTO",
    "PRODUTOEMPRESA",
    "PEDIDO",
    "VENDAS",
    "CAIXAVENDA",
    "CAIXAVENDAITENS",
    "NFSAIDA",
    "NFSAIITE",
    "PRODUTOMOVIMENTACAO",
    "TITRECEB",
    "TITPAGAR",
    "FORNEC",
    "NFENTRAD",
    "NFENTITE",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera inventario estrutural do banco Firebird em CSV."
    )
    parser.add_argument(
        "--resume-counts",
        action="store_true",
        help="Continua a contagem de linhas a partir de um contagem_linhas.csv ja existente.",
    )
    parser.add_argument(
        "--skip-counts",
        action="store_true",
        help="Gera tabelas, colunas e previews sem executar COUNT(*) nas tabelas.",
    )
    return parser.parse_args()


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def exports_dir() -> Path:
    path = project_root() / "exports"
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_csv(path: Path, rows: Sequence[Sequence[object]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerows(rows)


def append_csv_row(path: Path, row: Sequence[object]) -> None:
    with path.open("a", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(row)


def list_tables(cursor) -> List[List[object]]:
    query = """
    SELECT
        TRIM(r.RDB$RELATION_NAME) AS TABELA
    FROM RDB$RELATIONS r
    WHERE COALESCE(r.RDB$SYSTEM_FLAG, 0) = 0
      AND r.RDB$VIEW_BLR IS NULL
      AND r.RDB$RELATION_NAME NOT STARTING WITH 'RDB$'
      AND r.RDB$RELATION_NAME NOT STARTING WITH 'MON$'
      AND r.RDB$RELATION_NAME NOT STARTING WITH 'SEC$'
    ORDER BY TRIM(r.RDB$RELATION_NAME)
    """
    rows = cursor.execute(query).fetchall()
    return [["tabela"]] + [[row[0].strip()] for row in rows]


def list_columns(cursor) -> List[List[object]]:
    query = """
    SELECT
        TRIM(rf.RDB$RELATION_NAME) AS TABELA,
        TRIM(rf.RDB$FIELD_NAME) AS COLUNA,
        CASE f.RDB$FIELD_TYPE
            WHEN 7 THEN 'SMALLINT'
            WHEN 8 THEN 'INTEGER'
            WHEN 10 THEN 'FLOAT'
            WHEN 12 THEN 'DATE'
            WHEN 13 THEN 'TIME'
            WHEN 14 THEN 'CHAR'
            WHEN 16 THEN
                CASE
                    WHEN f.RDB$FIELD_SUB_TYPE = 1 THEN 'NUMERIC'
                    WHEN f.RDB$FIELD_SUB_TYPE = 2 THEN 'DECIMAL'
                    ELSE 'BIGINT'
                END
            WHEN 23 THEN 'BOOLEAN'
            WHEN 27 THEN 'DOUBLE'
            WHEN 35 THEN 'TIMESTAMP'
            WHEN 37 THEN 'VARCHAR'
            WHEN 261 THEN 'BLOB'
            ELSE 'TIPO_' || f.RDB$FIELD_TYPE
        END AS TIPO_DADO,
        COALESCE(f.RDB$CHARACTER_LENGTH, f.RDB$FIELD_LENGTH) AS TAMANHO,
        CASE rf.RDB$NULL_FLAG
            WHEN 1 THEN 'NAO'
            ELSE 'SIM'
        END AS ACEITA_NULO
    FROM RDB$RELATION_FIELDS rf
    JOIN RDB$FIELDS f
      ON f.RDB$FIELD_NAME = rf.RDB$FIELD_SOURCE
    JOIN RDB$RELATIONS r
      ON r.RDB$RELATION_NAME = rf.RDB$RELATION_NAME
    WHERE COALESCE(r.RDB$SYSTEM_FLAG, 0) = 0
      AND r.RDB$VIEW_BLR IS NULL
      AND r.RDB$RELATION_NAME NOT STARTING WITH 'RDB$'
      AND r.RDB$RELATION_NAME NOT STARTING WITH 'MON$'
      AND r.RDB$RELATION_NAME NOT STARTING WITH 'SEC$'
    ORDER BY
        TRIM(rf.RDB$RELATION_NAME),
        rf.RDB$FIELD_POSITION
    """
    rows = cursor.execute(query).fetchall()
    data = [["tabela", "coluna", "tipo_dado", "tamanho", "aceita_nulo"]]
    for row in rows:
        data.append(
            [
                row[0].strip(),
                row[1].strip(),
                row[2],
                row[3],
                row[4],
            ]
        )
    return data


def fetch_table_names(cursor) -> List[str]:
    rows = list_tables(cursor)[1:]
    return [row[0] for row in rows]


def export_preview(cursor, table_name: str, output_directory: Path) -> None:
    query = f"SELECT FIRST 10 * FROM {table_name}"
    cursor.execute(query)
    columns = [column[0].strip() if column[0] else "" for column in cursor.description]
    rows = [columns]
    for row in cursor.fetchall():
        rows.append(list(row))
    output_path = output_directory / f"preview_{table_name}.csv"
    write_csv(output_path, rows)
    print(f"{table_name}: preview salvo em {output_path}")


def export_relevant_previews(cursor, output_directory: Path) -> None:
    for table_name in RELEVANT_TABLES:
        try:
            export_preview(cursor, table_name, output_directory)
        except Exception as exc:
            print(f"{table_name}: erro ao gerar preview -> {exc}")


def read_counted_tables(path: Path) -> Set[str]:
    if not path.exists():
        return set()

    counted_tables: Set[str] = set()
    with path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        next(reader, None)
        for row in reader:
            if row and row[0].strip():
                counted_tables.add(row[0].strip().upper())
    return counted_tables


def count_rows_incrementally(
    cursor,
    table_names: Iterable[str],
    output_path: Path,
    resume: bool,
) -> None:
    counted_tables = read_counted_tables(output_path) if resume else set()

    if not resume or not output_path.exists():
        write_csv(
            output_path,
            [["tabela", "contagem_linhas_aproximada", "metodo"]],
        )

    for table_name in table_names:
        if table_name.upper() in counted_tables:
            print(f"{table_name}: contagem ja existente, pulando")
            continue

        query = f"SELECT COUNT(*) FROM {table_name}"
        try:
            count_value = cursor.execute(query).fetchone()[0]
            append_csv_row(output_path, [table_name, count_value, "COUNT(*)"])
            print(f"{table_name}: {count_value} linhas")
        except Exception as exc:
            append_csv_row(output_path, [table_name, "", f"ERRO: {exc}"])
            print(f"{table_name}: erro ao contar -> {exc}")


def main() -> None:
    args = parse_args()
    output_directory = exports_dir()

    with connect() as conn:
        cursor = conn.cursor()

        table_names = fetch_table_names(cursor)
        write_csv(output_directory / "tabelas.csv", list_tables(cursor))
        write_csv(output_directory / "colunas.csv", list_columns(cursor))
        export_relevant_previews(cursor, output_directory)

        if not args.skip_counts:
            count_rows_incrementally(
                cursor,
                table_names,
                output_directory / "contagem_linhas.csv",
                resume=args.resume_counts,
            )

    print("Inventario do banco gerado com sucesso.")


if __name__ == "__main__":
    main()
