## Doing a deployment:

Ref: https://cloud.google.com/python/django/appengine

1. Run `gcloud auth application-default login`
1. In a terminal, run `./cloud-sql-proxy resolute-tracer-402011:europe-west1:travelmate-backend-gpt` (make sure cloud-sql-proxy is installed)
1. Have the following in your `.env` file (replacing USERNAME and PASSWORD with the right values):
    ```.env
    DEBUG=True
    ENVIRONMENT=local
    LOG_LEVEL=DEBUG
    OPENAI_API_KEY=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
    OPENAI_MODEL=gpt-3.5-turbo
    SECRET_KEY=superdupersecretkey
    GOOGLE_CLOUD_PROJECT=resolute-tracer-402011
    USE_CLOUD_SQL_AUTH_PROXY=true
    DATABASE_URL=postgres://<USERNAME>:<PASSWORD>@//cloudsql/resolute-tracer-402011:europe-west1:travelmate-backend-gpt/api
    ```
1. In a new terminal, in the root of the repository, run `./manage.py makemigrations --dry-run` to check if anything was missed with new models being added
1. In the same terminal, run `./manage.py migrate`
1. In the same terminal, run `gcloud app deploy --promote` (omit the --promote flag if you don't want all traffic to be redirected to this version)

Done
