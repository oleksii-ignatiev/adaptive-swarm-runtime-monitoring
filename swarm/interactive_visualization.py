from __future__ import annotations

from typing import Optional

from matplotlib.lines import Line2D

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

from swarm.simulation import Simulation


class InteractiveSwarmView:
    """Interactive matplotlib view with Start and Finish buttons."""

    def __init__(self, simulation: Simulation, interval_ms: int = 250) -> None:
        self.simulation = simulation
        self.interval_ms = interval_ms
        self.running = False
        self.summary_printed = False
        self.animation: Optional[FuncAnimation] = None

        self.figure, self.axis = plt.subplots(figsize=(10, 7))
        self.figure.subplots_adjust(bottom=0.22)

        start_axis = self.figure.add_axes([0.32, 0.06, 0.14, 0.07])
        finish_axis = self.figure.add_axes([0.54, 0.06, 0.14, 0.07])

        self.start_button = Button(start_axis, "Start")
        self.finish_button = Button(finish_axis, "Finish")

        self.start_button.on_clicked(self._start)
        self.finish_button.on_clicked(self._finish)

        self.status_text = self.figure.text(0.5, 0.16, "", ha="center", fontsize=10)
        self.event_text = self.figure.text(0.5, 0.135, "", ha="center", fontsize=9)

        self._draw()

    def show(self) -> None:
        """Open the interactive simulation window."""
        self.animation = FuncAnimation(
            self.figure,
            self._animate,
            interval=self.interval_ms,
            cache_frame_data=False,
        )
        plt.show()

    def _start(self, event) -> None:
        """Start or resume the simulation."""
        if not self.simulation.finished:
            self.running = True

    def _finish(self, event) -> None:
        """Stop the simulation manually."""
        self.running = False
        self.simulation.finish_manually()
        self._print_summary_once()
        self._draw()

    def _animate(self, frame_index: int) -> None:
        """Animation callback."""
        if self.running and not self.simulation.finished:
            self.simulation.step()

            if self.simulation.finished:
                self.running = False
                self._print_summary_once()

        self._draw()

    def _print_summary_once(self) -> None:
        """Print monitor summary once."""
        if not self.summary_printed:
            self.simulation.monitor.print_summary()
            self.summary_printed = True

    def _draw(self) -> None:
        """Draw current simulation state."""
        self.axis.clear()

        self._draw_obstacles()
        self._draw_targets()
        self._draw_trajectories()
        self._draw_communication_links()
        self._draw_agents()

        title = "Adaptive Swarm Runtime Monitoring"
        if self.simulation.finished and self.simulation.finish_reason:
            title = f"{title} | {self.simulation.finish_reason}"

        self.axis.set_title(title)
        self.axis.set_xlim(-1, self.simulation.environment.width)
        self.axis.set_ylim(-1, self.simulation.environment.height)
        self.axis.set_xlabel("x")
        self.axis.set_ylabel("y")
        self.axis.grid(True)
        self._draw_custom_legend()

        self.status_text.set_text(self.simulation.monitor.get_latest_status())
        self.event_text.set_text(self.simulation.monitor.get_latest_event())

        self.figure.canvas.draw_idle()

    def _draw_obstacles(self) -> None:
        obstacles = self.simulation.environment.obstacles

        if not obstacles:
            return

        obstacle_x = [position[0] for position in obstacles]
        obstacle_y = [position[1] for position in obstacles]

        self.axis.scatter(
            obstacle_x,
            obstacle_y,
            marker="s",
            s=80,
            label="Obstacles",
        )

    def _draw_targets(self) -> None:
        targets = self.simulation.environment.targets

        if not targets:
            return

        target_x = [position[0] for position in targets]
        target_y = [position[1] for position in targets]

        self.axis.scatter(
            target_x,
            target_y,
            marker="*",
            s=180,
            label="Targets",
        )

    def _draw_agents(self) -> None:
        agents = [agent for agent in self.simulation.agents if agent.active]

        if not agents:
            return

        connected_agents = [agent for agent in agents if agent.communication_enabled]
        disconnected_agents = [agent for agent in agents if not agent.communication_enabled]

        if connected_agents:
            self.axis.scatter(
                [agent.position[0] for agent in connected_agents],
                [agent.position[1] for agent in connected_agents],
                marker="o",
                s=80,
                label="Agents",
            )

        if disconnected_agents:
            self.axis.scatter(
                [agent.position[0] for agent in disconnected_agents],
                [agent.position[1] for agent in disconnected_agents],
                marker="x",
                s=120,
                label="Communication disabled",
            )

        for agent in agents:
            self.axis.text(
                agent.position[0] + 0.15,
                agent.position[1] + 0.15,
                str(agent.agent_id),
                fontsize=9,
            )

            if agent.target is not None:
                self.axis.plot(
                    [agent.position[0], agent.target[0]],
                    [agent.position[1], agent.target[1]],
                    linestyle=":",
                    linewidth=0.8,
                )


    def _draw_trajectories(self) -> None:
        """Draw movement history for each agent."""
        for agent_id, path in self.simulation.agent_paths.items():
            if len(path) < 2:
                continue

            path_x = [position[0] for position in path]
            path_y = [position[1] for position in path]

            self.axis.plot(
                path_x,
                path_y,
                linestyle="-",
                linewidth=0.7,
                alpha=0.35,
            )

    def _draw_communication_links(self) -> None:
        """Draw active communication links between connected agents."""
        agents = [
            agent for agent in self.simulation.agents
            if agent.active and agent.communication_enabled
        ]

        radius = self.simulation.communication_radius

        for i, first in enumerate(agents):
            for second in agents[i + 1:]:
                distance = abs(first.position[0] - second.position[0]) + abs(first.position[1] - second.position[1])

                if distance <= radius:
                    self.axis.plot(
                        [first.position[0], second.position[0]],
                        [first.position[1], second.position[1]],
                        linestyle="-",
                        linewidth=0.6,
                        alpha=0.25,
                    )


    def _draw_custom_legend(self) -> None:
        """Draw custom legend entries for all visual layers."""
        legend_items = [
            Line2D([0], [0], marker="s", linestyle="", markersize=8, label="Obstacles"),
            Line2D([0], [0], marker="o", linestyle="", markersize=8, label="Agents"),
            Line2D([0], [0], marker="*", linestyle="", markersize=12, label="Targets"),
            Line2D([0], [0], linestyle="-", linewidth=1.0, alpha=0.35, label="Agent trajectory"),
            Line2D([0], [0], linestyle="-", linewidth=1.0, alpha=0.25, label="Communication link"),
            Line2D([0], [0], linestyle=":", linewidth=1.0, label="Target assignment"),
            Line2D([0], [0], marker="x", linestyle="", markersize=8, label="Communication disabled"),
        ]

        self.axis.legend(handles=legend_items, loc="upper right")
