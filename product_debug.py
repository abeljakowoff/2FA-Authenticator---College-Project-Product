# -------------------------------------------------------------------

"""
    ПРОЕКТ СТУДЕНТА ГРУППЫ ОИБ-122 БЕЛЯКОВА АЛЕКСАНДРА ВЛАДИСЛАВОВИЧА
    ТЕМА ПРОЕКТА: "ПРОГРАММНАЯ РЕАЛИЗАЦИЯ OTP (ONE-TIME PASSWORD)"
    "2FA AUTHENTICATOR"
"""

# -------------------------------------------------------------------

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import pyotp
import os
import datetime as date
import webbrowser as web


root = Tk()

root.geometry("300x500")
root.resizable(FALSE, FALSE)
root.title('Two-factor authentication')

list_of_obj = []
list_of_hotp1 = []
list_of_hotp2 = []
list_of_hotp3 = []

list_of_copy = []

jsoncount = 0
hotp_count = 0

def addnewkey_():
    global check_counter
    if jsoncount >= 5:
        messagebox.showwarning(title = "Достигнт лимит", message = "Вы можете добавить максимум 5 аунтификаторов. Удалите некоторые из существующих чтобы создать новый.")
    else:
        addnewkey_window = Toplevel()
        addnewkey_window.title("Добавить новый ключ")
        addnewkey_window.geometry("300x300")
        addnewkey_window.resizable(FALSE, FALSE)

        check_counter = BooleanVar(value = False)

        def close_():
            addnewkey_window.destroy()
        
        def ok_():
            key = keyname.get()
            token = keytoken.get()
            try:
                if check_counter.get() is True:
                    testing = pyotp.HOTP(str(token))
                    print(testing.at(1))
                else:
                    testing = pyotp.TOTP(str(token))
                    print(testing.now())
                    print('да?')

                print(check_counter)

                jsondata = {
                "name": str(key),
                "token": str(token),
                "counter": check_counter.get()
                }

                print("Успешно?")
                if key == "":
                    pass
                elif token == "":
                    pass
                else:
                    try:
                        with open(f"data/{str(key)}.json", "w") as write_file:
                            json.dump(jsondata, write_file, indent = 4, ensure_ascii = True)
                        totp_()
                        addnewkey_window.destroy()
                    except: 
                        messagebox.showerror(title = "Недопустимое имя", message = "В названии аккаунта присутствуют недопустимые символы символы")
            except:
                messagebox.showerror(title = "Неправильный ключ", message = "По вышему введёмному ключю не удалось сгенерировать пароль.")

                print("неправильный токен")

        
        ttk.Label(master = addnewkey_window, text = "Добавить новый ключ", font = "Verdana 16 bold").place(x = 150, y = 30, anchor = "ce")

        ttk.Label(master = addnewkey_window, text = "Название:").place(x = 150, y = 70, anchor = "ce")
        keyname = ttk.Entry(master = addnewkey_window, width = 32)
        keyname.place(x = 150, y = 100, anchor = "ce")

        ttk.Label(master = addnewkey_window, text = "Ключ:").place(x = 150, y = 130, anchor = "ce")
        keytoken = ttk.Entry(master = addnewkey_window, width = 32)
        keytoken.place(x = 150, y = 160, anchor = "ce")

        countered = ttk.Checkbutton(master = addnewkey_window, text = "По счетчику", variable = check_counter, onvalue = True, offvalue = False)
        countered.place(x = 150, y = 200, anchor = "ce")

        ttk.Button(master = addnewkey_window, text = "OK", width = 10, command = ok_).place(x = 225, y = 260, anchor = "ce")
        ttk.Button(master = addnewkey_window, text = "Отмена", width = 10, command = close_).place(x = 75, y = 260, anchor = "ce")

