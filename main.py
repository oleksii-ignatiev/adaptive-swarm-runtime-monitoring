from swarm.simulation import Simulation
from swarm.interactive_visualization import InteractiveSwarmView


def main() -> None:
    simulation = Simulation(
        width=20,
        height=15,
        agent_count=12,
        max_steps=120,
        communication_radius=5,
        seed=7,
    )

    view = InteractiveSwarmView(simulation=simulation, interval_ms=250)
    view.show()


if __name__ == "__main__":
    main()
