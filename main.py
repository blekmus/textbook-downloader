from src.app import App
from src.state import State
import shutil
import os


if __name__ == "__main__":
    # initialize state
    state = State()

    # if working dir exists from previous run, delete it
    if os.path.exists(state.workingPath):
        shutil.rmtree(state.workingPath)

    # initialize app
    app = App(state)

    # render app
    app.mainloop()

    # url
    # https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/01%3A_The_Dawn_of_the_Quantum_Theory/1.01%3A_Blackbody_Radiation_Cannot_Be_Explained_Classically
