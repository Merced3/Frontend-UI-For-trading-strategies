import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import ttkbootstrap as tb
from theme_manager import ThemeManager
from indicator_card import IndicatorCard
import indicators

class BacktesterApp(tb.Window):
    def __init__(self):
        # Initialize ttkbootstrap Window
        super().__init__(themename="cosmo", title="Backtester")
        
        # Initialize theme manager and load the default (light) theme
        self.theme_manager = ThemeManager()
        self.theme = self.theme_manager.get_theme()

        # Set window size
        self.attributes('-fullscreen', False)
        
        # State variables for the collapsible config section
        self.config_visible = True
        self.config_collapsed_width = 0
        self.config_expanded_width = 300
        self.config_arrow_button_width = 3

        # Create UI components first
        self.create_button_styles()  # Define the button styles for hover, pressed, etc.
        self.configure_ui()          # Create the UI components
        self.apply_theme()           # Apply the theme after creating the UI

    def create_button_styles(self):
        """Create custom styles for buttons with hover and active state colors."""
        style = ttk.Style()

        # Define a custom style for the theme switch button
        style.configure("Switch.TButton",
                        background=self.theme['button_bg'],  # Default background
                        foreground=self.theme['button_fg'],  # Default foreground
                        relief="flat",
                        padding=10)
        # Change the hover color and active color for the Switch button
        style.map("Switch.TButton",
                background=[("active", self.theme['button_active_bg']),  # Active color from JSON
                            ("!disabled", self.theme['button_hover_bg'])],  # Hover color from JSON
                foreground=[("active", "#ffffff"),  # Foreground when pressed
                            ("!disabled", "#ffffff")])  # Foreground on hover

        # Define a custom style for the config collapse button
        style.configure("Collapse.TButton",
                        background=self.theme['arrow_button_bg'],  # Default background from JSON
                        foreground=self.theme['arrow_button_fg'],  # Default foreground from JSON
                        relief="flat",
                        padding=5)
        # Change the hover color and active color for the Collapse button
        style.map("Collapse.TButton",
                background=[("active", self.theme['collapse_active_bg']),  # Active color from JSON
                            ("!disabled", self.theme['collapse_hover_bg'])],  # Hover color from JSON
                foreground=[("active", "#ffffff"),
                            ("!disabled", "#ffffff")])

    def configure_ui(self):
        # Create the layout with collapsible config section
        self.create_config_section()
        self.create_chart_section()
        self.create_logs_section()

        # Set up grid configuration to ensure proper resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=3)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)

    def apply_theme(self):
        """Apply the current theme to the UI elements dynamically."""
        # Config section
        self.config_frame.config(bg=self.theme['frame_bg'])
        self.top_frame.config(bg=self.theme['frame_bg'])
        self.bottom_frame.config(bg=self.theme['frame_bg'])

        # Logs section
        self.logs_frame.config(bg=self.theme['frame_bg'])
        self.log_text.config(bg=self.theme['log_bg'], fg=self.theme['log_fg'])

        # Settings window
        if hasattr(self, 'settings_window'):
            self.settings_window.config(bg=self.theme['frame_bg'])
        
        # Find Indicator window
        if hasattr(self, 'indicator_window'):
            self.indicator_window.config(bg=self.theme['frame_bg'])
        
        # Indicator cards in config section
        for widget in self.bottom_frame.winfo_children():
            if isinstance(widget, IndicatorCard):
                widget.config(bg=self.theme['card_bg'])  # Apply card background color
                widget.indicator_label.config(fg=self.theme['fg_color'])  # Card label text color

                # Set dropdown frame color
                widget.dropdown_frame.config(bg=self.theme['dropdown_bg'])
                
                # Apply colors to entries and buttons inside the card
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Entry):
                        child.config(style="Custom.TEntry")
                    elif isinstance(child, ttk.Button):
                        child.config(style="CardButton.TButton")

        # Update styles for ttk widgets
        style = ttk.Style()

        # Update global label style
        style.configure("TLabel", foreground=self.theme['fg_color'], background=self.theme['frame_bg'])

        # Update entry style
        style.configure("Custom.TEntry",
                        fieldbackground=self.theme['entry_bg'],  # Background for text entries
                        foreground=self.theme['entry_fg'])  # Foreground (text) color

        # Card buttons (e.g., "+" button and delete "X" button)
        style.configure("CardButton.TButton",
                        background=self.theme['button_bg'],
                        foreground=self.theme['button_fg'])

        # Other button styles (like the switch theme button)
        self.create_button_styles()  # Reapply button colors dynamically
        
        # Reapply button styles explicitly (like Collapse button)
        self.arrow_button.config(style="Collapse.TButton")

    def create_config_section(self):
        # Create the main config frame
        self.config_frame = tk.Frame(self, width=self.config_expanded_width, height=400, padx=10, pady=10)
        self.config_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid rows to allocate space for top and bottom sections
        self.config_frame.grid_rowconfigure(0, weight=0)  # Top section (fixed height)
        self.config_frame.grid_rowconfigure(1, weight=1)  # Bottom section (expands)
        self.config_frame.grid_columnconfigure(0, weight=1)

        # --- Top Portion ---
        self.top_frame = tk.Frame(self.config_frame, padx=10, pady=5)
        self.top_frame.grid(row=0, column=0, sticky="ew")

        # Label for "Config Settings" on the left
        self.config_label = ttk.Label(self.top_frame, text="Config Settings", font=("Helvetica", 16, "bold"))
        self.config_label.pack(side=tk.LEFT, padx=10)

        # Settings button on the right
        settings_button = ttk.Button(self.top_frame, text="⚙", command=self.open_settings_window)
        settings_button.pack(side=tk.RIGHT, padx=10)

        # --- Bottom Portion ---
        self.bottom_frame = tk.Frame(self.config_frame, padx=10, pady=5)
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")

        # --- Collapse Button (Separate from Top/Bottom Portions) ---
        self.arrow_button = ttk.Button(self, text="◀", style="Collapse.TButton", command=self.toggle_config_section, width=self.config_arrow_button_width)
        self.arrow_button.grid(row=0, column=1, sticky="nsew")

    def open_settings_window(self):
        """Open a pop-up window for settings."""
        settings_window = tk.Toplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("300x200")

        # Add the switch theme button inside the settings window
        switch_button = ttk.Button(settings_window, text="Switch Theme", style="Switch.TButton", command=self.switch_theme)
        switch_button.pack(pady=20)

        # Add the Find Indicator button to open a new window
        find_indicator_button = ttk.Button(settings_window, text="Find Indicator", command=self.open_find_indicator_window)
        find_indicator_button.pack(pady=10)
    
    def toggle_config_section(self):
        """Toggles the config section between collapsed and expanded."""
        if self.config_visible:
            # Collapse the config section
            self.config_frame.grid_forget()
            self.config_visible = False
            self.arrow_button.config(text="▶")  # Change arrow to point left
            self.grid_columnconfigure(0, weight=0, minsize=self.config_collapsed_width)
        else:
            # Expand the config section
            self.config_frame.grid(row=0, column=0, sticky="nsew")
            self.config_visible = True
            self.arrow_button.config(text="◀")  # Change arrow to point right
            self.grid_columnconfigure(0, weight=1, minsize=self.config_expanded_width)

    def open_find_indicator_window(self):
        """Open a pop-up window to search and find indicators."""
        indicator_window = tk.Toplevel(self)
        indicator_window.title("Find Indicator")
        indicator_window.geometry("600x700")

        # Search bar
        search_var = tk.StringVar()
        search_entry = ttk.Entry(indicator_window, textvariable=search_var, width=30)
        search_entry.pack(pady=10)

        # Listbox for indicators
        listbox = tk.Listbox(indicator_window, height=10)
        available_indicators = [func for func in dir(indicators) if callable(getattr(indicators, func)) and not func.startswith("__")]
        for indicator in available_indicators:
            listbox.insert(tk.END, indicator)
        listbox.pack(pady=10)

        # Bind listbox selection to an event
        listbox.bind('<<ListboxSelect>>', lambda event: self.select_indicator(event, listbox, indicator_window))

    def select_indicator(self, event, listbox, indicator_window):
        """Callback when an indicator is selected from the list."""
        selection = listbox.curselection()
        if selection:
            selected_indicator = listbox.get(selection[0])

            # Get the function from indicators.py dynamically
            indicator_func = getattr(indicators, selected_indicator)
            ui_setup = indicator_func()  # Call the function to get its UI setup

            # Add the selected indicator card to the main window
            self.add_indicator_card(selected_indicator, ui_setup)

            # Close the indicator window
            indicator_window.destroy()

    def add_indicator_card(self, indicator_name, ui_setup):
        """Add a new indicator card to the bottom frame."""
        indicator_card = IndicatorCard(self.bottom_frame, indicator_name=indicator_name, ui_setup=ui_setup)
        indicator_card.pack(fill="x", pady=10)

    def create_chart_section(self):
        chart_frame = ttk.Frame(self, width=600, height=400, relief="flat", padding=10)
        chart_frame.grid(row=0, column=2 if self.config_visible else 1, sticky="nsew")

        # Create a placeholder matplotlib chart
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot([0, 1, 2, 3], [1, 2, 0, 4], color="#ff5722")

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def create_logs_section(self):
        # Create a frame for logs with theme-based background
        self.logs_frame = tk.Frame(self, height=200, bg=self.theme['frame_bg'], padx=10, pady=10)
        self.logs_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        # Label for logs section
        logs_label = ttk.Label(self.logs_frame, text="Logs", font=("Helvetica", 16, "bold"))
        logs_label.pack(side=tk.TOP, pady=10)

        # Logs text box
        self.log_text = tk.Text(self.logs_frame, height=10, bg=self.theme['log_bg'], fg=self.theme['log_fg'], font=("Courier", 10), state='disabled', padx=10, pady=10, relief="flat", wrap="none")
        self.log_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def switch_theme(self):
        """Switch between light and dark themes."""
        new_theme = "dark" if self.theme_manager.current_theme == "light" else "light"
        self.theme = self.theme_manager.switch_theme(new_theme)  # Switch and load the new theme
        self.apply_theme()  # Apply the new theme to the UI

    def log_message(self, message):
        """Logs a message to the Logs section."""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state='disabled')

# Run the application
if __name__ == "__main__":
    app = BacktesterApp()
    app.mainloop()
