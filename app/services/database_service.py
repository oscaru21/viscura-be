import psycopg2
from psycopg2.extras import RealDictCursor

class DatabaseService:
    def __init__(self):
        self.connection = psycopg2.connect(
            user="myuser",
            password="mypassword",
            host="localhost",
            port=5432,
            database="mydb"
        )
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def insert_record(self, table, data):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.cursor.execute(query, list(data.values()))
        self.connection.commit()

    def read_records(self, table, conditions=None):
        query = f"SELECT * FROM {table}"
        if conditions:
            query += " WHERE " + ' AND '.join([f"{k}=%s" for k in conditions.keys()])
            self.cursor.execute(query, list(conditions.values()))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_similar_records(self, table, vector_column, event_id, query_vector, n):
        query = f"""
        SELECT event_id, content, 1 - ({vector_column} <-> %s) AS similarity
        FROM {table}
        WHERE event_id = %s
        ORDER BY similarity DESC
        LIMIT %s
        """
        self.cursor.execute(query, (query_vector, event_id, n))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()