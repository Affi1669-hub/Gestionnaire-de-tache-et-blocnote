"""
Module de gestion des tâches
Gestionnaire de tâches complet avec toutes les fonctionnalités
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from styles import ToolTip, add_placeholder

class TaskManager:
    """Classe principale du gestionnaire de tâches"""

    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.tasks = []
        self.filtered_tasks = []
        self.fichier_taches = "taches.json"

        # Charger d'abord
        self.load_tasks()

        # Ensuite créer l'interface
        self.setup_ui()

        # Enfin afficher
        self.update_display()

    def setup_ui(self):
        """Configure l'interface utilisateur complète"""
        # Titre principal
        title = tk.Label(
            self.parent,
            text="📋 Gestionnaire de Tâches",
            font=self.config.POLICE_TITRE,
            bg=self.config.style["fond"],
            fg=self.config.style["texte"]
        )
        title.pack(pady=(0, 20))

        # Frame pour ajouter une tâche
        self.setup_add_task_frame()

        # Frame pour recherche et filtres
        self.setup_filter_frame()

        # Frame pour la liste des tâches (avec scrollbar)
        self.setup_tasks_list_frame()

        # Frame pour les statistiques
        self.setup_stats_frame()

        # Maintenant on peut ajouter le trace pour la recherche
        self.search_var.trace_add("write", lambda *args: self.filter_tasks())

    def setup_add_task_frame(self):
        """Frame d'ajout de tâche"""
        frame = tk.Frame(
            self.parent,
            bg=self.config.style["cadre"],
            relief="groove",
            bd=2
        )
        frame.pack(fill="x", pady=(0, 10), padx=5)

        # Label
        label = tk.Label(
            frame,
            text="Nouvelle tâche:",
            font=self.config.POLICE,
            bg=self.config.style["cadre"],
            fg=self.config.style["texte"]
        )
        label.pack(side="left", padx=10, pady=10)

        # Entry pour saisir la tâche
        self.task_entry = ttk.Entry(frame, width=50, font=self.config.POLICE)
        self.task_entry.pack(side="left", padx=5, pady=10, fill="x", expand=True)
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        # Bouton ajouter
        btn_add = tk.Button(
            frame,
            text="➕ Ajouter",
            command=self.add_task,
            font=self.config.POLICE,
            bg=self.config.style["accent"],
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5
        )
        btn_add.pack(side="left", padx=10, pady=10)
        ToolTip(btn_add, "Ajouter une nouvelle tâche (Entrée)")

    def setup_filter_frame(self):
        """Frame de recherche et filtres"""
        frame = tk.Frame(self.parent, bg=self.config.style["fond"])
        frame.pack(fill="x", pady=(0, 10))

        # Frame de recherche
        search_frame = tk.Frame(frame, bg=self.config.style["fond"])
        search_frame.pack(side="left", fill="x", expand=True)

        # Entry de recherche (sans trace d'abord)
        self.search_var = tk.StringVar()

        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30,
            font=self.config.POLICE
        )
        self.search_entry.pack(side="left", padx=5)
        add_placeholder(self.search_entry, "🔍 Rechercher une tâche...")

        # Boutons d'action
        btn_frame = tk.Frame(frame, bg=self.config.style["fond"])
        btn_frame.pack(side="right")

        # Bouton trier
        btn_sort = tk.Button(
            btn_frame,
            text="↕️ Trier",
            command=self.show_sort_menu,
            font=self.config.POLICE,
            bg=self.config.style["bouton"],
            fg=self.config.style["texte"],
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=5
        )
        btn_sort.pack(side="left", padx=2)
        ToolTip(btn_sort, "Trier les tâches par date, nom ou état")

        # Bouton supprimer terminées
        btn_clear = tk.Button(
            btn_frame,
            text="🗑️ Supprimer terminées",
            command=self.clear_completed,
            font=self.config.POLICE,
            bg=self.config.style["danger"],
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=5
        )
        btn_clear.pack(side="left", padx=2)
        ToolTip(btn_clear, "Supprimer toutes les tâches terminées")

        # Bouton tout supprimer
        btn_clear_all = tk.Button(
            btn_frame,
            text="🗑️ Tout supprimer",
            command=self.clear_all_tasks,
            font=self.config.POLICE,
            bg=self.config.style["danger"],
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=5
        )
        btn_clear_all.pack(side="left", padx=2)
        ToolTip(btn_clear_all, "Supprimer TOUTES les tâches")

    def setup_tasks_list_frame(self):
        """Frame avec scrollbar pour les tâches"""
        container = tk.Frame(self.parent, bg=self.config.style["fond"])
        container.pack(fill="both", expand=True, pady=(0, 10))

        # Canvas avec scrollbar
        self.canvas = tk.Canvas(
            container,
            bg=self.config.style["fond"],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        # Frame interne pour les tâches
        self.tasks_frame = tk.Frame(self.canvas, bg=self.config.style["fond"])

        # Configurer le scroll
        self.tasks_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind scroll avec la molette
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        """Gestion du scroll avec la molette de souris"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def setup_stats_frame(self):
        """Frame pour les statistiques et progression"""
        self.stats_frame = tk.Frame(
            self.parent,
            bg=self.config.style["cadre"],
            relief="groove",
            bd=2
        )
        self.stats_frame.pack(fill="x", pady=(0, 5))

        # Label des statistiques
        self.stats_label = tk.Label(
            self.stats_frame,
            text="",
            font=self.config.POLICE,
            bg=self.config.style["cadre"],
            fg=self.config.style["texte"],
            pady=10
        )
        self.stats_label.pack()

        # Barre de progression
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            self.stats_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(pady=5)

    def add_task(self):
        """Ajoute une nouvelle tâche"""
        text = self.task_entry.get().strip()

        # Vérifier que le texte n'est pas vide ou le placeholder
        if not text or text == "🔍 Rechercher une tâche...":
            return

        # Créer la tâche
        task = {
            "id": len(self.tasks),
            "text": text,
            "completed": False,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.tasks.append(task)
        self.task_entry.delete(0, 'end')
        self.save_tasks()
        self.update_display()

    def toggle_task(self, task_id):
        """Change l'état d'une tâche (terminée/non terminée)"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                break

        self.save_tasks()
        self.update_display()

    def delete_task(self, task_id):
        """Supprime une tâche spécifique"""
        if messagebox.askyesno("Confirmation", "Supprimer cette tâche ?"):
            self.tasks = [t for t in self.tasks if t["id"] != task_id]
            self.save_tasks()
            self.update_display()

    def clear_completed(self):
        """Supprime toutes les tâches terminées"""
        completed = [t for t in self.tasks if t["completed"]]

        if not completed:
            messagebox.showinfo("Information", "Aucune tâche terminée à supprimer")
            return

        if messagebox.askyesno("Confirmation",
                               f"Supprimer {len(completed)} tâche(s) terminée(s) ?"):
            self.tasks = [t for t in self.tasks if not t["completed"]]
            self.save_tasks()
            self.update_display()
            messagebox.showinfo("Succès", f"{len(completed)} tâche(s) supprimée(s)")

    def clear_all_tasks(self):
        """Supprime TOUTES les tâches"""
        if not self.tasks:
            messagebox.showinfo("Information", "Aucune tâche à supprimer")
            return

        if messagebox.askyesno("⚠️ ATTENTION",
                               f"Supprimer TOUTES les {len(self.tasks)} tâches ?\n\nCette action est irréversible !"):
            count = len(self.tasks)
            self.tasks = []
            self.save_tasks()
            self.update_display()
            messagebox.showinfo("Succès", f"{count} tâche(s) supprimée(s)")

    def filter_tasks(self):
        """Filtre les tâches selon la recherche"""
        search = self.search_var.get().lower().strip()

        if not search or search == "🔍 rechercher une tâche...":
            self.filtered_tasks = self.tasks
        else:
            self.filtered_tasks = [
                t for t in self.tasks
                if search in t["text"].lower()
            ]

        self.update_display()

    def show_sort_menu(self):
        """Affiche le menu de tri"""
        menu = tk.Menu(self.parent, tearoff=0)
        menu.add_command(label="📅 Par date (récent → ancien)",
                        command=lambda: self.sort_tasks("date_desc"))
        menu.add_command(label="📅 Par date (ancien → récent)",
                        command=lambda: self.sort_tasks("date_asc"))
        menu.add_command(label="🔤 Alphabétique (A → Z)",
                        command=lambda: self.sort_tasks("alpha_asc"))
        menu.add_command(label="🔤 Alphabétique (Z → A)",
                        command=lambda: self.sort_tasks("alpha_desc"))
        menu.add_command(label="✅ Terminées d'abord",
                        command=lambda: self.sort_tasks("completed"))
        menu.add_command(label="⭕ Non terminées d'abord",
                        command=lambda: self.sort_tasks("active"))

        try:
            menu.tk_popup(self.parent.winfo_pointerx(), self.parent.winfo_pointery())
        finally:
            menu.grab_release()

    def sort_tasks(self, sort_type):
        """Trie les tâches selon le type"""
        if sort_type == "date_desc":
            self.tasks.sort(key=lambda x: x["date"], reverse=True)
        elif sort_type == "date_asc":
            self.tasks.sort(key=lambda x: x["date"])
        elif sort_type == "alpha_asc":
            self.tasks.sort(key=lambda x: x["text"].lower())
        elif sort_type == "alpha_desc":
            self.tasks.sort(key=lambda x: x["text"].lower(), reverse=True)
        elif sort_type == "completed":
            self.tasks.sort(key=lambda x: x["completed"], reverse=True)
        elif sort_type == "active":
            self.tasks.sort(key=lambda x: x["completed"])

        self.save_tasks()
        self.update_display()

    def update_display(self):
        """Met à jour l'affichage complet"""
        # Vider le frame
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        # Déterminer quelles tâches afficher
        display_tasks = (self.filtered_tasks if hasattr(self, 'filtered_tasks')
                        and self.filtered_tasks else self.tasks)

        # Afficher les tâches
        if not display_tasks:
            no_task_label = tk.Label(
                self.tasks_frame,
                text="📭 Aucune tâche à afficher",
                font=("Segoe UI", 12),
                bg=self.config.style["fond"],
                fg=self.config.style["hover"],
                pady=50
            )
            no_task_label.pack()
        else:
            for task in display_tasks:
                self.create_task_widget(task)

        # Mettre à jour les statistiques
        self.update_stats()

    def create_task_widget(self, task):
        """Crée un widget pour une tâche"""
        frame = tk.Frame(
            self.tasks_frame,
            bg=self.config.style["cadre"],
            relief="raised",
            bd=1
        )
        frame.pack(fill="x", padx=5, pady=3)

        # Checkbox
        var = tk.BooleanVar(value=task["completed"])
        check = tk.Checkbutton(
            frame,
            variable=var,
            command=lambda: self.toggle_task(task["id"]),
            bg=self.config.style["cadre"],
            activebackground=self.config.style["cadre"],
            cursor="hand2"
        )
        check.pack(side="left", padx=5)

        # Texte de la tâche
        if task["completed"]:
            text_style = ("Segoe UI", 10, "overstrike")
            text_color = self.config.style["hover"]
        else:
            text_style = self.config.POLICE
            text_color = self.config.style["texte"]

        label = tk.Label(
            frame,
            text=task["text"],
            font=text_style,
            bg=self.config.style["cadre"],
            fg=text_color,
            anchor="w"
        )
        label.pack(side="left", fill="x", expand=True, padx=5, pady=8)

        # Date
        date_label = tk.Label(
            frame,
            text=task["date"],
            font=("Segoe UI", 8),
            bg=self.config.style["cadre"],
            fg=self.config.style["hover"]
        )
        date_label.pack(side="left", padx=5)

        # Bouton supprimer
        btn_delete = tk.Button(
            frame,
            text="❌",
            command=lambda: self.delete_task(task["id"]),
            font=("Segoe UI", 9),
            bg=self.config.style["danger"],
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=2
        )
        btn_delete.pack(side="right", padx=5)
        ToolTip(btn_delete, "Supprimer cette tâche")

    def update_stats(self):
        """Met à jour les statistiques"""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["completed"]])
        remaining = total - completed

        # Calculer le pourcentage
        if total > 0:
            percentage = (completed / total) * 100
            self.progress_var.set(percentage)
        else:
            self.progress_var.set(0)
            percentage = 0

        # Texte des statistiques
        stats_text = (f"📊 Total: {total} | "
                     f"✅ Terminées: {completed} | "
                     f"⭕ Restantes: {remaining} | "
                     f"📈 Progression: {percentage:.0f}%")

        self.stats_label.config(text=stats_text)

    def save_tasks(self):
        """Sauvegarde les tâches dans un fichier JSON"""
        try:
            with open(self.fichier_taches, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder: {e}")

    def load_tasks(self):
        """Charge les tâches depuis le fichier JSON"""
        if os.path.exists(self.fichier_taches):
            try:
                with open(self.fichier_taches, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)

                # Vérifier et corriger le format des tâches
                for task in self.tasks:
                    # Ajouter les clés manquantes
                    if "id" not in task:
                        task["id"] = self.tasks.index(task)
                    if "completed" not in task:
                        task["completed"] = False
                    if "date" not in task:
                        task["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    if "text" not in task:
                        task["text"] = "Tâche sans titre"

                # Sauvegarder le format corrigé
                self.save_tasks()

            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger: {e}")
                self.tasks = []
        else:
            self.tasks = []