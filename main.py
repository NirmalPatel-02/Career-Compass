from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib, json, os, uuid, shap
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
from .questions import FEATURE_META, DOMAIN_QUESTIONS, SUB_DOMAIN_QUESTIONS

app = FastAPI()

BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
templates = Jinja2Templates(directory=FRONTEND_DIR)

@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def load_asset(folder):
    path = os.path.join(BASE_DIR, "models", folder)
    return {
        "model": joblib.load(os.path.join(path, "model.pkl")),
        "le": joblib.load(os.path.join(path, "label_encoder.pkl")),
        "features": json.load(open(os.path.join(path, "features.json")))
    }

ASSETS = {
    "domain": load_asset("domain"),
    "Technology & Engineering": load_asset("tech"),
    "Data & AI": load_asset("data_ai"),
    "Security & Infrastructure": load_asset("security"),
    "Business & Product": load_asset("business"),
    "Design & Creative": load_asset("design"),
    "Writing & Content": load_asset("writing")
}

EXPLANATIONS = json.load(open(os.path.join(BASE_DIR, "metadata", "explanations.json")))

sessions = {}

class SessionStart(BaseModel):
    familiarity: int

class AnswerPayload(BaseModel):
    session_id: str
    feature: str
    value: int

def entropy(p):
    p = np.clip(p, 1e-9, 1)
    return -np.sum(p * np.log2(p))

def softmax_temp(p, T=1.4):
    e = np.exp(np.log(p + 1e-9) / T)
    return e / e.sum()

def get_prediction_probs(model, features_list, current_state, phase):
    x = {}
    for f in features_list:
        if f in current_state:
            x[f] = current_state[f]
        else:
            if phase == "domain":
                x[f] = 1 if FEATURE_META[f][1] == 2 else 0.5
            else:
                x[f] = 1
    df = pd.DataFrame([x])[features_list]
    return softmax_temp(model.predict_proba(df)[0])

def explain(model, features_list, current_state, le, probs):
    try:
        x = {f: (current_state[f] if f in current_state else 0) for f in features_list}
        df = pd.DataFrame([x])[features_list]
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(df)
        
        top_class_idx = int(np.argmax(probs))
        if isinstance(shap_values, list):
            contributions = shap_values[top_class_idx][0]
        elif shap_values.ndim == 3:
            contributions = shap_values[0, :, top_class_idx]
        else:
            contributions = shap_values[0]

        importance = pd.DataFrame({"feature": features_list, "contribution": contributions, "val": [x[f] for f in features_list]})
        importance = importance[importance["val"] > 0].sort_values(by="contribution", ascending=False)
        
        reasons = []
        for _, row in importance.iterrows():
            if row["feature"] in EXPLANATIONS:
                reasons.append(EXPLANATIONS[row["feature"]])
            if len(reasons) >= 3: break
        return reasons
    except:
        return ["Your logical approach and interests strongly align with this field."]

def get_top_3_results(sid, asset):
    sess = sessions[sid]
    features = asset["features"]
    probs = get_prediction_probs(asset["model"], features, sess["state"], "career")
    top_indices = np.argsort(probs)[::-1][:3]
    
    results = []
    ranks = ["🥇 Gold Match", "🥈 Silver Match", "🥉 Bronze Match"]
    for i, idx in enumerate(top_indices):
        results.append({
            "rank_label": ranks[i],
            "career": asset["le"].inverse_transform([idx])[0],
            "confidence": round(float(probs[idx] * 100), 1)
        })
    reasons = explain(asset["model"], features, sess["state"], asset["le"], probs)
    return {"type": "result", "top_matches": results, "reasons": reasons}

def next_step(sid):
    sess = sessions[sid]
    phase = sess["phase"]
    model_key = "domain" if phase == "domain" else sess["locked_domain"]
    asset = ASSETS[model_key]
    
    probs = get_prediction_probs(asset["model"], asset["features"], sess["state"], phase)
    curr_ent = entropy(probs)
    
    threshold = 0.65 if phase == "domain" else 0.70
    min_q = 3 if phase == "domain" else 4
    
    if (probs.max() > threshold and len(sess["asked"]) >= min_q) or len(sess["asked"]) >= 10:
        if phase == "domain":
            sess["locked_domain"] = asset["le"].inverse_transform([np.argmax(probs)])[0]
            sess["phase"] = "career"; sess["asked"] = set(); sess["state"] = {}
            return next_step(sid)
        else:
            return get_top_3_results(sid, asset)

    q_bank = DOMAIN_QUESTIONS[sess["familiarity"]] if phase == "domain" else SUB_DOMAIN_QUESTIONS[model_key][sess["familiarity"]]
    best_f, best_gain = None, -1
    
    for f, q_text in q_bank.items():
        if f in sess["asked"] or f not in asset["features"]: continue
        low, high = FEATURE_META[f]
        ent_after = []
        for val in range(low, high + 1):
            tmp_state = sess["state"].copy(); tmp_state[f] = val
            p_next = get_prediction_probs(asset["model"], asset["features"], tmp_state, phase)
            ent_after.append(entropy(p_next))
        
        gain = curr_ent - np.mean(ent_after)
        if gain > best_gain:
            best_gain, best_f = gain, f

    if not best_f:
        if phase == "domain":
            sess["locked_domain"] = asset["le"].inverse_transform([np.argmax(probs)])[0]
            sess["phase"] = "career"; sess["asked"] = set(); sess["state"] = {}
            return next_step(sid)
        return get_top_3_results(sid, asset)

    return {"type": "question", "feature": best_f, "question": q_bank[best_f], "options": FEATURE_META[best_f]}

@app.post("/start")
async def start(data: SessionStart):
    sid = str(uuid.uuid4())
    sessions[sid] = {"familiarity": data.familiarity, "phase": "domain", "state": {}, "asked": set(), "locked_domain": None}
    return {"session_id": sid, "next_question": next_step(sid)}

@app.post("/submit")
async def submit(payload: AnswerPayload):
    sid = payload.session_id
    if sid not in sessions: raise HTTPException(404, "Session Expired")
    sessions[sid]["state"][payload.feature] = payload.value
    sessions[sid]["asked"].add(payload.feature)
    return next_step(sid)