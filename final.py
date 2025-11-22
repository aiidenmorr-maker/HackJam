mport customtkinter
import PIL
import time 
import random
from google import genai
import subprocess

clickCount = 0

client = genai.Client(api_key="AIzaSyBKrdvBmQwb0oS9i0u5Pw1kPxQz6c2e6xQ")
chat = client.chats.create(model="gemini-2.5-flash")


# GUI
app = customtkinter.CTk()
app.title("Login Screen")
app.attributes("-fullscreen", True)

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

# Global variable to control button movement
move = True

def stop_button():
    global move
    move = False
    # Position button in a fixed, accessible location
    submitButton.place(x=200, y=400)

def move_button():
    # Use place() instead of grid() to avoid layout manager conflicts
    if move == True:
        new_x = random.randint(50, screen_width - 200)  # Keep button within screen bounds
        new_y = random.randint(50, screen_height - 100)
        submitButton.place(x=new_x, y=new_y)
    else:
        submitButton.place(x=200, y=400)  # Fixed position when stopped

def move_button_continuously():
    move_button()
    app.after(100, move_button_continuously)  # Move every 500ms (0.5 seconds)

## ASK BUTTON
def send_hint():
    user_question = hint_input.get()
    if user_question.strip():
        #stop_button()
        try:
            # Add user question to hint display
            hint_display.configure(state="normal")
            hint_display.insert("end", f"You: {user_question}\n")
            hint_display.configure(state="disabled")
            
            # Send to Gemini with context that this is for hints
            hint_prompt = f"This is a hint request for a login screen game.-There is a moving SUBMIT button, and a hidden button to stop it from moving. -A Visually confusing Password input, that is simply there for confusion. Please provide a short helpful hint (1-2 sentences max) ALSO PLEASE REMEMBER TO NOT DIRECTLY GIVE AWAY ANSWERS: {user_question}"
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

def on_hint_enter(event):
    send_hint()

## SUBMIT BUTTON

def submit():
    global clickCount
    if clickCount < 1:
        move_button()
    clickCount += 1
    if clickCount > 1:
        passAccepted.pack(pady = 10)
        if username.get() != "" and password.get() != "":
            passAccepted.configure(app, text="Password accepted!", font=("Calibri", 20, "bold"), fg_color="#FFFFFF", text_color = "#00BF00")
            open_captcha_window
        elif password.get() == "" and username.get() == "":
            passAccepted.configure(app, text="Please enter a username and password.", font=("Calibri", 20, "bold"), fg_color="#FFFFFF", text_color = "red")
            open_captcha_window
        elif username.get() == "":
            passAccepted.configure(app, text="Please enter a username.", font=("Calibri", 20, "bold"), fg_color="#FFFFFF", text_color = "red")
            open_captcha_window        
        else:
            passAccepted.configure(app, text="Please enter a password.", font=("Calibri", 20, "bold"), fg_color="#FFFFFF", text_color = "red")
            open_captcha_window()
    # app.destroy()
    open_captcha_window()



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
    if event.keysym.lower() == "backspace" and width <= 150 or event.keysym.lower():
        width += 9 
        height += 3
        fontSize += 1
        submitButton.configure(width = width%150, height = height%50, font=("Calibri", fontSize%20, "bold"))
    # elif event.keysym.lower() and width > 0:
    #     width -= 9
    #     height -= 3
    #     fontSize -= 1
    #     submitButton.configure(width = width%150, height = height%50, font=("Calibri", fontSize%20, "bold"))

app.bind("<KeyPress>", on_key_press)

## 

#blank text for padding
padding = customtkinter.CTkLabel(app, text="")
padding.pack(pady = 70, padx = 20)

welcome = customtkinter.CTkLabel(app, text="Welcome Back", font=("Calibri", 50, "bold"), fg_color="#D7E9F3")
welcome.pack(pady=20, padx = 20)

# Label for password acceptance messages
passAccepted = customtkinter.CTkLabel(app, text="", font=("Calibri", 20, "bold"))

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




