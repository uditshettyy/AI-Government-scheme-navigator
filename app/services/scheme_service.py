from app.database import get_connection

def fetch_eligible_schemes(user):


    conn=get_connection()
    cursor=conn.cursor()
    query = """
        SELECT name, benefit, description, category, income_limit,
        benefit_amount, required_documents, priority_weight
        FROM schemes
        WHERE (LOWER(state) = 'all' OR LOWER(state) = LOWER(%s))
        AND LOWER(TRIM(occupation)) = LOWER(TRIM(%s))
        AND income_limit >= %s;
        """
    cursor.execute(query,(user.state,user.occupation,user.income))
    results=cursor.fetchall()
    cursor.close()
    conn.close()
    schemes=[
        {
            "name": row[0],
         "benefit": row[1],
         "description": row[2],
         "category": row[3],
         "income_limit": row[4],
         "benefit_amount": row[5],
         "required_documents": row[6],
         "priority_weight": row[7],
        }
        for row in results
        
    ]
    return schemes
