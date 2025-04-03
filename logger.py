import datetime
from typing import Dict, Any

class InteractionLogger:
    def log_interaction(self, interaction: Dict[str, Any]):
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"\n[{timestamp}]\n" + "\n".join(
            [f"{k.upper()}: {v}" for k, v in interaction.items()]
        ) + "\n" + "-" * 50
        print(log_entry)