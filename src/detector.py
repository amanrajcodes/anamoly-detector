import pandas as pd
# from datetime import datetime

from .db import UserCityOrders, db, engine

def anamoly_detector(threshold=3):
    conn = engine.connect()

    try:
        # Query data within the time range and order by time
        query = db.select(UserCityOrders).order_by(UserCityOrders.c.time)

        # Execute the query and fetch results into a DataFrame
        result_proxy = conn.execute(query)
        df = pd.DataFrame(result_proxy.fetchall(), columns=result_proxy.keys())

        # Calculate mean and standard deviation for 'orders'
        mean_orders = df['orders'].mean()
        std_orders = df['orders'].std()

        # Set threshold (e.g., 3 standard deviations for anomaly detection)
        threshold = 3
        lower_bound = mean_orders - threshold * std_orders
        upper_bound = mean_orders + threshold * std_orders

        # Identify anomalies
        df['is_anomaly'] = (df['orders'] < lower_bound) | (df['orders'] > upper_bound)

        # Display anomalies
        anomalies = df[df['is_anomaly']]
        print("Anomalies detected:")
        print(anomalies)
        print('\n\n')
    finally:
        conn.close()