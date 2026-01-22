"""
Module de styles
Configure les styles TTK et gère les widgets personnalisés
"""

import tkinter as tk
from tkinter import ttk


class AppStyles:
    """Gestion des styles de l'application"""

    def __init__(self, root):
        self.root = root
        self.style = ttk.Style()
        self.setup_styles()

    def setup_styles(self):
        """Configure tous les styles TTK"""
        # Utiliser un thème moderne
        self.style.theme_use('clam')

        # Styles généraux
        self.style.configure('TButton',
                           padding=6,
                           font=("Segoe UI", 10))

        self.style.configure('TEntry',
                           padding=5,
                           font=("Segoe UI", 10))

        self.style.configure('TLabel',
                           font=("Segoe UI", 10))

        self.style.configure('TCheckbutton',
                           font=("Segoe UI", 10))

        # Style pour les boutons accentués
        self.style.configure('Accent.TButton',
                           font=("Segoe UI", 10, "bold"),
                           padding=10)

        # Style pour la barre de progression
        self.style.configure('TProgressbar',
                           thickness=20)

    def update_theme(self):
        """Met à jour les styles après un changement de thème"""
        self.setup_styles()


class ToolTip:
    """
    Classe pour créer des infobulles (tooltips) sur les widgets

    Usage:
        ToolTip(mon_bouton, "Ceci est une infobulle")
    """

    def __init__(self, widget, text=''):
        self.widget = widget
        self.text = text
        self.tipwindow = None

        # Lier les événements
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        """Affiche l'infobulle"""
        if self.tipwindow or not self.text:
            return

        # Position de l'infobulle
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 20

        # Créer la fenêtre toplevel
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Pas de bordure
        tw.wm_geometry(f"+{x}+{y}")

        # Label avec le texte
        label = tk.Label(tw,
                        text=self.text,
                        justify='left',
                        background="#ffffe0",
                        relief='solid',
                        borderwidth=1,
                        font=("Segoe UI", 9),
                        padx=5,
                        pady=3)
        label.pack()

    def hide_tip(self, event=None):
        """Cache l'infobulle"""
        if self.tipwindow:
            self.tipwindow.destroy()
        self.tipwindow = None


def create_hover_effect(widget, normal_bg, hover_bg, normal_fg=None, hover_fg=None):
    """
    Crée un effet hover sur un widget

    Args:
        widget: Le widget à modifier
        normal_bg: Couleur de fond normale
        hover_bg: Couleur de fond au survol
        normal_fg: Couleur de texte normale (optionnel)
        hover_fg: Couleur de texte au survol (optionnel)
    """
    def on_enter(e):
        widget.config(bg=hover_bg)
        if hover_fg:
            widget.config(fg=hover_fg)

    def on_leave(e):
        widget.config(bg=normal_bg)
        if normal_fg:
            widget.config(fg=normal_fg)

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


def add_placeholder(entry, placeholder_text):
    """
    Ajoute un placeholder à une Entry

    Args:
        entry: Widget Entry
        placeholder_text: Texte du placeholder

    Note: ttk.Entry ne supporte pas l'attribut 'fg', on utilise juste le texte
    """
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, 'end')

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder_text)

    # Insérer le placeholder initial
    entry.insert(0, placeholder_text)

    # Lier les événements
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)