import pyautogui
import time
import threading
import tkinter as tk
from tkinter import ttk
import os

# Define the default interval (in seconds)
DEFAULT_INTERVAL = 10
# Default number of desktops
DEFAULT_DESKTOPS = 1

class DesktopSwitcherApp:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.current_desktop = 1
        self.interval = DEFAULT_INTERVAL
        self.total_desktops = DEFAULT_DESKTOPS
        self.thread = None
        
        # Configure the window
        self.root.title("KIB - Virtual Desktop Switcher")
        self.root.geometry("400x320")
        self.root.resizable(True, True)
        
        # Set custom theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TButton', font=('Arial', 10, 'bold'), background='#007bff', foreground='white')
        self.style.map('TButton', background=[('active', '#0069d9')])
        self.style.configure('TLabel', font=('Arial', 10), background='#f5f5f5')
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'), background='#f5f5f5')
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # App title
        header_label = ttk.Label(main_frame, text="Virtual Desktop Switcher", style='Header.TLabel')
        header_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.status_label = ttk.Label(status_frame, text="Status: Stopped", font=('Arial', 10))
        self.status_label.pack(side=tk.LEFT)
        
        self.status_indicator = tk.Canvas(status_frame, width=15, height=15, bg="#f5f5f5", highlightthickness=0)
        self.status_indicator.pack(side=tk.RIGHT)
        self.status_indicator.create_oval(2, 2, 13, 13, fill="red", outline="")
        
        # Desktop configuration frame
        desktop_frame = ttk.Frame(main_frame)
        desktop_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(desktop_frame, text="Number of Virtual Desktops:", font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.desktop_var = tk.StringVar(value=str(DEFAULT_DESKTOPS))
        desktop_spinbox = ttk.Spinbox(desktop_frame, from_=2, to=10, width=5, textvariable=self.desktop_var)
        desktop_spinbox.pack(side=tk.RIGHT)
        
        # Interval selection frame
        interval_frame = ttk.Frame(main_frame)
        interval_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(interval_frame, text="Switch Interval (seconds):", font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.interval_var = tk.StringVar(value=str(DEFAULT_INTERVAL))
        interval_spinbox = ttk.Spinbox(interval_frame, from_=1, to=60, width=5, textvariable=self.interval_var)
        interval_spinbox.pack(side=tk.RIGHT)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create and style buttons
        self.start_button = ttk.Button(buttons_frame, text="Start Switching", command=self.start_switching)
        self.start_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.stop_button = ttk.Button(buttons_frame, text="Stop", command=self.stop_switching, state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(footer_frame, text="Current Desktop: ", font=('Arial', 9)).pack(side=tk.LEFT)
        self.desktop_label = ttk.Label(footer_frame, text="1", font=('Arial', 9, 'bold'))
        self.desktop_label.pack(side=tk.LEFT)
        
        # Instructions
        instructions = "This app automatically cycles through all virtual desktops (1 → 2 → 3 → ... → n → 1). Set the number of desktops and the switching interval, then press Start."
        ttk.Label(main_frame, text=instructions, font=('Arial', 8), wraplength=360).pack(pady=(10, 0))
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("desktop_icon.ico")
        except:
            pass  # Icon file not found, continue without it
    
    def switch_to_next_desktop(self):
        pyautogui.hotkey('ctrl', 'win', 'right')
    
    def switch_to_desktop_1(self):
        """Switch back to desktop 1 by using left arrow key multiple times"""
        # Calculate how many times to press left to go back to desktop 1
        # from the last desktop
        presses = self.total_desktops - 1
        
        # Press left multiple times
        for _ in range(presses):
            pyautogui.hotkey('ctrl', 'win', 'left')
            time.sleep(0.2)  # Small delay to ensure keystrokes are registered
    
    def update_ui(self, is_running):
        if is_running:
            self.status_label.config(text="Status: Running")
            self.status_indicator.create_oval(2, 2, 13, 13, fill="green", outline="")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.desktop_var.set(str(self.total_desktops))  # Lock in the value
        else:
            self.status_label.config(text="Status: Stopped")
            self.status_indicator.create_oval(2, 2, 13, 13, fill="red", outline="")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def start_switching(self):
        # Parse and validate inputs
        try:
            self.interval = int(self.interval_var.get())
            if self.interval < 1:
                self.interval = 1
                self.interval_var.set("1")
        except ValueError:
            self.interval = DEFAULT_INTERVAL
            self.interval_var.set(str(DEFAULT_INTERVAL))
            
        try:
            self.total_desktops = int(self.desktop_var.get())
            if self.total_desktops < 2:
                self.total_desktops = 2
                self.desktop_var.set("2")
        except ValueError:
            self.total_desktops = DEFAULT_DESKTOPS
            self.desktop_var.set(str(DEFAULT_DESKTOPS))
        
        self.running = True
        self.update_ui(True)
        
        # Start switching in a separate thread
        self.thread = threading.Thread(target=self.cycling_loop)
        self.thread.daemon = True
        self.thread.start()
    
    def cycling_loop(self):
        """Cycle through all desktops in sequence: 1 -> 2 -> 3 -> ... -> n -> 1"""
        self.current_desktop = 1  # Start from desktop 1
        
        # Update the desktop label
        self.root.after(0, lambda: self.desktop_label.config(text=str(self.current_desktop)))
        
        while self.running:
            # Check if we're at the last desktop
            if self.current_desktop == self.total_desktops:
                # We're at the last desktop, go back to desktop 1
                self.switch_to_desktop_1()
                self.current_desktop = 1
            else:
                # Move to next desktop
                self.switch_to_next_desktop()
                self.current_desktop += 1
            
            # Update the desktop label
            self.root.after(0, lambda: self.desktop_label.config(text=str(self.current_desktop)))
            
            time.sleep(self.interval)
    
    def stop_switching(self):
        self.running = False
        self.update_ui(False)

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopSwitcherApp(root)
    root.mainloop()
