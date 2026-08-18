import logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS employees (
        id          INTEGER     PRIMARY KEY,
        name        TEXT        NOT NULL,
        department  TEXT        NOT NULL,
        salary      INTEGER     NOT NULL,
        join_date   DATE        NOT NULL
    );
"""

INSERT_SQL = """
    INSERT INTO employees (id, name, department, salary, join_date)
    VALUES %s
    ON CONFLICT (id) DO UPDATE SET
        name       = EXCLUDED.name,
        department = EXCLUDED.department,
        salary     = EXCLUDED.salary,
        join_date  = EXCLUDED.join_date;
"""


def get_connection(db_config: dict):
    """Tạo kết nối đến PostgreSQL."""
    try:
        conn = psycopg2.connect(**db_config)
        logger.info("Kết nối PostgreSQL thành công")
        return conn
    except psycopg2.OperationalError as e:
        raise ConnectionError(f"Không thể kết nối PostgreSQL: {e}")


def create_table(conn) -> None:
    """Tạo bảng employees nếu chưa tồn tại."""
    with conn.cursor() as cur:
        cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    logger.info("Tạo bảng employees thành công (hoặc đã tồn tại)")


SAMPLE_DATA = [
    (1, "John Doe",     "Marketing", 50000, "2022-01-01"),
    (2, "Jane Smith",   "Sales",     60000, "2021-05-15"),
    (3, "Mark Johnson", "Finance",   75000, "2023-02-28"),
    (4, "Emily Davis",  "HR",        55000, "2020-11-10"),
    (5, "Chris Wilson", "IT",        80000, "2019-07-22"),
]


def insert_sample(db_config: dict) -> None:
    """Insert sẵn 5 dòng mẫu vào bảng employees."""
    conn = get_connection(db_config)
    try:
        create_table(conn)
        with conn.cursor() as cur:
            execute_values(
                cur,
                """
                INSERT INTO employees (id, name, department, salary, join_date)
                VALUES %s
                ON CONFLICT (id) DO NOTHING
                """,
                SAMPLE_DATA,
            )
        conn.commit()
        logger.info(f"Insert sẵn {len(SAMPLE_DATA)} dòng mẫu thành công")
    except Exception as e:
        conn.rollback()
        logger.error(f"Lỗi insert sample: {e}")
        raise
    finally:
        conn.close()


def load(records: list[dict], db_config: dict) -> int:
    """
    Insert danh sách records vào bảng employees.

    Args:
        records:   list records đã transform
        db_config: dict chứa thông tin kết nối DB

    Returns:
        int: số record đã insert/update
    """
    if not records:
        logger.warning("Không có record nào để load")
        return 0

    conn = get_connection(db_config)

    try:
        create_table(conn)

        # Chuyển list[dict] thành list[tuple] để insert
        rows = [
            (
                r["id"],
                r["name"],
                r["department"],
                r["salary"],
                r["join_date"],
            )
            for r in records
        ]

        with conn.cursor() as cur:
            execute_values(cur, INSERT_SQL, rows)

        conn.commit()
        logger.info(f"Load thành công {len(rows)} records vào bảng employees")
        return len(rows)

    except Exception as e:
        conn.rollback()
        logger.error(f"Lỗi khi load dữ liệu: {e}")
        raise

    finally:
        conn.close()