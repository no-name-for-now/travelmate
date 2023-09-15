import psycopg2

# Replace these with your database connection details
db_host = "localhost"
db_name = "mydatabase"
db_user = "myuser"
db_password = "mypassword"

# Establish a connection to the database
conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)

cur = conn.cursor()

table_name = "unique_search_history"

delete_query = f"DELETE FROM {table_name}"
cur.execute(delete_query)

# Commit the changes to the database
conn.commit()
print(f"Deleted {table_name}")
