import json

class ThemeManager:
    def __init__(self, theme_file='themes.json'):
        self.theme_file = theme_file
        self.themes = self.load_themes()
        self.current_theme = "light"  # Default to light theme

    def load_themes(self):
        """Load theme configuration from JSON file."""
        with open(self.theme_file, 'r') as file:
            return json.load(file)

    def get_theme(self):
        """Return the current theme."""
        return self.themes[self.current_theme]

    def switch_theme(self, theme_name):
        """Switch to the given theme."""
        if theme_name in self.themes:
            self.current_theme = theme_name
        else:
            print(f"Theme '{theme_name}' not found, using default.")
        return self.get_theme()
