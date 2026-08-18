import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def extract(file_path: str) -> list[dict]:

    path = Path(file_path)
 
    if not path.exists():
        raise FileNotFoundError(f"File không tồn tại: {file_path}")
 
    if path.suffix.lower() != ".json":
        raise ValueError(f"File phải có định dạng .json, nhận được: {path.suffix}")
 
    logger.info(f"Đang đọc file: {file_path}")
 
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"File JSON không hợp lệ: {e}")
 
    if not isinstance(data, list):
        raise ValueError("Dữ liệu JSON phải là một list")
 
    logger.info(f"Đọc thành công {len(data)} records")
    return data

