# -------------------------------------------------------------------

"""
    ПРОЕКТ СТУДЕНТА ГРУППЫ ОИБ-122 БЕЛЯКОВА АЛЕКСАНДРА ВЛАДИСЛАВОВИЧА
    ТЕМА ПРОЕКТА: "ПРОГРАММНАЯ РЕАЛИЗАЦИЯ OTP (ONE-TIME PASSWORD)"
    "2FA CHECKER"
"""

# -------------------------------------------------------------------
from tkinter import *
from tkinter import ttk
import pyotp
import qrcode
import os
import random

root = Tk()
root.geometry('480x150')
root.title("2fa checker")
root.resizable(False, False)

def totp_():
    window = Toplevel()
    window.geometry("450x400")
    window.resizable(False, False)
    window.title("Проверка по TOTP")

    def done_button():
        if enter_password.get() == pyotp.TOTP(str(TOKEN)).now():
            print('да')
            canva.destroy()
            Label(master = window, text = "✔", font = "Arial 48 bold", foreground = "green", height = 2).place(x = 225, y = 170, anchor = CENTER)
            ttk.Label(master = window, foreground = "green", text = "Всё правильно! \nТеперь вы можете закрыть это окно и удалить аккаунт из \nприложения 2FA.", anchor = "ce").place(x = 240, y = 230, anchor = CENTER)
            done_but.destroy()
            enter_password.config(foreground = "green")
        else:
            enter_password.config(foreground = "red")

    TOKEN = pyotp.random_base32()
    qrcode_text = pyotp.totp.TOTP(TOKEN).provisioning_uri(name = "Delete this account after test", issuer_name = "2FA CHECK (TOTP)")

    ttk.Label(master = window, text = "Отсканируйте QR-код приложением 2-факторной аутентификации \n(например Authy) на вашем смартфоне или перепишите токен/ключ, \nпри этои установите генерацию пароля по времени.", font = "Verdana 8").place(x = 10, y = 20)
    img = qrcode.QRCode(version = 2, box_size = 4, border = 2)
    img.add_data(qrcode_text)
    img.make(fit = True)
    img1 = img.make_image(fill_color = "black", back_color = "white").save("qr.png")
    img1 = PhotoImage(file = "./qr.png")

    canva = Canvas(master = window, width = 210, height = 210)
    canva.create_image(0, 0, image = img1, anchor = NW)
    canva.place(x = 225, y = 200, anchor = CENTER)
    os.remove("./qr.png")

    token_in_entry = ttk.Label(master = window, text = TOKEN, font = "Verdana 12 bold", foreground = "red")
    token_in_entry.place(x = 225, y = 320, anchor = CENTER)

    enter_password = ttk.Entry(master = window, width = 6, font = "Verdana 18 bold")
    enter_password.place(x = 330, y = 360, anchor = CENTER)
    ttk.Label(master = window, text = "Теперь введите полученный пароль в поле:").place(x = 140, y = 360, anchor = CENTER)
    done_but = ttk.Button(master = window, text = "✔", width = 5, command = done_button)
    done_but.place(x = 415, y = 360, anchor = CENTER)


def hotp_():
    window = Toplevel()
    window.geometry("450x400")
    window.resizable(False, False)
    window.title("Проверка по HOTP")

    def done_button():
        if enter_password.get() == pyotp.HOTP(str(TOKEN)).at(counter) or enter_password.get() == pyotp.HOTP(str(TOKEN)).at(counter + 1):
            print('да')
            canva.destroy()
            Label(master = window, text = "✔", font = "Arial 48 bold", foreground = "green", height = 2).place(x = 225, y = 170, anchor = CENTER)
            ttk.Label(master = window, foreground = "green", text = "Всё правильно! \nТеперь вы можете закрыть это окно и удалить аккаунт из \nприложения 2FA.", anchor = "ce").place(x = 240, y = 230, anchor = CENTER)
            done_but.destroy()
            enter_password.config(foreground = "green")
        else:
            enter_password.config(foreground = "red")

    counter = random.randint(0, 99)
    TOKEN = pyotp.random_base32()
    qrcode_text = pyotp.hotp.HOTP(TOKEN).provisioning_uri(name = "Delete this account after test", issuer_name = "2FA CHECK (HOTP)", initial_count = counter)

    ttk.Label(master = window, text = "Отсканируйте QR-код приложением 2-факторной аутентификации \n(например Authy) на вашем смартфоне или перепишите токен/ключ, \nпри этои установите генерацию пароля по счетчику.", font = "Verdana 8").place(x = 10, y = 20)
    ttk.Label(master = window, text = f"Число счетчика: {counter} и {counter + 1}", font = "Arial 8 bold").place(x = 225, y = 80, anchor = CENTER)
    img = qrcode.QRCode(version = 2, box_size = 4, border = 2)
    img.add_data(qrcode_text)
    img.make(fit = True)
    img1 = img.make_image(fill_color = "black", back_color = "white").save("qr.png")
    img1 = PhotoImage(file = "./qr.png")

    canva = Canvas(master = window, width = 210, height = 210)
    canva.create_image(0, 0, image = img1, anchor = NW)
    canva.place(x = 225, y = 200, anchor = CENTER)
    os.remove("./qr.png")

    token_in_entry = ttk.Label(master = window, text = TOKEN, font = "Verdana 12 bold", foreground = "red")
    token_in_entry.place(x = 225, y = 320, anchor = CENTER)

    enter_password = ttk.Entry(master = window, width = 6, font = "Verdana 18 bold")
    enter_password.place(x = 330, y = 360, anchor = CENTER)
    ttk.Label(master = window, text = "Теперь введите полученный пароль в поле:").place(x = 140, y = 360, anchor = CENTER)
    done_but = ttk.Button(master = window, text = "✔", width = 5, command = done_button)
    done_but.place(x = 415, y = 360, anchor = CENTER)


ttk.Label(master = root, text = "Проверьте работу 2-факторной аутентификации", font = "Verdana 12 bold").place(x = 240, y = 30, anchor = CENTER)
totp_check_button = ttk.Button(master = root, text = "Проверить по временному паролю (TOTP)", width = 48, command = totp_)
totp_check_button.place(x = 240, y = 70, anchor = CENTER)
hotp_check_button = ttk.Button(master = root, text = "Проверить по паролю с счетчиком (HOTP)", width = 48, command = hotp_)
hotp_check_button.place(x = 240, y = 100, anchor = CENTER)

root.mainloop()