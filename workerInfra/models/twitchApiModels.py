from typing import Dict, List


class TwitchAuth:
    def __init__(
        self,
        access_token: str = "",
        expires_in: int = 0,
        token_type: str = "",
        client_id: str = "",
    ):
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.client_id = client_id
        pass


class TwitchChannel:
    # might go away
    def __init__(self, obj: Dict = {}):
        self.broadcaster_language: str = obj.get("broadcaster_language")
        self.display_name: str = obj.get("display_name")
        self.game_id: int = int(obj.get("game_id"))
        self.id: int = int(obj.get("id"))
        self.is_live: bool = bool(obj.get("is_live"))
        self.tag_ids: List[str] = obj.get("tag_ids")
        self.thumbnail_url: str = str(obj.get("thumbnail_url"))
        self.title: str = str(obj.get("title"))
        self.started_at: str = str(obj.get("started_at"))
        self.game_data = TwitchGameData()


class TwitchUser:
    def __init__(self, obj: Dict):
        self.id = obj.get("id")
        self.login = obj.get("login")
        self.display_name = obj.get("display_name")
        self.type = obj.get("type")
        self.broadcaster_type = obj.get("broadcaster_type")
        self.description = obj.get("description")
        self.profile_image_url = obj.get("profile_image_url")
        self.offline_image_url = obj.get("offline_image_url")
        self.view_count = obj.get("view_count")


class TwitchVideo:
    def __init__(self, obj: Dict):
        self.id = obj.get("id")
        self.user_id = obj.get("user_id")
        self.user_name = obj.get("user_name")
        self.title = obj.get("title")
        self.description = obj.get("description")
        self.created_at = obj.get("created_at")
        self.published_at = obj.get("published_at")
        self.url = obj.get("url")
        self.thumbnail_url = obj.get("thumbnail_url")
        self.viewable = obj.get("viewable")
        self.view_count = obj.get("view_count")
        self.language = obj.get("language")
        self.type = obj.get("type")
        self.duration = obj.get("duration")
        pass


class TwitchClip:
    def __init__(self, obj: Dict = {}):
        self.id = obj.get("id")
        self.url = obj.get("url")
        self.embed_url = obj.get("embed_url")
        self.broadcaster_id = obj.get("broadcaster_id")
        self.broadcaster_name = obj.get("broadcaster_name")
        self.creator_id = obj.get("creator_id")
        self.creator_name = obj.get("creator_name")
        self.video_id = obj.get("video_id")
        self.game_id = obj.get("game_id")
        self.language = obj.get("language")
        self.title = obj.get("title")
        self.view_count = obj.get("view_count")
        self.created_at = obj.get("created_at")
        self.thumbnail_url = obj.get("thumbnail_url")
        pass


class TwitchGameData:
    def __init__(self, obj: Dict = {}):
        self.id = 0
        try:
            self.id = int(obj.get("id"))
        except Exception as e:
            print(f"TwitchGameData Error: {e}")
            self.id = 0

        self.name: str = obj.get("name")
        self.box_art_url: str = obj.get("box_art_url")
        pass


class TwitchStream:
    def __init__(self, obj: Dict = {}):
        self.id = obj.get("id")
        self.user_id = obj.get("user_id")
        self.user_name = obj.get("user_name")
        self.game_id = obj.get("game_id")
        self.type = obj.get("type")
        self.title = obj.get("title")
        self.viewer_count = obj.get("viewer_count")
        self.started_at = obj.get("started_at")
        self.language = obj.get("language")
        self.thumbnail_url = obj.get("thumbnail_url")
        self.tags_ids = obj.get("tag_ids")
