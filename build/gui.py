import threading
import requests
import webbrowser
from tkinter import *
from pathlib import Path

# === API Configuration ===
BACKEND_URL = "https://pychat-6djk.onrender.com/"  # Flask backend endpoint

# === UI Setup ===
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Admin\Downloads\PyChat v1.0\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("320x568")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=568,
    width=320,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)
canvas.create_rectangle(0.0, 0.0, 320.0, 63.0, fill="#C5BDBD", outline="")
canvas.create_rectangle(0.0, 63.0, 320.0, 568.0, fill="#E5E5E5", outline="")

canvas.create_text(160, 22, anchor="center", text="PyChat",
                   fill="#000000", font=("Inter", 24))
canvas.create_text(160, 51, anchor="center", text="Powered by Groq",
                   fill="#000000", font=("Inter", 12))
canvas.create_text(10.0, 77.0, anchor="nw", text="Enter Prompt:",
                   fill="#000000", font=("Inter", 10 * -1))

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
canvas.create_image(159.5, 126.0, image=entry_image_1)
entry_1 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_1.place(x=9.0, y=94.0, width=301.0, height=62.0)

# === Function to run the query ===
def run_query():
    user_input = entry_1.get().strip()
    if not user_input:
        return
    entry_2.delete("1.0", "end")
    entry_2.insert("1.0", "⏳ Generating response...")

    def query_backend():
        try:
            response = requests.post(BACKEND_URL, json={"message": user_input})
            result = response.json()

            if "choices" in result:
                reply = result["choices"][0]["message"]["content"].strip()
            elif "error" in result:
                reply = f"⚠️ Error: {result['error']}"
            else:
                reply = "⚠️ Unexpected response format."
        except Exception as e:
            reply = f"❌ Error: {str(e)}"

        entry_2.delete("1.0", "end")
        entry_2.insert("1.0", reply)

    threading.Thread(target=query_backend).start()

# === GitHub button function ===
def open_github():
    webbrowser.open("https://github.com/Habibur-Rahaman-0786/PyChat")

# === Go Button ===
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0,
                  highlightthickness=0, command=run_query, relief="flat")
button_1.place(x=116.0, y=172.0, width=87.0, height=32.0)

# === GitHub Button ===
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2, borderwidth=0,
                  highlightthickness=0, command=open_github, relief="flat")
button_2.place(x=93.0, y=521.0, width=133.005615234375, height=32.0)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
canvas.create_image(160.0, 364.5, image=entry_image_2)
entry_2 = Text(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, wrap="word")
entry_2.place(x=10.0, y=218.0, width=300.0, height=291.0)

canvas.create_text(0.0, 553.0, anchor="nw", text="PyChat v1.0.03",
                   fill="#000000", font=("Inter", 10 * -1))
window.resizable(False, False)
window.mainloop()

