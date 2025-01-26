FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    libffi-dev \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy pyproject.toml and poetry.lock first (for caching layers)
COPY pyproject.toml poetry.lock ./

# Copy the rest of the application code into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "meowbot.bot.meowbot"]
