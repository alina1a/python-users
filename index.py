import tkinter as tk
import sqlite3

try:
    sqlite_connection = sqlite3.connect('python.db')
    sqlite_connection.row_factory = sqlite3.Row
    cursor = sqlite_connection.cursor()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        print("Соединение")

def auth():
    errorLabel["text"] = ""
    query = "SELECT * FROM user WHERE login = '" + loginInput.get() + "' COLLATE NOCASE"
    cursor.execute(query)
    record = cursor.fetchone()
    if (record == None):
        showError("Логин или пароль неверный")
        return
    
    print(record['login'])
    if (record['password'] != passwordInput.get()):
        showError("Логин или пароль неверный")
        return

    showUsersListWindow()

    
def showUsersListWindow():
    window.destroy()
    usersWindows.deiconify()

    printUsers()

    createLoginLabel = tk.Label(text="Логин", master=usersWindows)
    createLoginLabel.grid(row=0, column=0)

    createPasswordLabel = tk.Label(text="Пароль", master=usersWindows)
    createPasswordLabel.grid(row=0, column=1)
    
    createLoginInput = tk.Entry(fg="black", bg="white", width=50, master=usersWindows)
    createLoginInput.grid(row=1, column=0)

    createPasswordInput = tk.Entry(fg="black", bg="white", width=50, master=usersWindows)
    createPasswordInput.grid(row=1, column=1)

    createUserButton = tk.Button(
        master=usersWindows,
        text="Добавить пользователя",
        command=lambda: createUser(createLoginInput.get(), createPasswordInput.get())
    )

    createUserButton.grid(row=1, column=2, sticky="nsew")

def createUser(login, password):
    print('create -', login, password)
    try:
        query = "INSERT INTO user(login, password) VALUES (?, ?);"
        cursor.execute(query, [login, password])
        sqlite_connection.commit()
        printUsers()
    except sqlite3.Error as error:
        print("Ошибка при создания пользователя", error)

def printUsers():
    tableHead = tk.Label(text="ID", master=usersWindows)
    tableHead.grid(row=2, column=0)
    
    tableHead = tk.Label(text="Логин", master=usersWindows)
    tableHead.grid(row=2, column=1)
    
    tableHead = tk.Label(text="Удалить?", master=usersWindows)
    tableHead.grid(row=2, column=2)

    for label in usersWindows.grid_slaves():
        if int(label.grid_info()['row']) > 3:
            label.grid_forget()

    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    for index, user in enumerate(users):
        userLabel = tk.Label(text=user['id'], master=usersWindows)
        userLabel.grid(row=index + 3, column=0)

        userLabel = tk.Label(text=user['login'], master=usersWindows)
        userLabel.grid(row=index + 3, column=1)

        removeUserButton = tk.Button(
            master=usersWindows,
            text="X",
            background="red",
            command=lambda: removeUser(user['id'])
        )

        removeUserButton.grid(row=index + 3, column=2, sticky="nsew")

def removeUser(id):
    try:
        query = "DELETE FROM user WHERE id = ?;"
        cursor.execute(query, [id])
        sqlite_connection.commit()
        printUsers()
    except sqlite3.Error as error:
        print("Ошибка при удалении пользователя", error)
        

def showError(text):
    errorLabel["text"] = text
    return
    

def resetTable():
    tableQuery = """
    DROP TABLE user;
    CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    INSERT INTO user(login, password) VALUES ("Alina", "password");
    INSERT INTO user(login, password) VALUES ("CuBeR116", "password116");
    """
    cursor.executescript(tableQuery)
    sqlite_connection.commit()

window = tk.Tk()
window.rowconfigure(0, minsize=50)
window.columnconfigure([0], minsize=50)

usersWindows = tk.Tk(screenName="Список добавленных пользователей")
usersWindows.rowconfigure(0, minsize=50)
usersWindows.columnconfigure([0, 1, 2], minsize=50)
usersWindows.withdraw()

loginLabel = tk.Label(text="Логин")
loginLabel.grid(row=0, column=0)

loginInput = tk.Entry(fg="black", bg="white", width=50)
loginInput.grid(row=1, column=0)

passwordLabel = tk.Label(text="Пароль")
passwordLabel.grid(row=2, column=0)

passwordInput = tk.Entry(fg="black", bg="white", width=50)
passwordInput.grid(row=3, column=0)

errorLabel = tk.Label(fg="red")
errorLabel.grid(row=4, column=0)

btn_decrease = tk.Button(
    master=window,
    text="Войти",
    command=auth
)

btn_decrease.grid(row=5, column=0, sticky="nsew")


btnResetTable = tk.Button(
    master=window,
    text="Пересоздать таблицы",
    command=resetTable
)

btnResetTable.grid(row=6, column=0, sticky="nsew")

window.mainloop()