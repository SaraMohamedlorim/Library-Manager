# ui/borrow_ui.py
import customtkinter as ctk
from tkinter import messagebox, ttk
from members import fetch_all_members
from books import fetch_all_books, get_book
from borrow import borrow_book, return_borrowing, get_member_borrowings, get_all_borrowings

class BorrowWindow(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Borrow / Return")
        self.geometry("1000x600")

        top = ctk.CTkFrame(self); top.pack(fill="x", padx=10, pady=6)
        ctk.CTkLabel(top, text="Borrow / Return Books", font=("Arial", 16, "bold")).pack(side="left")

        # pick member and book
        form = ctk.CTkFrame(self); form.pack(fill="x", padx=10, pady=6)
        members = fetch_all_members()
        members_vals = [f"{m[0]} | {m[1]}" for m in members] or ["No Members"]
        self.member_menu = ctk.CTkOptionMenu(form, values=members_vals, width=360); self.member_menu.grid(row=0,column=0,padx=6)
        books = fetch_all_books()
        books_vals = [f"{b[0]} | {b[1]}" for b in books] or ["No Books"]
        self.book_menu = ctk.CTkOptionMenu(form, values=books_vals, width=360); self.book_menu.grid(row=0,column=1,padx=6)
        ctk.CTkButton(form, text="Borrow", command=self.borrow_action).grid(row=0,column=2,padx=6)
        ctk.CTkButton(form, text="Show All Borrowings", command=self.load_all_borrowings).grid(row=0,column=3,padx=6)

        # borrowed list
        cols = ("BorrowID","Member","Book","Borrowed","Due","Returned","ReturnDate")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=8)

        btn_frame = ctk.CTkFrame(self); btn_frame.pack(fill="x", padx=10, pady=6)
        ctk.CTkButton(btn_frame, text="Return Selected", command=self.return_selected).pack(side="left", padx=8)
        ctk.CTkButton(btn_frame, text="Refresh", command=self.load_all_borrowings).pack(side="left", padx=8)

        self.load_all_borrowings()

    def borrow_action(self):
        member = self.member_menu.get()
        book = self.book_menu.get()
        if "No Members" in member or "No Books" in book:
            messagebox.showwarning("Warning","Select valid member and book"); return
        member_id = int(member.split(" | ")[0]); book_id = int(book.split(" | ")[0])
        # ensure book exists
        if not get_book(book_id):
            messagebox.showerror("Error","Book not found"); return
        ok = borrow_book(member_id, book_id)
        if ok:
            messagebox.showinfo("Success","Book borrowed"); self.load_all_borrowings()
        else:
            messagebox.showerror("Error","Cannot borrow book")

    def load_all_borrowings(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        rows = get_all_borrowings()
        for r in rows:
            # (id, member_name, book_title, borrow_date, due_date, returned, return_date)
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], "Yes" if r[5] else "No", r[6] or ""))

    def return_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning","Select borrowing record"); return
        bid = int(self.tree.item(sel[0])['values'][0])
        ok = return_borrowing(bid)
        if ok:
            messagebox.showinfo("Success","Marked as returned"); self.load_all_borrowings()
        else:
            messagebox.showerror("Error","Could not return (maybe already returned)")
