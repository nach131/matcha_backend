from app.database import get_connection

def find_user_by_id(user_id):

    query = """
        SELECT
            id,
            name,
            email
        FROM users
        WHERE id = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            print (f"Executing query: {query} with parameters: user_id={user_id}")

            # cursor.execute(
            #     query,
            #     (user_id,)
            # )

            # row = cursor.fetchone()

    # if row is None:
    #     return None

    # return {
    #     "id": row[0],
    #     "name": row[1],
    #     "email": row[2]
    # }

def insert_user(name, email):
    
    query = """
        INSERT INTO users (name, email)
        VALUES (%s, %s)
        RETURNING id
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            print (f"Executing query: {query} with parameters: name={name}, email={email}")
            user_id = 1

            # cursor.execute(
            #     query,
            #     (name, email)
            # )

            # user_id = cursor.fetchone()[0]

    return {
        "id": user_id,
        "name": name,
        "email": email
    }