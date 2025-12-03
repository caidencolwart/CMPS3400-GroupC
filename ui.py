def load_ui_settings(filepath="ui.txt"):
    """
    Reads simple KEY=VALUE settings from a text file.
    Returns a dictionary.
    """
    
    settings = {}

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)
            settings[key.strip()] = value.strip()

    return settings
