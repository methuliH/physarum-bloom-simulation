<h1 align="center">Physarum Bloom Simulation</h1>
<p align="center">A slime mold simulation built with Pygame and NumPy - agents sense, follow trails, and paint emergent organic patterns in real time.</p>

[![Python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org/)

## Description

This project simulates slime mold behaviour using thousands of autonomous agents moving across a 2D grid. Each agent deposits a chemical trail, senses the trail ahead of it, and steers toward stronger concentrations - causing the swarm to self-organise into vein-like, branching structures. The repo also includes **Prism Iris**, a small turtle-graphics rainbow colour wheel.
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
| Prism Iris graphic | `turtle` + `colorsys` (standard library) |
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

The repo contains two standalone scripts:

```bash
# Physarum slime mold simulation with radial bloom
python main.py

# Prism Iris - rainbow colour-wheel graphic drawn with turtle
python prism_iris.py
```

### Controls (main.py)

| Key | Action |
|-----|--------|
| `UP` arrow | Increase gamma by 0.1 |
| `DOWN` arrow | Decrease gamma by 0.1 |
| Close window | Quit |

The current gamma and radial strength are shown in the top-left corner of the window.

## Prism Iris

`prism_iris.py` is a separate generative graphic built with Python's built-in `turtle` and `colorsys` modules. On a black background it draws 360 rotated sets of concentric circles and dots, stepping the hue slightly each iteration (`hsv_to_rgb`) to produce a glowing rainbow colour wheel. It needs no extra packages beyond a Python install with Tkinter; close the window to exit.

## Project Structure

```
physarum-bloom-simulation/
├── main.py         # Slime mold sim: sensing, steering, blur, age-based colour, gamma, radial bloom
├── prism_iris.py   # Rainbow colour-wheel graphic using turtle
└── README.md
```

## Key Parameters (main.py)

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
| `TURN_SPEED` | 0.1 | How sharply agents steer toward the strongest trail (radians/frame) |
| `RADIAL_STRENGTH` | 0.02 | Outward bias from screen centre |

## License

Released under the [MIT License](LICENSE).
