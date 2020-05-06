FROM continuumio/miniconda3

RUN conda create --name py35 python=3.5

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN conda update conda

COPY . /usr/src/app

ENV PATH /opt/conda/envs/py35/bin:$PATH

RUN conda install -n py35 -c conda-forge openjdk
RUN conda install -n py35 -c estnltk -c conda-forge estnltk==1.4.1
RUN conda install -n py35 spacy && \
    conda install -n py35 Flask && \
    pip install connexion==2.3.0 && \
    conda install -n py35 Werkzeug=0.16.1 && \
    conda install -n py35 swagger-ui-bundle && \
    conda install -n py35 parsedatetime && \
    pip install textblob==0.15.3 && \
    pip install python-dateutil==2.8.1
RUN python -m spacy download en_core_web_sm

CMD python -m swagger_server
