from src.db import UserCityOrders, db, engine
from datetime import datetime

def insert_data():
    date = input("Enter date (dd/mm/yyyy): ")
    user = input("Enter user: ")
    city = input("Enter city: ")
    orders = int(input("Enter orders: "))

    date_object = datetime.strptime(date, "%d/%m/%Y")

    insert_query = db.insert(UserCityOrders)

    conn = engine.connect()
    res = conn.execute(insert_query, [{
        "time": date_object,
        "user": user,
        "city": city,
        "orders": orders
    }])
    conn.commit()

    output = conn.execute(db.select(UserCityOrders)).fetchall()
    print("Total rows: ", len(output))
    conn.close()


if __name__ == "__main__":
    insert_data()