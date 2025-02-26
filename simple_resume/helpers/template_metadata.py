"""Contains helpers to work with the metadata of the templates."""

from __future__ import annotations

from simple_resume.type_definitions.template_metadata import ColorSystem


def get_colors_by_color_system(color_system: ColorSystem) -> set[str]:
    """Get the colors for a given color system."""
    match color_system:
        case ColorSystem.OpenColor:
            return get_open_color_colors()
        case ColorSystem.RadixColors:
            return get_radix_colors_colors()
        case ColorSystem.ReasonableColors:
            return get_reasonable_colors_colors()


def get_open_color_colors() -> set[str]:
    """Get the colors of the Open Color color system."""
    return {
        "blue",
        "cyan",
        "grape",
        "gray",
        "green",
        "indigo",
        "lime",
        "orange",
        "pink",
        "red",
        "teal",
        "violet",
        "yellow",
    }


def get_radix_colors_colors() -> set[str]:
    """Get the colors of the Radix Colors color system."""
    return {
        "amber",
        "blue",
        "bronze",
        "brown",
        "crimson",
        "cyan",
        "gold",
        "grass",
        "gray",
        "green",
        "indigo",
        "iris",
        "jade",
        "lime",
        "mauve",
        "mint",
        "olive",
        "orange",
        "pink",
        "plum",
        "purple",
        "red",
        "ruby",
        "sage",
        "sand",
        "sky",
        "slate",
        "teal",
        "tomato",
        "violet",
        "yellow",
    }


def get_reasonable_colors_colors() -> set[str]:
    """Get the colors of the Reasonable Colors color system."""
    return {
        "amber",
        "aquamarine",
        "azure",
        "blue",
        "cerulean",
        "chartreuse",
        "cinnamon",
        "cyan",
        "emerald",
        "gray",
        "green",
        "indigo",
        "lime",
        "magenta",
        "orange",
        "pink",
        "powder",
        "purple",
        "raspberry",
        "red",
        "rose",
        "sky",
        "teal",
        "violet",
        "yellow",
    }
