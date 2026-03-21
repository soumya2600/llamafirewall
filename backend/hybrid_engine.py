"""
Hybrid Security Engine v3.0
Two layers: HuggingFace AI + Rule Engine
HF AI leads, rules act as safety floor and fast pre-filter.
"""

import os
from security_engine import SecurityEngine
from hf_ai_engine    import HFAIEngine

THRESHOLD_ALLOWED      = 0.30
THRESHOLD_SUSPICIOUS   = 0.70
RULE_SKIP_AI_THRESHOLD = 0.90   # skip HF call if rules are already 90%+ sure


class HybridEngine:
    def __init__(self, hf_key: str = None):
        self.rules = SecurityEngine()
        self.hf    = HFAIEngine(hf_key)

        if self.hf.available:
            print(f"[Engine] HuggingFace AI + Rules  (model: {self.hf.model})")
        else:
            print("[Engine] Rules Only — add HF_API_KEY to .env to enable AI")

    @property
    def ai_available(self): return self.hf.available
    @property
    def ai_mode(self):      return "huggingface" if self.hf.available else "none"
    @property
    def model_name(self):   return self.hf.model if self.hf.available else None

    def analyze(self, prompt: str) -> dict:
        text = prompt.strip()

        # Step 1 — Rules (always, instant)
        rule_result = self.rules.analyze(text)
        rule_score  = rule_result["risk_score"]

        # Step 2 — HuggingFace AI (skip if rules already very confident)
        ai_result = None
        ai_used   = False
        if self.hf.available and rule_score < RULE_SKIP_AI_THRESHOLD:
            try:
                ai_result = self.hf.analyze(text)
                if ai_result:
                    ai_used = True
            except Exception as e:
                print(f"[Engine] HF analysis error: {e}")

        # Step 3 — Fuse scores
        if ai_used:
            blended = ai_result["risk_score"] * 0.70 + rule_score * 0.30
            final   = round(max(blended, rule_score), 4)
            mode    = "ai_huggingface+rules"
        else:
            final = rule_score
            mode  = "rules_only"

        final = min(final, 1.0)

        # Step 4 — Status
        if final >= THRESHOLD_SUSPICIOUS:
            status = "blocked"
        elif final >= THRESHOLD_ALLOWED:
            status = "suspicious"
        else:
            status = "allowed"

        return {
            "prompt":        text,
            "risk_score":    final,
            "status":        status,
            "reason":        _build_reason(status, final, rule_result, ai_result, ai_used),
            "analysis_mode": mode,
            "ai_reasoning":  ai_result["reasoning"]   if ai_result else None,
            "threat_type":   ai_result["threat_type"] if ai_result else None,
        }


def _build_reason(status, score, rule_result, ai_result, ai_used):
    label = {"blocked": "BLOCKED", "suspicious": "SUSPICIOUS", "allowed": "ALLOWED"}[status]
    parts = [f"{label} (score {score:.3f})"]

    if ai_used and ai_result:
        threat    = ai_result.get("threat_type", "none")
        reasoning = ai_result.get("reasoning", "")
        if threat and threat != "none":
            parts.append(f"HuggingFace AI detected: {threat.replace('_', ' ')}.")
        if reasoning:
            parts.append(reasoning)
    elif status in ("blocked", "suspicious"):
        core = rule_result.get("reason", "").split(".")[0]
        if core:
            parts.append(core)

    if not ai_used and status == "allowed":
        parts.append("No significant attack patterns detected.")

    return " ".join(parts)