import pandas as pd
# from datetime import datetime

from .db import UserCityOrders, db, engine

def anomaly_detector(threshold=3):
    conn = engine.connect()

    try:
        # Query data within the time range and order by time
        query = db.select(UserCityOrders).order_by(UserCityOrders.c.time)

        # Execute the query and fetch results into a DataFrame
        result_proxy = conn.execute(query)
        df = pd.DataFrame(result_proxy.fetchall(), columns=result_proxy.keys())

        # Group by city and apply anomaly detection within each group
        anomalies = pd.DataFrame()  # DataFrame to store all anomalies
        for city, group in df.groupby('city'):
            # Calculate mean and standard deviation for 'orders' within each city
            mean_orders = group['orders'].mean()
            std_orders = group['orders'].std()

            # Set threshold (e.g., 3 standard deviations for anomaly detection)
            lower_bound = mean_orders - threshold * std_orders
            upper_bound = mean_orders + threshold * std_orders

            # Identify anomalies for this city
            group['is_anomaly'] = (group['orders'] < lower_bound) | (group['orders'] > upper_bound)

            # Append anomalies to the anomalies DataFrame
            anomalies = pd.concat([anomalies, group[group['is_anomaly']]])

        # Display anomalies
        print("Anomalies detected:")
        print(anomalies)
        print('\n\n')

    finally:
        conn.close()
