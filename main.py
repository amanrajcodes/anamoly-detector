import psycopg2
from src.trigger import create_trigger
from src.detector import anamoly_detector

init_msg = """
--- ANAMOLY DETECTOR ---

This program will detect anamolies in a postgres table 'city_user_orders' which
has number of orders of each user in each city on different dates.

The detector will run automatically whenever a new row is inserted in the table.
So you can manually insert data in the database via the PGAdmin.

While running with docker compose, the postgres and PGAdmin services also run
automatically,

Postgres DB URL: postgres://postgres:postgres@localhost:5432/postgres
PGAdmin URL: http://localhost:8888
PGAdmin email: admin@admin.com
PGAdmin password: password

NOTE: you might need to use "host.docker.internal" instead of "localhost" while
connecting the database inside the PGAdmin

============

Extra functionalities:

1. Insert random data 
\tCall the following command in new terminal while docker running to insert random data
\t\tdocker compose exec app sh -c "python insert_random_data.py"

2. Insert custom data 
\tCall the following command in new terminal while docker running to insert custom data
\t\tdocker compose exec app sh -c "python insert_custom_data.py"

3. Get total rows
\tCall the following command in new terminal while docker running to get count of total rows
\t\tdocker compose exec app sh -c "python get_rows.py"

"""

listen_connection = None

def trigger_listener():
    while True:
        listen_connection.poll()
        while listen_connection.notifies:
            notify = listen_connection.notifies.pop(0)
            print("\n\nNew rows inserted!")
            anamoly_detector()


def main():
    global listen_connection

    print(init_msg)
    
    # create trigger if does not exist
    create_trigger()

    # Set up a separate connection for LISTENing with psycopg2 directly
    listen_connection = psycopg2.connect("dbname=postgres user=postgres password=postgres host=host.docker.internal")
    listen_connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    listen_cursor = listen_connection.cursor()

    # Listen to the custom channel
    listen_cursor.execute("LISTEN user_city_orders_channel;")
    print("Listening for notifications on user_city_orders_channel...")

    try: 
        trigger_listener()
    finally:
        listen_cursor.close()
        listen_connection.close()

if __name__ == "__main__":
    main()