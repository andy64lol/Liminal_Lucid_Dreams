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


class Anomaly:
    """Represents an anomaly that can affect the player's sanity and reality"""
    
    def __init__(self, name, description, effect):
        """
        Initialize an anomaly
        
        Args:
            name: The anomaly's name
            description: A description of the anomaly
            effect: The effect type this anomaly has
        """
        self.name = name
        self.description = description
        self.effect = effect
    
    def apply_effect(self, player):
        """
        Apply effects to player based on anomaly effect type
        
        Args:
            player: The player object to apply effects to
        """
        effect_values = {
            "time_loop": lambda: (
                -random.randint(10, 20),
                -random.randint(5, 15),
                None
            ),
            "physics_distortion": lambda: (
                -random.randint(3, 8),
                -random.randint(8, 15),
                None
            ),
            "memory_manifestation": lambda: (
                -random.randint(5, 12),
                None,
                -random.randint(10, 25)
            ),
            "dimensional_breach": lambda: (
                -random.randint(8, 15),
                -random.randint(15, 30),
                None
            ),
            "gravity_distortion": lambda: (
                -random.randint(4, 9),
                -random.randint(5, 12),
                None
            ),
            "perception_shift": lambda: (
                -random.randint(6, 12),
                -random.randint(4, 10),
                None
            ),
            "reality_flicker": lambda: (
                -random.randint(3, 7),
                -random.randint(6, 14),
                None
            ),
            "temporal_stutter": lambda: (
                -random.randint(5, 10),
                None,
                -random.randint(8, 16)
            ),
            "spatial_loop": lambda: (
                -random.randint(4, 8),
                -random.randint(3, 9),
                None
            ),
            "void_manifestation": lambda: (
                -random.randint(10, 18),
                -random.randint(12, 22),
                None
            )
        }
        
        effect_fn = effect_values.get(self.effect)
        if effect_fn:
            sanity_change, reality_change, memory_change = effect_fn()
            if sanity_change is not None:
                player.sanity = max(0, player.sanity + sanity_change)
                print(f"{colours.MAGENTA}The {self.name} affects your mind: {abs(sanity_change)} sanity.{colours.RESET_ALL}")
            if reality_change is not None and hasattr(player, 'reality_coherence'):
                player.reality_coherence = max(0, player.reality_coherence + reality_change)
                print(f"{colours.MAGENTA}The {self.name} distorts reality: {abs(reality_change)} reality.{colours.RESET_ALL}")
            if memory_change is not None and hasattr(player, 'memory_stability'):
                player.memory_stability = max(0, player.memory_stability + memory_change)
                print(f"{colours.MAGENTA}The {self.name} affects your memory: {abs(memory_change)} memory.{colours.RESET_ALL}")
        
        if hasattr(player, 'anomaly_exposures'):
            player.anomaly_exposures += 1
        if hasattr(player, 'update_psychological_state'):
            player.update_psychological_state()


class MemoryFragment:
    """Represents a memory fragment that can be found and triggered"""
    
    def __init__(self, content, emotional_weight, clarity=1.0):
        """
        Initialize a memory fragment
        
        Args:
            content: The content/description of the memory
            emotional_weight: The emotional weight (1-10 scale)
            clarity: How clear the memory is (0.0-1.0)
        """
        self.content = content
        self.emotional_weight = emotional_weight
        self.clarity = clarity
        self.triggered = False
    
    def apply_effect(self, player):
        """
        Apply effects to player based on memory fragment properties
        
        Args:
            player: The player object to apply effects to
        """
        self.triggered = True
        
        print(f"\n{colours.YELLOW}🧠 Memory Fragment Activated:{colours.RESET_ALL}")
        print(f"{self.content}")
        
        # Apply emotional effects based on weight
        if self.emotional_weight >= 8:
            sanity_change = -random.randint(5, 15)
            player.sanity = max(0, player.sanity + sanity_change)
            print(f"{colours.RED}The intensity of this memory weighs heavily on your mind...{colours.RESET_ALL}")
        elif self.emotional_weight >= 6:
            sanity_change = -random.randint(2, 8)
            player.sanity = max(0, player.sanity + sanity_change)
            print(f"{colours.YELLOW}This memory stirs something deep within you...{colours.RESET_ALL}")
        else:
            sanity_change = random.randint(1, 5)
            player.sanity = min(100, player.sanity + sanity_change)
            print(f"{colours.GREEN}This gentle memory provides some comfort...{colours.RESET_ALL}")
        
        # Clarity affects reality perception
        if self.clarity < 0.5 and hasattr(player, 'reality_coherence'):
            reality_change = -random.randint(3, 10)
            player.reality_coherence = max(0, player.reality_coherence + reality_change)
            print(f"{colours.MAGENTA}The unclear nature of this memory distorts your perception...{colours.RESET_ALL}")