## HINTS 

chatbot_frame = customtkinter.CTkFrame(app, width=300, height=200, fg_color="#F0F8FF")
chatbot_frame.place(x=screen_width-320, y=screen_height-350)  # Position in bottom-right corner

chatbot_label = customtkinter.CTkLabel(chatbot_frame, text="One STOP shop for Hints", font=("Calibri", 14, "bold"))
chatbot_label.pack(pady=5)

hint_display = customtkinter.CTkTextbox(chatbot_frame, width=280, height=120, font=("Calibri", 9), state="disabled", wrap="word")
hint_display.pack(expand=True, fill="both", pady=5)

hint_input = customtkinter.CTkEntry(chatbot_frame, placeholder_text="Ask for a hint...", width=200, height=25, font=("Calibri", 10))
hint_input.pack(pady=2)

hint_button = customtkinter.CTkButton(chatbot_frame, text="Ask", command=send_hint, width=60, height=25, font=("Calibri", 10))
hint_button.pack(pady=2)


hint_input.bind("<Return>", on_hint_enter)

## END HINTS 

# Create a button to process the input
submitButton = customtkinter.CTkButton(app, text="Submit", command=submit, width=150, height = 50, font=("Calibri", 20, "bold"))
# Don't use pack() for the submit button since we want it to move with place()
hiddenButton = customtkinter.CTkButton(app, text="Stop", command=stop_button, width=0, height=5, 
                                       fg_color="#F0F8FF",
                                       hover_color="#E0E8F0",
                                       border_width=0,
                                       text_color="black",
                                       font=("Calibri", 14, "bold"))

# Position it over the "STOP" part of "One STOPHint Helper"
hiddenButton.place(x=screen_width-235, y=screen_height-343)

app.after(1000, move_button_continuously)  # Start the moving button effect

## CAPTCHA WINDOW FUNCTION
def open_captcha_window():
    captcha_app = customtkinter.CTk()
    captcha_app.title("CAPTCHA")
    captcha_app.geometry("600x600")
    customtkinter.set_appearance_mode("Light")

    header = customtkinter.CTkLabel(captcha_app, text="Please write a 300 word response \nabout why you are not a robot.", font=("Calibri", 30, "bold"))
    header.pack(pady=10, padx=20)

    essay = customtkinter.CTkTextbox(captcha_app, width=450, height=350, font=("Calibri", 20, "bold"))
    essay.pack(pady=5, padx=20)

    def captcha_submit():
        essayResponse = essay.get("1.0", "end-1c")
        essay2 = essayResponse.split()
        if len(essay2) >= 300:
            print("essay is long enough")
            validation.configure(text="Reviewing your response", font=("Calibri", 20, "bold"))
            
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=(f"In one word, yes or no, does this essay discuss being human?: {essayResponse}")
                )
                
                print(response.text)
                if "yes" in response.text.lower():
                    validation.configure(text="Our AI has deemed your essay worthy.", font=("Calibri", 20, "bold"))
                    captcha_app.after(3000, captcha_app.destroy)
                else:
                    validation.configure(text="Our AI has deemed your essay unworthy. Try again.", font=("Calibri", 20, "bold"))
            except Exception as e:
                validation.configure(text="Error processing essay. Try again.", font=("Calibri", 20, "bold"))
        else:
            validation.configure(text="Your essay is not long enough", font=("Calibri", 20, "bold"))

    validation = customtkinter.CTkLabel(captcha_app, text="", font=("Calibri", 20, "bold"))
    validation.pack(pady=10)

    captcha_submit_button = customtkinter.CTkButton(captcha_app, text="Submit", command=captcha_submit, width=200, height=75, font=("Calibri", 20, "bold"))
    captcha_submit_button.pack(pady=5)

    def on_close():
        pass
    
    captcha_app.protocol("WM_DELETE_WINDOW", on_close)
    captcha_app.mainloop()

app.mainloop()
