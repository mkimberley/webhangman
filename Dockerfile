FROM python:latest
ADD webhangman.py /
EXPOSE 80
COPY templates /templates
RUN pip install flask
CMD ["python","/webhangman.py"]
