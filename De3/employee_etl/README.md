# ETL Employee Pipeline

Pipeline ETL đọc dữ liệu nhân viên từ JSON, transform và load vào PostgreSQL.

## Cấu trúc project

```
etl_employee/
├── data/
│   └── employees.json       # File dữ liệu đầu vào
├── etl/
│   ├── __init__.py
│   ├── extract.py           # Đọc JSON
│   ├── transform.py         # Validate & chuyển đổi
│   └── load.py              # Insert vào PostgreSQL
├── main.py                  # Entry point
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                     # Config (không đẩy lên git)
├── .env.example             # Mẫu config
└── .gitignore
```

## Chạy với Docker (khuyến nghị)

```bash
# 1. Build và chạy toàn bộ
docker-compose up --build

# 2. Chỉ chạy lại ETL (postgres đang chạy)
docker-compose run etl
```

## Chạy local (không Docker)

```bash
# 1. Cài dependencies
pip install -r requirements.txt

# 2. Tạo file .env (copy từ mẫu)
cp .env.example .env

# 3. Chạy pipeline
python main.py
```

## Biến môi trường

| Biến | Mô tả | Mặc định |
|---|---|---|
| DB_HOST | Host PostgreSQL | localhost |
| DB_PORT | Port PostgreSQL | 5432 |
| DB_NAME | Tên database | employees_db |
| DB_USER | Username | postgres |
| DB_PASSWORD | Password | postgres |
| INPUT_FILE | Đường dẫn file JSON | data/employees.json |