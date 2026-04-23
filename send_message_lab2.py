import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import os

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.expanduser("~/ansible-automation")
PLAYBOOK = os.path.join(BASE_DIR, "playbook/windows/17-send-message-to-users.yml")
INVENTORY = os.path.join(BASE_DIR, "inventory/lab2-windows-inventory.yml")
ANSIBLE_BIN = os.path.join(BASE_DIR, "venv", "bin", "ansible-playbook")

DEFAULT_MSG = "*** LAB ALERT ***\nPlease focus on your lab work. No games or non-educational activities.\n\nThank you."

class LabMessengerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab Monitor Pro - PL1 Grid")
        self.root.geometry("1100x700") # Adjusted for 5-row layout
        self.selected_systems = set()
        self.system_buttons = {}

        # DATA MAPPED DIRECTLY FROM YOUR NEW IMAGE (5 Rows, 7 Columns)
        self.layout_data = [
            ["PL1-1", "PL1-3", "PL1-5", "PL1-7", "PL1-9"],             # Col 1
            ["PL1-2", "PL1-4", "PL1-6", "PL1-8", "PL1-10"],            # Col 2
            ["", "PL1-11", "PL1-14", "PL1-17", "PL1-20"],             # Col 3
            ["", "PL1-12", "PL1-15", "PL1-18", "PL1-21"],             # Col 4
            ["", "PL1-13", "PL1-16", "PL1-19", "PL1-22"],             # Col 5
            ["PL1-23", "PL1-25", "PL1-27", "PL1-29", "PL1-31"],        # Col 6
            ["PL1-24", "PL1-26", "PL1-28", "PL1-30", "PL1-32"]         # Col 7
        ]
        
        self.setup_ui()

    def setup_ui(self):
        # --- TOP ACTION BAR ---
        action_frame = tk.Frame(self.root, bg="#1a5276", pady=12)
        action_frame.pack(fill="x")

        self.send_btn = tk.Button(
            action_frame, text="🚀 SEND MESSAGE TO SELECTED", command=self.run_ansible,
            bg="#27ae60", fg="white", font=("Arial", 11, "bold"), 
            padx=20, pady=8, relief="raised", cursor="hand2"
        )
        self.send_btn.pack()

        # Selection Utils
        util_frame = tk.Frame(self.root, pady=8)
        util_frame.pack(fill="x")
        
        btn_container = tk.Frame(util_frame)
        btn_container.pack()
        tk.Button(btn_container, text="SELECT ALL", font=("Arial", 9, "bold"), 
                  command=self.select_all, width=15, bg="#ecf0f1").pack(side="left", padx=5)
        tk.Button(btn_container, text="CLEAR SELECTION", font=("Arial", 9, "bold"), 
                  command=self.clear_all, width=15, bg="#ecf0f1").pack(side="left", padx=5)

        # --- LAB GRID (CENTERED) ---
        grid_container = tk.Frame(self.root, padx=20, pady=10)
        grid_container.pack(fill="both", expand=True)

        grid_frame = tk.LabelFrame(grid_container, text=" Lab System Layout (PL1) ", 
                                   padx=15, pady=15, font=("Arial", 11, "bold"))
        grid_frame.pack(expand=True)

        for col_idx, col_list in enumerate(self.layout_data):
            col_frame = tk.Frame(grid_frame)
            col_frame.pack(side="left", padx=10, anchor="n")
            
            for sys_name in col_list:
                if sys_name == "":
                    # Spacer for Row 1 in middle columns
                    tk.Label(col_frame, text="", width=10, height=2).pack(pady=2)
                else:
                    btn = tk.Button(
                        col_frame, text=sys_name, width=10, height=2, 
                        bg="white", fg="black",
                        activebackground="white", activeforeground="black",
                        font=("Arial", 9, "bold"), relief="groove",
                        command=lambda s=sys_name: self.toggle_system(s)
                    )
                    btn.pack(pady=2)
                    self.system_buttons[sys_name] = btn

        # --- MESSAGE AREA (BOTTOM) ---
        msg_frame = tk.Frame(self.root, padx=60, pady=15)
        msg_frame.pack(fill="x", side="bottom")
        
        tk.Label(msg_frame, text="Message Body (Max 255 chars):", font=("Arial", 10, "bold")).pack(anchor="w")
        self.msg_input = scrolledtext.ScrolledText(msg_frame, height=4, font=("Arial", 11), bd=2)
        self.msg_input.pack(fill="x", pady=5)
        self.msg_input.insert(tk.END, DEFAULT_MSG)
        
        self.count_label = tk.Label(msg_frame, text="Chars: 0/255", font=("Arial", 9))
        self.count_label.pack(anchor="e")
        self.msg_input.bind("<KeyRelease>", self.update_counter)
        self.update_counter()

    def update_counter(self, event=None):
        content = self.msg_input.get("1.0", tk.END).strip()
        count = len(content)
        self.count_label.config(text=f"Chars: {count}/255", fg="black" if count <= 255 else "red")

    def toggle_system(self, sys_name):
        btn = self.system_buttons[sys_name]
        if sys_name in self.selected_systems:
            self.selected_systems.remove(sys_name)
            btn.config(bg="white", fg="black", activebackground="white", activeforeground="black")
        else:
            self.selected_systems.add(sys_name)
            btn.config(bg="#3498db", fg="white", activebackground="#3498db", activeforeground="white")

    def select_all(self):
        for sys_name in self.system_buttons:
            if sys_name not in self.selected_systems:
                self.toggle_system(sys_name)

    def clear_all(self):
        for sys_name in list(self.selected_systems):
            self.toggle_system(sys_name)

    def run_ansible(self):
        if not self.selected_systems:
            messagebox.showwarning("Empty", "Select systems first.")
            return

        msg = self.msg_input.get("1.0", tk.END).strip()
        if len(msg) > 255:
            messagebox.showerror("Error", f"Message is {len(msg)} chars. Limit is 255.")
            return

        target_str = ",".join(self.selected_systems).lower()
        self.send_btn.config(state=tk.DISABLED, text="⌛ SENDING...")
        self.root.update_idletasks()
        
        env = os.environ.copy()
        env["LANG"] = "en_US.UTF-8"
        env["LC_ALL"] = "en_US.UTF-8"

        cmd = [ANSIBLE_BIN, "-i", INVENTORY, PLAYBOOK, "--extra-vars", f"target_host='{target_str}' custom_msg='{msg}'"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR, env=env)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Sent to {len(self.selected_systems)} systems.")
            else:
                messagebox.showerror("Ansible Error", result.stderr or result.stdout)
        except Exception as e:
            messagebox.showerror("System Error", str(e))
        finally:
            self.send_btn.config(state=tk.NORMAL, text="🚀 SEND MESSAGE TO SELECTED")

if __name__ == "__main__":
    root = tk.Tk()
    app = LabMessengerApp(root)
    root.mainloop()
