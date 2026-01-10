
# -*- coding: utf-8 -*-
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
import os

# -------------------------
# CHEMIN DE SAUVEGARDE
# -------------------------
TASKS_FILE = os.path.join(
    os.environ.get("SNAP_USER_DATA", "."),
    "tasks.json"
)

# S'assure que le dossier existe
os.makedirs(os.path.dirname(TASKS_FILE) or ".", exist_ok=True)


class LmrTaskApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # -------------------------
        # CONFIG FENÊTRE
        # -------------------------
        self.title("LmrTask")
        self.geometry("420x600")
        self.minsize(320, 420)

        # Thème par défaut
        ctk.set_appearance_mode("dark")           # Sombre
        ctk.set_default_color_theme("blue")       # Bleu

        # Couleur d'accent locale (boutons / hover)
        self.accent_colors = {
            "Bleu": "#1f6aa5",
            "Vert": "#2cc985",
            "Violet": "#a55eea",
            "Orange": "#ff8f1f",
            "Rouge": "#e05a5a",
            "Sarcelle": "#1abc9c",   # teal
            "Bleu foncé": "#144870", # custom pour "dark-blue"
        }
        self.current_accent = self.accent_colors["Bleu"]

        # -------------------------
        # BARRE DE MENU
        # -------------------------
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quitter", command=self.quit_app)
        menubar.add_cascade(label="Fichier", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="À propos", command=self.open_about)
        menubar.add_cascade(label="Aide", menu=helpmenu)
        self.config(menu=menubar)

        # -------------------------
        # TITRE
        # -------------------------
        self.title_label = ctk.CTkLabel(
            self,
            text="Mes Tâches 2025",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(12, 6))

        # -------------------------
        # SELECTEURS THÈME / COULEUR
        # -------------------------
        top_controls = ctk.CTkFrame(self)
        top_controls.pack(fill="x", padx=12, pady=(0, 8))

        # Thème (Sombre/Clair)
        self.theme_selector = ctk.CTkOptionMenu(
            top_controls,
            values=["Sombre", "Clair"],
            command=self.change_theme
        )
        self.theme_selector.set("Sombre")
        self.theme_selector.pack(side="left", padx=6, pady=8)

        # Couleur d'accent locale (n’affecte pas tout le thème)
        self.color_selector = ctk.CTkOptionMenu(
            top_controls,
            values=["Bleu", "Vert", "Violet", "Orange", "Rouge", "Sarcelle", "Bleu foncé"],
            command=self.change_color
        )
        self.color_selector.set("Bleu")
        self.color_selector.pack(side="right", padx=6, pady=8)

        # -------------------------
        # SAISIE + BOUTON AJOUT
        # -------------------------
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(fill="x", padx=12, pady=(8, 8))

        self.new_task_entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Qu'avez-vous à faire ?"
        )
        self.new_task_entry.pack(side="left", fill="x", expand=True, padx=(6, 4), pady=6)

        self.add_button = ctk.CTkButton(
            entry_frame,
            text="+",
            width=44,
            command=self.add_clicked,
            fg_color=self.current_accent,
            hover_color=self._hover_from(self.current_accent)
        )
        self.add_button.pack(side="left", padx=(4, 6), pady=6)

        # Séparateur
        
        # Séparateur visuel (fine ligne)
        sep = ctk.CTkFrame(self, height=1, fg_color="#3a3a3a")
        sep.pack(fill="x", padx=12, pady=8)
        # Évite que le frame se dilate verticalement
        sep.pack_propagate(False)


        # -------------------------
        # ZONE DES TÂCHES (SCROLL)
        # -------------------------
        self.tasks_frame = ctk.CTkScrollableFrame(self)
        self.tasks_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Charger les tâches existantes
        self.load_tasks()

    # -------------------------
    # UTILITAIRES
    # -------------------------
    @staticmethod
    def _hover_from(color_hex: str) -> str:
        """Crée une nuance un peu plus sombre pour le hover."""
        try:
            color_hex = color_hex.lstrip("#")
            r = max(int(color_hex[0:2], 16) - 20, 0)
            g = max(int(color_hex[2:4], 16) - 20, 0)
            b = max(int(color_hex[4:6], 16) - 20, 0)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return color_hex

    # -------------------------
    # PERSISTENCE
    # -------------------------
    def save_tasks(self):
        tasks = []
        # Chaque enfant de tasks_frame est un row_frame qui contient checkbox et bouton supprimer
        for row in self.tasks_frame.winfo_children():
            # On cherche le premier enfant de type CTkCheckBox
            for child in row.winfo_children():
                if isinstance(child, ctk.CTkCheckBox):
                    label = child.cget("text")
                    checked = bool(child.get())
                    tasks.append({"label": label, "checked": checked})
                    break
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)

    def load_tasks(self):
        if not os.path.exists(TASKS_FILE):
            return
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                tasks = json.load(f)
            for task in tasks:
                self.create_task(task.get("label", ""), task.get("checked", False))
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les tâches:\n{e}")

    # -------------------------
    # GESTION TÂCHES
    # -------------------------
    def delete_task(self, row_frame: ctk.CTkFrame):
        # Supprimer la ligne UI + sauvegarder
        row_frame.destroy()
        self.save_tasks()

    def create_task(self, label: str, checked: bool = False):
        if not label.strip():
            return

        row_frame = ctk.CTkFrame(self.tasks_frame)
        row_frame.pack(fill="x", padx=6, pady=4)
        row_frame.grid_columnconfigure(0, weight=1)
        row_frame.grid_columnconfigure(1, weight=0)

        # CheckBox
        var = tk.BooleanVar(value=checked)
        checkbox = ctk.CTkCheckBox(
            row_frame,
            text=label,
            variable=var,
            command=self.save_tasks,
            # Couleur d'accent appliquée au check
            fg_color=self.current_accent,
            hover_color=self._hover_from(self.current_accent)
        )
        checkbox.grid(row=0, column=0, sticky="w", padx=(8, 4), pady=8)

        # Bouton supprimer
        delete_btn = ctk.CTkButton(
            row_frame,
            text="🗑",
            width=36,
            fg_color="#cf3c3c",
            hover_color=self._hover_from("#cf3c3c"),
            command=lambda rf=row_frame: self.delete_task(rf)
        )
        delete_btn.grid(row=0, column=1, sticky="e", padx=(4, 8), pady=8)

    def add_clicked(self):
        text = self.new_task_entry.get().strip()
        if text:
            self.create_task(text, checked=False)
            self.new_task_entry.delete(0, tk.END)
            self.save_tasks()

    # -------------------------
    # THÈME & COULEUR
    # -------------------------
    def change_theme(self, value: str):
        # Sombre -> "dark" | Clair -> "light"
        mode = "dark" if value == "Sombre" else "light"
        ctk.set_appearance_mode(mode)

    def change_color(self, value: str):
        # Gestion accent local (boutons / checkboxes)
        self.current_accent = self.accent_colors.get(value, self.current_accent)

        # Optionnel: modifier le thème global pour 3 couleurs natives de CTk
        if value == "Bleu":
            ctk.set_default_color_theme("blue")
        elif value == "Vert":
            ctk.set_default_color_theme("green")
        elif value == "Bleu foncé":
            ctk.set_default_color_theme("dark-blue")

        # Appliquer l'accent sur les widgets existants
        # Bouton d'ajout
        self.add_button.configure(
            fg_color=self.current_accent,
            hover_color=self._hover_from(self.current_accent)
        )

        # Checkboxes existantes
        for row in self.tasks_frame.winfo_children():
            for child in row.winfo_children():
                if isinstance(child, ctk.CTkCheckBox):
                    child.configure(
                        fg_color=self.current_accent,
                        hover_color=self._hover_from(self.current_accent)
                    )

    # -------------------------
    # DIALOGS & QUIT
    # -------------------------
    def open_about(self):
        messagebox.showinfo(
            "À propos",
            "LmrTask\nVersion 1.0\n© 2025"
        )

    def quit_app(self):
        # La sauvegarde est faite à chaque action ; on peut fermer directement
        self.destroy()


if __name__ == "__main__":
    app = LmrTaskApp()
    app.mainloop()
