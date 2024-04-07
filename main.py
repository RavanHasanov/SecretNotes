from tkinter import *
from tkinter import messagebox
import base64


FONT = ("Verdena", 15, "normal")

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)



def saveAndEncrypt():
    title = titleEntry.get()
    message = text.get("1.0", END)
    master = masterEntry.get()

    if len(title) == 0 or len(message) == 0 or len(master) == 0:
        messagebox.showinfo(title="Error!", message="Enter all info")

    else:

        messageEncrypted = encode(master, message)

        try:
            with open("mysecret.txt", "a") as dataFile:
                dataFile.write(f"\n{title}\n{messageEncrypted}")

        except FileNotFoundError:
            with open("mysecret.txt", "w") as dataFile:
                dataFile.write(f"\n{title}\n{messageEncrypted}")

        finally:
            titleEntry.delete(0, END)
            text.delete("1.0", END)
            masterEntry.delete(0, END)


def decrypt():
    message = text.get("1.0", END)
    master = masterEntry.get()

    if len(message) == 0 or len(master) == 0:
        messagebox.showinfo(title="Error!", message="Enter all info")

    else:
        try:
            decoding = decode(master, message)
            text.delete("1.0", END)
            text.insert("1.0", decoding)

        except :
            messagebox.showinfo(title="Error!", message="Enter encrypted text")



window = Tk()
window.title("SecretNotes")
window.config(padx=10, pady=0)
window.minsize(width=200, height=570)
# window.update()
# print(window.winfo_width())

photo = PhotoImage(file="TopSecret.png")
canvas = Canvas(height=140, width=286)
canvas.create_image(145, 70, image=photo)
canvas.pack()


titleInfo = Label(text="Enter your title", font=FONT)
titleInfo.pack()
titleEntry = Entry(width=50)
titleEntry.pack()


inputLabel = Label(text="Enter your label", font=FONT)
inputLabel.pack()
text = Text(width=40, height=12)
text.pack()


masterLabel = Label(text="Enter master key", font=FONT)
masterLabel.pack()
masterEntry = Entry(width=50)
masterEntry.pack()


saveButton = Button(text="Save & Encrypt", command=saveAndEncrypt)
saveButton.pack()
saveButton.place(x=120, y=475)
decryptButton = Button(text="Decrypt", command=decrypt)
decryptButton.pack()
decryptButton.place(x=140, y=510)


window.mainloop()