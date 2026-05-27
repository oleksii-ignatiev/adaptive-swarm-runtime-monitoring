from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List

from swarm.agent import Agent
from swarm.environment import Environment
from swarm.monitor import RuntimeMonitor
from swarm.visualization import visualize


@dataclass
class Simulation:
    """Runs the adaptive swarm simulation."""

    width: int
    height: int
    agent_count: int
    max_steps: int
    communication_radius: int
    seed: int = 1
    environment: Environment = field(init=False)
    agents: List[Agent] = field(init=False)
    monitor: RuntimeMonitor = field(default_factory=RuntimeMonitor)

    def __post_init__(self) -> None:
        random.seed(self.seed)
        self.environment = Environment(width=self.width, height=self.height)
        self._create_obstacles()
        self._create_targets()
        self._create_agents()

    def run(self, show_visualization: bool = True) -> None:
        """Run the simulation loop."""
        for step in range(self.max_steps):
            self._apply_runtime_changes(step)
            self._move_agents()
            self._complete_tasks()
            self.monitor.evaluate(
                step=step,
                agents=self.agents,
                environment=self.environment,
                communication_radius=self.communication_radius,
            )

            if not self.environment.targets:
                print(f"All tasks completed at step {step}.")
                break

        self.monitor.print_summary()

        if show_visualization:
            visualize(self.environment, self.agents, self.monitor.metrics)

    def _create_obstacles(self) -> None:
        """Create static obstacles in the environment."""
        for x in range(6, 14):
            self.environment.add_obstacle((x, 7))

        for y in range(2, 6):
            self.environment.add_obstacle((11, y))

    def _create_targets(self) -> None:
        """Create task targets."""
        targets = {
            (18, 2), (17, 12), (3, 13), (15, 10),
            (2, 4), (10, 13), (18, 7), (5, 10),
        }
        self.environment.targets.update(targets)

    def _create_agents(self) -> None:
        """Create agents and assign initial targets."""
        start_positions = [
            (1, 1), (2, 1), (1, 2), (2, 2),
            (1, 3), (3, 1), (4, 1), (1, 4),
            (3, 3), (4, 2), (2, 4), (4, 4),
        ]

        targets = list(self.environment.targets)

        self.agents = [
            Agent(
                agent_id=index,
                position=start_positions[index],
                target=targets[index % len(targets)],
            )
            for index in range(self.agent_count)
        ]

    def _apply_runtime_changes(self, step: int) -> None:
        """Introduce dynamic runtime changes."""
        if step == 20:
            self.environment.add_obstacle((9, 6))
            self.environment.add_obstacle((9, 8))
            print("[step 20] Dynamic obstacle introduced.")

        if step == 35:
            for agent in self.agents[:3]:
                agent.communication_enabled = False
            print("[step 35] Temporary communication loss for agents 0, 1, 2.")

        if step == 50:
            for agent in self.agents[:3]:
                agent.communication_enabled = True
            print("[step 50] Communication restored for agents 0, 1, 2.")

    def _move_agents(self) -> None:
        """Move all agents one step according to their local policy."""
        proposed_positions = {
            agent.agent_id: agent.choose_next_position(self.environment)
            for agent in self.agents
        }

        occupied = set()

        for agent in self.agents:
            proposed = proposed_positions[agent.agent_id]

            if proposed in occupied:
                continue

            agent.position = proposed
            occupied.add(proposed)

    def _complete_tasks(self) -> None:
        """Handle completed tasks and reassign agents."""
        for agent in self.agents:
            if agent.has_completed_task():
                self.environment.remove_target(agent.position)
                agent.target = None

        for agent in self.agents:
            if agent.target is None and self.environment.targets:
                agent.target = min(
                    self.environment.targets,
                    key=lambda target: abs(target[0] - agent.position[0]) + abs(target[1] - agent.position[1]),
                )
