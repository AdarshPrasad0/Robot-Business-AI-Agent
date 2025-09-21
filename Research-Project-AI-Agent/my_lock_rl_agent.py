import asyncio
from openai import OpenAI
from my_lock import MyLock  # Make sure this points to your MyLock class file/module

# --- Hardcoded OpenAI API key ---
OPENAI_KEY = "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"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_KEY)

# --- LLM reasoning ---
async def llm_decide_action(scenario_text: str, current_state: str, history: list) -> str:
    if current_state == "Jammed":
        return "ClearJam"

    history_text = "\n".join([f"{h['scenario']} -> {h['action']}" for h in history[-5:]])

    prompt = f"""
You are an AI assistant controlling a smart lock. The lock state is currently '{current_state}'.
Past actions:
{history_text}

Decide whether to Lock, Unlock, or ClearJam based on the user's instruction:
Instruction: "{scenario_text}"

Only respond with one of these options exactly: Lock, Unlock, ClearJam, or None (if no action needed).
"""

    # Wrap blocking call in a thread
    def blocking_call():
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0
        )
        return response.choices[0].message.content.strip()

    action = await asyncio.to_thread(blocking_call)

    if action not in ["Lock", "Unlock", "ClearJam", "None"]:
        action = "None"
    return action

# --- Reinforcement Agent ---
class MyLockReinforcementAgent:
    """Autonomous agent for MyLock with memory and GPT reasoning."""

    def __init__(self, lock: MyLock):
        self.lock = lock
        self.history = []

    def get_state(self):
        if self.lock.is_jammed:
            return "Jammed"
        elif self.lock._is_locking:
            return "Locking"
        elif self.lock._is_unlocking:
            return "Unlocking"
        elif self.lock.is_locked:
            return "Locked"
        else:
            return "Unlocked"

    async def decide_action(self, scenario_text: str) -> str:
        return await llm_decide_action(scenario_text, self.get_state(), self.history)

    async def execute_action(self, action: str):
        if action == "Lock":
            await self.lock.async_lock(code="AI")
        elif action == "Unlock":
            await self.lock.async_unlock(code="AI")
        elif action == "ClearJam":
            self.lock.clear_jam()

    async def handle_scenario(self, scenario_text: str):
        action = await self.decide_action(scenario_text)
        if action and action != "None":
            print(f"[AGENT] Scenario: '{scenario_text}', Action: {action}")
            await self.execute_action(action)
        else:
            print(f"[AGENT] Scenario: '{scenario_text}', No action needed.")
            action = "None"

        # Update history
        self.history.append({"scenario": scenario_text, "action": action})
        print(f"[AGENT] Lock State after action: {self.get_state()}")
        print(f"[AGENT] Memory (last 5 actions): {self.history[-5:]}")

# --- Example Usage ---
async def main():
    my_lock = MyLock("Front Door")
    agent = MyLockReinforcementAgent(my_lock)

    await agent.handle_scenario("I am leaving for work, lock the door.")
    await agent.handle_scenario("Guests are coming over, unlock the front door.")
    await agent.handle_scenario("Leaving for a jog.")
    my_lock.jam()
    await agent.handle_scenario("Something seems wrong with the lock, check it.")
    await agent.handle_scenario("Going to bed now.")
    await agent.handle_scenario("I just returned home, unlock the front door.")

if __name__ == "__main__":
    asyncio.run(main())
