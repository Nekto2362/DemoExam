import psycopg2

def connect_auth(login, password):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        print("Подключение установлено")

        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM user_import WHERE login = '{login}'")
        rows = cursor.fetchall()[0]
        if rows[3] == password:
            print(rows)
            conn.commit()
            conn.close()
            return True, rows[0], rows[1]

    except Exception:
        return False

def connect_tovar():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )

        cursor = conn.cursor()
        cursor.execute(""" SELECT * FROM "Tovar" """)
        a = cursor.fetchall()

        return a

    except Exception as e:
        print(str(e))
        return False, 8

def get_categories():
    """Возвращает список уникальных категорий товаров"""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT "Product category" FROM "Tovar" WHERE "Product category" IS NOT NULL')
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]
    except Exception as e:
        print("Ошибка получения категорий:", e)
        return []

def get_manufacturers():
    """Возвращает список уникальных производителей"""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT "Manufacturer" FROM "Tovar" WHERE "Manufacturer" IS NOT NULL')
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]
    except Exception as e:
        print("Ошибка получения производителей:", e)
        return []

def insert_tovar(artikul, name, unit, price, postavshchik, manufacturer, category, discount, quantity, description, photo_path):
    """
    Вставляет новую запись в таблицу Tovar.
    Возвращает (True, сообщение) при успехе, (False, ошибка) при неудаче.
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO "Tovar" (
                "Article", "Product Name", "Unit measurement", "Price",
                "Supplier", "Manufacturer", "Product category", "Current discount",
                "Quantity", "Product Description", "Photo"
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (artikul, name, unit, price, postavshchik, manufacturer, category, discount, quantity, description, photo_path))
        conn.commit()
        conn.close()
        return True, "Товар успешно добавлен"
    except Exception as e:
        return False, str(e)