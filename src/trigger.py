from sqlalchemy import text

from .db import engine

# SQL for checking if the trigger exists
check_trigger_sql = """
SELECT EXISTS (
    SELECT 1 
    FROM pg_trigger 
    WHERE tgname = 'user_city_orders_insert_trigger'
);
"""

# SQL for creating the trigger function and trigger
create_trigger_function_sql = """
CREATE OR REPLACE FUNCTION notify_user_city_orders() RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('user_city_orders_channel', 'rows inserted!');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

create_trigger_sql = """
CREATE TRIGGER user_city_orders_insert_trigger
AFTER INSERT ON user_city_orders
FOR EACH STATEMENT
EXECUTE FUNCTION notify_user_city_orders();
"""

def create_trigger():
    conn = engine.connect()
    # Check if the trigger already exists
    trigger_exists = conn.execute(text(check_trigger_sql)).scalar()
    
    if not trigger_exists:
        # Create the function and trigger if they don't exist
        conn.execute(text(create_trigger_function_sql))
        conn.execute(text(create_trigger_sql))
        conn.commit()
        print("Trigger and function created.")
    else:
        print("Trigger already exists.")

    conn.close()