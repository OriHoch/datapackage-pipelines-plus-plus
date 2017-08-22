FROM docker.elastic.co/elasticsearch/elasticsearch:5.5.0

USER root
RUN echo vm.max_map_count=262144 > /etc/sysctl.d/01-es.conf

USER elasticsearch

ADD ./config /usr/share/elasticsearch/config
