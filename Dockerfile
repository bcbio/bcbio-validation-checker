# Base Image
FROM ubuntu:16.04

# File Author / Maintainer
MAINTAINER Brad Chapman <chapmanb@fastmail.com>

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends python-dev git python-setuptools python-pip

COPY bin/bcbio_check_validation.py /usr/local/bin/
RUN chmod a+x /usr/local/bin/bcbio_check_validation.py

CMD ["/bin/bash"]
