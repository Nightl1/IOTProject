import test_oop
import tkinter as tk
from tkinter import ttk

class WasteManagementGUI:
    interact = test_oop.interactions()
    
    def __init__(self, master):
        self.master = master
        master.title("Smart Waste Management System")
        percentage = 0

        # Create label and disabled text field for waste level
        self.waste_level_label = ttk.Label(master, text="Waste Level:")
        self.waste_level_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.waste_level_text = ttk.Entry(master)
        self.waste_level_text.insert(1, '0%')
        self.waste_level_text.config(state="disabled")
        self.waste_level_text.grid(row=0, column=1, padx=5, pady=5)

        # Create label, text field, and button for setting level
        self.set_level_label = ttk.Label(master, text="Set Level:")
        self.set_level_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.set_level_text = ttk.Entry(master)
        self.set_level_text.grid(row=1, column=1, padx=5, pady=5)
        self.set_level_button = ttk.Button(master, text="Set", command=self.set_level)
        self.set_level_button.grid(row=1, column=2, padx=5, pady=5)

        # Create label for status
        self.status_label = ttk.Label(master, text="Garbage is not full", foreground="green")
        self.status_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        
        # Create the unothorized entry label. By default, there is no text so it is "invisible"
        self.unothorized_label = ttk.Label(master, text="", foreground="red")
        self.unothorized_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        
        # initializing the act method
        self.act()
        
    def act(self):
        # Call the act method of the interactions instance
        self.interact.act()
        self.percentage = self.interact.get_percentage()
        max_waste_level = int(self.waste_level_text.get()[:-1])
        
        if self.percentage > max_waste_level:
            self.status_label.config(text='Garbage is full', foreground="red")
        else:
            self.status_label.config(text='Garbage is not full', foreground="green")
            
        if self.interact.get_authorization():
            self.unothorized_label.config(text="UNOTHORIZED ENTRY!")
        else:
            self.unothorized_label.config(text="")
            
            # Schedule the next call after 500 ms
        self.master.after(10, self.act)

    def set_level(self):
        try:
            level = int(self.set_level_text.get())
            self.waste_level_text.config(state="normal")
            self.waste_level_text.delete(0, tk.END)
            self.waste_level_text.insert(0, str(level) + "%")
            self.waste_level_text.config(state="disabled")
        except ValueError:
            pass

root = tk.Tk()
waste_management_gui = WasteManagementGUI(root)
root.mainloop()