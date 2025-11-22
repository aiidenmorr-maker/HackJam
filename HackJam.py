import customtkinter
import PIL

app = customtkinter.CTk()

app.title("Login Screen")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

customtkinter.set_appearance_mode("Light")

image = PIL.Image.open("Wallpaper.jpg")
backgroundImage = customtkinter.CTkImage(image, size=(screen_width, screen_height))
bgLabel = customtkinter.CTkLabel(app, image=backgroundImage, text="")
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

app.geometry(f"{screen_width}x{screen_height}+0+0")

def submit():
    # Retrieve the text from the entry box
    user_input = username.get()
    print(f"User entered: {user_input}")

#blank text for padding
padding = customtkinter.CTkLabel(app, text="")
padding.pack(pady = 70, padx = 20)

welcome = customtkinter.CTkLabel(app, text="Welcome back, User", font=("Calibri", 50, "bold"), fg_color="#D7E9F3")
welcome.pack(pady=20, padx = 20)

username = customtkinter.CTkEntry(app, placeholder_text="Username", width=300, height=50, font=("Calibri", 20, "bold"))
username.pack(pady=20, padx=20)

password = customtkinter.CTkEntry(app, placeholder_text="Password", width=300, height=50, font=("Calibri", 20, "bold"))
password.pack(pady=20, padx=20)

# Create a button to process the input
submitButton = customtkinter.CTkButton(app, text="Submit", command=submit, width=150, height = 50, font=("Calibri", 20, "bold"))
submitButton.pack(pady=10)

app.mainloop()


