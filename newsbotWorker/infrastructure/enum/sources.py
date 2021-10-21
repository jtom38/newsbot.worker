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

    @staticmethod
    def fromString(item: str):
        if item == 'finalfantasyxiv': return SourcesSource.FINALFANTASYXIV
        elif item == 'phantasystaronline2': return SourcesSource.PHANTASYSTARONLINE2
        elif item == "youtube": return SourcesSource.YOUTUBE
        elif item == 'pokemongohub': return SourcesSource.POKEMONGO
        elif item == 'reddit': return SourcesSource.REDDIT
        elif item == "rss": return SourcesSource.RSS
        elif item == 'twitch': return SourcesSource.TWITCH
        elif item == 'twitter': return SourcesSource.TWITTER
        elif item == 'instagram': return SourcesSource.INSTAGRAM
        else: return SourcesSource.INVALID