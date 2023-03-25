<div align="center">
    <img src="https://cdn1.iconfinder.com/data/icons/material-apps/512/icon-music-material-design-512.png" alt="logo" height="128">
</div>

# learn-music

![coding_style](https://img.shields.io/badge/code%20style-black-000000.svg)

A Django app to help with music homework

## Getting Started

### Install

```zsh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Use `pip install -r requirements-dev.txt` for development. It will install `pylint` and `black` to enable linting and auto-formatting.

### Setup

Create a `.env` file to configure the AWS S3 bucket

```zsh
touch .env
```

And put down the the following information

```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...
AWS_S3_REGION_NAME=...
SECRET_KEY=..
```

## Credits

- [Logo][1] by [Maurilio Monsù][2]

[1]: https://www.iconfinder.com/icons/3116880/design_material_music_audio_media_play_square_icon
[2]: https://www.iconfinder.com/maurilio94
