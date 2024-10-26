from tkinter import *
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# root = Tk()
root = customtkinter.CTk()

root.title('Ransom? Note ')
# root.iconbitmap('images/codemy.ico')
root.geometry('600x400')


def input_window():
    # create a new toplevel window
    input_window = customtkinter.CTkToplevel(root)
    input_window.geometry("300x150")
    input_window.title("Hello Victim!")

    # create a label and an entry field
    input_label = customtkinter.CTkLabel(input_window, text="What is your name?")
    input_label.pack(pady=10)

    input_entry = customtkinter.CTkEntry(input_window)
    input_entry.pack(pady=10)

    def process_input():
        user_input = input_entry.get()
        if user_input:
            my_label.configure(text = f"Your input: \"{user_input}\" \n If everything is in order, you will hear from us soon")
            my_button.destroy()
        else:
            my_label.configure(text=f"You have to input something")
        input_window.destroy()

    def close_window():
        input_window.destroy()

    # Create a frame to hold the buttons
    button_frame = customtkinter.CTkFrame(input_window)
    button_frame.pack(pady=10)

    # Create the Submit and Close buttons inside the frame, side by side
    submit_button = customtkinter.CTkButton(button_frame, text="Submit", command=process_input)
    submit_button.pack(side=LEFT, padx=5)

    close_button = customtkinter.CTkButton(button_frame, text="Close", command=close_window)
    close_button.pack(side=LEFT, padx=5)


# create a label
my_label = customtkinter.CTkLabel(root, text= 'All of your files are encrypted <^.^> \n Pay us the ransom if you want your files back')
my_label.pack(pady = 2)

# create a button
my_button = customtkinter.CTkButton(root, text="Pay up!", command=input_window)
my_button.pack(pady = 150)


root.mainloop()
