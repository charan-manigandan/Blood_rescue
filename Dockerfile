FROM PYTHON=3.12.4-bullseye

RUN pip install --upgrade pip

COPY ./requirements.txt
RUN pip install -r requirements.txt

COPY ./blood_rescue /mysite

WORKDIR /mysite

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "./entrypoint.sh"]