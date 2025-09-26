import psycopg2
from tkinter import *
from tkinter import ttk

def win_sales():
    conn = psycopg2.connect(dbname="postgres",
                            user="postgres",
                            password="1111",
                            host="localhost",
                            port="5432")
    print("Подключение установлено")

    cursor = conn.cursor()
    cursor.execute("""Select * FROM partner_products_import WHERE kolvo >0 """)
    a = cursor.fetchall()
    cursor.execute("""Select name FROM partners""")
    b = cursor.fetchall()
    types = []
    for i in b:
        types.append(i[0])

    root_1 = Tk()
    root_1.title("Продажи")
    root_1.geometry("900x600")
    def filter(event):
        name = filtr.get()
        tree.delete(*tree.get_children())
        cursor.execute(f"""Select * FROM partner_products_import WHERE kolvo >0 and name_partner = '{name}'""")
        c = cursor.fetchall()
        for i in c:
            tree.insert("", END, values=i)


    filtr = ttk.Combobox(root_1, values=types,  state="readonly", )
    filtr.bind("<<ComboboxSelected>>", filter)
    filtr.pack()

    # определяем данные для отображения
    people = a

    # определяем столбцы
    columns = ("product", "name_partner", "kolvo", "date")

    tree = ttk.Treeview(root_1, columns=columns, show="headings")
    tree.pack(fill=BOTH, expand=1)

    # определяем заголовки
    tree.heading("product", text="Продукт")
    tree.heading("name_partner", text="Партнер")
    tree.heading("kolvo", text="Количество")
    tree.heading("date", text="Дата")

    # добавляем данные
    for person in people:
        tree.insert("", END, values=person)

    root_1.mainloop()

if __name__ == "__main__":
    win_sales()