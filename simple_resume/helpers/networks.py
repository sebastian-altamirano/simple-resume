"""Contains helpers to work with networks."""

from __future__ import annotations

from simple_resume.type_definitions.networks import NetworkInfo


def get_supported_networks() -> dict[str, NetworkInfo]:
    """Returns a dictionary with the supported networks.

    The keys can use the following formats:
    - Normalized network name (lowercase and without spaces). E.g. "googleplay" (Google Play),
    "googleplaystore" (Google Play Store), "mastodon" (Mastodon), "steam" (Steam), etc.
    - URL FQDN. E.g. "play.google.com", "mastodon.social" (a Mastodon server),
    "fosstodon.org" (another Mastodon server), "store.steampowered.com", "steamcommunity.com", etc.
    - URL FQDN without the TLD. E.g. "play.google", "mastodon", "fosstodon", "store.steampowered",
    "steamcommunity", etc.
    - URL Domain. E.g. "google", "mastodon", "fosstodon", "steampowered", "steamcommunity", etc.
    """
    google_play_info: NetworkInfo = {
        "icon_id": {"bootstrap": "google-play"},
        "label": "Google Play",
    }
    mastodon_info: NetworkInfo = {
        "icon_id": {"bootstrap": "mastodon"},
        "label": "Mastodon",
    }
    steam_info: NetworkInfo = {
        "icon_id": {"bootstrap": "steam"},
        "label": "Steam",
    }
    x_info: NetworkInfo = {
        "icon_id": {"bootstrap": "twitter-x"},
        "label": "X",
    }

    return {
        "amazon": {
            "icon_id": {"bootstrap": "amazon"},
            "label": "Amazon",
        },
        "behance": {
            "icon_id": {"bootstrap": "behance"},
            "label": "Behance",
        },
        "discord": {
            "icon_id": {"bootstrap": "discord"},
            "label": "Discord",
        },
        "dribbble": {
            "icon_id": {"bootstrap": "dribbble"},
            "label": "Dribbble",
        },
        "facebook": {
            "icon_id": {"bootstrap": "facebook"},
            "label": "Facebook",
        },
        "fosstodon.org": mastodon_info,
        "github": {
            "icon_id": {"bootstrap": "github"},
            "label": "GitHub",
        },
        "gitlab": {
            "icon_id": {"bootstrap": "gitlab"},
            "label": "GitLab",
        },
        "google": {
            "icon_id": {"bootstrap": "google"},
            "label": "Google",
        },
        "googleplay": google_play_info,
        "googleplaystore": google_play_info,  # Google Play is also known as Google Play Store.
        "hachyderm.io": mastodon_info,
        "instagram": {
            "icon_id": {"bootstrap": "instagram"},
            "label": "Instagram",
        },
        "linkedin": {
            "icon_id": {"bootstrap": "linkedin"},
            "label": "LinkedIn",
        },
        "mastodon": mastodon_info,
        "medium": {
            "icon_id": {"bootstrap": "medium"},
            "label": "Medium",
        },
        "mstdn.social": mastodon_info,
        "play.google": google_play_info,
        "quora": {
            "icon_id": {"bootstrap": "quora"},
            "label": "Quora",
        },
        "reddit": {
            "icon_id": {"bootstrap": "reddit"},
            "label": "Reddit",
        },
        "skype": {
            "icon_id": {"bootstrap": "skype"},
            "label": "Skype",
        },
        "snapchat": {
            "icon_id": {"bootstrap": "snapchat"},
            "label": "Snapchat",
        },
        "sourceforge": {
            "icon_id": {"bootstrap": "sourceforge"},
            "label": "SourceForge",
        },
        "spotify": {
            "icon_id": {"bootstrap": "spotify"},
            "label": "Spotify",
        },
        "stackoverflow": {
            "icon_id": {"bootstrap": "stack-overflow"},
            "label": "Stack Overflow",
        },
        "steam": steam_info,
        "steamcommunity": steam_info,
        "steampowered": steam_info,
        "substack": {
            "icon_id": {"bootstrap": "substack"},
            "label": "Substack",
        },
        "techhub.social": mastodon_info,
        "threads": {
            "icon_id": {"bootstrap": "threads"},
            "label": "Threads",
        },
        "tiktok": {
            "icon_id": {"bootstrap": "tiktok"},
            "label": "TikTok",
        },
        "twitch": {
            "icon_id": {"bootstrap": "twitch"},
            "label": "Twitch",
        },
        "twitter": x_info,  # Twitter is the previous name of X.
        "vimeo": {
            "icon_id": {"bootstrap": "vimeo"},
            "label": "Vimeo",
        },
        "wikipedia": {
            "icon_id": {"bootstrap": "wikipedia"},
            "label": "Wikipedia",
        },
        "x": x_info,
        "xbox": {
            "icon_id": {"bootstrap": "xbox"},
            "label": "Xbox",
        },
        "yelp": {
            "icon_id": {"bootstrap": "yelp"},
            "label": "Yelp",
        },
        "youtube": {
            "icon_id": {"bootstrap": "youtube"},
            "label": "YouTube",
        },
    }
