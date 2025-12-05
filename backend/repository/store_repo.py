from db.schema import get_connection

def obtainCoffees():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM products WHERE is_active = 1")
    rows = cur.fetchall()
    coffees = [dict(row) for row in rows]
    con.close()
    return coffees

def obtainCoffeeById(coffee_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM products WHERE id = ? AND is_active = 1", (coffee_id,))
    row = cur.fetchone()
    coffee = dict(row) if row else {"error": "Coffee not found"}
    con.close()
    return coffee

def obtainUsers():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id, email, first_name, last_name, phone, role, is_active, created_at FROM users")
    rows = cur.fetchall()
    users = [dict(row) for row in rows]
    con.close()
    return users

def obtainUserById(user_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id, email, first_name, last_name, phone, role, is_active, created_at FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    user = dict(row) if row else {"error": "User not found"}
    con.close()
    return user