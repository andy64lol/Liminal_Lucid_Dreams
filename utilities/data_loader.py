"""
Data Loader - Loads game data from JSON files in the data/ directory
"""

import json
import os
import random

# Get the base directory (parent of utilities folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_json(filename):
    """Load a JSON file from the data directory"""
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Data file {filename} not found")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filename}: {e}")
        return {}

# Load all data files
_settings = load_json('settings.json')
_entities = load_json('entities.json')
_memory_fragments = load_json('memory_fragments.json')
_anomalies = load_json('anomalies.json')
_themes = load_json('themes.json')

# Settings accessors
def get_world_bounds():
    return _settings.get('world_bounds', {'x_min': -100, 'x_max': 100, 'y_min': -100, 'y_max': 100, 'z_min': -10, 'z_max': 10})

def get_save_settings():
    return _settings.get('save_settings', {'save_dir': 'saves', 'max_slots': 5})

def get_player_stats():
    return _settings.get('player_stats', {'sanity_max': 100, 'reality_max': 100, 'memory_max': 100})

def get_gameplay_settings():
    return _settings.get('gameplay', {
        'min_heaven_door_distance': 10,
        'entity_spawn_chance': 0.15,
        'anomaly_chance': 0.25,
        'temporal_distortion_chance': 0.10,
        'memory_fragment_chance': 0.20,
        'dimensional_rift_chance': 0.08,
        'echo_event_chance': 0.15,
        'phantom_interaction_chance': 0.12
    })

# Entity accessors
def get_liminal_entities():
    return _entities.get('liminal_entities', {})

def get_nightmare_entities():
    return _entities.get('nightmare_entities', {})

def get_nightmare_entities_for_theme(theme):
    """Get nightmare entities for a specific theme"""
    all_nightmare = get_nightmare_entities()
    return all_nightmare.get(theme, [])

# Memory fragments accessor
def get_memory_fragments():
    return _memory_fragments.get('memory_fragments', [])

# Anomaly accessors
def get_anomalies():
    return _anomalies.get('anomalies', {})

def get_dimensional_rifts():
    return _anomalies.get('dimensional_rifts', {})

def get_echo_events():
    return _anomalies.get('echo_events', [])

# Theme accessors
def get_themes():
    return _themes.get('themes', ['hospital', 'school', 'home', 'limbo', 'mall'])

def get_theme_weights(level):
    """Get theme weights based on player level"""
    weights = _themes.get('theme_weights', {})
    if level < 10:
        return weights.get('early', [1] * 7)
    elif level < 25:
        return weights.get('mid', [1] * 7)
    elif level < 40:
        return weights.get('high', [1] * 7)
    else:
        return weights.get('very_high', [1] * 7)

def get_theme_colors():
    return _themes.get('theme_colors', {})

def get_theme_data(theme):
    """Get full theme data (descriptions, features, paths, interactables)"""
    return _themes.get('rooms', {}).get(theme, {})

def get_all_theme_rooms():
    """Get all theme room data"""
    return _themes.get('rooms', {})

def get_theme_list():
    """Get list of all available themes"""
    return _themes.get('themes', ['hospital', 'school', 'home', 'limbo', 'mall'])

def get_theme_for_level(level, themes_list=None):
    """Get a random theme based on player level"""
    if themes_list is None:
        themes_list = get_theme_list()
    
    weights = get_theme_weights(level)
    
    # Make sure weights match themes
    while len(weights) < len(themes_list):
        weights.append(1)
    
    return random.choices(themes_list, weights=weights[:len(themes_list)], k=1)[0]

