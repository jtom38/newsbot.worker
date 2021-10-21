from typing import List
from dataclasses import dataclass

@dataclass
class EnvDiscordDetails:
    name: str
    server: str
    channel: str
    url: str


@dataclass
class EnvRssDetails:
    """
    This class is a collection object that holds values, nothing more.
    """
    name: str
    url: str
    discordLinkName: List[str]


@dataclass
class EnvYoutubeConfig:
    debugScreenshots: bool

@dataclass
class EnvYoutubeDetails:
    """
    This class is a collection object that holds values, nothing more.
    """
    name: str
    url: str
    discordLinkName: List[str]


@dataclass
class EnvRedditConfig:
    allowNsfw: bool
    pullTop: bool
    pullHot: bool


@dataclass
class EnvRedditDetails:
    subreddit: str
    discordLinkName: List[str]
    

@dataclass
class EnvTwitchConfig:
    clientId: str
    clientSecret: str
    monitorClips: bool
    monitorLiveStreams: bool
    monitorVod: bool


@dataclass
class EnvTwitchDetails:
    user: str
    discordLinkName: str
    

@dataclass
class EnvTwitterConfig:
    """
    This is a collection object.  
    To get access to this, call Env().twitter_config
    """
    apiKey: str
    apiKeySecret: str
    preferredLang: str
    ignoreRetweet: bool


@dataclass
class EnvTwitterDetails:
    name: str
    type: str
    discordLinkName: List[str]


@dataclass
class EnvInstagramDetails:
    name: str
    type: str
    discordLinkName: List[str]


@dataclass
class EnvInstagramDetails:
    name: str
    type: str
    discordLinkName: List[str]


@dataclass
class EnvPokemonGoDetails:
    enabled: bool
    discordLinkName: List[str]


@dataclass
class EnvPhantasyStarOnline2Details:
    enabled: bool
    discordLinkName: List[str]


@dataclass
class EnvFinalFantasyXIVDetails:
    discordLinkName: List[str]
    topicsEnabled: bool = False
    noticesEnabled: bool = False
    maintenanceEnabled: bool = False
    updateEnabled: bool = False
    statusEnabled: bool = False

