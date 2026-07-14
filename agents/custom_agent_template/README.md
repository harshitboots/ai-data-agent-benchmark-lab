# custom_agent_template

Starting point for contributors adding a new agent. Copy
[`template_agent.py`](template_agent.py) into your own `agents/<your_agent>/`
folder and implement `run()` — it subclasses `arena.agent.BaseAgent`, the
same interface [`agents/baseline_agent/`](../baseline_agent/) implements.

See [ROADMAP.md](../../ROADMAP.md) for the phase plan.

