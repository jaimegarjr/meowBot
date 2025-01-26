run-meowbot-docker:
    source bin/run-latest.sh

run-meowbot-local:
    poetry run python -m meowbot.bot.meowbot

build-docker-image:
    source bin/build-docker.sh

push-image-to-gcp:
    docker push gcr.io/meowbot-448505/meow-bot:latest

ssh-to-bot-vm:
    gcloud compute ssh --zone "us-central1-c" "meowbot-instance-vm" --project "meowbot-448505"

pre-commit:
    just lint
    just format
    just run-unit-tests

format:
    poetry run black .

lint:
    poetry run flake8 .

generate-coverage:
    poetry run pytest --cov=meowbot/ --cov-report=html

run-unit-tests:
    poetry run pytest tests/unit/ 