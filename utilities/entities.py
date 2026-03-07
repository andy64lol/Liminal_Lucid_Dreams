"""
Entity module for liminal and nightmare entities
"""
import random
import utilities.data_loader as data_loader
import utilities.colours as colours


class LiminalEntity:
    """Represents a liminal entity that can be encountered in rooms"""
    
    def __init__(self, name, description, behavior, threat_level=1):
        """
        Initialize a liminal entity
        
        Args:
            name: The entity's name
            description: A description of the entity
            behavior: The entity's behavior type
            threat_level: The threat level of the entity (0-5)
        """
        self.name = name
        self.description = description
        self.behavior = behavior
        self.threat_level = threat_level
        self.active = True
    
    def apply_effect(self, player):
        """
        Apply effects to player based on entity behavior and threat level
        
        Args:
            player: The player object to apply effects to
        """
        # Scale effects based on threat level (0-5)
        threat_multiplier = 1 + (self.threat_level * 0.2)
        
        behavior_effects = {
            "follows_player": lambda: (
                int(-random.randint(2, 5) * threat_multiplier),
                int(-random.randint(1, 3) * threat_multiplier)
            ),
            "reality_distortion": lambda: (
                int(-random.randint(5, 10) * threat_multiplier),
                int(-random.randint(3, 7) * threat_multiplier)
            ),
            "temporal_manipulation": lambda: (
                int(-random.randint(8, 15) * threat_multiplier),
                int(-random.randint(5, 10) * threat_multiplier)
            ),
            "constant_surveillance": lambda: (
                int(-random.randint(3, 8) * threat_multiplier),
                None
            ),
            "replays_memories": lambda: (
                int(-random.randint(2, 6) * threat_multiplier),
                int(-random.randint(1, 3) * threat_multiplier)
            ),
            "mimics_player": lambda: (
                int(-random.randint(4, 8) * threat_multiplier),
                int(-random.randint(2, 5) * threat_multiplier)
            ),
            "shape_shifting": lambda: (
                int(-random.randint(3, 7) * threat_multiplier),
                None
            ),
            "memory_absorption": lambda: (
                int(-random.randint(5, 10) * threat_multiplier),
                int(-random.randint(3, 8) * threat_multiplier)
            ),
            "rift_protection": lambda: (
                int(-random.randint(2, 5) * threat_multiplier),
                None
            ),
            "event_repetition": lambda: (
                int(-random.randint(4, 8) * threat_multiplier),
                None
            ),
            "memory_theft": lambda: (
                int(-random.randint(6, 12) * threat_multiplier),
                int(-random.randint(5, 10) * threat_multiplier)
            ),
            "time_revelation": lambda: (
                int(random.randint(1, 3) * threat_multiplier),
                int(-random.randint(2, 5) * threat_multiplier)
            ),
            "psychic_messaging": lambda: (
                int(-random.randint(3, 7) * threat_multiplier),
                None
            ),
            "reality_manipulation": lambda: (
                int(-random.randint(4, 8) * threat_multiplier),
                None
            ),
            "shadow_attachment": lambda: (
                int(-random.randint(3, 6) * threat_multiplier),
                None
            ),
            "paralysis_induction": lambda: (
                int(-random.randint(5, 10) * threat_multiplier),
                None
            ),
            "spatial_manipulation": lambda: (
                int(-random.randint(4, 9) * threat_multiplier),
                None
            ),
            "nightmare_harvesting": lambda: (
                int(-random.randint(3, 6) * threat_multiplier),
                int(-random.randint(2, 5) * threat_multiplier)
            ),
            "dream_protection": lambda: (
                int(random.randint(5, 10) * threat_multiplier),
                None
            ),
            "dream_consumption": lambda: (
                int(-random.randint(7, 15) * threat_multiplier),
                int(-random.randint(5, 12) * threat_multiplier)
            ),
            "reality_leakage": lambda: (
                int(-random.randint(4, 8) * threat_multiplier),
                int(-random.randint(3, 7) * threat_multiplier)
            ),
            "realm_creation": lambda: (
                int(-random.randint(5, 10) * threat_multiplier),
                int(-random.randint(4, 8) * threat_multiplier)
            )
        }
        
        effect = behavior_effects.get(self.behavior)
        if effect:
            sanity_change, reality_change = effect()
            if sanity_change is not None:
                player.sanity = max(0, player.sanity + sanity_change)
                # Log threat level effect
                if self.threat_level >= 4:
                    print(f"{colours.RED}The {self.name} (Threat: {self.threat_level}) deals {abs(sanity_change)} sanity damage!{colours.RESET_ALL}")
                elif self.threat_level >= 2:
                    print(f"{colours.YELLOW}The {self.name} (Threat: {self.threat_level}) affects you for {abs(sanity_change)} sanity.{colours.RESET_ALL}")
            if reality_change is not None and hasattr(player, 'reality_coherence'):
                player.reality_coherence = max(0, player.reality_coherence + reality_change)
        
        player.entity_encounters += 1
        player.last_entity_encounter = self.name
        player.update_psychological_state()


