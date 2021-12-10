from enum import Enum


class EnvEnum(Enum):
    YOUTUBEDEBUGSCREENSHOTS = 'NEWSBOT_YOUTUBE_DEBUG_SCREENSHOTS'

    REDDITALLOWNSFW = 'NEWSBOT_REDDIT_ALLOW_NSFW'
    REDDITPULLTOP = 'NEWSBOT_REDDIT_PULL_TOP'
    REDDITPULLHOT = 'NEWSBOT_REDDIT_PULL_HOT'

    TWITCHCLIENTID = 'NEWSBOT_TWITCH_CLIENT_ID'
    TWITCHCLIENTSECRET = 'NEWSBOT_TWITCH_CLIENT_SECRET'
    TWITCHMONITORCLIPS = 'NEWSBOT_TWITCH_MONITOR_CLIPS'
    TWITCHMONITORLIVESTREMS = 'NEWSBOT_TWITCH_MONITOR_LIVE_STREAMS'
    TWITCHMONITORVOD = 'NEWSBOT_TWITCH_MONITOR_VOD'

    TWITTERAPIKEY = 'NEWSBOT_TWITTER_API_KEY'
    TWITTERAPIKEYSECRET = 'NEWSBOT_TWITTER_API_KEY_SECRET'
    TWITTERPREFERREDLANG = 'NEWSBOT_TWITTER_PREFERRED_LANG'
    TWITTERIGNORERETWEET = 'NEWSBOT_TWITTER_IGNORE_RETWEET'

    POKEMONGOENABLED = 'NEWSBOT_POGO_ENABLED'

    PSO2ENABLED = 'NEWSBOT_PSO2_ENABLED'

    FFXIVALL = 'NEWSBOT_FFXIV_ALL'
    FFXIVTOPICS = 'NEWSBOT_FFXIV_TOPICS'
    FFXIVNOTICES = 'NEWSBOT_FFXIV_NOTICES'
    FFXIVMAINTENANCE = 'NEWSBOT_FFXIV_MAINTENANCE'
    FFXIVUPDATES = 'NEWSBOT_FFXIV_UPDATES'
    FFXIVSTATUS = 'NEWSBOT_FFXIV_STATUS'
