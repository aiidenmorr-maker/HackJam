import customtkinter
from google import genai
import time

client = genai.Client(api_key="AIzaSyBKrdvBmQwb0oS9i0u5Pw1kPxQz6c2e6xQ")

app = customtkinter.CTk()

app.title("CAPTCHA")

app.geometry("600x600")

customtkinter.set_appearance_mode("Light")

header = customtkinter.CTkLabel(app, text="Please write a 300 word response \nabout why you are not a robot.", font=("Calibri", 30, "bold"))
header.pack(pady=10, padx = 20)

essay = customtkinter.CTkTextbox(app, width=450, height=350, font=("Calibri", 20, "bold"))
essay.pack(pady=5, padx=20)

prompt = ""

def on_close():
    pass

def submit():
    global prompt
    essayResponse = essay.get("1.0", "end-1c")
    essay2 = essayResponse.split()
    if len(essay2) >= 300:
        print("essay is long enough")
        validation.configure(text = "Reviewing your response", font = ("Calibri", 20, "bold"))
        prompt = essay.get("1.0", "end-1c")

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=(f"In one word, yes or no, does this essay discuss being human?: {prompt}")
        )

        print(response.text)
        if response.text == "Yes":
            validation.configure(text = "Our AI has deemed your essay worthy.", font = ("Calibri", 20, "bold"))
            app.after(3000, app.destroy)
        else:
            validation.configure(text = "Our AI has deemed your essay unworthy. Try again.", font = ("Calibri", 20, "bold"))

    else:
        validation.configure(text = "Your essay is not long enough", font=("Calibri", 20, "bold"))


validation = customtkinter.CTkLabel(app, text = "", font=("Calibri", 20, "bold"))
validation.pack(pady=10)

submitButton = customtkinter.CTkButton(app, text="Submit", command = submit, width=200, height = 75, font=("Calibri", 20, "bold"))
submitButton.pack(pady=5)

app.protocol("WM_DELETE_WINDOW", on_close)

app.mainloop()



