import psycopg2
from tkinter import ttk
from tkinter import *
from connect_bd import connect_auth
from Tovar import tovar

def authorization():
    Authorization = Tk()
    Authorization.title("ООО «Обувь» Авторизация")
    Authorization.geometry("250x300")
    icon = PhotoImage(file = "import/Icon.png")
    Authorization.iconphoto(False, icon)

    style = ttk.Style()
    style.configure('TLabel', font=('Times New Roman', 10))
    style.configure('TButton', font=('Times New Roman', 10))

    ttk.Label(text="Авторизация", font=('Times New Roman' , 15 , 'bold')).pack(padx=8, pady= 8)

    ttk.Label(text="Логин", font=('Times New Roman' , 12 , 'bold')).pack()
    login = ttk.Entry(font=('Times New Roman', 10), width=30)
    login.pack(padx=8, pady=8)

    ttk.Label(text="Пароль", font=('Times New Roman' , 12 , 'bold')).pack()
    password = ttk.Entry(font=('Times New Roman', 10), width=30)
    password.pack(padx=8, pady=8)

    ttk.Button(text="Вход", command=lambda: check_auth(login, password)).pack(padx=8, pady=8)
    ttk.Button(text="Войти как Гость", command=lambda: check_guest()).pack(padx=8, pady=8)

    def check_auth(login, password):
        result = connect_auth(login.get(), password.get())

        if result:
            print(f"Авторизация успешна. Добро пожаловать, {result[1]} {result[2]}!")
            Authorization.destroy()
            tovar(name=f"{result[2]}", user_role=f"{result[1]}")
        else:
            print("Ошибка авторизации")

    def check_guest():
        print("Авторизован как гость")
        Authorization.destroy()
        tovar(name="Гость", user_role="Гость")
    
    Authorization.mainloop()

if __name__ == "__main__":
    authorization()

#94d5ous@gmail.com
#uzWC67