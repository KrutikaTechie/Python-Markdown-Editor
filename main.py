import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import font as tkfont
import markdown


class MarkdownEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro Markdown Editor")
        self.root.geometry("1100x750")

        # CSS for the Exported HTML
        self.css_style = "<style>body{font-family:sans-serif;line-height:1.6;padding:40px;max-width:800px;margin:auto;} h1{color:#2c3e50;border-bottom:2px solid #3498db;} blockquote{border-left:5px solid #3498db;background:#f9f9f9;padding:10px;}</style>"

        self.current_font_family = "Consolas"
        self.setup_ui()

    def setup_ui(self):
        # Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Styled HTML", command=self.export_html)

        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Change Editor Font", command=self.open_font_picker)

        theme_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="Themes", menu=theme_menu)
        theme_menu.add_command(label="☀️ Light", command=lambda: self.apply_theme("light"))
        theme_menu.add_command(label="🌙 Dark", command=lambda: self.apply_theme("dark"))
        theme_menu.add_command(label="🧪 Neon", command=lambda: self.apply_theme("neon"))

        # Main Layout
        self.panes = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=6, sashrelief=tk.RAISED)
        self.panes.pack(fill="both", expand=True)

        self.editor = tk.Text(self.panes, font=(self.current_font_family, 12), undo=True, padx=15, pady=15)
        self.panes.add(self.editor)
        self.editor.bind("<KeyRelease>", self.update_preview)

        self.preview = tk.Text(self.panes, font=("Consolas", 10), bg="#ffffff", padx=15, pady=15, state="disabled")
        self.panes.add(self.preview)

    def apply_theme(self, theme):
        if theme == "light":
            self.editor.config(bg="white", fg="black", insertbackground="black")
            self.preview.config(bg="#f4f4f4", fg="black")
        elif theme == "dark":
            self.editor.config(bg="#2c3e50", fg="#ecf0f1", insertbackground="white")
            self.preview.config(bg="#34495e", fg="#ecf0f1")
        elif theme == "neon":
            self.editor.config(bg="black", fg="#39FF14", insertbackground="#39FF14")
            self.preview.config(bg="#0a0a0a", fg="#39FF14")

    def open_font_picker(self):
        picker = tk.Toplevel(self.root)
        picker.title("Select Font")
        fonts = sorted(list(tkfont.families()))
        combo = ttk.Combobox(picker, values=fonts, state="readonly", width=30)
        combo.set(self.current_font_family)
        combo.pack(pady=20, padx=20)

        def apply():
            self.current_font_family = combo.get()
            self.editor.config(font=(self.current_font_family, 12))
            picker.destroy()

        tk.Button(picker, text="Apply", command=apply).pack(pady=10)

    def update_preview(self, event=None):
        content = self.editor.get("1.0", tk.END)
        html = markdown.markdown(content)
        self.preview.config(state="normal")
        self.preview.delete("1.0", tk.END)
        self.preview.insert(tk.END, html)
        self.preview.config(state="disabled")

    def export_html(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".html")
        if file_path:
            content = self.editor.get("1.0", "end-1c")
            html_body = markdown.markdown(content)
            full_html = f"<html><head>{self.css_style}</head><body>{html_body}</body></html>"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(full_html)
            messagebox.showinfo("Success", "Exported with Styles!")


if __name__ == "__main__":
    root = tk.Tk()
    app = MarkdownEditor(root)
    root.mainloop()