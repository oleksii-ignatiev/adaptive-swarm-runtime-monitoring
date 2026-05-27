from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set, Tuple

Position = Tuple[int, int]


@dataclass
class Environment:
    """Grid environment with obstacles and task targets."""

    width: int
    height: int
    obstacles: Set[Position] = field(default_factory=set)
    targets: Set[Position] = field(default_factory=set)

    def is_inside(self, position: Position) -> bool:
        """Return True if the position is inside the grid."""
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def is_obstacle(self, position: Position) -> bool:
        """Return True if the position is blocked by an obstacle."""
        return position in self.obstacles

    def add_obstacle(self, position: Position) -> None:
        """Add one obstacle if it is inside the grid."""
        if self.is_inside(position):
            self.obstacles.add(position)

    def remove_target(self, position: Position) -> None:
        """Remove completed target from the environment."""
        self.targets.discard(position)
