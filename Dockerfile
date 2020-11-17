FROM python:latest
ADD webhangman.py /
COPY templates /templates
RUN pip install flask
CMD ["python","/webhangman.py"]
