import customtkinter
import PIL
import time 
import random

from google import genai
import os
client = genai.Client(api_key="AIzaSyBKrdvBmQwb0oS9i0u5Pw1kPxQz6c2e6xQ")
chat = client.chats.create(model="gemini-2.5-flash")

# Commented out the blocking chat loop so GUI can start
# while True:
#     message = input("> ")
#     if message == "exit":
#         break
#     res = chat.send_message(message)
#     print(res.text)

# GUI
app = customtkinter.CTk()
app.title("Login Screen")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

## IMAGE
customtkinter.set_appearance_mode("Light")
image = PIL.Image.open("Background.jpg")
backgroundImage = customtkinter.CTkImage(image, size=(screen_width, screen_height))
bgLabel = customtkinter.CTkLabel(app, image=backgroundImage, text="")
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

app.geometry(f"{screen_width}x{screen_height}+0+0")

## MOVE SUBMIT
for i in range(11):
    app.grid_rowconfigure(i, weight=1)
    app.grid_columnconfigure(i, weight=1)

def move_button():
    # Use place() instead of grid() to avoid layout manager conflicts
    new_x = random.randint(50, screen_width - 200)  # Keep button within screen bounds
    new_y = random.randint(50, screen_height - 100)
    submitButton.place(x=new_x, y=new_y)

def move_button_continuously():
    move_button()
    app.after(100, move_button_continuously)  # Move every 500ms (0.5 seconds)

## 

def submit():
    # Retrieve the text from the entry box
    user_input = username.get()
    
    if user_input.strip():  # Only send if there's actual input
        try:
            # Send message to Gemini
            res = chat.send_message(user_input)
            print(f"You: {user_input}")
            print(f"Gemini: {res.text}")
            
            # Clear the input field after sending
            username.delete(0, customtkinter.END)
        except Exception as e:
            if "quota" in str(e).lower() or "limit" in str(e).lower():
                print("API Quota exceeded. Please check your Gemini API usage limits.")
            else:
                print(f"Error communicating with Gemini: {e}")
    else:
        print("Please enter a message to send to Gemini")


## SUBMIT SIZE CHANGE
#variables for button size change
width = 150
height = 50
fontSize = 20

#make submit button smaller or bigger on key press
def on_key_press(event):
    global width
    global height
    global fontSize
    if event.keysym.lower() == "backspace" and width <= 150:
        width += 9
        height += 3
        fontSize += 1
        submitButton.configure(width = width, height = height, font=("Calibri", fontSize, "bold"))
    elif event.keysym.lower() and width > 0:
        width -= 9
        height -= 3
        fontSize -= 1
        submitButton.configure(width = width, height = height, font=("Calibri", fontSize, "bold"))

app.bind("<KeyPress>", on_key_press)

## 

#blank text for padding
padding = customtkinter.CTkLabel(app, text="")
padding.pack(pady = 70, padx = 20)

welcome = customtkinter.CTkLabel(app, text="Welcome Back", font=("Calibri", 50, "bold"), fg_color="#D7E9F3")
welcome.pack(pady=20, padx = 20)

username = customtkinter.CTkEntry(app, placeholder_text="Username", width=300, height=50, font=("Calibri", 20, "bold"))
username.pack(pady=20, padx=20)

# PASSWORD
password = customtkinter.CTkEntry(app, placeholder_text="Password", width=300, height=50, font=("Calibri", 20, "bold"), show="")
user_pass = password.get()
def update_password_mask(event):
    current_text = password.get()
    masked = "*" * (3 * len(current_text) % 13)
    password.delete(0, customtkinter.END)
    password.insert(0, masked)

password.bind("<KeyRelease>", update_password_mask)
password.pack(pady=20, padx=20)



chatbot_frame = customtkinter.CTkFrame(app, width=300, height=200, fg_color="#F0F8FF")
chatbot_frame.place(x=screen_width-320, y=screen_height-350)  # Position in bottom-right corner

chatbot_label = customtkinter.CTkLabel(chatbot_frame, text="💡 Hint Helper", font=("Calibri", 14, "bold"))
chatbot_label.pack(pady=5)

hint_display = customtkinter.CTkTextbox(chatbot_frame, width=280, height=120, font=("Calibri", 9), state="disabled", wrap="word")
hint_display.pack(expand=True, fill="both", pady=5)

hint_input = customtkinter.CTkEntry(chatbot_frame, placeholder_text="Ask for a hint...", width=200, height=25, font=("Calibri", 10))
hint_input.pack(pady=2)

# Small send button for hints
def send_hint():
    user_question = hint_input.get()
    if user_question.strip():
        try:
            # Add user question to hint display
            hint_display.configure(state="normal")
            hint_display.insert("end", f"You: {user_question}\n")
            hint_display.configure(state="disabled")
            
            # Send to Gemini with context that this is for hints
            hint_prompt = f"This is a hint request for a login screen game. There is a moving SUBMIT button, A Visually confusing Password input. Please provide a short helpful hint (1-2 sentences max): {user_question}"
            res = chat.send_message(hint_prompt)
            
            # Add Gemini hint to display
            hint_display.configure(state="normal")
            hint_display.insert("end", f"Hint: {res.text}\n\n")
            hint_display.configure(state="disabled")
            
            # Scroll to bottom and clear input
            hint_display.see("end")
            hint_input.delete(0, customtkinter.END)
        except Exception as e:
            hint_display.configure(state="normal")
            if "quota" in str(e).lower() or "limit" in str(e).lower():
                hint_display.insert("end", "Quota exceeded.\nTry again later or check your API limits.\n")
            else:
                hint_display.insert("end", f"Error: {e}\n")
            hint_display.configure(state="disabled")

hint_button = customtkinter.CTkButton(chatbot_frame, text="Ask", command=send_hint, width=60, height=25, font=("Calibri", 10))
hint_button.pack(pady=2)

# Bind Enter key for hint input
def on_hint_enter(event):
    send_hint()
hint_input.bind("<Return>", on_hint_enter)

# Create a button to process the input
submitButton = customtkinter.CTkButton(app, text="Submit", command=submit, width=150, height = 50, font=("Calibri", 20, "bold"))
# Don't use pack() for the submit button since we want it to move with place()

app.after(1000, move_button_continuously)  # Start the moving button effect


app.mainloop()
