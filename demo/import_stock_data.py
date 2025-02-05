import os
import csv
from datetime import datetime
import django

# 设置 Django 环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
django.setup()

from predictor.models import StockPrice


def import_directory(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(".csv"):
            filepath = os.path.join(directory, filename)
            import_csv(filepath)


def import_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        # reader = csv.DictReader(f)
        reader = csv.DictReader(f, delimiter='\t')  # 如果是制表符分隔
        for row in reader:
            try:
                print(row)
                date_obj = datetime.strptime(row["Date"], "%Y-%m-%d").date()

                StockPrice.objects.update_or_create(
                    date=date_obj,
                    company_code=row["Company Code"],
                    defaults={
                        "company_name": row["Company Name"],
                        "stock_price": float(row["Stock Price"]),
                    },
                )
                print(f"Processed: {row['Company Code']} {date_obj}")
            except Exception as e:
                print(f"Error in {filepath} line {reader.line_num}: {str(e)}")


if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")

    stock_price_dir = os.path.join(current_dir, "../data/stock_logs")
    import_directory(stock_price_dir)
    print("Import completed.")
