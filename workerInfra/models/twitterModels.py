from dataclasses import dataclass


@dataclass
class TwitterSettings():
    ignoreRetweet: bool
    preferedLanguage: str
