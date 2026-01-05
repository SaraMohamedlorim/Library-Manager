# ui/register_ui.py
import customtkinter as ctk
from tkinter import messagebox
from auth import create_user

class RegisterWindow(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Register")
        self.geometry("360x240")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Create Account", font=("Arial", 14, "bold")).pack(pady=8)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=6, padx=20)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=6, padx=20)
        self.password_confirm = ctk.CTkEntry(self, placeholder_text="Confirm Password", show="*")
        self.password_confirm.pack(pady=6, padx=20)

        ctk.CTkButton(self, text="Register", command=self.register).pack(pady=10)

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.password_confirm.get().strip()
        if not username:
            messagebox.showwarning("Warning","Username required"); return
        if password != confirm:
            messagebox.showerror("Error","Passwords do not match"); return
        ok = create_user(username, password)
        if ok:
            messagebox.showinfo("Success","Account created")
            self.destroy()
        else:
            messagebox.showerror("Error","Username already exists")
