import psycopg2
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from connect_bd import connect_tovar

def tovar(name="Гость", user_role="Администратор"):
    tovar = Tk()
    tovar.title("ООО «Обувь» Товары")
    tovar.geometry("800x600")
    icon = PhotoImage(file = "import/Icon.png")
    tovar.iconphoto(False, icon)

    style = ttk.Style()
    style.configure('lightgrey.TFrame', background='lightgrey')
    style.configure('green.TFrame', background='#7FFF00')
    style.configure('blue.TFrame', background='#00FA9A')
    style.configure('darkgreen.TFrame', background='#2E8B57')
    style.configure('lightblue.TFrame', background='lightblue')
    style.configure('TLabel', font=('Times New Roman', 10))
    style.configure('TButton', font=('Times New Roman', 10))

    top_frame = ttk.Frame(tovar, style='lightgrey.TFrame')
    top_frame.pack(fill=X, padx=10, pady=5)

    exit_btn = ttk.Button(top_frame, text="Выход", command=lambda: logout())
    exit_btn.pack(side=RIGHT, padx=5)

    user_info = f"{name} ({user_role})"
    user_label = ttk.Label(top_frame, font=('Times New Roman', 10, 'bold'), text=user_info)
    user_label.pack(side=RIGHT, padx=10)

    images = []
    data = connect_tovar()

    if user_role == "Администратор":
        add_btn = ttk.Button(top_frame, text="Добавить товар", command=lambda: Add_Tovar())
        add_btn.pack(side=LEFT, padx=5)

    if user_role in ("Менеджер", "Администратор"):
        controls_frame = ttk.Frame(tovar, style='lightgrey.TFrame')
        controls_frame.pack(fill=X, padx=10, pady=5)

        # Поисковая строка
        ttk.Label(controls_frame, text="Поиск:").pack(side=LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(controls_frame, textvariable=search_var, width=35).pack(side=LEFT, padx=5)

        # Сортировка по количеству
        ttk.Label(controls_frame, text="Сортировка:").pack(side=LEFT, padx=5)
        sort_var = tk.StringVar()
        sort_combo = ttk.Combobox(controls_frame, textvariable=sort_var, state="readonly", width=20)
        sort_combo.pack(side=LEFT, padx=5)
        
        sort_combo['values'] = ["Без сортировки", "По количеству (возрастание)", "По количеству (убывание)"]
        sort_combo.current(0) 

        # Фильтр по поставщику
        ttk.Label(controls_frame, text="Поставщик:").pack(side=LEFT, padx=5)
        supplier_var = tk.StringVar()
        supplier_combo = ttk.Combobox(controls_frame, textvariable=supplier_var, state="readonly", width=20)
        supplier_combo.pack(side=LEFT, padx=5)

        suppliers = sorted(set(row[4] for row in data))
        supplier_combo['values'] = ["Все поставщики"] + suppliers
        supplier_combo.current(0) 

    main_container = ttk.Frame(tovar, style='lightgrey.TFrame')
    main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)

    canvas = tk.Canvas(main_container)
    scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def logout():
        tovar.destroy()
        from Authorization import authorization
        authorization()
    
    def Add_Tovar():
        from Add_Tovar import add_tovar
        add_tovar(tovar)

    def update_display():
        for frame in scrollable_frame.winfo_children():
            frame.destroy()
        images.clear()

        if user_role in ("Менеджер", "Администратор"):
            search_text = search_var.get().lower().strip()
            selected_supplier = supplier_var.get()
            sort_mode = sort_var.get()
        else:
            search_text = ""
            selected_supplier = "Все поставщики"
            sort_mode = "Без сортировки"

        filtered = []
        for row in data:
            # Фильтр по поставщику
            if selected_supplier != "Все поставщики" and row[4] != selected_supplier:
                continue
            # Поиск по текстовым полям (регистронезависимый)
            if search_text:
                # Поля: название (1), описание (9), производитель (5), поставщик (4), категория (6), единица изм. (2)
                text_fields = [str(row[1]).lower(), str(row[9]).lower(), str(row[5]).lower(),str(row[4]).lower(), str(row[6]).lower(), str(row[2]).lower()]
                if not any(search_text in field for field in text_fields):
                    continue
            filtered.append(row)
        
        if sort_mode == "По количеству (возрастание)":
            filtered.sort(key=lambda x: x[8])
        elif sort_mode == "По количеству (убывание)":
            filtered.sort(key=lambda x: x[8], reverse=True)
        
        if not filtered:
            ttk.Label(scrollable_frame, text="Нет товаров, соответствующих критериям.").pack(pady=20)
            return
    
        for row in filtered:
            if len(row) < 11:
                continue  # пропускаем некорректные строки
            art, name, unit, price, supplier, manufacturer, category, discount, quantity, description, photo = row

            if discount > 15:
                discount_style = 'darkgreen.TFrame'
            else:
                discount_style = 'blue.TFrame'
            
            if quantity > 0:
                quantity_style = 'green.TFrame'
            else:
                quantity_style = 'lightblue.TFrame'

            # Контейнер товара
            tovar_container = ttk.Frame(scrollable_frame, style=quantity_style, width=750, height=200)
            tovar_container.pack_propagate(False)
            tovar_container.pack(pady=5)

            # Фото
            photo_container = ttk.Frame(tovar_container, style='blue.TFrame', width=180, height=180)
            photo_container.pack_propagate(False)
            photo_container.pack(side=tk.LEFT, padx=(10, 5), pady=10)
            if photo:
                image = Image.open(f"import/{photo}")
            else:
                image = Image.open(f"import/picture.png")
            image = image.resize((180, 180))
            img = ImageTk.PhotoImage(image)
            images.append(img)
            ttk.Label(photo_container, image=img).pack(expand=True)

            # Информация (наименование, категория, цена, количество)
            info_container = ttk.Frame(tovar_container, style='blue.TFrame', width=350, height=180)
            info_container.pack_propagate(False)
            info_container.pack(side=tk.LEFT, padx=5, pady=10)

            # Наименование
            name_label = ttk.Label(info_container, text=f"{category} | {name}", font=('Times New Roman', 12, 'bold'))
            name_label.pack(anchor='w', padx=5, pady=2)

            # Описание товара
            desc_label = f"Описане: {description}"
            desc_label = ttk.Label(info_container, text=desc_label, wraplength=330, width=330).pack(anchor='w', padx=5, pady=2)

            # Производитель
            manuf_text = f"Производитель: {manufacturer}"
            ttk.Label(info_container, text=manuf_text).pack(anchor='w', padx=5, pady=2)

            # Поставщик
            supp_text = f"Поставщик: {supplier}"
            ttk.Label(info_container, text=supp_text).pack(anchor='w', padx=5, pady=2)

            price_frame = ttk.Frame(info_container)
            price_frame.pack(anchor='w', padx=5, pady=2)

            if discount > 0:
                # Старая цена перечёркнутая, красная
                ttk.Label(price_frame, text=f"Цена: {price} руб.",foreground='red', font=('Times New Roman', 10, 'overstrike')).pack(side=tk.LEFT)
                ttk.Label(price_frame, text=f"{(price * (100 - discount) / 100):.2f} руб.",foreground='black').pack(side=tk.LEFT)
            else:
                # Без скидки
                ttk.Label(price_frame, text=f"Цена: {price} руб.").pack(side=tk.LEFT)

            # Единица измерения
            unit_text = f"Ед. изм.: {unit}"
            ttk.Label(info_container, text=unit_text).pack(anchor='w', padx=5, pady=2)

            # Количество на складе
            quantity_text = f"Количество на складе: {quantity}"
            ttk.Label(info_container, text=quantity_text).pack(anchor='w', padx=5, pady=2)

            # Cкидка (Cкидка)
            description_container = ttk.Frame(tovar_container, style=discount_style, width=180, height=180)
            description_container.pack_propagate(False)
            description_container.pack(side=tk.LEFT, padx=5, pady=10)

            # Cкидка
            supp_text = f"{discount}%"
            ttk.Label(description_container, text=supp_text, font=('Times New Roman', 20, 'bold')).pack(anchor=CENTER, pady=75)

    if user_role in ("Менеджер", "Администратор"):
        search_var.trace_add('write', lambda *args: update_display())
        sort_var.trace_add('write', lambda *args: update_display())
        supplier_var.trace_add('write', lambda *args: update_display())

    update_display()

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tovar.mainloop()

if __name__ == "__main__":
    tovar()