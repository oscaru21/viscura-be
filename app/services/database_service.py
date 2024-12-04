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

    def __enter__(self):
        """
        Enter method for context manager
        """
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit method for context manager, it closes the connection
        """
        self.close()

    def insert_record(self, table, data, return_id=True):
        """
        Insert a record into the specified table.
        :param table: Name of the table.
        :param data: Dictionary containing column-value pairs to insert.
        :param return_id: Whether to return the ID of the inserted record.
        :return: The ID of the inserted record if return_id is True, otherwise None.
        """
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        
        if return_id:
            query += " RETURNING id"

        self.cursor.execute(query, list(data.values()))
        self.connection.commit()
        
        if return_id:
            return self.cursor.fetchone()["id"]
        return None

    def read_records(self, table, conditions=None):
        query = f"SELECT * FROM {table}"
        if conditions:
            query += " WHERE " + ' AND '.join([f"{k}=%s" for k in conditions.keys()])
            self.cursor.execute(query, list(conditions.values()))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def update_record(self, table, data, conditions):
        """
        Update records in the database based on conditions
        :param table: Name of the table
        :param data: Dictionary with column-value pairs to update
        :param conditions: Dictionary with column-value pairs for WHERE clause
        :return: Number of rows affected
        """
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        condition_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition_clause}"
        
        values = list(data.values()) + list(conditions.values())
        self.cursor.execute(query, values)
        self.connection.commit()
        
        return self.cursor.rowcount 
    
    def delete_record(self, table, conditions):
        query = f"DELETE FROM {table} WHERE " + ' AND '.join([f"{k}=%s" for k in conditions.keys()])
        self.cursor.execute(query, list(conditions.values()))
        self.connection.commit()

    def get_similar_records(self, table, vector_column, event_id, query_vector):
        query = f"""
        SELECT *, 1 - ({vector_column} <=> %s) AS similarity
        FROM {table}
        WHERE event_id = %s
        ORDER BY similarity DESC
        """
        self.cursor.execute(query, (query_vector, event_id))
        return self.cursor.fetchall()
    
    def get_top_k_similar_records(self, table, vector_column, event_id, query_vector, n: int = 3):
        query = f"""
        SELECT *, 1 - ({vector_column} <=> %s) AS similarity
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