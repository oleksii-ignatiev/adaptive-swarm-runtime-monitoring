from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from swarm.environment import Environment

Position = Tuple[int, int]


@dataclass
class Agent:
    """Represents one autonomous agent in the swarm."""

    agent_id: int
    position: Position
    target: Optional[Position]
    active: bool = True
    communication_enabled: bool = True

    def choose_next_position(self, environment: "Environment") -> Position:
        """Choose the next position using a simple local greedy policy."""
        if not self.active or self.target is None:
            return self.position

        x, y = self.position

        candidate_moves = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
            (x, y),
        ]

        valid_moves = [
            move for move in candidate_moves
            if environment.is_inside(move) and not environment.is_obstacle(move)
        ]

        if not valid_moves:
            return self.position

        return min(valid_moves, key=lambda move: manhattan_distance(move, self.target))

    def has_completed_task(self) -> bool:
        """Return True if the agent reached its assigned target."""
        return self.target is not None and self.position == self.target


def manhattan_distance(a: Position, b: Position) -> int:
    """Calculate Manhattan distance between two grid positions."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
