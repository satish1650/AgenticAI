# Cloud Run — ADK Capital Agent (Minimal Sample)

Deploy a simple ADK agent to **Cloud Run** using the recommended `adk deploy cloud_run` command.

## 1) Prereqs
- `gcloud auth login` and `gcloud config set project <your-project-id>`
- `pip install google-adk`
- (Optional) `jq` for the test script

## 2) Set env
Edit and source:
```bash
source scripts/env_example.sh
```

## 3) Deploy
```bash
bash scripts/deploy_cloud_run_adk.sh
```
When prompted:
- `y` = public URL (simplest for demos)
- `n` = private; you’ll need an identity token for API calls

## 4) Test
Set the service URL printed by the deploy step:
```bash
export APP_URL="https://<service>-<hash>-<region>.a.run.app"
# If private:
export TOKEN=$(gcloud auth print-identity-token)
bash scripts/test_cloud_run.sh
```

## 5) Pitfalls
- **No root_agent found** → ensure `capital_agent/agent.py` exports `root_agent` and `capital_agent/__init__.py` has `from . import agent`.
- **Wrong project/region** → check `GOOGLE_CLOUD_PROJECT` / `GOOGLE_CLOUD_LOCATION` and `gcloud config get-value project`.
- **Missing auth** → for private services, send `Authorization: Bearer $(gcloud auth print-identity-token)`.
- **Extra deps** → add to `capital_agent/requirements.txt`.
- **Service name** → must be dash-case (`capital-agent-service`), not snake_case.

You’re ready to demo: deploy, open the Dev UI (since we used `--with_ui`), or hit the REST endpoints.
