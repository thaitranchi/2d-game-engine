# 2D Game Engine

A lightweight and modular 2D game engine built with **Pygame**. This engine provides a flexible framework for creating 2D games with support for networking, particle effects, multiple levels, and a save system.

## Features

- **Entity Management**: Modular entity system with player, enemy, and power-up entities.
- **Networking**: Basic multiplayer support using Flask-SocketIO.
- **Particle System**: Customizable particle effects.
- **Save System**: Persistent game state using JSON.
- **Multiple Levels**: Support for multiple levels with adjustable difficulty.
- **Sound Effects**: Integrated sound system for collisions and events.

## Prerequisites

- **Python 3.8 or higher**
- **Pygame**: `pip install pygame`
- **Flask-SocketIO**: `pip install flask flask-socketio`

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/2d-game-engine.git
   cd 2d-game-engine
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Flask-SocketIO Server:**
   ```bash
   python ./server/server.py
   ```
2. **Run the Lobby Server:**
   ```bash
   python ./server/lobby_server.py
   ```
3. **Run the Game:**
   ```bash
   python main.py
   ```

## Controls

- **Left Arrow**: Move Left
- **Right Arrow**: Move Right
- **Spacebar**: Jump

## File Structure

```
2d-game-engine/
├── assets/
│   ├── images/
│   ├── sounds/
├── src/
│   ├── entity.py
│   ├── level.py
│   ├── game.py
│   ├── network.py
│   ├── save_system.py
│   └── power_up.py
├── server/
│    ├── server.py
│    ├── lobby_server.py
│    └── auth_helpers.py
├── requirements.txt
├── README.md
```

## Contributing

Contributions are welcome! Feel free to fork the repository and create a pull request.

## License

This project is licensed under the **MIT License**.
