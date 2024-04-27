from src.ui import App
from src.state import State

# # state
# # path to selenium driver
# # path to save downloaded html

# # flow
# # first checks if the driver path is set, if not, the driver path in the GUI is set to dowload or change the driver path
# # then checks if the download path is set, if not, asks for the download path

# # both of the above are displayed in the GUI with buttons to change it
# # after a seperator is an input field to enter the url
# # and a button to download the webpage

# # after the download, a success message is displayed.

#     # # select output folder input button
#     # # input for the link

#     # # button to run the script
#     # # is output folder set?
#     # # is input link set?
#     # # also have a warning

if __name__ == "__main__":
    # initialize state
    state = State()

    # initialize app
    app = App(state)

    # render app
    app.mainloop()
