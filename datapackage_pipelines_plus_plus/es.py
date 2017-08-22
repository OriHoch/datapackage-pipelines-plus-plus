import os, logging
from elasticsearch import Elasticsearch


def get_engine():
    engine = Elasticsearch(hosts=[os.environ.get("DPP_ELASTICSEARCH", "localhost:9200")])
    try:
        if not engine.ping():
            raise Exception("failed to ping server")
    except Exception:
        logging.exception('Failed to connect to server %s', engine)
        raise
    return engine
