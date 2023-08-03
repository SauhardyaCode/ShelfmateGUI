import mysql.connector as conn

try:
    connection = conn.connect(
        host="sql10.freesqldatabase.com",
        user="sql10618972",
        password="fBNE8Pwvag",
        database="sql10618972"
    )
    # using a buffered cursor, the connector fetches ALL rows and takes one from the connector
    cursor = connection.cursor(buffered=True)
except:
    print("[CONNECTION ERROR]")
    exit()

cursor.execute("select * from logged_users")
print(*cursor.fetchall(), sep='\n\n')