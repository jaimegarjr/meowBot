# Use an official lightweight Python image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    libffi-dev \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and poetry.lock first (for caching layers)
COPY pyproject.toml poetry.lock ./

# Export dependencies to requirements.txt
RUN poetry export --without-hashes -f requirements.txt -o requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Install dependencies from the exported requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to start the bot
CMD ["python", "-m", "meowbot.bot.meowbot"]
