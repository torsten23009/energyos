"""A saved options form is a complete mapping, not a partial overlay."""
ROLES = ("pv_roof", "pv_carport", "pv", "grid", "grid_import", "grid_export", "battery", "soc", "load", "ev")


def effective_config(entry):
    """Do not resurrect removed source roles from the initial config entry."""
    return dict(entry.options if entry.options else entry.data)
