"""
Module de configuration
Gère les thèmes et les paramètres globaux de l'application
"""


class AppConfig:
    """Classe de configuration de l'application"""

    def __init__(self):
        # Polices
        self.POLICE = ("Segoe UI", 10)
        self.POLICE_TITRE = ("Segoe UI", 14, "bold")
        self.POLICE_GRANDE = ("Segoe UI", 12)

        # Thèmes disponibles
        self.themes = {
            "clair": {
                "fond": "#f0f4f8",
                "cadre": "#ffffff",
                "texte": "#2d3748",
                "accent": "#4299e1",
                "bouton": "#e2e8f0",
                "hover": "#cbd5e0",
                "success": "#48bb78",
                "danger": "#f56565",
                "warning": "#ed8936"
            },
            "sombre": {
                "fond": "#1a202c",
                "cadre": "#2d3748",
                "texte": "#e2e8f0",
                "accent": "#4299e1",
                "bouton": "#4a5568",
                "hover": "#718096",
                "success": "#48bb78",
                "danger": "#fc8181",
                "warning": "#f6ad55"
            }
        }

        # Thème actuel
        self.theme_actuel = "clair"
        self.style = self.themes[self.theme_actuel].copy()

    def toggle_theme(self):
        """Bascule entre le thème clair et sombre"""
        if self.theme_actuel == "clair":
            self.theme_actuel = "sombre"
        else:
            self.theme_actuel = "clair"

        self.style = self.themes[self.theme_actuel].copy()

    def get_style(self):
        """Retourne le dictionnaire de style actuel"""
        return self.style

    def get_theme_name(self):
        """Retourne le nom du thème actuel"""
        return self.theme_actuel