def launchapp_():
    global jsoncount, hotp_count, list_of_obj, list_of_hotp1, list_of_hotp2, list_of_hotp3, list_of_copy
    list_of_obj = []
    list_of_hotp1 = []
    list_of_hotp2 = []
    list_of_hotp3 = []
    list_of_copy = []
    jsoncount = 0
    hotp_count = 0

    for i in os.listdir("./data"):
        if i.endswith('.json'):
            jsoncount += 1
            with open("./data/" + str(i[0:int(i.rfind("."))]) + ".json", "r", encoding = 'utf-8') as f:
                jsonfile = json.load(f)
            lframe = ttk.LabelFrame(master = mainframe, text = str(jsonfile["name"]), width = 240, height = 40)
            lframe.pack(side = TOP, padx = 12, pady = 10)
            text_with_token = Text(master = lframe, width = 6, height = 1)
            text_with_token.place(x = 200, y = -3, anchor = "ne")
            copy_clipboard_button = ttk.Button(master = lframe, text = "❐", width = 3, command = eval(f"copy_{jsoncount}"))
            copy_clipboard_button.place(x = 233, y = -6, anchor = "ne")

            if jsonfile['counter'] == True:
                hotp_count += 1
                count_entry = ttk.Entry(master = lframe, width = 6)
                count_entry.place(x = 105, y = -4, anchor = "ne")
                count_button_gen = ttk.Button(master = lframe, text = "➜", width = 3, name = f"count_button_{hotp_count}", command = eval(f"hotp_{hotp_count}"))
                count_button_gen.place(x = 140, y = -6, anchor = "ne")

                ttk.Label(master = lframe, text = "HOTP", font = "Arial 6", background = "#E8E8E8", foreground = "grey").place(x = 5, y = 1)

                if count_entry.get() == "":
                    text_with_token.insert(0.0, "------")
                    text_with_token.config(state = DISABLED)
                else: 
                    text_with_token.insert(0.0, pyotp.HOTP(str(jsonfile["token"])).at(int(count_entry.get())))
                    text_with_token.config(state = DISABLED)
                    print(count_entry.get())

                list_of_hotp1.append(count_entry)
                list_of_hotp2.append(str(i[0:int(i.rfind("."))]))
                list_of_hotp3.append(text_with_token)

                print(list_of_hotp1)

            else:
                ttk.Label(master = lframe, text = "TOTP", font = "Arial 6", background = "#E8E8E8", foreground = "grey").place(x = 5, y = 1)
                text_with_token.insert(0.0, pyotp.TOTP(str(jsonfile["token"])).now())
                text_with_token.config(state = DISABLED)

            list_of_obj.append(lframe)
            list_of_copy.append(text_with_token)

        else: 
            print("чтото не так с этим самым")
    print(list_of_hotp2)
    if jsoncount == 0: 
        if_nopasswords_()
    else:
        update_time_button.place(x = 224, y = 73.1)
        dass.place(x = 20, y = 58)
        das.place(x = 150, y = 470, anchor = "ce")
        progresstime.place(x = 20, y = 75)
        addbutton.place(x = 75, y = 430, anchor = CENTER)
        editbutton.place(x = 225, y = 430, anchor = CENTER)

def hotp_1():
    with open("./data/" + list_of_hotp2[0] + ".json", "r") as f:
        jsonfile = json.load(f)
    number = list_of_hotp1[0].get()
    list_of_hotp3[0].config(state = NORMAL)
    list_of_hotp3[0].delete('1.0', END)
    if number == "":
        list_of_hotp3[0].insert(0.0, "------")
    else:
        try:
            list_of_hotp3[0].insert(0.0, pyotp.HOTP(str(jsonfile["token"])).at(int(number)))
        except:
            list_of_hotp3[0].insert(0.0, "xxxxxx")

def hotp_2():
    with open("./data/" + list_of_hotp2[0] + ".json", "r") as f:
        jsonfile = json.load(f)
    number = list_of_hotp1[1].get()
    list_of_hotp3[1].config(state = NORMAL)
    list_of_hotp3[1].delete('1.0', END)
    if number == "":
        list_of_hotp3[1].insert(0.0, "------")
    else:
        try:
            list_of_hotp3[1].insert(0.0, pyotp.HOTP(str(jsonfile["token"])).at(int(number)))
        except:
            list_of_hotp3[1].insert(0.0, "xxxxxx")

def hotp_3():
    with open("./data/" + list_of_hotp2[0] + ".json", "r") as f:
        jsonfile = json.load(f)
    number = list_of_hotp1[2].get()
    list_of_hotp3[2].config(state = NORMAL)
    list_of_hotp3[2].delete('1.0', END)
    if number == "":
        list_of_hotp3[2].insert(0.0, "------")
    else:
        try:
            list_of_hotp3[2].insert(0.0, pyotp.HOTP(str(jsonfile["token"])).at(int(number)))
        except:
            list_of_hotp3[2].insert(0.0, "xxxxxx")

def hotp_4():
    with open("./data/" + list_of_hotp2[0] + ".json", "r") as f:
        jsonfile = json.load(f)
    number = list_of_hotp1[3].get()
    list_of_hotp3[3].config(state = NORMAL)
    list_of_hotp3[3].delete('1.0', END)
    if number == "":
        list_of_hotp3[3].insert(0.0, "------")
    else:
        try:
            list_of_hotp3[3].insert(0.0, pyotp.HOTP(str(jsonfile["token"])).at(int(number)))
        except:
            list_of_hotp3[3].insert(0.0, "xxxxxx")

def hotp_5():
    with open("./data/" + list_of_hotp2[0] + ".json", "r") as f:
        jsonfile = json.load(f)
    number = list_of_hotp1[4].get()
    list_of_hotp3[4].config(state = NORMAL)
    list_of_hotp3[4].delete('1.0', END)
    if number == "":
        list_of_hotp3[4].insert(0.0, "------")
    else:
        try:
            list_of_hotp3[4].insert(0.0, pyotp.HOTP(str(jsonfile["token"])).at(int(number)))
        except:
            list_of_hotp3[4].insert(0.0, "xxxxxx")

def copy_1():
    global list_of_copy
    root.clipboard_clear()
    root.clipboard_append(list_of_copy[0].get(0.0, END))

