# OpsPulse — Operations Performance Intelligence

A small portfolio prototype for a Forward Deployed AI Engineer learning path.

## What it does
- Displays task completion, completion rate, dent count, and average quality score.
- Filters by team member and work slice.
- Charts throughput and quality trends.
- Generates transparent, rule-based operational insight cards.
- Lets the viewer download filtered records as CSV.

## Important data note
All records are synthetic and created for this demo. This app is not connected to any employer, customer, or private dataset. Do not upload confidential work data to a public repository.

## Run locally
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Tech stack
- Python
- Pandas
- Streamlit

## FDE-style next steps
1. Replace sample records with an approved, anonymized data source.
2. Add data validation and metric definitions.
3. Connect to a database or warehouse using least-privilege credentials.
4. Add an LLM summary behind a secure API key, with evaluation and human review.
5. Deploy the app and document reliability, privacy, and limitations.

## Current limitation
The insight cards are rule-based, not LLM-generated. This is an intentionally small first version to validate the workflow before adding AI.
