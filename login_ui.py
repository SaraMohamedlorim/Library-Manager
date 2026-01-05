# ui/login_ui.py
# ui/login_ui.py
import customtkinter as ctk
from tkinter import messagebox
from auth import authenticate_user
from ui.register_ui import RegisterWindow
from ui.change_pass_ui import ChangePasswordWindow

class LoginWindow(ctk.CTkToplevel):
    """
    Modal login window. on_success is a callback: on_success(user_id, username)
    """
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.title("Login")
        self.geometry("380x240")
        self.resizable(False, False)
        self.on_success = on_success

        ctk.CTkLabel(self, text="Library Manager", font=("Arial", 16, "bold")).pack(pady=8)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=6, padx=20)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=6, padx=20)

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Login", command=self.login).grid(row=0, column=0, padx=8)
        ctk.CTkButton(btn_frame, text="Register", command=self.open_register).grid(row=0, column=1, padx=8)
        ctk.CTkButton(btn_frame, text="Change Password", command=self.open_change_password).grid(row=0, column=2, padx=8)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username:
            messagebox.showwarning("Warning","Enter username"); return
        uid = authenticate_user(username, password)
        if uid:
            messagebox.showinfo("Welcome", f"Logged in as {username}")
            self.destroy()
            if self.on_success:
                self.on_success(uid, username)
        else:
            messagebox.showerror("Error","Invalid username or password")

    def open_register(self):
        RegisterWindow(self)

    def open_change_password(self):
        ChangePasswordWindow(self)
