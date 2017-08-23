from datapackage_pipelines_plus_plus.base_processors.base import BaseProcessor
import pytest, os
from datapackage_pipelines_plus_plus import db, es
from sqlalchemy import Table, Column, Text, MetaData, TEXT
from elasticsearch import NotFoundError


class MockBaseProcessor(BaseProcessor):

    def _process(self, datapackage, resources):
        datapackage["foo"] = "bar"
        resources.append([{"baz": "bax"}])
        self._incr_stat("hello world")
        self._incr_stat("hello world", incr_by=2)
        assert self._get_stat("hello world") == 3
        self._set_stat("booyah", "yes")
        return datapackage, resources

    def _filter_stat_key(self, stat):
        # allows to add a prefix / suffix to stat titles
        stat = "{}: {}".format("~~", stat)
        # calling warn_once twice only warns once
        self._warn_once("prefixing stats with ~~")
        self._warn_once("prefixing stats with ~~")
        # test the DB
        self.db_connect()
        assert str(self.db_session.bind.url) == os.environ.get("DPP_DB_ENGINE", 'sqlite:///.data.db')
        test_table = self.db_meta.tables.get("plus_plus_test")
        if test_table is not None:
            test_table.drop()
            self._db_session = None
            self._db_meta = None
        test_table = Table("plus_plus_test", self.db_meta, Column("test", Text))
        test_table.create()
        test_table.insert().values({"test": "foobar1"}).execute()
        test_table.insert().values({"test": "foobar2"}).execute()
        self.db_session.commit()
        pytest.set_trace()
        try:
            self.elasticsearch.indices.delete("plus_plus_test")
        except NotFoundError:
            pass
        self.elasticsearch.indices.create("plus_plus_test")
        self.elasticsearch.indices.refresh("plus_plus_test")
        assert self.elasticsearch.indices.exists("plus_plus_test")
        return stat


def test_base_processor():
    parameters = {}
    datapackage = {}
    resources = []
    with pytest.warns(UserWarning) as record:
        processor = MockBaseProcessor(parameters, datapackage, resources)
        datapackage, resources, stats = processor.spew()
        resources = list(resources)
    assert [r.message.args for r in record] == [('prefixing stats with ~~',)]
    assert datapackage == {"foo": "bar"}
    assert list(resources) == [[{'baz': 'bax'}]]
    assert stats == {"~~: hello world": 3, "~~: booyah": "yes"}
    session = db.get_session(connection_string="sqlite:///.data.db")
    metadata = MetaData(bind=session.get_bind())
    metadata.reflect()
    test_table = metadata.tables["plus_plus_test"]
    assert test_table.c.test.name == "test"
    assert test_table.c.test.type.__class__ == TEXT
    assert session.query(test_table).filter(test_table.c.test=="foobar2").count() == 1