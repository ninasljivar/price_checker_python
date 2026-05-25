from dotenv import load_dotenv
load_dotenv()
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from twilio.rest import Client
import os

window = Tk()
window.title("Your price checker")
window.config(bg="#1E293B", padx=30, pady=20)

image = Image.open("logo.png")

height = 400
ratio = height / image.height
width = int(image.width * ratio)

image = image.resize((width, height))

canvas = Canvas()
canvas.config(bg="#1E293B", width=600, height=300, highlightthickness=0)
logo_image = ImageTk.PhotoImage(image)
canvas.create_image(300, 150, image=logo_image)
canvas.grid(column=0, row=0, columnspan=2)

url_input = Entry(window, width=60, fg="#60A5FA", bg="#2A3A4D", font=("Montserrat ExtraBold", 11, "underline"))
url_input.grid(column=0, row=1, sticky="ew", padx=5, pady=5)

url_label = Label(bg="#1E293B", fg="#FBBF24", text="URL ↑", font=("Montserrat ExtraBold", 14, "italic"))
url_label.grid(column=0, row=2, padx=5, pady=5)

price_input = Entry(window, fg="#60A5FA", bg="#2A3A4D", font=("Montserrat ExtraBold", 11, "bold"), justify="center")
price_input.grid(column=1, row=1, padx=5, pady=5)

price_label = Label(bg="#1E293B", fg="#FBBF24", text="Wanted price ↑", font=("Montserrat ExtraBold", 12, "italic"))
price_label.grid(column=1, row=2, padx=5, pady=5)

confirmation_label = Label(text= "↵ Press Enter", bg="#1E293B", fg="#94A3B8", font=("Montserrat", 9), justify="center")
confirmation_label.grid(column=0, row=3, columnspan=2,  padx=5, pady=5)

def check_store(event=None):
    global url
    url = str(url_input.get())
    wanted_price = float(price_input.get())
    # if "gigatron" in url:
    #     headers = {
    #         "User-Agent":"Mozilla/5.0"
    #     }
    #     response = requests.get(url, headers=headers)
    #     soup = BeautifulSoup(response.text, "html.parser")
    #     print(soup.prettify())
    #     price_str = soup.find("span", itemprop="price").getText().split(" ")[0].replace(".", "")
    #     price_str=price_str.replace(",", ".")
    #     price = float(price_str)
    #     if price < wanted_price:
    #         print(f"Your product price went down, check it out! {url}")
    if "tehnomedia" in url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        price_div = soup.find("div", class_="price")
        price_str = price_div.find("strong").getText().replace(".", "")
        price_str = price_str.replace(",", ".")
        price = float(price_str)
        if price < wanted_price:
            # print("radi")
            send_message()
            window.after(60000, check_store)
    else:
        messagebox.showinfo(title= "Site not found", message="Site you are trying to check is not supported by this app.")

def send_message(event=None):
    try:
        num = phone_entry.get()
        with open("phone_number.txt", "w") as data:
            data.write(num)
    except:
        with open("phone_number.txt", "r") as data:
            num = data.read()

    mssg_body = f"Your product price went down, check it out! {url}"
    client = Client(os.getenv("ACCOUNT_SID"), os.getenv("AUTH_TOKEN"))
    message = client.messages.create(
        body=mssg_body,
        from_="(218) 357-6881",
        to=num
    )

    phone_window.destroy()



def open_phone_window(event=None):
    global phone_window
    global phone_entry

    phone_window = Toplevel(window)
    phone_window.title("Phone number")
    phone_window.geometry("320x160")
    phone_window.config(bg="#202124")

    Label(phone_window,
          text="Enter your phone number ↓",
          bg="#202124",
          fg="white",
          ).grid(
        row=0, column=0, padx=10, pady=10
    )

    phone_entry = Entry(phone_window,
                        width=25,
                        font=("Arial", 12),
                        bg="#303134",
                        fg="white",
                        insertbackground="white",
                        relief="flat"
                        )
    phone_entry.grid(row=1, column=0, padx=10, pady=10)

    phone_entry.insert(0, "+381 ")

    phone_entry.focus_set()

    phone_entry.bind("<Return>", check_store)


window.bind("<Return>", open_phone_window)


























window.mainloop()