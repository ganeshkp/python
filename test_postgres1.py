import psycopg2
"""
#TEST1
try:
    # connect_str = "dbname='testpython' user='matt' host='localhost' " + \
    #               "password='myOwnPassword'"
    # conn = psycopg2.connect(connect_str)



    # use our connection values to establish a connection
    conn = psycopg2.connect(dbname='testpython',
                            user='ganeshp',
                            password='ganeshp',
                            host='localhost',
                            port='5432')
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # create a new table with a single column called "name"
    cursor.execute("CREATE TABLE tutorials2(name char(40)); ")
    # run a SELECT statement - no data in there, but we can try it
    cursor.execute("SELECT * from tutorials")
    conn.commit()  # <--- makes sure the change is shown in the database
    rows = cursor.fetchall()
    print(rows)
    cursor.close()
    conn.close()
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)
"""


# TEST2
try:
    # use our connection values to establish a connection
    conn = psycopg2.connect(dbname='dvdrental',
                            user='ganeshp',
                            password='ganeshp',
                            host='localhost',
                            port='5432')
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # run a SELECT statement - no data in there, but we can try it
    cursor.execute(
        """SELECT * from address ORDER BY address_id ASC LIMIT 20""")
    # conn.commit()  # <--- makes sure the change is shown in the database
    rows = cursor.fetchall()
    print(rows)

    cursor.execute(
        "SELECT first_name, last_name FROM actor ORDER BY last_name ASC LIMIT 10;")
    rows = cursor.fetchall()
    print(rows)
    cursor.close()
    conn.close()
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)
