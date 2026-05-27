# Adaptive Swarm Runtime Monitoring

A small Python simulation of adaptive swarm coordination with runtime safety monitoring.

This project was created as a compact research-oriented demonstration for work on trustworthy adaptive autonomous systems. It models a group of agents moving in a grid environment, reacting to dynamic obstacles, temporary communication loss, and task reassignment.

The goal is not to simulate real drones physically. The goal is to demonstrate the core software ideas behind adaptive swarm systems:

- decentralized agents
- local decision-making
- runtime adaptation
- safety constraint monitoring
- communication graph tracking
- event logging and metrics

## Research motivation

Heterogeneous adaptive swarm systems need to continue operating when the environment changes at runtime. A swarm may face obstacles, communication degradation, disconnected agents, task failures, or unsafe movement decisions.

This project explores a simplified version of that problem:

How can a group of agents adapt their movement and task allocation during execution while a runtime monitor checks safety-relevant conditions?

The simulation focuses on:

- collision avoidance
- obstacle avoidance
- communication connectivity
- dynamic task completion
- runtime event tracing

## Project structure

```text
adaptive-swarm-runtime-monitoring/
├── main.py
├── requirements.txt
├── README.md
└── swarm/
    ├── __init__.py
    ├── agent.py
    ├── environment.py
    ├── monitor.py
    ├── simulation.py
    └── visualization.py
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The simulation prints runtime events and opens a simple visualization of the swarm state.

## What the simulation does

1. Creates a grid environment.
2. Creates agents with individual start positions and assigned target tasks.
3. Adds static obstacles.
4. Introduces a dynamic obstacle during runtime.
5. Simulates temporary communication loss for selected agents.
6. Lets agents adapt their movement locally.
7. Uses a runtime monitor to check collisions, obstacle violations, communication connectivity, and task progress.
8. Records metrics for each step.

## Why this is relevant to adaptive swarm systems

Real swarm systems require runtime assurance. A swarm can adapt its behavior, and the system still needs to remain safe, traceable, and understandable.

This project demonstrates the basic software pattern:

```text
Environment state
      ↓
Agent decision
      ↓
Runtime adaptation
      ↓
Safety monitor
      ↓
Metrics and logs
```

## Possible extensions

- Add heterogeneous agent types
- Add energy/battery constraints
- Add probabilistic communication failure
- Add reinforcement learning based movement policies
- Add ROS2 integration
- Add digital twin style monitoring dashboard
- Add formal temporal logic constraints
- Add distributed consensus for task allocation

## Author

Oleksii Ignatiev  
Software Engineer with background in Mathematics and Computer Science
