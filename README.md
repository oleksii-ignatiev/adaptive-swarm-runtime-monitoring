# Adaptive Swarm Runtime Monitoring

A small interactive Python simulation of adaptive swarm coordination with runtime safety monitoring.

This project demonstrates a simplified adaptive swarm system. Agents start from an initial position, move toward assigned targets, adapt around obstacles, react to dynamic runtime changes, and are monitored for safety and communication issues.

The simulation has an interactive window with:

- initial swarm state
- Start button
- Finish button
- step-by-step movement
- dynamic obstacle introduction
- temporary communication failure
- runtime monitor status
- automatic stop when all tasks are completed or the maximum step count is reached

## Research idea

The project explores a simplified version of this question:

How can a group of autonomous agents adapt at runtime while a monitor checks safety-relevant conditions?

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

## What the simulation demonstrates

- decentralized agents
- local movement decisions
- runtime adaptation
- dynamic obstacles
- temporary communication degradation
- collision monitoring
- obstacle violation monitoring
- communication graph monitoring
- task completion tracking

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

Then press Start in the simulation window.

Press Finish to stop manually.

The simulation also stops automatically when all tasks are completed or the maximum step count is reached.

## Runtime events

At step 20, a dynamic obstacle is introduced.

At step 35, communication is disabled for agents 0, 1, and 2.

At step 50, communication is restored for these agents.

The runtime monitor displays current status in the window and prints a summary after the simulation is finished.

## Author

Oleksii Ignatiev
