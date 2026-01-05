# ui/change_password_ui.py
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from auth import authenticate_user, change_user_password

class ChangePasswordWindow(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Change Password")
        self.geometry("360x240")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Change Password", font=("Arial", 14, "bold")).pack(pady=8)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=6, padx=20)
        self.old_password_entry = ctk.CTkEntry(self, placeholder_text="Current Password", show="*")
        self.old_password_entry.pack(pady=6, padx=20)
        self.new_password_entry = ctk.CTkEntry(self, placeholder_text="New Password", show="*")
        self.new_password_entry.pack(pady=6, padx=20)

        ctk.CTkButton(self, text="Change", command=self.change).pack(pady=10)

    def change(self):
        username = self.username_entry.get().strip()
        old = self.old_password_entry.get().strip()
        new = self.new_password_entry.get().strip()
        if not username or not old or not new:
            messagebox.showwarning("Warning","All fields required"); return
        uid = authenticate_user(username, old)
        if uid is None:
            messagebox.showerror("Error","Current credentials invalid"); return
        ok = change_user_password(username, new)
        if ok:
            messagebox.showinfo("Success","Password changed"); self.destroy()
        else:
            messagebox.showerror("Error","Failed to change password")
