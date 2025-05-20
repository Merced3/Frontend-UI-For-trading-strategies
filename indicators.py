def EMAs():
    """
    This function returns a JSON-like structure that defines the UI components
    for the EMA indicator for the card.
    """
    ui_setup = {
        'frontend': {
            'display_name': "EMAs",
            'button': {'placeholder': '+', 'result': 'add_row'}  # When clicked, add row to dropdown
        },
        'dropdown': [
            {
                'display_name': 'EMA',
                'inputfields': [
                    {'type': int, 'placeholder': 13},  # EMA number
                    {'type': str, 'placeholder': 'yellow'}  # EMA color
                ]
            }
        ]
    }
    return ui_setup

def SMAs():
    ui_setup = {
        'frontend': {
            'display_name': "SMAs",
            'button': {'placeholder': '+', 'result': 'add_row'}  # When clicked, add row to dropdown
        },
        'dropdown': [
            {
                'display_name': 'SMA',
                'inputfields': [
                    {'type': int, 'placeholder': 13},  # EMA number
                    {'type': str, 'placeholder': 'yellow'}  # EMA color
                ]
            }
        ]
    }
    return ui_setup

def RSI():
    """
    This function defines the UI components for the RSI indicator.
    """
    ui_setup = {
        'frontend': {
            'display_name': "RSI"
        },
        'dropdown': [
            {
                'display_name': 'RSI Period',
                'inputfields': [
                    {'type': int, 'placeholder': 14}  # RSI period (e.g., 14)
                ]
            },
            {
                'display_name': 'Upper Threshold',
                'inputfields': [
                    {'type': int, 'placeholder': 70}  # Overbought threshold (e.g., 70)
                ]
            },
            {
                'display_name': 'Lower Threshold',
                'inputfields': [
                    {'type': int, 'placeholder': 30}  # Oversold threshold (e.g., 30)
                ]
            },
            {
                'display_name': 'Color',
                'inputfields': [
                    {'type': str, 'placeholder': 'blue'}  # RSI line color
                ]
            }
        ]
    }
    return ui_setup
