```
gcloud run deploy mpa-runtime --source . --region us-central1 --allow-unauthenticated --set-env-vars=GOOGLE_GENAI_USE_VERTEXAI=0,GOOGLE_API_KEY=<VALUE_HERE>,GOOGLE_MAPS_API_KEY=<VALUE_HERE>
```