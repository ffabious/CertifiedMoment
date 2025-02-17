FROM python:3

WORKDIR /Users/m3/Documents/projects/CertifiedMoment

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./main.py"]