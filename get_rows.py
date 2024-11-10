from src.db import UserCityOrders, engine
from sqlalchemy import select, func

def get_total_rows():
    conn = engine.connect()

    count_query = select(func.count()).select_from(UserCityOrders)
    result = conn.execute(count_query).scalar()

    print(f"Total rows: {result}")
    
    conn.close()

if __name__ == "__main__":
    get_total_rows()