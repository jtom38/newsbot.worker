from typing import List


class RedditPostPreviewImage():
    """
    This contains the images attached with the post
    """
    id: str
    imageUrl: str
    imageWidth: int
    imageHeight: int


class RedditPostPreview():
    """
    This contains the preview items of a reddit object.
    """
    images: List[RedditPostPreviewImage]


class RedditPostMediaRedditVideo():
    """
    This contains the information about the video hosted on the reddit platform
    """
    bitrateKbps: int
    fallbackUrl: str
    height: int
    width: int
    duration: int
    transcodingStatus: str


class RedditPostMedia():
    """
    This contains the video details attached to the post
    """
    reddit_video = RedditPostMediaRedditVideo()


class RedditPost():
    """
    This contains a subset of all the properties that can be found in the Reddit Json.  
    """
    subreddit: str
    #subreddit_id: str
    selftext: str
    author: str
    #saved: bool
    title: str
    nsfw: bool 
    #locked: bool
    #numberOfComments: int
    permalink: str
    thumbnail: str
    preview: List[RedditPostPreview]
    media: RedditPostMedia
    pass

    def __init__(self, data: dict) -> None:
        self.subreddit = data['subreddit']
        self.selftext = data['selftext']
        self.author = data['author']
        self.permalink = data['permalink']
        self.nsfw = data['over_18']
        self.thumbnail = data['thumbnail']
        if len(data['preview']) == 0:
            self.preview = list()
        else:
            self.preview = self.__convertPreview__(data['preview'])

        if len(data['media']) == 0:
            self.media = RedditPostMedia()
        else:
            self.media = self.__convertPreview__(data['media'])

    def __convertPreview__(self, preview: dict) -> List[RedditPostPreview]:
        l = list()
        if len(preview) == 0:
            return l

        try:
            for i in preview:
                p = RedditPostPreview()
                p.id = i['id']
                p.imageHeight = i['source']['height']
                p.imageWidth = i['source']['width']
                p.imageUrl = i['source']['url']
                l.append(p)

            return l
        except:
            pass
        
    def __convertPreviewImages__(self):
        pass

    def __convertMedia__(self, media: dict) -> None:
        r = RedditPostMedia()
        if len(media) > 0:

            return r
        try:
            m = media['reddit_video']
            r.reddit_video.bitrateKbps = m['bitrate_kbps']
            r.reddit_video.duration = m['duration']
            r.reddit_video.fallbackUrl = m['fallback_url']
            r.reddit_video.height = m['height']
            r.reddit_video.width = m['width']
            r.reddit_video.transcodingStatus = m['transcoding_status']
            return r
        except:
            pass