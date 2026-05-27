from __future__ import annotations

from typing import List

import matplotlib.pyplot as plt

from swarm.agent import Agent
from swarm.environment import Environment


def visualize(environment: Environment, agents: List[Agent], metrics: List[dict]) -> None:
    """Render the final state of the simulation."""
    fig, ax = plt.subplots(figsize=(9, 6))

    if environment.obstacles:
        obstacle_x = [position[0] for position in environment.obstacles]
        obstacle_y = [position[1] for position in environment.obstacles]
        ax.scatter(obstacle_x, obstacle_y, marker="s", label="Obstacles")

    if environment.targets:
        target_x = [position[0] for position in environment.targets]
        target_y = [position[1] for position in environment.targets]
        ax.scatter(target_x, target_y, marker="*", s=160, label="Remaining targets")

    agent_x = [agent.position[0] for agent in agents if agent.active]
    agent_y = [agent.position[1] for agent in agents if agent.active]
    ax.scatter(agent_x, agent_y, marker="o", label="Agents")

    for agent in agents:
        ax.text(agent.position[0] + 0.15, agent.position[1] + 0.15, str(agent.agent_id), fontsize=9)

    ax.set_title("Adaptive Swarm Runtime Monitoring: Final State")
    ax.set_xlim(-1, environment.width)
    ax.set_ylim(-1, environment.height)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    ax.legend()
    plt.show()
