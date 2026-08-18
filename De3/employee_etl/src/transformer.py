

import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = {"id", "name", "department", "salary", "join_date"}


def validate_record(record: dict, index: int) -> list[str]:
    """Kiểm tra record có đầy đủ và hợp lệ không. Trả về list lỗi."""
    errors = []

    # Kiểm tra trường bắt buộc
    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        errors.append(f"Thiếu trường: {missing}")
        return errors  # không kiểm tra tiếp nếu thiếu trường

    # Validate id
    if not isinstance(record["id"], int) or record["id"] <= 0:
        errors.append(f"id phải là số nguyên dương, nhận được: {record['id']}")

    # Validate name
    if not isinstance(record["name"], str) or not record["name"].strip():
        errors.append("name không được rỗng")

    # Validate department
    if not isinstance(record["department"], str) or not record["department"].strip():
        errors.append("department không được rỗng")

    # Validate salary
    if not isinstance(record["salary"], (int, float)) or record["salary"] < 0:
        errors.append(f"salary phải là số không âm, nhận được: {record['salary']}")

    # Validate join_date
    try:
        datetime.strptime(str(record["join_date"]), "%Y-%m-%d")
    except ValueError:
        errors.append(f"join_date phải có định dạng YYYY-MM-DD, nhận được: {record['join_date']}")

    return errors


def transform(records: list[dict]) -> list[dict]:
    """
    Validate và transform dữ liệu:
    - Chuyển join_date từ string sang date
    - Chỉ giữ lại các trường cần thiết
    - Bỏ qua record lỗi và log cảnh báo

    Args:
        records: list raw records từ extract

    Returns:
        list[dict]: list records đã được làm sạch
    """
    cleaned = []
    skipped = 0

    for i, record in enumerate(records):
        errors = validate_record(record, i)

        if errors:
            logger.warning(f"Record #{i} bị bỏ qua do lỗi: {errors} | Data: {record}")
            skipped += 1
            continue

        # Chỉ giữ các trường cần thiết (loại bỏ trường thừa)
        cleaned.append({
            "id":         int(record["id"]),
            "name":       record["name"].strip(),
            "department": record["department"].strip(),
            "salary":     int(record["salary"]),
            "join_date":  datetime.strptime(record["join_date"], "%Y-%m-%d").date(),
        })

    logger.info(f"Transform xong: {len(cleaned)} hợp lệ, {skipped} bị bỏ qua")
    return cleaned