def copy_2():
    global list_of_copy
    root.clipboard_clear()
    root.clipboard_append(list_of_copy[1].get(0.0, END))

def copy_3():
    global list_of_copy
    root.clipboard_clear()
    root.clipboard_append(list_of_copy[2].get(0.0, END))

def copy_4():
    global list_of_copy
    root.clipboard_clear()
    root.clipboard_append(list_of_copy[3].get(0.0, END))

def copy_5():
    global list_of_copy
    root.clipboard_clear()
    root.clipboard_append(list_of_copy[4].get(0.0, END))

def test_():
    print(list_of_obj)
    print(jsoncount)


def totp_():
    global list_of_obj
    secs = date.datetime.now().time().second
    microsecs = date.datetime.now().time().microsecond
    if secs > 30: secs -= 30
    progresstime["value"] = float(f"{secs}.{microsecs}") * 100 / 30
    for a in range(int(jsoncount)):
        print(a-1)
        list_of_obj[a-1].destroy()
    launchapp_()

def totp_afterstart():
    global list_of_obj
    secs = date.datetime.now().time().second
    microsecs = date.datetime.now().time().microsecond
    if secs > 30: secs -= 30
    progresstime["value"] = float(f"{secs}.{microsecs}") * 100 / 30

def change_passwords():

    def ok__():
        try:
            print(".data/" + enter_a_file.get() + ".json")
            with open(file = "./data/" + enter_a_file.get() + ".json", mode = "r") as f: filemenu = json.load
            confirm_please = messagebox.askyesno(title = "Подтверждение", message = "Вы действительно хотите удалить аккаунт? Эту операцию невозможно будет отменить.")
            if confirm_please:
                os.remove("./data/" + enter_a_file + '.json')
                totp_()
                enter_a_file.delete(0, END)
        except Exception as error:
            messagebox.showerror(title = "Ошибка", message = "Аккаунта с таким названием не существует. Соблюдайте регистр букв.")
            print(error)
    
    def cancel_():
        configure_window.destroy()


    configure_window = Toplevel()
    configure_window.geometry('250x300')
    configure_window.resizable(FALSE, FALSE)
    configure_window.focus_set()

    ttk.Label(master = configure_window, text = "Удалить аккаунт", font = 'Verdana 16 bold').place(x = 125, y = 30, anchor = CENTER)
    enter_a_file = ttk.Entry(master = configure_window, width = 32)
    enter_a_file.place(x = 125, y = 150, anchor = CENTER)
    ttk.Button(master = configure_window, text = "Подтвержить", width = 14, command = ok__).place(x = 185, y = 250, anchor = CENTER)
    ttk.Button(master = configure_window, text = "Отмена", width = 14, command = cancel_).place(x = 62, y = 250, anchor = CENTER)

def openrepo_():
    web.open(url = "https://github.com/abeljakowoff/2FA-Authenticator---College-Project-Product", new = 0)

def aboutprogram_():
    web.open(url = "https://github.com/abeljakowoff/2FA-Authenticator---College-Project-Product/blob/master/README.md", new = 0)


ttk.Label(master = root, text = "2-FA AUTHENTICATION", font = "Verdana 14 bold").place(x = 150, y = 30, anchor = "ce") # title

mainmenu = Menu(root)
root.config(menu = mainmenu)

filemenu = Menu(mainmenu, tearoff = 0)
filemenu.add_command(label = "Добавить новый ключ", command = addnewkey_)
filemenu.add_command(label = "Изменить существующие ключи", command = change_passwords)
mainmenu.add_cascade(label = "Конфигурация", menu = filemenu)
filemenu.add_separator()
filemenu.add_command(label = "О программе", command = aboutprogram_)
filemenu.add_command(label = "Репозиторий в GitHub", command = openrepo_)


mainframe = ttk.Frame(master = root, width = 250, height = 400, relief = RIDGE)
mainframe.pack(side = TOP, padx = 12, pady = 100)
progresstime = ttk.Progressbar(master = root, length = 200, mode = "determinate", orient = HORIZONTAL)
addnew = Label(master = mainframe, text = "Нет аутентификаторов.\n\nДобавьте новый!")
update_time_button = ttk.Button(master = root, text = "⟳", width = 8, command = totp_)
das = ttk.Label(master = root, text = "Одноразовые коды по времени работают \nза счёт времени на вашем комьютере.", font = "Arial 7 italic", foreground = "grey")
dass = ttk.Label(master = root, text = "Осталось до обновления паролей:", font = "Arial 6", foreground = "grey")

def if_nopasswords_():
    addbutton.place(x = 150, y =275, anchor = CENTER)
    addnew.place(x = 125, y = 125, anchor = CENTER)

editbutton = ttk.Button(master = root, text = "✷ Редактировать", width = 17, command = change_passwords) # СЕЙЧАС ТУТ ПРИВЯЗАНА ТЕСТ ФУНКЦИЯ

addbutton = ttk.Button(master = root, text = "✚ Добавить", width = 17, command = addnewkey_)

launchapp_()

root.after(10, totp_afterstart)
root.mainloop()