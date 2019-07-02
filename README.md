# Blog Bot TestTask

### Usage:

Update `config.py` as you wish and build

#### Run in container:

```bash
docker build -t blog-bot .
```

Run

```bash
docker run blog-bot
```

#### Run locally:

```bash
pipenv install && pipenv shell
python bot.py
```