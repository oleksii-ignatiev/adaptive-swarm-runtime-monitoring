from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Set, Tuple

from swarm.agent import Agent
from swarm.environment import Environment
from swarm.monitor import RuntimeMonitor

Position = Tuple[int, int]


@dataclass
class Simulation:
    """Runs one adaptive swarm simulation."""

    width: int
    height: int
    agent_count: int
    max_steps: int
    communication_radius: int
    seed: int = 1
    current_step: int = field(default=0, init=False)
    finished: bool = field(default=False, init=False)
    finish_reason: str = field(default="", init=False)
    completed_task_count: int = field(default=0, init=False)
    completed_targets: Set[Position] = field(default_factory=set, init=False)
    environment: Environment = field(init=False)
    agents: List[Agent] = field(init=False)
    monitor: RuntimeMonitor = field(default_factory=RuntimeMonitor)

    def __post_init__(self) -> None:
        random.seed(self.seed)
        self.environment = Environment(width=self.width, height=self.height)
        self._create_obstacles()
        self._create_targets()
        self._create_agents()
        self.monitor.evaluate(
            step=self.current_step,
            agents=self.agents,
            environment=self.environment,
            communication_radius=self.communication_radius,
            completed_task_count=self.completed_task_count,
        )

    def step(self) -> None:
        """Execute one simulation step."""
        if self.finished:
            return

        self.current_step += 1
        self._apply_runtime_changes(self.current_step)
        self._move_agents()
        self._complete_tasks()
        self.monitor.evaluate(
            step=self.current_step,
            agents=self.agents,
            environment=self.environment,
            communication_radius=self.communication_radius,
            completed_task_count=self.completed_task_count,
        )

        if not self.environment.targets:
            self.finished = True
            self.finish_reason = f"All tasks completed at step {self.current_step}."

        if self.current_step >= self.max_steps:
            self.finished = True
            self.finish_reason = f"Maximum step count reached at step {self.current_step}."

    def finish_manually(self) -> None:
        """Stop the simulation manually."""
        self.finished = True
        self.finish_reason = f"Stopped manually at step {self.current_step}."

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
            (19, 13), (16, 4), (4, 12), (14, 2),
            (18, 10), (7, 13),
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
        """Introduce dynamic runtime changes before the simulation can finish."""
        if step == 8:
            self.environment.add_obstacle((9, 6))
            self.environment.add_obstacle((9, 8))
            self.monitor.events.append("[step 8] Dynamic obstacle introduced.")

        if step == 14:
            for agent in self.agents[:3]:
                agent.communication_enabled = False
            self.monitor.events.append("[step 14] Temporary communication loss for agents 0, 1, 2.")

        if step == 20:
            for agent in self.agents[:3]:
                agent.communication_enabled = True
            self.monitor.events.append("[step 20] Communication restored for agents 0, 1, 2.")

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
            if agent.target is not None and agent.position == agent.target:
                completed_target = agent.target

                if completed_target not in self.completed_targets:
                    self.completed_targets.add(completed_target)
                    self.completed_task_count += 1

                self.environment.remove_target(completed_target)
                agent.target = None

        for agent in self.agents:
            if agent.target is None and self.environment.targets:
                agent.target = min(
                    self.environment.targets,
                    key=lambda target: abs(target[0] - agent.position[0]) + abs(target[1] - agent.position[1]),
                )
