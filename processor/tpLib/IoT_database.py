import psycopg2
from datetime import datetime

dsn = "host={} dbname={} user={} password={}".format('127.0.0.1', 'IoTDB', 'sawtoothIoT', 'pass')

class IoT_Database:

    def __init__(self, name, temperature, humidity):
        self.name = name
        self.temperature = temperature
        self.humidity = humidity
        self.time = datetime.now()
        self.count = 0
    
    def submit(self, count):
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        self.count = count
        cur.execute("""
        INSERT INTO dataInfo (name, temperature, humidity, time)
        VALUES (%s, %s, %s, %s);
        """,
        (self.name, self.temperature, self.humidity, self.time))

        if self.count % 2 == 1:
            conn.commit()

