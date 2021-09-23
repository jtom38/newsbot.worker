from newsbot.worker.sources.youtube import YoutubeReader
from newsbot.core.sql.tables import Sources, DiscordWebHooks, SourcesTable
import pytest

class TestYouTube:
    @pytest.fixture
    def enableSource(self):
        table = SourcesTable()
        table.add(
            Sources(
                name="LoadingReadyRun",
                source="YouTube",
                url="https://www.youtube.com/user/loadingreadyrun",
            )
        )
        res = table.findAllBySource(source="YouTube")
        
        if len(res) >= 1:
            assert True
        else:
            assert False

    def test_01CheckSource(self, enableSource):
        yt = YoutubeReader()
        assert yt.sourceEnabled == True

    def test_01CheckHooks(self):
        yt = YoutubeReader()
        if len(yt.hooks) == 0:
            assert True
        else:
            assert False

    def test_01PullRss(self):
        yt = YoutubeReader()
        res = yt.getArticles()
        if len(res) >= 15:
            assert True
        else:
            assert False

    def test_02ClearSources(self):
        Sources().clearTable()
        res = Sources(name="Youtube").findAllByName()
        if len(res) == 0:
            assert True
        else:
            assert False

    def test_03EnableDiscordWebHook(self):
        DiscordWebHooks(name="Youtube LoadingReadyRun", key="invalidKey").add()
        res = DiscordWebHooks(name="Youtube").findAllByName()
        if len(res) >= 1:
            assert True
        else:
            assert False
