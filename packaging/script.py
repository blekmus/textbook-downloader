# implement a datastore to save state

# state
# path to selenium driver
# path to save downloaded html

# flow
# first checks if the driver path is set, if not, the driver path in the GUI is set to dowload or change the driver path
# then checks if the download path is set, if not, asks for the download path

# both of the above are displayed in the GUI with buttons to change it
# after a seperator is an input field to enter the url
# and a button to download the webpage

# after the download, a success message is displayed.




import customtkinter
from tkinter.filedialog import askopenfilename

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
# customtkinter.set_default_color_theme(
#     "blue"
# )  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1000x500")    

def button_function():
    filename = (
        askopenfilename()
    )  # show an "Open" dialog box and return the path to the selected file
    print(filename)

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

app.mainloop()
