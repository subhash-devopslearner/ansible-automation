import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import os

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.expanduser("~/ansible-automation")
PLAYBOOK = os.path.join(BASE_DIR, "playbook/windows/17-send-message-to-users.yml")
INVENTORY = os.path.join(BASE_DIR, "inventory/lab1-windows-inventory.yml")
ANSIBLE_BIN = os.path.join(BASE_DIR, "venv", "bin", "ansible-playbook")

DEFAULT_MSG = "*** LAB ALERT ***\nPlease focus on your lab work. No games or non-educational activities.\n\nThank you."

class LabMessengerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab Monitor Pro - Exact Grid")
        self.root.geometry("1100x820")
        self.selected_systems = set()
        self.system_buttons = {}

        # DATA MAPPED DIRECTLY FROM YOUR IMAGE
        self.layout_data = [
            ["CC1-1", "CC1-3", "CC1-5", "CC1-7", "CC1-9", "CC1-11", "CC1-13", "CC1-15", "CC1-17"], # Col 1
            ["CC1-2", "CC1-4", "CC1-6", "CC1-8", "CC1-10", "CC1-12", "CC1-14", "CC1-16", "CC1-18"], # Col 2
            ["", "CC1-19", "CC1-22", "CC1-25", "CC1-28", "CC1-31", "CC1-34", "CC1-37", "CC1-40"], # Col 3
            ["", "CC1-20", "CC1-23", "CC1-26", "CC1-29", "CC1-32", "CC1-35", "CC1-38", "CC1-41"], # Col 4
            ["", "CC1-21", "CC1-24", "CC1-27", "CC1-30", "CC1-33", "CC1-36", "CC1-39", "CC1-42"], # Col 5
            ["CC1-43", "CC1-45", "CC1-47", "CC1-49", "CC1-51", "CC1-53", "CC1-55", "CC1-57", "CC1-59"], # Col 6
            ["CC1-44", "CC1-46", "CC1-48", "CC1-50", "CC1-52", "CC1-54", "CC1-56", "CC1-58", "CC1-60"]  # Col 7
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

        grid_frame = tk.LabelFrame(grid_container, text=" Lab System Layout ", 
                                   padx=15, pady=15, font=("Arial", 11, "bold"))
        grid_frame.pack(expand=True)

        for col_idx, col_list in enumerate(self.layout_data):
            col_frame = tk.Frame(grid_frame)
            col_frame.pack(side="left", padx=10, anchor="n")
            
            for sys_name in col_list:
                if sys_name == "":
                    tk.Label(col_frame, text="", width=10, height=2).pack(pady=2)
                else:
                    # FIX: activebackground set to white to match unselected state initially
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
            # Reset to White unselected state
            btn.config(bg="white", fg="black", 
                       activebackground="white", activeforeground="black")
        else:
            self.selected_systems.add(sys_name)
            # Set to Blue selected state
            btn.config(bg="#3498db", fg="white", 
                       activebackground="#3498db", activeforeground="white")

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
