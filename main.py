"""
Gestionnaire de Tâches et Bloc-notes
Application principale avec menu de navigation
"""

import tkinter as tk
from tkinter import ttk
from config import AppConfig
from styles import AppStyles
from tasks import TaskManager
from notepad import Notepad


class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestionnaire Personnel")
        self.root.geometry("900x700")

        # Configuration
        self.config = AppConfig()
        self.styles = AppStyles(self.root)

        # Variables
        self.current_view = None

        # Interface
        self.setup_ui()
        self.show_tasks()

    def setup_ui(self):
        """Configure l'interface principale"""
        self.root.configure(bg=self.config.style["fond"])

        # Frame principale
        self.main_frame = tk.Frame(self.root, bg=self.config.style["fond"])
        self.main_frame.pack(fill="both", expand=True)

        # Menu latéral
        self.setup_sidebar()

        # Zone de contenu
        self.content_frame = tk.Frame(
            self.main_frame,
            bg=self.config.style["fond"]
        )
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def setup_sidebar(self):
        """Crée le menu de navigation latéral"""
        sidebar = tk.Frame(
            self.main_frame,
            bg=self.config.style["accent"],
            width=200
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Titre
        title = tk.Label(
            sidebar,
            text="📋 Menu",
            font=("Segoe UI", 16, "bold"),
            bg=self.config.style["accent"],
            fg="white",
            pady=20
        )
        title.pack(fill="x")

        # Séparateur
        sep = tk.Frame(sidebar, height=2, bg="white")
        sep.pack(fill="x", padx=10)

        # Boutons de navigation
        self.create_nav_button(sidebar, "✓ Tâches", self.show_tasks)
        self.create_nav_button(sidebar, "📝 Bloc-notes", self.show_notepad)

        # Espacement
        spacer = tk.Frame(sidebar, bg=self.config.style["accent"])
        spacer.pack(fill="both", expand=True)

        # Bouton thème en bas
        theme_btn = tk.Button(
            sidebar,
            text="🌓 Changer thème",
            command=self.toggle_theme,
            font=self.config.POLICE,
            bg=self.config.style["fond"],
            fg=self.config.style["texte"],
            relief="flat",
            cursor="hand2",
            pady=10
        )
        theme_btn.pack(fill="x", padx=10, pady=10)

    def create_nav_button(self, parent, text, command):
        """Crée un bouton de navigation"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 11),
            bg=self.config.style["accent"],
            fg="white",
            activebackground="white",
            activeforeground=self.config.style["accent"],
            relief="flat",
            cursor="hand2",
            anchor="w",
            padx=20,
            pady=15
        )
        btn.pack(fill="x", pady=2)

        # Effet hover
        def on_enter(e):
            btn.config(bg="white", fg=self.config.style["accent"])

        def on_leave(e):
            btn.config(bg=self.config.style["accent"], fg="white")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def clear_content(self):
        """Efface le contenu actuel"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_tasks(self):
        """Affiche le gestionnaire de tâches"""
        self.clear_content()
        self.current_view = TaskManager(self.content_frame, self.config)

    def show_notepad(self):
        """Affiche le bloc-notes"""
        self.clear_content()
        self.current_view = Notepad(self.content_frame, self.config)

    def toggle_theme(self):
        """Change le thème de l'application"""
        self.config.toggle_theme()
        self.styles.update_theme()

        # Recharger la vue actuelle
        if isinstance(self.current_view, TaskManager):
            self.show_tasks()
        elif isinstance(self.current_view, Notepad):
            self.show_notepad()
        else:
            self.show_tasks()

        # Recréer le sidebar
        for widget in self.main_frame.winfo_children():
            if widget != self.content_frame:
                widget.destroy()
        self.setup_sidebar()

    def run(self):
        """Lance l'application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApplication()
    app.run()