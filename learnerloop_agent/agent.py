from google.adk.agents import Agent

ALLOWED_DECISIONS = {
    "HOLD",
    "WATCH",
    "INVESTIGATE",
    "SCALE_CANDIDATE",
    "REDUCE_CANDIDATE",
    "PAUSE_CANDIDATE",
}

RISKY_DECISIONS = {
    "SCALE_CANDIDATE",
    "REDUCE_CANDIDATE",
    "PAUSE_CANDIDATE",
}

def create_intervention_request(
    decision: str,
    reason: str,
    confidence: float,
    recommended_action: str,
) -> dict:
    """Create a validated intervention request without modifying live campaigns."""
    decision = decision.strip().upper()
    if decision not in ALLOWED_DECISIONS:
        return {
            "status": "rejected",
            "error": f"Unsupported decision: {decision}",
            "allowed_decisions": sorted(ALLOWED_DECISIONS),
        }

    confidence = max(0.0, min(float(confidence), 1.0))
    return {
        "status": "created",
        "decision": decision,
        "reason": reason.strip(),
        "confidence": round(confidence, 3),
        "recommended_action": recommended_action.strip(),
        "requires_human_approval": decision in RISKY_DECISIONS,
        "execution_mode": "decision_support_only",
    }

root_agent = Agent(
    name="learnerloop_growth_agent",
    model="gemini-3.5-flash",
    description=(
        "A state-aware operations agent that compares current and prior growth state "
        "and creates a structured intervention request."
    ),
    instruction=r"""
You are LearnerLoop Growth Agent.

You receive one JSON object that may contain:
- current_performance
- previous_performance
- verified_revenue
- previous_decision
- targets
- notes

Do this:
1. Observe the current state.
2. Compare it with previous state and targets.
3. Prefer verified revenue/purchase evidence over platform-attributed revenue when both exist.
4. Decide whether there is enough evidence for an intervention.
5. Choose exactly one:
   HOLD, WATCH, INVESTIGATE, SCALE_CANDIDATE, REDUCE_CANDIDATE, PAUSE_CANDIDATE.
6. Call create_intervention_request exactly once.
7. After the tool returns, return that tool result with no extra commentary.

Constraints:
- Never claim to directly change budgets, bids, campaigns, ad sets, or ads.
- SCALE_CANDIDATE, REDUCE_CANDIDATE and PAUSE_CANDIDATE require human approval.
- If evidence is thin or contradictory, choose WATCH or INVESTIGATE.
- Do not invent missing metrics.
- Keep the reason concise and evidence-based.
""",
    tools=[create_intervention_request],
)
