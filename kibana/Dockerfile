FROM docker.elastic.co/kibana/kibana:5.5.1

ADD ./config /usr/share/kibana/config

RUN bin/kibana 2>&1 | grep -m 1 "Optimization of .* complete in .* seconds"
