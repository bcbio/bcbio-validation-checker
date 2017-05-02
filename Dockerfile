# Base Image
FROM ubuntu:16.04

# File Author / Maintainer
MAINTAINER Brad Chapman <chapmanb@fastmail.com>

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends python-dev git python-setuptools python-pip

COPY bin/check_bcbio_validation.py /usr/local/bin/
RUN chmod a+x /usr/local/bin/check_bcbio_validation.py

CMD ["/bin/bash"]