class DimensionalRift:
    """Represents a dimensional rift that allows travel between areas"""
    
    def __init__(self, destination_type, stability=0.5):
        """
        Initialize a dimensional rift
        
        Args:
            destination_type: The type of destination this rift leads to
            stability: The stability of the rift (0.0-1.0)
        """
        self.destination_type = destination_type
        self.stability = stability
        self.uses_remaining = random.randint(1, 3)
    
    def apply_effect(self, player):
        """
        Apply effects to player based on rift stability
        
        Args:
            player: The player object to apply effects to
        """
        print(f"\n{colours.MAGENTA}🌀 Dimensional Rift Activated:{colours.RESET_ALL}")
        print(f"You step through the rift and find yourself in...")
        print(f"{self.destination_type}")
        
        # Apply stability effects
        if self.stability < 0.3:
            reality_change = -random.randint(10, 20)
            sanity_change = -random.randint(5, 15)
            if hasattr(player, 'reality_coherence'):
                player.reality_coherence = max(0, player.reality_coherence + reality_change)
            player.sanity = max(0, player.sanity + sanity_change)
            print(f"{colours.RED}The unstable rift tears at your very being!{colours.RESET_ALL}")
        elif self.stability < 0.6:
            reality_change = -random.randint(5, 10)
            if hasattr(player, 'reality_coherence'):
                player.reality_coherence = max(0, player.reality_coherence + reality_change)
            print(f"{colours.YELLOW}The rift's instability makes you feel disoriented...{colours.RESET_ALL}")
        else:
            memory_change = random.randint(5, 15)
            if hasattr(player, 'memory_stability'):
                player.memory_stability = min(100, player.memory_stability + memory_change)
            print(f"{colours.GREEN}The stable rift grants you new insights...{colours.RESET_ALL}")
        
        self.uses_remaining -= 1
        if self.uses_remaining <= 0:
            print(f"{colours.LIGHTBLACK_EX}The rift collapses behind you...{colours.RESET_ALL}")


class EchoEvent:
    """Represents an echo event that creates atmospheric interactions"""
    
    def __init__(self, event_type, intensity, duration=1):
        """
        Initialize an echo event
        
        Args:
            event_type: The type of echo event
            intensity: The intensity (1-5 scale)
            duration: How many turns the event lasts
        """
        self.event_type = event_type
        self.intensity = intensity
        self.duration = duration
        self.active_turns = 0
    
    def apply_effect(self, player):
        """
        Apply effects to player based on echo event properties
        
        Args:
            player: The player object to apply effects to
        """
        self.active_turns += 1
        
        effect_values = {
            "whisper": lambda: -random.randint(1, 3),
            "footstep": lambda: -random.randint(2, 5),
            "voice": lambda: -random.randint(3, 7),
            "scream": lambda: -random.randint(5, 12),
            "laughter": lambda: -random.randint(2, 6),
            "weeping": lambda: -random.randint(3, 8),
            "breathing": lambda: -random.randint(1, 4),
            "mumbling": lambda: -random.randint(1, 3)
        }
        
        effect_fn = effect_values.get(self.event_type)
        if effect_fn:
            sanity_change = effect_fn() * (self.intensity / 3)
            sanity_change = int(sanity_change)
            player.sanity = max(0, player.sanity + sanity_change)
            
            descriptions = {
                "whisper": "You hear whispered words you can't quite make out.",
                "footstep": "Footsteps echo from somewhere nearby.",
                "voice": "A voice calls out to you from the darkness.",
                "scream": "A piercing scream echoes through the space!",
                "laughter": "Mad laughter echoes around you.",
                "weeping": "You hear someone weeping softly.",
                "breathing": "Heavy breathing seems to come from everywhere.",
                "mumbling": "Mumbling voices compete for your attention."
            }
            print(f"{colours.CYAN}{descriptions.get(self.event_type, 'An echo resonates through the space.')}{colours.RESET_ALL}")


class PhantomInteraction:
    """Represents a phantom interaction with an entity"""
    
    def __init__(self, interaction_type, entity_name, success_chance=0.7):
        """
        Initialize a phantom interaction
        
        Args:
            interaction_type: The type of interaction
            entity_name: The name of the entity being interacted with
            success_chance: Chance of successful interaction (0.0-1.0)
        """
        self.interaction_type = interaction_type
        self.entity_name = entity_name
        self.success_chance = success_chance
        self.completed = False
    
    def apply_effect(self, player):
        """
        Apply effects to player based on interaction result
        
        Args:
            player: The player object to apply effects to
        """
        self.completed = True
        
        success = random.random() < self.success_chance
        
        interaction_effects = {
            "communicate": lambda s: (
                random.randint(5, 10) if s else -random.randint(3, 8),
                "The entity seems to understand you." if s else "The entity ignores your attempts to communicate."
            ),
            "observe": lambda s: (
                random.randint(2, 5) if s else -random.randint(1, 3),
                "You observe the entity carefully." if s else "The entity notices you watching."
            ),
            "challenge": lambda s: (
                -random.randint(8, 15) if s else -random.randint(5, 10),
                "You challenge the entity's presence." if s else "You hesitate to challenge the entity."
            ),
            "bargain": lambda s: (
                random.randint(3, 8) if s else -random.randint(4, 9),
                "The entity accepts your bargain." if s else "The entity rejects your offer."
            ),
            "flee": lambda s: (
                -random.randint(2, 5) if not s else 0,
                "You manage to escape unnoticed." if s else "Your attempt to flee attracts attention!"
            )
        }
        
        effect_fn = interaction_effects.get(self.interaction_type)
        if effect_fn:
            sanity_change, message = effect_fn(success)
            player.sanity = max(0, min(100, player.sanity + sanity_change))
            print(f"{colours.LIGHTRED_EX}{message}{colours.RESET_ALL}")


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

