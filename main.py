"""
Main application 
"""
import customtkinter as ctk
from db import init_db
from ui.login_ui import LoginWindow
from ui.books_ui import BooksWindow
from ui.members_ui import MembersWindow
from ui.borrow_ui import BorrowWindow

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Manager")
        self.geometry("700x420")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        init_db()  # ensure DB/tables exist

        ctk.CTkLabel(self, text="📚 Library Manager", font=("Arial", 20, "bold")).pack(pady=20)

        btn_frame = ctk.CTkFrame(self); btn_frame.pack(pady=10, padx=30, fill="x")
        ctk.CTkButton(btn_frame, text="🔐 Login / Register", command=self.open_login).pack(fill="x", pady=6)
        ctk.CTkButton(btn_frame, text="📚 Manage Books", command=self.open_books).pack(fill="x", pady=6)
        ctk.CTkButton(btn_frame, text="👥 Manage Members", command=self.open_members).pack(fill="x", pady=6)
        ctk.CTkButton(btn_frame, text="📖 Borrow / Return", command=self.open_borrow).pack(fill="x", pady=6)
        ctk.CTkButton(btn_frame, text="❌ Quit", command=self.quit).pack(fill="x", pady=12)

    def open_login(self):
        LoginWindow(self, on_success=self.on_login_success)

    def on_login_success(self, user_id, username):
        # currently we do nothing special, but you can store current user if needed
        print(f"Logged in: {username} (id={user_id})")

    def open_books(self):
        BooksWindow(self)

    def open_members(self):
        MembersWindow(self)

    def open_borrow(self):
        BorrowWindow(self)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
