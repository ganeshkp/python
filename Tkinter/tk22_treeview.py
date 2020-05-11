import csv
import tkinter as tk
import tkinter.ttk as ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ttk Treeview")
        columns = ("#1", "#2", "#3")

        self.tree = ttk.Treeview(self, show="headings", columns=columns)
        self.tree.heading("#1", text="Last name")
        self.tree.heading("#2", text="First name")
        self.tree.heading("#3", text="Email")
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL,
                            command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)

        with open("contacts.csv", newline="") as f:
            for contact in csv.reader(f):
                result=self.tree.insert("", tk.END, values=contact)
                #print(result)

        self.tree.bind("<<TreeviewSelect>>", self.print_selection)
        self.tree.bind("<Double-1>", self.onDoubleClick)
        self.tree.grid(row=0, column=0)
        ysb.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def onDoubleClick(self, event):
        print("Double clicked")
        selected_items = self.tree.selection()
        for selected_item in selected_items:
            self.tree.delete(selected_item)


    def print_selection(self, event):
        for selection in self.tree.selection():
            item = self.tree.item(selection)
            last_name, first_name, email = item["values"][0:3]
            text = "Selection: {}, {} <{}>"
            print(text.format(last_name, first_name, email))

if __name__ == "__main__":
    app = App()
    app.mainloop()