# Adaptive Swarm Runtime Monitoring

A small interactive Python simulation of adaptive swarm coordination with runtime safety monitoring.

This project demonstrates a simplified adaptive swarm system. Agents start from an initial position, move toward assigned targets, adapt around obstacles, react to dynamic runtime changes, and are monitored for safety and communication issues.

## Runtime scenario

The runtime scenario is timed so that all major events happen before the simulation can finish:

- Step 8: a dynamic obstacle is introduced.
- Step 14: communication is disabled for agents 0, 1, and 2.
- Step 20: communication is restored for agents 0, 1, and 2.
- The simulation continues until all targets are completed or until the maximum step count is reached.

## Run

```bash
python main.py
```

Then press Start in the simulation window.

Press Finish to stop manually.

## What the window shows

- orange circles: active agents
- blue squares: obstacles
- star markers: remaining targets
- dotted lines: current agent-to-target assignments
- thin lines between agents: active communication links
- pale trajectory lines: previous movement paths
- x markers: agents with disabled communication
- status line: current step, active agents, completed tasks, remaining targets, communication components
- latest monitor event

## Research idea

The goal is not physical drone realism. The goal is to show the software pattern behind adaptive swarm systems:

```text
Environment state
      ↓
Local agent decisions
      ↓
Runtime adaptation
      ↓
Safety and communication monitoring
      ↓
Metrics and event log
```


## Visualization details

The interactive view includes two extra layers:

1. Agent trajectories  
   Each agent leaves a movement trace. This makes adaptation visible because the viewer can see how the swarm moved around obstacles and how agents changed direction during the run.

2. Communication links  
   Agents within communication radius are connected by thin lines. When communication is disabled for agents 0, 1, and 2, those agents are shown with x markers and their communication links disappear. This makes communication fragmentation visible directly in the simulation window.
