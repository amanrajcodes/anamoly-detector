import sqlalchemy as db
engine = db.create_engine("postgresql+psycopg2://postgres:postgres@host.docker.internal:5432/postgres")

conn = engine.connect()
metadata = db.MetaData()

UserCityOrders = db.Table('user_city_orders', metadata,
              db.Column('time', db.DateTime, default=db.func.now()),
              db.Column('user', db.String(255), nullable=False),
              db.Column('city', db.String(255), nullable=False),
              db.Column('orders', db.Integer())
            )

# Create the table if it does not exist
metadata.create_all(engine) 

conn.close()