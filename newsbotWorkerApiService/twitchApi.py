from newsbotWorkerApiInfra.models import TwitchAuth, TwitchChannel, TwitchClip, TwitchGameData, TwitchStream, TwitchUser, TwitchVideo
from newsbotWorkerApiService.logger import Logger
from requests import get, post
from json import loads
from typing import List, Dict
from os import getenv

class TwitchAPI:
    def __init__(self):
        self.uri: str = "https://id.twitch.tv"
        self.apiUri: str = "https://api.twitch.tv/helix"
        pass

    def auth(self) -> TwitchAuth:
        """
        https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#oauth-client-credentials-flow
        """
        client_id = str(getenv("NEWSBOT_TWITCH_CLIENT_ID"))
        client_secret = str(getenv("NEWSBOT_TWITCH_CLIENT_SECRET"))
        scopes = "user:read:email"
        uri = f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials&scopes={scopes}"

        res = post(uri)
        if res.status_code != 200:
            Logger(__class__).error(res.text)
            raise Exception("Failed to auth with Twitch.  Make sure NEWSBOT_TWITCH_CLIENT_ID anf NEWSBOT_TWITCH_CLIENT_SECRET are defined.")
        else:
            token = loads(res.content)
            try:
                o = TwitchAuth(
                    access_token=token["access_token"],
                    expires_in=token["expires_in"],
                    token_type=token["token_type"],
                    client_id=client_id,
                )
            except Exception as e:
                raise Exception("Failed to auth with Twitch.  Make sure NEWSBOT_TWITCH_CLIENT_ID anf NEWSBOT_TWITCH_CLIENT_SECRET are defined.")
            return o

    def getUser(self, auth: TwitchAuth, username: str) -> None:
        uri = f"{self.apiUri}/users?login={username}"
        res = get(uri, headers=self.__header__(auth))
        if res.status_code != 200:
            Logger().error(
                f"Failed to get user information. StatusCode: {res.status_code}, Error: {res.text}"
            )
        else:
            json = loads(res.content)
            if len(json["data"]) == 1:
                user = TwitchUser(json["data"][0])
            else:
                Logger().error(f"Did not get a usable object.")
                user = TwitchUser({})
            return user

    def searchForUser(self, auth: TwitchAuth, username: str = "") -> None:
        if username == "":
            Logger().error(
                f"Request to search for user was requested but no user was given."
            )
        else:
            uri: str = f"{self.apiUri}/search/channels?query={username}"
            header = self.__header__(auth)
            res = get(uri, headers=header)
            if res.status_code != 200:
                Logger().error(
                    f"Attempted to pull user information but failed. status_code: {res.status_code}, output: {res.text}"
                )
            else:
                l = list()
                j = loads(res.content)
                for i in j["data"]:
                    # Convert the Json date to an object
                    stream = TwitchChannel(i)
                    # Get the game details
                    # stream.game_data = self.getGame(auth,stream.game_id)
                    # video = self.getVideos(auth=auth, user_id=stream.id)
                    l.append(stream)
                return l

    def getGame(self, auth: TwitchAuth, game_id: int) -> TwitchGameData:
        uri = f"{self.apiUri}/games?id={game_id}"
        headers = self.__header__(auth)
        res = get(uri, headers=headers)

        if res.status_code != 200:
            Logger().error(
                f"Attempted to get Twich Game data but failed on game_id: {game_id}. output: {res.text}"
            )
            return TwitchGameData()
        else:
            j = loads(res.content)
            if len(j["data"]) != 0:
                game = TwitchGameData(j["data"][0])
            else:
                game = TwitchGameData()
            return game

    def getVideos(
        self, auth: TwitchAuth, id: int = 0, user_id: int = 0, game_id: int = 0
    ) -> List[TwitchVideo]:
        uri = f"{self.apiUri}/videos"
        if id != 0:
            uri = f"{uri}?id={id}"
        elif user_id != 0:
            uri = f"{uri}?user_id={user_id}"
        elif game_id != 0:
            uri = f"{uri}?game_id={game_id}"

        res = get(uri, headers=self.__header__(auth))
        videos = list()
        if res.status_code != 200:
            Logger().error(f"Failed to request videos")
            return videos
        else:
            json = loads(res.content)
            for i in json["data"]:
                videos.append(TwitchVideo(i))
            return videos

    def getClips(
        self, auth: TwitchAuth, user_id: int = 0, clip_id: str = "", game_id: int = 0
    ) -> List[TwitchClip]:
        uri = f"{self.apiUri}/clips"
        if user_id != 0:
            uri = f"{uri}?broadcaster_id={user_id}"
        elif clip_id != "":
            uri = f"{uri}?id={clip_id}"
        elif game_id != 0:
            uri = f"{uri}?game_id={game_id}"
        else:
            Logger().error(
                f"Clips was requested but was given invalid parameters, returning empty object."
            )
            return ""

        res = get(uri, headers=self.__header__(auth))
        clips = list()
        if res.status_code != 200:
            Logger().error(
                f"Clips request returned a bad status_code. Code: {res.status_code}, Error: {res.text}"
            )
            return clips
        else:
            json = loads(res.content)
            for i in json["data"]:
                clips.append(TwitchClip(i))

        return clips

    def getStreams(
        self, auth: TwitchAuth, game_id: int = 0, user_id: int = 0, user_login: str = ""
    ) -> None:
        uri = f"{self.apiUri}/streams"
        if game_id != 0:
            uri = f"{uri}?game_id={game_id}"
        elif user_id != 0:
            uri = f"{uri}?user_id={user_id}"
        elif user_login != "":
            uri = f"{uri}?user_login={user_login}"
        else:
            pass

        res = get(uri, headers=self.__header__(auth))
        streams = list()
        if res.status_code != 200:
            Logger().error(
                f"Streams request returned a bad status_code. Code: {res.status_code}, Error: {res.test}"
            )
            return streams
        else:
            json = loads(res.content)
            if len(json["data"]) == 0:
                streams.append(TwitchStream())
            for i in json["data"]:
                streams.append(TwitchStream(i))

        return streams

    def __header__(self, auth: TwitchAuth) -> Dict:
        return {
            "Authorization": f"Bearer {auth.access_token}",
            "Client-ID": f"{auth.client_id}",
        }

