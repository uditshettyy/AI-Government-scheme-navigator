from app.database import get_connection

def fetch_eligible_schemes(user):


    conn=get_connection()
    cursor=conn.cursor()

    query="""
        SELECT name,benefit,description 
        FROM schemes
        WHERE LOWER(state) =LOWER(%s)
        AND LOWER(occupation) =LOWER(%s)
        AND income_limit>=%s;
    """
    cursor.execute(query,(user.state,user.occupation,user.income))
    results=cursor.fetchall()
    cursor.close()
    conn.close()
    schemes=[
        {
            "name":row[0],
         "benefit":row[1],
         "description":row[2]
        }
        for row in results
    ]
    return schemes