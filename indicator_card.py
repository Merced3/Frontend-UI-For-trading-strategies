import tkinter as tk
from tkinter import ttk

class IndicatorCard(tk.Frame):
    def __init__(self, parent, indicator_name="Indicator Name", ui_setup=None, **kwargs):
        super().__init__(parent, **kwargs)

        # Save ui_setup for later use
        self.ui_setup = ui_setup
        
        # Configure card appearance
        self.config(bg="#e0e0e0", bd=2, relief="groove", padx=10, pady=10)

        # Dropdown toggle button (far left)
        self.dropdown_button = ttk.Button(self, text=">", command=self.toggle_card_dropdown)
        self.dropdown_button.grid(row=0, column=0, padx=(5, 5), sticky="w")

        # Indicator Label (next to the dropdown button)
        self.indicator_label = ttk.Label(self, text=indicator_name, font=("Helvetica", 14, "bold"))
        self.indicator_label.grid(row=0, column=1, sticky="w", padx=5)
        
        # "+" Button (far right if present in frontend)
        if ui_setup and 'button' in ui_setup['frontend']:
            add_button = ttk.Button(self, text=ui_setup['frontend']['button']['placeholder'], command=self.add_row)
            add_button.grid(row=0, column=4, padx=(10, 0), sticky="e")

        # Delete Button (far right, next to the "+")
        delete_button = ttk.Button(self, text="X", command=self.delete_card, width=2)
        delete_button.grid(row=0, column=5, padx=(5, 5), sticky="e")
        
        # Create the dropdown frame for dynamic rows (hidden by default)
        self.dropdown_frame = tk.Frame(self, bg="#f5f5f5")
        self.dropdown_frame.grid(row=1, column=0, columnspan=5, sticky="ew", pady=(10, 0))
        self.dropdown_frame.grid_remove()  # Hidden by default

        # If there are predefined dropdown rows (like RSI), add them directly
        if 'dropdown' in ui_setup and len(ui_setup['dropdown']) > 0:
            self.populate_dropdown_initially(ui_setup['dropdown'])

    def build_ui(self, ui_setup):
        """Dynamically create the UI based on the ui_setup structure."""
        dropdown_config = ui_setup['dropdown']

        # Populate dropdown fields immediately for certain indicators (like RSI)
        if dropdown_config:
            self.add_row(dropdown_config)

    def populate_dropdown_initially(self, dropdown_config):
        """Immediately populate dropdown rows (e.g., for RSI or predefined EMAs)."""
        for i, row_config in enumerate(dropdown_config):
            self.add_predefined_row(i, row_config)

    def add_predefined_row(self, row_index, row_config):
        """Add a predefined row to the dropdown for indicators like RSI or others."""
        display_name = row_config['display_name']

        # Append the row number if the indicator has a '+' button (for EMA, SMA, etc.)
        if 'button' in self.ui_setup['frontend']:
            display_name = f"{display_name} {row_index + 1}"
        
        # Add the label
        ttk.Label(self.dropdown_frame, text=f"{display_name}:").grid(row=row_index, column=0, sticky="w", padx=5)

        # Loop through all input fields in the row_config and create corresponding input fields
        for j, field in enumerate(row_config['inputfields']):
            input_type, placeholder = field['type'], field['placeholder']

            # Create Entry field with a placeholder
            entry = ttk.Entry(self.dropdown_frame)
            entry.grid(row=row_index, column=j + 1, padx=(10, 0))

            # Set placeholder for the entry
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>", lambda e, ph=placeholder: self.clear_placeholder(e, ph))
            entry.bind("<FocusOut>", lambda e, ph=placeholder: self.set_placeholder(e, ph))

    def add_row(self, dropdown_config=None):
        """Add a new row to the dropdown dynamically (e.g., for EMAs/SMAs)."""
        # Show dropdown if it's hidden
        self.dropdown_frame.grid()

        # Calculate the current number of rows
        num_rows = len(self.dropdown_frame.winfo_children()) // 3  # Assuming 3 widgets per row

        # If no config is provided, use the default config
        dropdown_config = dropdown_config or self.ui_setup['dropdown']

        # Loop through the dropdown rows and add all fields dynamically
        for i, field in enumerate(dropdown_config):
            display_name = field['display_name']
            input_fields = field['inputfields']

            # Add label for the row
            ttk.Label(self.dropdown_frame, text=f"{display_name} {num_rows + 1}:").grid(row=num_rows, column=0, sticky="w", padx=5)

            # Add input fields from dropdown config dynamically
            for j, field_config in enumerate(input_fields):
                placeholder = field_config['placeholder']

                # Create Entry field with proper validation
                entry = ttk.Entry(self.dropdown_frame)
                entry.grid(row=num_rows, column=j + 1, padx=(10, 0))

                # Set placeholder for each field
                entry.insert(0, placeholder)
                entry.bind("<FocusIn>", lambda e, ph=placeholder: self.clear_placeholder(e, ph))
                entry.bind("<FocusOut>", lambda e, ph=placeholder: self.set_placeholder(e, ph))

    def clear_placeholder(self, event, placeholder):
        """Clear the placeholder when the entry is clicked."""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)

    def set_placeholder(self, event, placeholder):
        """Restore placeholder if entry is empty when it loses focus."""
        if event.widget.get() == "":
            event.widget.insert(0, placeholder)

    def toggle_card_dropdown(self):
        """Toggle the dropdown content visibility."""
        if self.dropdown_frame.winfo_ismapped():
            self.dropdown_frame.grid_remove()
            self.dropdown_button.config(text=">")  # Change button text back
        else:
            self.dropdown_frame.grid()  # Show the dropdown frame
            self.dropdown_button.config(text="v")  # Change button text to dropdown indicator

    def delete_card(self):
        """Remove the card from its parent."""
        self.destroy()