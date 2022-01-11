from unittest import TestCase
from workerService.sources import RssWorkerService
from workerInfra.enum import SourcesEnum


class TestRssWorkerService(TestCase):
    _service: RssWorkerService

    def testInit(self):
        self._service = RssWorkerService()
        assert self._service

    def testActiveSource(self):
        self._service = RssWorkerService()
        assert self._service._feedName == SourcesEnum.RSS
