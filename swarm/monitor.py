from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

import networkx as nx

from swarm.agent import Agent
from swarm.environment import Environment


@dataclass
class RuntimeMonitor:
    """Checks runtime safety and coordination properties."""

    events: List[str] = field(default_factory=list)
    metrics: List[Dict[str, int]] = field(default_factory=list)

    def evaluate(
        self,
        step: int,
        agents: List[Agent],
        environment: Environment,
        communication_radius: int,
        completed_task_count: int,
    ) -> None:
        """Evaluate safety and coordination constraints for the current step."""
        self._check_collisions(step, agents)
        self._check_obstacle_violations(step, agents, environment)
        connected_components = self._check_connectivity(step, agents, communication_radius)

        active = sum(1 for agent in agents if agent.active)

        self.metrics.append({
            "step": step,
            "active_agents": active,
            "completed_tasks": completed_task_count,
            "remaining_targets": len(environment.targets),
            "connected_components": connected_components,
        })

    def _check_collisions(self, step: int, agents: List[Agent]) -> None:
        positions = {}

        for agent in agents:
            if not agent.active:
                continue

            if agent.position in positions:
                self.events.append(
                    f"[step {step}] Collision risk: agent {agent.agent_id} and "
                    f"agent {positions[agent.position]} at {agent.position}"
                )
            else:
                positions[agent.position] = agent.agent_id

    def _check_obstacle_violations(
        self,
        step: int,
        agents: List[Agent],
        environment: Environment,
    ) -> None:
        for agent in agents:
            if agent.active and environment.is_obstacle(agent.position):
                self.events.append(
                    f"[step {step}] Safety violation: agent {agent.agent_id} entered obstacle {agent.position}"
                )

    def _check_connectivity(
        self,
        step: int,
        agents: List[Agent],
        communication_radius: int,
    ) -> int:
        active_agents = [
            agent for agent in agents
            if agent.active and agent.communication_enabled
        ]

        graph = nx.Graph()

        for agent in active_agents:
            graph.add_node(agent.agent_id)

        for i, first in enumerate(active_agents):
            for second in active_agents[i + 1:]:
                distance = abs(first.position[0] - second.position[0]) + abs(first.position[1] - second.position[1])

                if distance <= communication_radius:
                    graph.add_edge(first.agent_id, second.agent_id)

        if graph.number_of_nodes() == 0:
            return 0

        components = nx.number_connected_components(graph)

        if components > 1:
            self.events.append(
                f"[step {step}] Communication warning: swarm split into {components} components"
            )

        return components

    def get_latest_status(self) -> str:
        """Return a compact status line for the visualization."""
        if not self.metrics:
            return "Step: 0 | Waiting to start"

        latest = self.metrics[-1]

        return (
            f"Step: {latest['step']} | "
            f"Active agents: {latest['active_agents']} | "
            f"Completed tasks: {latest['completed_tasks']} | "
            f"Remaining targets: {latest['remaining_targets']} | "
            f"Communication components: {latest['connected_components']}"
        )

    def get_latest_event(self) -> str:
        """Return the latest monitor event."""
        if not self.events:
            return "No monitor warnings."
        return self.events[-1]

    def print_summary(self) -> None:
        """Print event log and final metrics."""
        print("\\nRuntime monitor events")
        print("----------------------")

        if not self.events:
            print("No safety warnings recorded.")
        else:
            for event in self.events[-60:]:
                print(event)

        print("\\nFinal metrics")
        print("-------------")

        if self.metrics:
            for key, value in self.metrics[-1].items():
                print(f"{key}: {value}")
