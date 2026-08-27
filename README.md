<h1 align="center">Physarum Bloom Simulation</h1>
<p align="center">A slime mold simulation built with Pygame and NumPy - agents sense, follow trails, and paint emergent organic patterns in real time.</p>

[![Python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org/)

## Description

This project simulates slime mold behaviour using thousands of autonomous agents moving across a 2D grid. Each agent deposits a chemical trail, senses the trail ahead of it, and steers toward stronger concentrations - causing the swarm to self-organise into vein-like, branching structures. The simulation is developed incrementally across several goal files, each adding a new layer of behaviour or visual effect.
<img width="800" height="630" alt="image" src="https://github.com/user-attachments/assets/3aa2648a-0d31-48c5-8a33-64cdc014b3f2" />
<img width="793" height="625" alt="image" src="https://github.com/user-attachments/assets/504fa213-86d9-4546-a6da-2c4dd876b19d" />




## Features

- **Trail map with decay and blur** - each agent deposits onto a float32 grid that fades and diffuses each frame using `uniform_filter`, producing smooth, spreading trails
- **Three-sensor steering** - agents read trail intensity at left, center, and right positions ahead and turn toward the strongest signal, creating emergent path-following
- **Age-based colour palette** - a second `age` array tracks how long each pixel has been active and interpolates through a 4-colour palette (Hot Paprika → Honeycomb → Biscuit → Crumpet)
- **Gamma correction control** - UP/DOWN arrow keys adjust the gamma exponent live, crushing dim areas toward black or opening up the midtones
- **Radial bloom mode** - agents receive a gentle outward bias from the screen centre, producing flower-like radiating structures
- **60 FPS real-time rendering** via `pygame.surfarray.blit_array` with direct NumPy array blitting

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Simulation | NumPy (vectorised agent arrays) |
| Rendering | Pygame / pygame-ce |
| Image processing | SciPy (`uniform_filter` blur) |
| Language | Python 3.14 |

## Getting Started

### Prerequisites

- Python 3.14
- pip

### Installation

```bash
pip install pygame-ce numpy scipy
```

> Note: use `pygame-ce` (community edition) instead of `pygame` - the standard `pygame` package does not build on Python 3.14.

## Usage

Each file is a self-contained simulation. Run any of them directly:

```bash
# Bare agents with random walk
python main.py

# Agents with trail deposit and decay
python goal2.py

# Sensing, turning, blur, age-based colour, and gamma control
python goal3.py

# Sensing and turning (clean reference version)
python goal4.py
```

### Controls (goal3.py)

| Key | Action |
|-----|--------|
| `UP` arrow | Increase gamma by 0.1 |
| `DOWN` arrow | Decrease gamma by 0.1 |
| Close window | Quit |

## Project Structure

```
generative_art_game/
├── main.py      # Step 1: random-walk agents, no trail
├── goal2.py     # Step 2: trail deposit, decay, grayscale render
├── goal4.py     # Step 3: three-sensor steering
└── goal3.py     # Step 4: blur, age array, 4-colour palette, gamma, radial bloom
```

## Key Parameters (goal3.py)

| Parameter | Default | Effect |
|-----------|---------|--------|
| `N` | 5000 | Number of agents |
| `SPEED` | 1.5 | Pixels moved per frame |
| `DEPOSIT_AMOUNT` | 15.0 | Trail added per agent per frame |
| `DECAY` | 0.97 | Trail fade rate (per frame multiplier) |
| `AGE_INCREMENT` | 6.0 | Age added per deposit event |
| `AGE_DECAY` | 0.995 | Age fade rate (slower than trail) |
| `AGE_MAX` | 100.0 | Maximum age value before clipping |
| `SENSOR_DIST` | 15.0 | How far ahead sensors look (pixels) |
| `SENSOR_ANGLE` | 0.5 | Left/right sensor offset (radians) |
| `RADIAL_STRENGTH` | 0.02 | Outward bias from screen centre |
