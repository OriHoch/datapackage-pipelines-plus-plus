import os, logging
from elasticsearch import Elasticsearch


def get_engine(hosts=None):
    if not hosts:
        hosts = [os.environ.get("DPP_ELASTICSEARCH", "localhost:9200")]
    engine = Elasticsearch(hosts=hosts)
    try:
        if not engine.ping():
            raise Exception("failed to ping server")
    except Exception:
        logging.exception('Failed to connect to server %s', engine)
        raise
    return engine
