FROM python:3.10-slim

#changes the working directory to this in the image
WORKDIR /blinkApp

#copy this
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]