import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple

try:
    import pyodbc
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Dependencia ausente: pyodbc.\n"
        "Instale com o mesmo Python usado para executar o script:\n"
        f'"{sys.executable}" -m pip install pyodbc'
    ) from exc


REQUIRED_ENV_VARS = [
    "FIREBIRD_HOST",
    "FIREBIRD_PORT",
    "FIREBIRD_DATABASE",
    "FIREBIRD_USER",
    "FIREBIRD_PASSWORD",
]


def load_env_file() -> None:
    script_dir = Path(__file__).resolve().parent
    project_dir = script_dir.parent
    candidates = [
        project_dir / ".env",
        project_dir / ".env.local",
        script_dir / ".env",
        script_dir / ".env.local",
    ]

    for env_path in candidates:
        if not env_path.exists():
            continue

        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key and key not in os.environ:
                os.environ[key] = value
        return


def get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None or not str(value).strip():
        raise RuntimeError(
            f"Variavel de ambiente obrigatoria ausente: {name}"
        )
    return str(value).strip()


def validate_env() -> dict:
    load_env_file()
    config = {name: get_env(name) for name in REQUIRED_ENV_VARS}
    config["FIREBIRD_CHARSET"] = os.getenv("FIREBIRD_CHARSET", "UTF8").strip()
    config["FIREBIRD_DATABASE"] = normalize_database_path(config["FIREBIRD_DATABASE"])
    return config


def normalize_database_path(database: str) -> str:
    value = database.strip()

    # Permite usar tanto o caminho puro quanto formatos como "servidor:C:\pasta\banco.fdb"
    if ":" in value and not is_windows_drive_path(value):
        _, remainder = value.split(":", 1)
        cleaned = remainder.strip()
        if cleaned:
            return cleaned

    return value


def is_windows_drive_path(value: str) -> bool:
    return len(value) >= 3 and value[1] == ":" and value[2] in ("\\", "/")


def find_firebird_driver() -> str:
    installed = pyodbc.drivers()
    candidates = [
        driver
        for driver in installed
        if "firebird" in driver.lower() or "interbase" in driver.lower()
    ]
    if not candidates:
        raise RuntimeError(
            "Nenhum driver ODBC do Firebird foi encontrado. "
            "Instale o driver e confirme se ele aparece em pyodbc.drivers()."
        )
    return candidates[0]


def build_connection_variants(driver: str, config: dict) -> List[str]:
    host = config["FIREBIRD_HOST"]
    port = config["FIREBIRD_PORT"]
    database = config["FIREBIRD_DATABASE"]
    user = config["FIREBIRD_USER"]
    password = config["FIREBIRD_PASSWORD"]
    charset = config["FIREBIRD_CHARSET"]
    dbname_remote = f"{host}/{port}:{database}"

    return [
        (
            f"DRIVER={{{driver}}};"
            f"DBNAME={dbname_remote};"
            f"UID={user};PWD={password};"
            f"CHARSET={charset};"
        ),
        (
            f"DRIVER={{{driver}}};"
            f"DATABASE={dbname_remote};"
            f"UID={user};PWD={password};"
            f"CHARSET={charset};"
        ),
        (
            f"DRIVER={{{driver}}};"
            f"DBNAME={database};"
            f"CLIENT=localhost;"
            f"UID={user};PWD={password};"
            f"CHARSET={charset};"
        ),
        (
            f"DRIVER={{{driver}}};"
            f"SERVER={host};PORT={port};DATABASE={database};"
            f"UID={user};PWD={password};"
            f"CHARSET={charset};"
        ),
    ]


def connect() -> pyodbc.Connection:
    config = validate_env()
    driver = find_firebird_driver()
    attempts: List[Tuple[str, str]] = []

    for conn_str in build_connection_variants(driver, config):
        try:
            return pyodbc.connect(conn_str, timeout=10)
        except pyodbc.Error as exc:
            attempts.append((conn_str, str(exc)))

    attempt_messages = "\n".join(
        f"- {conn_str}\n  erro: {error}"
        for conn_str, error in attempts
    )
    raise RuntimeError(
        "Falha ao conectar no Firebird via ODBC. Tentativas executadas:\n"
        f"{attempt_messages}"
    )


def test_connection() -> None:
    with connect() as conn:
        cursor = conn.cursor()
        row = cursor.execute("SELECT CURRENT_TIMESTAMP FROM RDB$DATABASE").fetchone()
        print("Conexao OK")
        print(f"Timestamp do banco: {row[0]}")


if __name__ == "__main__":
    test_connection()
