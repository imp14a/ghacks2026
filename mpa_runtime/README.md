```
export GOOGLE_CLOUD_PROJECT="ghacks2026-argo-team"
export GOOGLE_CLOUD_LOCATION="us-central1"
export AGENT_PATH="./mpa"

adk deploy cloud_run \
--project=$GOOGLE_CLOUD_PROJECT \
--region=$GOOGLE_CLOUD_LOCATION \
--with_ui \
$AGENT_PATH \
```