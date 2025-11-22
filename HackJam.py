import customtkinter
import time

app = customtkinter.CTk()


app.title("test")
app.attributes('-fullscreen', True)
app.geometry("500x500")

def submit():
    # Retrieve the text from the entry box
    user_input = my_entry.get()
    print(f"User entered: {user_input}")

my_entry = customtkinter.CTkEntry(app, placeholder_text="Enter your text here")
my_entry.pack(pady=20, padx=20)

my_entry2 = customtkinter.CTkEntry(app, placeholder_text="Enter your text here")
my_entry2.pack(pady=20, padx=20)

# Create a button to process the input
my_button = customtkinter.CTkButton(app, text="Submit", command=submit)
my_button.pack(pady=10)

app.mainloop()


