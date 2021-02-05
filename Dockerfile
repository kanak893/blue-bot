FROM python:3.7-slim-buster

ADD . .

# Install the dependencies
RUN cat requirement.txt | while read PACKAGE; do pip install "$PACKAGE"; done

ENV SIMPLE_SETTINGS=settings.production

CMD ["python","bot.py"]
