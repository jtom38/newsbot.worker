from dataclasses import dataclass

@dataclass
class TwitterSettings():
    ignoreRetweet: bool
    preferedLanguage: str
    #def __init__(self):
    #    self.ignoreRetweet: bool = c.findBool("twitter.ignore.retweet")
    #    self.preferedLanguage: str = c.find("twitter.preferred.lang")
