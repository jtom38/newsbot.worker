from enum import Enum


class SourcesEnum(Enum):
    """
    This Enum maps to Sources().source
    """
    FINALFANTASYXIV = 'finalfantasyxiv'
    PHANTASYSTARONLINE2 = 'phantasystaronline2'
    YOUTUBE = 'youtube'
    POKEMONGO = 'pokemongohub'
    REDDIT = 'reddit'
    RSS = 'rss'
    TWITCH = 'twitch'
    TWITTER = 'twitter'
    INSTAGRAM = 'instagram'
    INVALID = 'invalid'
