from datapackage_pipelines.wrapper import ingest, spew
from sqlalchemy import MetaData
import logging, time
from sqlalchemy.exc import OperationalError
from datapackage_pipelines_plus_plus import db
from datapackage_pipelines_plus_plus import es


class BaseProcessor(object):
    """
    Common base class for all processors
    """

    def __init__(self, parameters, datapackage, resources):
        self._parameters = parameters
        self._datapackage = datapackage
        self._resources = resources
        self._stats = {}
        self._warned_once = []
        self._db_session = None
        self._db_meta = None
        self._elasticsearch = None

    @classmethod
    def main(cls):
        # can be used like this in datapackage processor files:
        # if __name__ == '__main__':
        #      Processor.main()
        spew(*cls(*ingest()).spew())

    def spew(self):
        self._datapackage, self._resources = self._process(self._datapackage, self._resources)
        return self._datapackage, self._resources, self._get_stats()

    def _get_stats(self):
        return self._stats

    def _get_stat(self, stat, default=None):
        stat = self._filter_stat_key(stat)
        return self._stats.get(stat, default)

    def _incr_stat(self, stat, incr_by=1):
        stat = self._filter_stat_key(stat)
        self._stats.setdefault(stat, 0)
        self._stats[stat] += incr_by
        return self._stats[stat]

    def _set_stat(self, stat, value):
        stat = self._filter_stat_key(stat)
        self._stats[stat] = value
        return self._stats[stat]

    def _filter_stat_key(self, stat):
        # allows to add a prefix / suffix to stat titles
        return stat

    def _process(self, datapackage, resources):
        raise NotImplementedError()

    def _warn_once(self, msg):
        if msg not in self._warned_once:
            self._warned_once.append(msg)
            logging.warning(msg)

    @property
    def db_session(self):
        if self._db_session is None:
            self._db_session = self._get_new_db_session()
        return self._db_session

    def _get_new_db_session(self):
        return db.get_session()

    @property
    def db_meta(self):
        if self._db_meta is None:
            self._db_meta = MetaData(bind=self.db_session.get_bind())
            self._db_meta.reflect()
        return self._db_meta

    def db_commit(self):
        if self._db_session is not None:
            self._db_session.commit()

    def db_connect(self, retry=False, **kwargs):
        try:
            self.db_session.get_bind().connect()
        except OperationalError:
            logging.exception("db connection error")
            if not retry:
                raise
            else:
                retry_num = kwargs.setdefault("retry_num", 0) + 1
                max_retries = kwargs.setdefault("max_retries", 5)
                retry_sleep_seconds = kwargs.setdefault("retry_sleep_seconds", 2)
                if retry_num < max_retries:
                    time.sleep(retry_sleep_seconds)
                    return self.db_connect(**dict(kwargs, **{"retry_num": retry_num}))
        return True

    @property
    def elasticsearch(self):
        if self._elasticsearch is None:
            self._elasticsearch = es.get_engine()
        return self._elasticsearch