class NightmareEntity:
    """Represents a nightmare entity in nightmare mode"""
    
    def __init__(self, name, speed, friendly=False, theme="unknown"):
        """
        Initialize a nightmare entity
        
        Args:
            name: The entity's name
            speed: Movement speed (0.0-1.0)
            friendly: Whether the entity is friendly
            theme: The theme this entity belongs to
        """
        self.name = name
        self.speed = speed
        self.friendly = friendly
        self.theme = theme
        self.pos = (0, 0, 0)
    
    def move_towards(self, player_x, player_y, player_z, world_bounds):
        """
        Move towards the player
        
        Args:
            player_x, player_y, player_z: Player position
            world_bounds: Dictionary with x_min, x_max, y_min, y_max, z_min, z_max
        """
        if self.friendly:
            return  # Friendly entities don't chase
        
        if random.random() < self.speed:
            dx = player_x - self.pos[0]
            dy = player_y - self.pos[1]
            dz = player_z - self.pos[2]
            
            directions = []
            if dx != 0:
                directions.append(('x', 1 if dx > 0 else -1))
            if dy != 0:
                directions.append(('y', 1 if dy > 0 else -1))
            if dz != 0:
                directions.append(('z', 1 if dz > 0 else -1))
            
            if directions:
                axis, step = random.choice(directions)
                x, y, z = self.pos
                if axis == 'x':
                    x += step
                elif axis == 'y':
                    y += step
                else:
                    z += step
                
                # Keep within bounds
                x = max(world_bounds['x_min'], min(world_bounds['x_max'], x))
                y = max(world_bounds['y_min'], min(world_bounds['y_max'], y))
                z = max(world_bounds['z_min'], min(world_bounds['z_max'], z))
                
                self.pos = (x, y, z)
    
    def distance_to(self, x, y, z):
        """Calculate Manhattan distance to a position"""
        return abs(self.pos[0] - x) + abs(self.pos[1] - y) + abs(self.pos[2] - z)


def get_liminal_entities():
    """
    Get all liminal entities from data file
    
    Returns:
        Dictionary of LiminalEntity objects
    """
    entities_data = data_loader.get_liminal_entities()
    return {
        key: LiminalEntity(data['name'], data['description'], data['behavior'], data.get('threat_level', 1))
        for key, data in entities_data.items()
    }


def get_nightmare_entities_for_theme(theme):
    """
    Get nightmare entities for a specific theme
    
    Args:
        theme: The theme name
        
    Returns:
        List of NightmareEntity objects
    """
    entities_data = data_loader.get_nightmare_entities_for_theme(theme)
    return [
        NightmareEntity(data['name'], data['speed'], data.get('friendly', False), data.get('theme', theme))
        for data in entities_data
    ]


def create_nightmare_entity(entity_data, position):
    """
    Create a nightmare entity from data with position
    
    Args:
        entity_data: Dictionary with entity data
        position: Tuple of (x, y, z) position
        
    Returns:
        NightmareEntity object
    """
    entity = NightmareEntity(
        entity_data['name'],
        entity_data['speed'],
        entity_data.get('friendly', False),
        entity_data.get('theme', 'unknown')
    )
    entity.pos = position
    return entity
