from src.db import UserCityOrders, db, engine
from datetime import datetime, timedelta
import random


def insert_random_data():
    users = ["a", "b", "c", "d"]
    cities = ["delhi", "mumbai"]
    print(
f"""
Creating 200 random data where users will be one of ({', '.join(users)})
and cities will be one of ({', '.join(cities)})
and date will be in the month of November, 2024.
""")
    data = []
    start_date = datetime(2024, 11, 1)

    # Generate a dataset with 200 data points
    for _ in range(200):
        user = random.choice(users)
        city = random.choice(cities)
        time = start_date + timedelta(days=random.randint(0, 29))
        orders = random.randint(10, 20)

        # Create the data point
        data_point = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "user": user, "city": city, "orders": orders}
        data.append(data_point)

    insert_query = db.insert(UserCityOrders)

    conn = engine.connect()
    res = conn.execute(insert_query, data)
    conn.commit()

    output = conn.execute(db.select(UserCityOrders)).fetchall()
    print("Total rows: ", len(output))
    conn.close()


if __name__ == "__main__":
    insert_random_data()