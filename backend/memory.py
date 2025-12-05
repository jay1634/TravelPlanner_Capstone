from typing import Dict, List, Any


class Memory:
    def __init__(self) -> None:
        self.chat_history: Dict[str, List[str]] = {}
        self.preferences: Dict[str, Dict[str, Any]] = {}

    def get_history(self, session_id: str) -> List[str]:
        return self.chat_history.setdefault(session_id, [])

    def add_turn(self, session_id: str, text: str) -> None:
        self.chat_history.setdefault(session_id, []).append(text)

    def get_prefs(self, session_id: str) -> Dict[str, Any]:
        return self.preferences.setdefault(session_id, {})

    def update_prefs(self, session_id: str, updates: Dict[str, Any]) -> None:
        self.preferences.setdefault(session_id, {}).update(updates)


memory = Memory()
