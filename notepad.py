"""
Module Bloc-notes
Éditeur de texte simple avec sauvegarde
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime

class Notepad:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.notes = []
        self.current_note = None
        self.fichier_notes = "notes.json"

        self.setup_ui()
        self.load_notes()
        self.update_notes_list()

    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Titre
        title = tk.Label(
            self.parent,
            text="📝 Bloc-notes",
            font=self.config.POLICE_TITRE,
            bg=self.config.style["fond"],
            fg=self.config.style["texte"]
        )
        title.pack(pady=(0, 20))

        # Frame principal avec deux colonnes
        main_frame = tk.Frame(self.parent, bg=self.config.style["fond"])
        main_frame.pack(fill="both", expand=True)

        # Colonne gauche : Liste des notes
        self.setup_notes_list(main_frame)

        # Colonne droite : Éditeur
        self.setup_editor(main_frame)

    def setup_notes_list(self, parent):
        """Frame de la liste des notes"""
        list_frame = tk.Frame(
            parent,
            bg=self.config.style["cadre"],
            relief="groove",
            bd=2,
            width=250
        )
        list_frame.pack(side="left", fill="both", padx=(0, 10))
        list_frame.pack_propagate(False)

        # Titre de la liste
        list_title = tk.Label(
            list_frame,
            text="Mes notes",
            font=("Segoe UI", 12, "bold"),
            bg=self.config.style["cadre"],
            fg=self.config.style["texte"],
            pady=10
        )
        list_title.pack(fill="x")

        # Bouton nouvelle note
        btn_new = tk.Button(
            list_frame,
            text="➕ Nouvelle note",
            command=self.new_note,
            font=self.config.POLICE,
            bg=self.config.style["accent"],
            fg="white",
            relief="flat",
            cursor="hand2",
            pady=8
        )
        btn_new.pack(fill="x", padx=10, pady=(0, 10))

        # Listbox avec scrollbar
        scroll_frame = tk.Frame(list_frame, bg=self.config.style["cadre"])
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side="right", fill="y")

        self.notes_listbox = tk.Listbox(
            scroll_frame,
            font=self.config.POLICE,
            bg=self.config.style["fond"],
            fg=self.config.style["texte"],
            selectbackground=self.config.style["accent"],
            selectforeground="white",
            relief="flat",
            activestyle="none",
            yscrollcommand=scrollbar.set
        )
        self.notes_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.notes_listbox.yview)

        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)

        # Bouton supprimer
        btn_delete = tk.Button(
            list_frame,
            text="🗑️ Supprimer",
            command=self.delete_note,
            font=self.config.POLICE,
            bg=self.config.style["danger"],
            fg="white",
            relief="flat",
            cursor="hand2",
            pady=8
        )
        btn_delete.pack(fill="x", padx=10, pady=10)

    def setup_editor(self, parent):
        """Frame de l'éditeur"""
        editor_frame = tk.Frame(parent, bg=self.config.style["fond"])
        editor_frame.pack(side="right", fill="both", expand=True)

        # Barre d'outils
        toolbar = tk.Frame(editor_frame, bg=self.config.style["cadre"], relief="groove", bd=2)
        toolbar.pack(fill="x", pady=(0, 10))

        # Titre de la note
        title_frame = tk.Frame(toolbar, bg=self.config.style["cadre"])
        title_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(
            title_frame,
            text="Titre:",
            font=self.config.POLICE,
            bg=self.config.style["cadre"],
            fg=self.config.style["texte"]
        ).pack(side="left", padx=(0, 10))

        self.title_entry = ttk.Entry(title_frame, width=40)
        self.title_entry.pack(side="left", fill="x", expand=True)

        # Boutons d'action
        btn_frame = tk.Frame(toolbar, bg=self.config.style["cadre"])
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        btn_save = tk.Button(
            btn_frame,
            text="💾 Sauvegarder",
            command=self.save_current_note,
            font=self.config.POLICE,
            bg=self.config.style["success"],
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5
        )
        btn_save.pack(side="left", padx=5)

        btn_export = tk.Button(
            btn_frame,
            text="📤 Exporter",
            command=self.export_note,
            font=self.config.POLICE,
            bg=self.config.style["bouton"],
            fg=self.config.style["texte"],
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5
        )
        btn_export.pack(side="left", padx=5)

        btn_clear = tk.Button(
            btn_frame,
            text="🗑️ Effacer",
            command=self.clear_editor,
            font=self.config.POLICE,
            bg=self.config.style["danger"],
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5
        )
        btn_clear.pack(side="left", padx=5)

        # Zone de texte avec scrollbar
        text_frame = tk.Frame(editor_frame, bg=self.config.style["fond"])
        text_frame.pack(fill="both", expand=True)

        text_scrollbar = ttk.Scrollbar(text_frame)
        text_scrollbar.pack(side="right", fill="y")

        self.text_editor = tk.Text(
            text_frame,
            font=("Consolas", 11),
            bg=self.config.style["cadre"],
            fg=self.config.style["texte"],
            insertbackground=self.config.style["texte"],
            relief="flat",
            wrap="word",
            undo=True,
            maxundo=-1,
            yscrollcommand=text_scrollbar.set,
            padx=10,
            pady=10
        )
        self.text_editor.pack(side="left", fill="both", expand=True)
        text_scrollbar.config(command=self.text_editor.yview)

        # Raccourcis clavier
        self.text_editor.bind('<Control-s>', lambda e: self.save_current_note())
        self.text_editor.bind('<Control-n>', lambda e: self.new_note())

        # Info en bas
        info_label = tk.Label(
            editor_frame,
            text="💡 Ctrl+S: Sauvegarder | Ctrl+N: Nouvelle note",
            font=("Segoe UI", 9),
            bg=self.config.style["fond"],
            fg=self.config.style["hover"],
            pady=5
        )
        info_label.pack(fill="x")

    def new_note(self):
        """Crée une nouvelle note"""
        if self.check_unsaved_changes():
            self.current_note = None
            self.title_entry.delete(0, 'end')
            self.text_editor.delete(1.0, 'end')
            self.title_entry.focus()

    def save_current_note(self):
        """Sauvegarde la note actuelle"""
        title = self.title_entry.get().strip()
        content = self.text_editor.get(1.0, 'end-1c').strip()

        if not title:
            messagebox.showwarning("Attention", "Veuillez entrer un titre pour la note")
            return

        if not content:
            messagebox.showwarning("Attention", "La note est vide")
            return

        if self.current_note is None:
            # Nouvelle note
            note = {
                "id": len(self.notes),
                "title": title,
                "content": content,
                "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "date_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.notes.append(note)
            self.current_note = note["id"]
        else:
            # Modification d'une note existante
            for note in self.notes:
                if note["id"] == self.current_note:
                    note["title"] = title
                    note["content"] = content
                    note["date_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    break

        self.save_notes()
        self.update_notes_list()
        messagebox.showinfo("Succès", "Note sauvegardée avec succès!")

    def delete_note(self):
        """Supprime la note sélectionnée"""
        selection = self.notes_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner une note à supprimer")
            return

        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette note ?"):
            index = selection[0]
            note_id = self.notes[index]["id"]
            self.notes = [n for n in self.notes if n["id"] != note_id]

            if self.current_note == note_id:
                self.new_note()

            self.save_notes()
            self.update_notes_list()

    def on_note_select(self, event):
        """Gère la sélection d'une note"""
        selection = self.notes_listbox.curselection()
        if not selection:
            return

        if self.check_unsaved_changes():
            index = selection[0]

            # Récupérer la note depuis la liste triée
            sorted_notes = sorted(self.notes, key=lambda x: x["date_modified"], reverse=True)
            note = sorted_notes[index]

            self.current_note = note["id"]
            self.title_entry.delete(0, 'end')
            self.title_entry.insert(0, note["title"])

            self.text_editor.delete(1.0, 'end')
            self.text_editor.insert(1.0, note["content"])

    def check_unsaved_changes(self):
        """Vérifie s'il y a des modifications non sauvegardées"""
        if self.current_note is not None:
            current_title = self.title_entry.get().strip()
            current_content = self.text_editor.get(1.0, 'end-1c').strip()

            for note in self.notes:
                if note["id"] == self.current_note:
                    if note["title"] != current_title or note["content"] != current_content:
                        response = messagebox.askyesnocancel(
                            "Modifications non sauvegardées",
                            "Voulez-vous sauvegarder les modifications ?"
                        )
                        if response is True:
                            self.save_current_note()
                            return True
                        elif response is False:
                            return True
                        else:
                            return False
        return True

    def clear_editor(self):
        """Efface le contenu de l'éditeur"""
        if messagebox.askyesno("Confirmation", "Effacer le contenu de l'éditeur ?"):
            self.text_editor.delete(1.0, 'end')

    def export_note(self):
        """Exporte la note actuelle en fichier texte"""
        content = self.text_editor.get(1.0, 'end-1c').strip()
        if not content:
            messagebox.showwarning("Attention", "Aucun contenu à exporter")
            return

        title = self.title_entry.get().strip() or "note"
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fichier texte", "*.txt"), ("Tous les fichiers", "*.*")],
            initialfile=f"{title}.txt"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Titre: {title}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(content)
                messagebox.showinfo("Succès", "Note exportée avec succès!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'exporter: {e}")

    def update_notes_list(self):
        """Met à jour la liste des notes"""
        self.notes_listbox.delete(0, 'end')

        # Trier par date de modification (plus récent en premier)
        sorted_notes = sorted(self.notes, key=lambda x: x["date_modified"], reverse=True)

        for note in sorted_notes:
            display_text = f"{note['title']}"
            self.notes_listbox.insert('end', display_text)

    def save_notes(self):
        """Sauvegarde les notes dans un fichier JSON"""
        try:
            with open(self.fichier_notes, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder: {e}")

    def load_notes(self):
        """Charge les notes depuis le fichier JSON"""
        if os.path.exists(self.fichier_notes):
            try:
                with open(self.fichier_notes, 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger: {e}")
                self.notes = []
        else:
            self.notes = []