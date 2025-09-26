import psycopg2

def db():
    conn = psycopg2.connect(dbname="postgres",
                            user="postgres",
                            password="1111",
                            host="localhost",
                            port="5432")
    print("Подключение установлено")

    cursor = conn.cursor()
    cursor.execute("""Select type, name, director, phone_num, rating FROM partners ORDER BY name""")
    a = cursor.fetchall()
    cursor.execute("""Select name_partner, SUM(kolvo) FROM partner_products_import GROUP BY name_partner ORDER BY name_partner""")
    b = cursor.fetchall()
    # до 10000 – 0%, от 10000 – до 50000 – 5%, от 50000 – до 300000 – 10%, более 300000 – 15%.
    sale = []
    for i, j in b:
        if j < 10000:
            sale.append(0)
        elif j >= 10000 and j < 50000:
            sale.append(5)
        elif j >= 50000 and j < 300000:
            sale.append(10)
        else:
            sale.append(15)
    conn.close()
    return a, sale

