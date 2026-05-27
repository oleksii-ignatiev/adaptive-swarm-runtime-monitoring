from swarm.simulation import Simulation


def main() -> None:
    simulation = Simulation(
        width=20,
        height=15,
        agent_count=12,
        max_steps=80,
        communication_radius=5,
        seed=7,
    )
    simulation.run(show_visualization=True)


if __name__ == "__main__":
    main()
