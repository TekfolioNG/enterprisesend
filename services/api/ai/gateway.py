"""All AI calls go through here. The AI only flags; a person decides."""
import json


def flag_anomalies(settings, rows: list[dict]) -> dict:
    if settings.ai_model.startswith("SET_ME"):
        return {"enabled": False, "flags": []}
    from google import genai  # pip install google-genai
    client = genai.Client(vertexai=True, project=settings.project_id,
                          location=settings.ai_location)
    # Send only what the check needs (no names, phones or emails).
    slim = [{"row": i + 2, "account_id": r["account_id"], "amount": r["invoice_amount"],
             "description": r.get("description", "")} for i, r in enumerate(rows)]
    prompt = ("You review a billing batch before sending. Return JSON only: "
              '{"flags":[{"row":int,"reason":str}]}. Flag typos in descriptions, '
              "likely double billing, and unusual amounts.\n" + json.dumps(slim))
    resp = client.models.generate_content(
        model=settings.ai_model, contents=prompt,
        config={"response_mime_type": "application/json"})
    return {"enabled": True, **json.loads(resp.text)}
