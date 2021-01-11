FROM python:3.7.9

RUN apt-get update -y && apt-get upgrade -y

COPY ./requirements.txt /summarizer/requirements.txt

WORKDIR /summarizer

RUN pip install -r requirements.txt

# Install spacy model
RUN python -m spacy download en_core_web_sm

COPY summarizer /summarizer/summarizer

ENV FLASK_APP=summarizer
ENTRYPOINT [ "flask" ]

CMD ["run", "--host=0.0.0.0", "--port=80"]