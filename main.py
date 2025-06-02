# main.py
# This is the main entry point for the UART Terminal Application.

import tkinter as tk
import gui # Import the gui module where UartTerminalGUI is defined

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()

    # Instantiate the UartTerminalGUI class from the gui module
    # The UartTerminalGUI class itself will handle its title, geometry, etc.
    app = gui.UartTerminalGUI(root)

    # Start the Tkinter event loop
    root.mainloop()
