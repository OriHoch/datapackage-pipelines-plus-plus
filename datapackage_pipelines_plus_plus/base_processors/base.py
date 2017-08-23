from datapackage_pipelines.wrapper import ingest, spew
from sqlalchemy import MetaData
import logging, time, datetime, warnings
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
        self._delay_limit = None
        self._delay_limit_reached = False
        self._start_time = None

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
            warnings.warn(msg, UserWarning)

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

    def _get_new_es_engine(self):
        return es.get_engine()

    @property
    def elasticsearch(self):
        if self._elasticsearch is None:
            self._elasticsearch = self._get_new_es_engine()
        return self._elasticsearch

    def _delay_limit_initialize(self):
        stop_after_seconds = self._parameters.get("stop-after-seconds")
        if stop_after_seconds:
            self._delay_limit = int(stop_after_seconds)
            self._start_time = datetime.datetime.now()

    def _delay_limit_check(self):
        if self._delay_limit_reached:
            return True
        elif self._delay_limit and self._delay_limit > 0:
            time_gap = (datetime.datetime.now() - self._start_time).total_seconds()
            if time_gap > self._delay_limit:
                self._delay_limit_reached = True
                self._warn_once("ran for {} seconds, reached delay limit".format(time_gap))
                self._stats["reached delay limit seconds"] = time_gap
                return True
