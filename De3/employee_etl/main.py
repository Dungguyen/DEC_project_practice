import logging
import os
from dotenv import load_dotenv
from src.json_extract import extract
from src.transformer import transform
from src import load
from src.load import insert_sample


load_dotenv()

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Cấu hình DB từ biến môi trường
DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     int(os.getenv("DB_PORT", "5432")),
    "dbname":   os.getenv("DB_NAME",     "employees_db"),
    "user":     os.getenv("DB_USER",     "postgres"),
    "password": os.getenv("DB_PASSWORD", "123"),
}

INPUT_FILE = os.getenv("INPUT_FILE", "data/employees.json")


def run_pipeline():
    logger.info("=" * 50)
    logger.info("BẮT ĐẦU ETL PIPELINE")
    logger.info("=" * 50)

    try:
        # 1. Extract
        logger.info("[1/3] EXTRACT")
        raw_data = extract(INPUT_FILE)

        # 2. Transform
        logger.info("[2/3] TRANSFORM")
        clean_data = transform(raw_data)

        # 3. Load
        logger.info("[3/3] LOAD")
        n = load(clean_data, DB_CONFIG)

        # 4. Insert sẵn 5 dòng mẫu (nếu chưa có)
        logger.info("[4/4] INSERT SAMPLE DATA")
        insert_sample(DB_CONFIG)

        logger.info("=" * 50)
        logger.info(f"ETL HOÀN TẤT – đã load {n} records")
        logger.info("=" * 50)

    except FileNotFoundError as e:
        logger.error(f"Không tìm thấy file: {e}")
        raise
    except ConnectionError as e:
        logger.error(f"Lỗi kết nối DB: {e}")
        raise
    except Exception as e:
        logger.error(f"Lỗi không xác định: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()