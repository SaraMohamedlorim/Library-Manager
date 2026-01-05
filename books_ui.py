
# ui/books_ui.py
import customtkinter as ctk
from tkinter import messagebox, ttk
from books import add_book, fetch_all_books, update_book, delete_book, search_books

class BooksWindow(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Manage Books")
        self.geometry("1000x600")

        top_frame = ctk.CTkFrame(self); top_frame.pack(fill="x", padx=10, pady=8)
        ctk.CTkLabel(top_frame, text="Books Catalog", font=("Arial", 16, "bold")).pack(side="left")

        # Form
        form = ctk.CTkFrame(self); form.pack(fill="x", padx=10, pady=6)
        self.title_entry = ctk.CTkEntry(form, placeholder_text="Title", width=300); self.title_entry.grid(row=0, column=0, padx=6, pady=6)
        self.author_entry = ctk.CTkEntry(form, placeholder_text="Author", width=220); self.author_entry.grid(row=0, column=1, padx=6, pady=6)
        self.status_menu = ctk.CTkOptionMenu(form, values=["available","checked_out"], dynamic_resizing=False); self.status_menu.grid(row=0,column=2,padx=6)
        self.status_menu.set("available")
        self.rating_entry = ctk.CTkEntry(form, placeholder_text="Rating (1-5)", width=100); self.rating_entry.grid(row=0,column=3,padx=6)
        self.notes_entry = ctk.CTkEntry(form, placeholder_text="Short notes", width=300); self.notes_entry.grid(row=0,column=4,padx=6)

        ctk.CTkButton(form, text="Add Book", command=self.add_book_action).grid(row=0, column=5, padx=6)

        # Search
        search_frame = ctk.CTkFrame(self); search_frame.pack(fill="x", padx=10, pady=6)
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search by title/author...", width=420); self.search_entry.grid(row=0,column=0,padx=6)
        ctk.CTkButton(search_frame, text="Search", command=self.search_action).grid(row=0,column=1,padx=6)
        ctk.CTkButton(search_frame, text="Refresh", command=self.load_books).grid(row=0,column=2,padx=6)

        # Treeview
        cols = ("ID","Title","Author","Status","Rating","Notes","Added")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            if c=="Title": self.tree.column(c, width=320, anchor="w")
            elif c=="Notes": self.tree.column(c, width=220, anchor="w")
            elif c=="Author": self.tree.column(c, width=180, anchor="w")
            else: self.tree.column(c, width=90, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=6)
        self.tree.bind("<Double-1>", lambda e: self.open_edit_window())

        # Buttons
        btn_frame = ctk.CTkFrame(self); btn_frame.pack(fill="x", padx=10, pady=6)
        ctk.CTkButton(btn_frame, text="Edit Selected", command=self.open_edit_window).pack(side="left", padx=8)
        ctk.CTkButton(btn_frame, text="Delete Selected", fg_color="red", command=self.delete_selected).pack(side="left", padx=8)

        self.load_books()

    def load_books(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        rows = fetch_all_books(order_by="added_date")
        for r in rows:
            self.tree.insert("", "end", values=r)

    def add_book_action(self):
        title = self.title_entry.get().strip(); author = self.author_entry.get().strip()
        status = self.status_menu.get(); rating_raw = self.rating_entry.get().strip(); notes = self.notes_entry.get().strip()
        rating = None
        if rating_raw:
            try:
                rr = int(rating_raw)
                if 1 <= rr <= 5: rating = rr
                else: messagebox.showwarning("Rating","Rating must be 1-5"); return
            except:
                messagebox.showwarning("Rating","Invalid rating"); return
        if not title or not author:
            messagebox.showwarning("Warning","Title and Author required"); return
        add_book(title, author, status, rating, notes)
        messagebox.showinfo("Success","Book added")
        self.title_entry.delete(0,"end"); self.author_entry.delete(0,"end"); self.rating_entry.delete(0,"end"); self.notes_entry.delete(0,"end")
        self.status_menu.set("available"); self.load_books()

    def selected_item(self):
        sel = self.tree.selection()
        if not sel: return None
        return self.tree.item(sel[0])['values']

    def open_edit_window(self):
        sel = self.selected_item()
        if not sel:
            messagebox.showwarning("Warning","Select a book"); return
        # simple edit dialog using simpledialog sequence
        EditBookDialog(self, sel, self.load_books)

    def delete_selected(self):
        sel = self.selected_item()
        if not sel:
            messagebox.showwarning("Warning","Select a book"); return
        if not messagebox.askyesno("Confirm","Delete selected book?"): return
        book_id = sel[0]
        delete_book(book_id)
        messagebox.showinfo("Deleted","Book deleted")
        self.load_books()

    def search_action(self):
        kw = self.search_entry.get().strip()
        if not kw:
            self.load_books(); return
        rows = search_books(kw)
        for r in self.tree.get_children(): self.tree.delete(r)
        for r in rows: self.tree.insert("", "end", values=r)

# Small Edit dialog class
from tkinter import simpledialog
class EditBookDialog(simpledialog.Dialog):
    def __init__(self, parent, item, on_saved):
        self.item = item
        self.on_saved = on_saved
        super().__init__(parent, title="Edit Book")

    def body(self, master):
        import tkinter as tk
        tk.Label(master, text="Title:").grid(row=0); tk.Label(master, text="Author:").grid(row=1)
        tk.Label(master, text="Status:").grid(row=2); tk.Label(master, text="Rating:").grid(row=3)
        tk.Label(master, text="Notes:").grid(row=4)
        self.e_title = ctk.CTkEntry(master); self.e_title.grid(row=0, column=1, padx=6, pady=4)
        self.e_author = ctk.CTkEntry(master); self.e_author.grid(row=1, column=1, padx=6, pady=4)
        self.status_menu = ctk.CTkOptionMenu(master, values=["available","checked_out"]); self.status_menu.grid(row=2,column=1,padx=6,pady=4)
        self.e_rating = ctk.CTkEntry(master); self.e_rating.grid(row=3, column=1, padx=6, pady=4)
        self.e_notes = ctk.CTkTextbox(master, width=420, height=100); self.e_notes.grid(row=4, column=1, padx=6, pady=4)
        # populate
        self.e_title.insert(0, self.item[1]); self.e_author.insert(0, self.item[2]); self.status_menu.set(self.item[3])
        self.e_rating.insert(0, "" if self.item[4] is None else str(self.item[4])); self.e_notes.insert("0.0", self.item[5] or "")
        return self.e_title

    def apply(self):
        title = self.e_title.get().strip(); author = self.e_author.get().strip()
        status = self.status_menu.get(); rating_raw = self.e_rating.get().strip(); notes = self.e_notes.get("0.0","end").strip()
        rating = None
        if rating_raw:
            try:
                rr = int(rating_raw)
                if 1<=rr<=5: rating=rr
                else: ctk.CTk = None
            except:
                rating=None
        update_book(self.item[0], title, author, status, rating, notes)
        if self.on_saved: self.on_saved()
