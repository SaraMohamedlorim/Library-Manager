# ui/members_ui.py
# ui/members_ui.py
import customtkinter as ctk
from tkinter import messagebox, ttk
from members import add_member, fetch_all_members, update_member, delete_member

class MembersWindow(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Manage Members")
        self.geometry("900x520")

        top = ctk.CTkFrame(self); top.pack(fill="x", padx=10, pady=6)
        ctk.CTkLabel(top, text="Library Members", font=("Arial", 16, "bold")).pack(side="left")

        form = ctk.CTkFrame(self); form.pack(fill="x", padx=10, pady=6)
        self.name_entry = ctk.CTkEntry(form, placeholder_text="Full Name", width=320); self.name_entry.grid(row=0,column=0,padx=6,pady=6)
        self.email_entry = ctk.CTkEntry(form, placeholder_text="Email", width=260); self.email_entry.grid(row=0,column=1,padx=6,pady=6)
        self.phone_entry = ctk.CTkEntry(form, placeholder_text="Phone", width=180); self.phone_entry.grid(row=0,column=2,padx=6,pady=6)
        ctk.CTkButton(form, text="Add Member", command=self.add_member_action).grid(row=0,column=3,padx=6)

        cols = ("ID","Full Name","Email","Phone","Created")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c); self.tree.column(c, width=150 if c=="Full Name" else 120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=8)
        self.tree.bind("<Double-1>", lambda e: self.open_edit_dialog())

        btn_frame = ctk.CTkFrame(self); btn_frame.pack(fill="x", padx=10, pady=6)
        ctk.CTkButton(btn_frame, text="Edit Selected", command=self.open_edit_dialog).pack(side="left", padx=8)
        ctk.CTkButton(btn_frame, text="Delete Selected", fg_color="red", command=self.delete_selected).pack(side="left", padx=8)
        ctk.CTkButton(btn_frame, text="Refresh", command=self.load_members).pack(side="left", padx=8)

        self.load_members()

    def load_members(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        rows = fetch_all_members()
        for r in rows: self.tree.insert("", "end", values=r)

    def add_member_action(self):
        name = self.name_entry.get().strip(); email = self.email_entry.get().strip(); phone = self.phone_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning","Name required"); return
        add_member(name, email, phone)
        messagebox.showinfo("Success","Member added"); self.name_entry.delete(0,"end"); self.email_entry.delete(0,"end"); self.phone_entry.delete(0,"end")
        self.load_members()

    def selected(self):
        sel = self.tree.selection()
        if not sel: return None
        return self.tree.item(sel[0])['values']

    def open_edit_dialog(self):
        sel = self.selected()
        if not sel:
            messagebox.showwarning("Warning","Select a member"); return
        EditMemberDialog(self, sel, self.load_members)

    def delete_selected(self):
        sel = self.selected()
        if not sel:
            messagebox.showwarning("Warning","Select a member"); return
        if not messagebox.askyesno("Confirm","Delete selected member?"): return
        delete_member(sel[0]); messagebox.showinfo("Deleted","Member deleted"); self.load_members()

# Simple edit dialog
from tkinter import simpledialog
class EditMemberDialog(simpledialog.Dialog):
    def __init__(self, parent, item, on_saved):
        self.item = item; self.on_saved = on_saved
        super().__init__(parent, title="Edit Member")

    def body(self, master):
        import tkinter as tk
        tk.Label(master, text="Full Name:").grid(row=0); tk.Label(master, text="Email:").grid(row=1); tk.Label(master, text="Phone:").grid(row=2)
        self.e_name = ctk.CTkEntry(master); self.e_name.grid(row=0,column=1,padx=6,pady=4)
        self.e_email = ctk.CTkEntry(master); self.e_email.grid(row=1,column=1,padx=6,pady=4)
        self.e_phone = ctk.CTkEntry(master); self.e_phone.grid(row=2,column=1,padx=6,pady=4)
        self.e_name.insert(0, self.item[1]); self.e_email.insert(0, self.item[2]); self.e_phone.insert(0, self.item[3])
        return self.e_name

    def apply(self):
        name = self.e_name.get().strip(); email = self.e_email.get().strip(); phone = self.e_phone.get().strip()
        from members import update_member
        update_member(self.item[0], name, email, phone)
        if self.on_saved: self.on_saved()
