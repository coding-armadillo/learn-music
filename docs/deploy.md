# Deploy

## Fly.io

Use the following commands to set the environment variables of the app

```zsh
fly secrets set AWS_ACCESS_KEY_ID=...
fly secrets set AWS_SECRET_ACCESS_KEY=...
fly secrets set AWS_STORAGE_BUCKET_NAME=...
fly secrets set AWS_S3_REGION_NAME=...
fly secrets set SECRET_KEY=...
fly secrets set DEBUG=false
```

## Heroku

Use the following commands to set the environment variables of the app

```zsh
heroku config:set AWS_ACCESS_KEY_ID=...
heroku config:set AWS_SECRET_ACCESS_KEY=...
heroku config:set AWS_STORAGE_BUCKET_NAME=...
heroku config:set AWS_S3_REGION_NAME=...
heroku config:set SECRET_KEY=...
heroku config:set DEBUG=false
```
