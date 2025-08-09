# Demo Script (2 Minutes)

This script is intended for a live demonstration or recording. It guides you through the main features of Aegis Health. The goal is to tell a cohesive story from the patient’s perspective while highlighting technical depth.

## Set up

* Start the backend and ML services via `make dev`.  
* Launch the mobile app in an emulator using `npx expo start`.  
* Open the clinician dashboard at `http://localhost:3000`.

## Narrative

### 0:00 – Intro

> **Speaker**: “Hi everyone, I’m excited to show you Aegis Health, a platform that helps people with chronic conditions stay ahead of their flare‑ups. I’m going to play both patient and clinician to illustrate how we close the loop between logging, prediction and intervention.”

### 0:20 – Logging a Symptom

> Walk through the mobile app. Tap “Log Symptom”. Enter a free text note: *‘woke up with joint stiffness’*. Adjust the pain slider to 6 and fatigue to 3. Tap “Submit”.
>
> **Speaker**: “All logs are timestamped and stored locally first; once connectivity is available they sync to the backend securely.”

### 0:40 – Sync Wearables

> Trigger a mock wearable sync in the app (use the “Sync” button). This posts snapshot data to the API which publishes events to Pub/Sub. The Dataflow pipeline will build features in the background. Mention that adapters exist for Apple Health and Google Fit.

### 1:00 – Check Risk Score

> Go to the “Risk” tab. The app requests the latest risk score from `/v1/risk/latest`. Show the card displaying, for example, **32 % risk** with top drivers: low sleep efficiency and high pain. Explain that the baseline model runs in our ML service with sub‑80 ms inference time and provides SHAP‑based explanations.

> **Speaker**: “Here you can see that my low sleep efficiency over the past 7 days and today’s pain score drive the risk. We also estimate that a flare‑up could occur in about 18 hours unless I act.”

### 1:30 – Nudge & Clinician Dashboard

> Wait a few seconds; a push notification appears: *“Hydrate and do 5 minutes of stretching to reduce your risk.”* Tap it to show the in‑app nudge. Explain that these messages are configurable and part of our experimentation framework.

> Switch to the web dashboard. Show metrics such as adherence (66 %), false‑alert rate (21 %) and median lead time (14 hours). Trigger a manual intervention from the dashboard, e.g., send a motivational message.

> **Speaker**: “Clinicians can monitor their entire cohort. Here we see aggregated metrics and can test different nudge templates. All actions are audited.”

### 1:50 – Outro

> **Speaker**: “In two minutes we’ve logged symptoms, ingested wearables, computed a risk score with explanations and delivered a timely nudge. Behind the scenes, scalable pipelines ingest data, our ML service serves predictions, and our dashboard empowers clinicians. Aegis Health aims to reduce flare‑ups and improve quality of life. Thank you!”

## Tips

* Keep an eye on the timer to ensure you finish within two minutes.
* Use a real emulator and not screenshots to convey realism.
* If running live, ensure all containers are healthy beforehand.
