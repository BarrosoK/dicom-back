FROM python:3.8
COPY ./app/ /app

RUN pip install -r /app/requirements.txt && rm -fr /root/.cache
WORKDIR /
ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENTRYPOINT ["python"]
CMD ["/app/DicomApi.py"]