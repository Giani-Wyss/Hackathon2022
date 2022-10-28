FROM python:3.10.6-slim

# Install app
COPY . /usr/app
WORKDIR /usr/app

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Update more often
ENV PYTHONUNBUFFERED=1

# Run Battlesnake
CMD [ "python", "main.py" ]
