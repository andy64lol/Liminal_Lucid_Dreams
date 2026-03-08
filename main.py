import random
import os
import sys
import time

# Import utility modules
import utilities.colours as colours
import utilities.save_load as save_load
import utilities.styling as styling
import utilities.data_loader as data_loader
import utilities.entities as entities
from utilities.entities import (
    LiminalEntity, 
    Anomaly, 
    MemoryFragment, 
    DimensionalRift, 
    EchoEvent, 
    PhantomInteraction
)

# Game settings from data files
world_bounds = data_loader.get_world_bounds()
X_MIN, X_MAX = world_bounds['x_min'], world_bounds['x_max']
Y_MIN, Y_MAX = world_bounds['y_min'], world_bounds['y_max']
Z_MIN, Z_MAX = world_bounds['z_min'], world_bounds['z_max']

save_settings = data_loader.get_save_settings()
SAVE_DIR = save_settings['save_dir']
MAX_SLOTS = save_settings['max_slots']

player_stats = data_loader.get_player_stats()
SANITY_MAX = player_stats['sanity_max']
REALITY_MAX = player_stats['reality_max']
MEMORY_MAX = player_stats['memory_max']

gameplay = data_loader.get_gameplay_settings()
MIN_HEAVEN_DOOR_DISTANCE = gameplay['min_heaven_door_distance']
ENTITY_SPAWN_CHANCE = gameplay['entity_spawn_chance']
ANOMALY_CHANCE = gameplay['anomaly_chance']
TEMPORAL_DISTORTION_CHANCE = gameplay['temporal_distortion_chance']
MEMORY_FRAGMENT_CHANCE = gameplay['memory_fragment_chance']
DIMENSIONAL_RIFT_CHANCE = gameplay['dimensional_rift_chance']
ECHO_EVENT_CHANCE = gameplay['echo_event_chance']
PHANTOM_INTERACTION_CHANCE = gameplay['phantom_interaction_chance']

# Ensure save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Directions mapping
directions = {
    '/right': (1, 0, 0),
    '/left': (-1, 0, 0),
    '/forward': (0, 1, 0),
    '/backward': (0, -1, 0),
    '/upstairs': (0, 0, 1),
    '/downstairs': (0, 0, -1)
}

doors = ['door1', 'door2', 'door3', 'door4']

# Define liminal entities from data file
liminal_entities_data = data_loader.get_liminal_entities()
ENTITIES = {
    key: LiminalEntity(
        data['name'],
        data['description'],
        data['behavior'],
        data['threat_level']
    )
    for key, data in liminal_entities_data.items()
}

# Memory Fragments from data file
memory_fragments_data = data_loader.get_memory_fragments()
MEMORY_FRAGMENTS = [
    MemoryFragment(data['content'], data['emotional_weight'], data['clarity'])
    for data in memory_fragments_data
]

# Dimensional Rifts from data file
dimensional_rifts_data = data_loader.get_dimensional_rifts()
DIMENSIONAL_RIFTS = {
    key: DimensionalRift(data['destination_type'], data['stability'])
    for key, data in dimensional_rifts_data.items()
}

# Echo Events from data file
echo_events_data = data_loader.get_echo_events()
ECHO_EVENTS = [
    EchoEvent(data['event_type'], data['intensity'], data['duration'])
    for data in echo_events_data
]

# Anomalies from data file
anomalies_data = data_loader.get_anomalies()
ANOMALIES = {
    key: Anomaly(data['name'], data['description'], data['effect'])
    for key, data in anomalies_data.items()
}

# Get available themes from data
AVAILABLE_THEMES = data_loader.get_theme_list()

class Room:
    def __init__(self, theme=None, level=1):
        # Use provided theme or select random one from available themes
        if theme is None:
            theme = random.choice(AVAILABLE_THEMES)
        self.theme = theme
        
        self.level = level
        self.entities = []
        self.anomalies = []
        self.memory_fragments = []
        self.dimensional_rifts = []
        self.echo_events = []
        self.phantom_interactions = []
        self.atmosphere_intensity = random.uniform(0.3, 1.0)
        self.temporal_stability = random.uniform(0.5, 1.0)
        self.reality_coherence = random.uniform(0.4, 1.0)
        self.visited_count = 0
        self.hidden_secrets = random.randint(0, 3)
        self.emotional_resonance = random.uniform(0.2, 1.0)
        
        # Load theme data from JSON using data_loader
        theme_data = data_loader.get_theme_data(self.theme)
        
        # If theme not found in JSON, use fallback data
        if not theme_data:
            theme_data = data_loader.get_theme_data('limbo')
        
        # Get theme-specific data
        self.theme_descriptions = theme_data.get('descriptions', [])
        self.theme_features = theme_data.get('features', ["There are stairs leading up and down."])
        self.theme_paths = theme_data.get('paths', ["Paths extend in all directions."])
        self.theme_interactables = theme_data.get('interactables', [])
        
        self.spawn_entities()
        self.generate_anomalies()
        self.generate_memory_fragments()
        self.generate_dimensional_rifts()
        self.generate_echo_events()
        self.generate_phantom_interactions()
        self.generate_description()

    def spawn_entities(self):
        if random.random() < ENTITY_SPAWN_CHANCE * (1 + self.level * 0.1):
            entity_key = random.choice(list(ENTITIES.keys()))
            self.entities.append(ENTITIES[entity_key])

    def generate_anomalies(self):
        if random.random() < ANOMALY_CHANCE * (1 + self.level * 0.05):
            anomaly_key = random.choice(list(ANOMALIES.keys()))
            self.anomalies.append(ANOMALIES[anomaly_key])

    def generate_memory_fragments(self):
        if random.random() < MEMORY_FRAGMENT_CHANCE:
            fragment = random.choice(MEMORY_FRAGMENTS)
            if not fragment.triggered:
                self.memory_fragments.append(fragment)

    def generate_dimensional_rifts(self):
        if random.random() < DIMENSIONAL_RIFT_CHANCE:
            rift_key = random.choice(list(DIMENSIONAL_RIFTS.keys()))
            rift = DIMENSIONAL_RIFTS[rift_key]
            if rift.uses_remaining > 0:
                self.dimensional_rifts.append(rift)

    def generate_echo_events(self):
        if random.random() < ECHO_EVENT_CHANCE:
            event = random.choice(ECHO_EVENTS)
            self.echo_events.append(event)

    def generate_phantom_interactions(self):
        if random.random() < PHANTOM_INTERACTION_CHANCE and self.entities:
            entity = random.choice(self.entities)
            interaction_types = ["communicate", "observe", "challenge", "bargain", "flee"]
            interaction_type = random.choice(interaction_types)
            phantom = PhantomInteraction(interaction_type, entity.name)
            self.phantom_interactions.append(phantom)

    def get_atmosphere_description(self):
        descriptions = []
        if self.atmosphere_intensity > 0.8:
            descriptions.append(f"{colours.RED}{colours.BRIGHT}The air feels thick and oppressive, making breathing difficult.{colours.RESET_ALL}")
        elif self.atmosphere_intensity > 0.6:
            descriptions.append(f"{colours.YELLOW}An unsettling tension permeates the space.{colours.RESET_ALL}")
        elif self.atmosphere_intensity > 0.4:
            descriptions.append(f"{colours.CYAN}The atmosphere feels slightly off, like something is watching.{colours.RESET_ALL}")

        if self.temporal_stability < 0.3:
            descriptions.append(f"{colours.MAGENTA}{colours.BRIGHT}Time seems to stutter and skip around you.{colours.RESET_ALL}")
        elif self.temporal_stability < 0.6:
            descriptions.append(f"{colours.LIGHTMAGENTA_EX}The flow of time feels inconsistent here.{colours.RESET_ALL}")

        if self.reality_coherence < 0.4:
            descriptions.append(f"{colours.BACK_RED}{colours.WHITE}Reality flickers like a damaged screen.{colours.RESET_ALL}")
        elif self.reality_coherence < 0.7:
            descriptions.append(f"{colours.LIGHTBLACK_EX}The edges of your vision seem to blur and shift.{colours.RESET_ALL}")

        return descriptions

    def get_interactive_elements(self):
        """Get interactive elements that the player can engage with"""
        elements = []
        
        # Memory fragments create interactive opportunities
        for fragment in self.memory_fragments:
            if not fragment.triggered:
                elements.append(f"{colours.YELLOW}🧠 A memory fragment glows softly in the corner{colours.RESET_ALL}")
        
        # Dimensional rifts offer travel options
        for rift in self.dimensional_rifts:
            if rift.uses_remaining > 0:
                elements.append(f"{colours.MAGENTA}🌀 A dimensional rift shimmers in the air{colours.RESET_ALL}")
        
        # Echo events create atmospheric interactions
        for event in self.echo_events:
            if event.active_turns < event.duration:
                elements.append(f"{colours.CYAN}👻 An echo resonates through the space{colours.RESET_ALL}")
        
        # Phantom interactions with entities
        for interaction in self.phantom_interactions:
            if not interaction.completed:
                elements.append(f"{colours.LIGHTRED_EX}👤 You sense a presence nearby that might respond to interaction{colours.RESET_ALL}")
        
        return elements

    def trigger_memory_fragment(self, player):
        """Trigger a memory fragment and affect the player"""
        if self.memory_fragments:
            fragment = self.memory_fragments[0]
            fragment.triggered = True
            
            print(f"\n{colours.YELLOW}🧠 Memory Fragment Activated:{colours.RESET_ALL}")
            print(f"{fragment.content}")
            
            # Apply emotional effects
            if fragment.emotional_weight >= 8:
                player.sanity -= random.randint(5, 15)
                print(f"{colours.RED}The intensity of this memory weighs heavily on your mind...{colours.RESET_ALL}")
            elif fragment.emotional_weight >= 6:
                player.sanity -= random.randint(2, 8)
                print(f"{colours.YELLOW}This memory stirs something deep within you...{colours.RESET_ALL}")
            else:
                player.sanity += random.randint(1, 5)
                print(f"{colours.GREEN}This gentle memory provides some comfort...{colours.RESET_ALL}")
            
            # Clarity affects reality perception
            if fragment.clarity < 0.5:
                player.reality -= random.randint(3, 10)
                print(f"{colours.MAGENTA}The unclear nature of this memory distorts your perception...{colours.RESET_ALL}")
            
            self.memory_fragments.remove(fragment)
            return True
        return False

    def use_dimensional_rift(self, player):
        """Use a dimensional rift for travel"""
        if self.dimensional_rifts:
            rift = self.dimensional_rifts[0]
            rift.uses_remaining -= 1
            
            print(f"\n{colours.MAGENTA}🌀 Dimensional Rift Activated:{colours.RESET_ALL}")
            print("You step through the rift and find yourself in...")
            print(f"{rift.destination_type}")
            
            # Apply stability effects
            if rift.stability < 0.3:
                player.reality -= random.randint(10, 20)
                player.sanity -= random.randint(5, 15)
                print(f"{colours.RED}The unstable rift tears at your very being!{colours.RESET_ALL}")
            elif rift.stability < 0.6:
                player.reality -= random.randint(5, 10)
                print(f"{colours.YELLOW}The rift's instability makes you feel disoriented...{colours.RESET_ALL}")
            else:
                player.memory += random.randint(5, 15)
                print(f"{colours.GREEN}The stable rift grants you new insights...{colours.RESET_ALL}")
            
            if rift.uses_remaining <= 0:
                self.dimensional_rifts.remove(rift)
                print(f"{colours.LIGHTBLACK_EX}The rift collapses behind you...{colours.RESET_ALL}")
            
            return True
        return False

    def generate_description(self):
        """Generate room description using theme data from JSON"""
        # Higher-level rooms have more complex descriptions
        if self.level > 25:
            # Add more disturbing elements for higher levels
            base_descriptions = [(desc[0] + colours.RED + " Something feels very wrong here." + colours.RESET_ALL, desc[1]) for desc in self.theme_descriptions]
        else:
            base_descriptions = self.theme_descriptions

        # Select descriptions based on theme
        if not base_descriptions:
            # Fallback if no descriptions available
            base_descriptions = [(colours.MAGENTA + "A liminal space where reality bends." + colours.RESET_ALL, ['door1', 'door2'])]

        self.description, self.doors = random.choice(base_descriptions)
        self.stairs = random.choice(self.theme_features)
        self.paths = random.choice(self.theme_paths)
        self.interactable = random.choice(self.theme_interactables)

        # Always make some directions available
        # This ensures the player doesn't get stuck in a room
        random_directions = []
        if random.random() < 0.8:  # 80% chance for forward/backward
            random_directions.extend(['/forward', '/backward'])
        if random.random() < 0.7:  # 70% chance for left/right
            random_directions.extend(['/left', '/right'])
        if random.random() < 0.5:  # 50% chance for stairs
            if random.random() < 0.5:
                random_directions.append('/upstairs')
            else:
                random_directions.append('/downstairs')

        # Set available directions based on descriptions + random availability
        self.available_directions = {
            '/upstairs': 'up' in self.stairs.lower() or '/upstairs' in random_directions,
            '/downstairs': ('down' in self.stairs.lower() or 'below' in self.stairs.lower()) or '/downstairs' in random_directions,
            '/forward': ('forward' in self.paths.lower() or 'all' in self.paths.lower()) or '/forward' in random_directions,
            '/backward': ('back' in self.paths.lower() or 'all' in self.paths.lower()) or '/backward' in random_directions,
            '/left': ('left' in self.paths.lower() or 'all' in self.paths.lower()) or '/left' in random_directions,
            '/right': ('right' in self.paths.lower() or 'all' in self.paths.lower()) or '/right' in random_directions
        }

# Enhanced items with effects
items = {
    'battery': 'Restores sanity slightly',
    'flashlight': 'Reveals hidden paths and increases sanity recovery',
    'mysterious key': 'May unlock special doors',
    'old map': 'Shows nearby points of interest',
    'strange coin': 'Makes unusual sounds when danger is near',
    'polaroid camera': 'Captures evidence of the impossible',
    'music box': 'Calms the mind, restoring sanity',
    'compass': 'Points to... something',
    'pills': 'Restores significant sanity',
    'sanity': 'A manifestation of your mental state'
}

class Player:
    def __init__(self, name="Unknown", x=0, y=0, z=0, inventory=None, sanity=100, level=1):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.inventory = inventory if inventory is not None else []
        self.sanity = int(sanity)
        self.reality_coherence = REALITY_MAX
        self.memory_stability = MEMORY_MAX
        self.temporal_awareness = 100
        self.has_light = False
        self.level = level
        self.entity_encounters = 0
        self.anomaly_exposures = 0
        self.deepest_level = 0
        self.psychological_state = "stable"
        self.last_entity_encounter = None
        self.active_effects = []
    def update_psychological_state(self):
        """Update psychological state based on various metrics"""
        if self.sanity < 20:
            self.psychological_state = "critical_breakdown"
        elif self.sanity < 40:
            self.psychological_state = "severe_distress"
        elif self.sanity < 60:
            self.psychological_state = "unstable"
        elif self.sanity < 80:
            self.psychological_state = "deteriorating"
        else:
            self.psychological_state = "stable"

        # Reality coherence affects perception
        if self.reality_coherence < 30:
            self.psychological_state += "_reality_fragmenting"
        elif self.reality_coherence < 60:
            self.psychological_state += "_reality_unstable"

    def apply_entity_effects(self, entity):
        """Apply effects from entity encounters"""
        if entity.behavior == "follows_player":
            self.sanity -= random.randint(2, 5)
            self.reality_coherence -= random.randint(1, 3)
        elif entity.behavior == "reality_distortion":
            self.reality_coherence -= random.randint(5, 10)
            self.temporal_awareness -= random.randint(3, 7)
        elif entity.behavior == "temporal_manipulation":
            self.temporal_awareness -= random.randint(8, 15)
            self.memory_stability -= random.randint(5, 10)
        elif entity.behavior == "constant_surveillance":
            self.sanity -= random.randint(3, 8)

        self.entity_encounters += 1
        self.last_entity_encounter = entity.name
        self.update_psychological_state()

    def apply_anomaly_effects(self, anomaly):
        """Apply effects from anomaly exposure"""
        if anomaly.effect == "time_loop":
            self.temporal_awareness -= random.randint(10, 20)
            self.memory_stability -= random.randint(5, 15)
        elif anomaly.effect == "physics_distortion":
            self.reality_coherence -= random.randint(8, 15)
            self.sanity -= random.randint(3, 8)
        elif anomaly.effect == "memory_manifestation":
            self.memory_stability -= random.randint(10, 25)
            self.sanity -= random.randint(5, 12)
        elif anomaly.effect == "dimensional_breach":
            self.reality_coherence -= random.randint(15, 30)
            self.sanity -= random.randint(8, 15)

        self.anomaly_exposures += 1
        self.update_psychological_state()

    def get_status_display(self):
        """Get colored status display"""
        status_parts = []

        # Sanity with color coding
        if self.sanity >= 80:
            sanity_color = colours.GREEN
        elif self.sanity >= 60:
            sanity_color = colours.YELLOW
        elif self.sanity >= 40:
            sanity_color = colours.LIGHTRED_EX
        else:
            sanity_color = colours.RED + colours.BRIGHT

        status_parts.append(f"{sanity_color}Sanity: {self.sanity}/100{colours.RESET_ALL}")

        # Reality Coherence
        if self.reality_coherence >= 80:
            reality_color = colours.CYAN
        elif self.reality_coherence >= 60:
            reality_color = colours.YELLOW
        elif self.reality_coherence >= 40:
            reality_color = colours.LIGHTRED_EX
        else:
            reality_color = colours.MAGENTA + colours.BRIGHT

        status_parts.append(f"{reality_color}Reality: {self.reality_coherence}/100{colours.RESET_ALL}")

        # Memory Stability
        if self.memory_stability >= 80:
            memory_color = colours.LIGHTBLUE_EX
        elif self.memory_stability >= 60:
            memory_color = colours.YELLOW
        else:
            memory_color = colours.LIGHTRED_EX

        status_parts.append(f"{memory_color}Memory: {self.memory_stability}/100{colours.RESET_ALL}")

        return " | ".join(status_parts)

class Game:
    def __init__(self):
        self.player = None
        self.exit = None
        self.special_door = None
        self.running = True
        self.discovered_areas = set()
        self.game_mode = None
        self.entities = []
        self.high_score = self.load_high_score()
        self.current_room = None
        # Initialize game state, menu will be shown explicitly from main()

    def clear_screen(self):
        styling.clear_screen()

    def animate_text(self, text, delay=0.03):
        """Display text with a typewriter effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def show_load_menu(self):
        while True:
            print(colours.CYAN + "\nSave slots:" + colours.RESET_ALL)
            for slot in range(1, MAX_SLOTS + 1):
                save_data = save_load.load_save(slot)
                if save_data is not None:
                    player = save_data['player']
                    print(f"{slot}. {player.name} - Level {player.level} - Sanity: {player.sanity}")
                else:
                    print(f"{slot}. [Empty]")

            choice = input("\nEnter slot number to load (0 to return): ").strip()
            if choice == "0":
                return False
            if not choice.isdigit() or int(choice) < 1 or int(choice) > MAX_SLOTS:
                print(colours.RED + f"Invalid slot number. Choose 1-{MAX_SLOTS} or 0 to return." + colours.RESET_ALL)
                continue
            if self.load(choice):
                return True
            else:
                print(colours.RED + "Failed to load save. Please try again." + colours.RESET_ALL)

    def load_high_score(self):
        try:
            with open('highscore.txt', 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError) as e:
            print(colours.RED + f"\nCould not load high score: {e}" + colours.RESET_ALL)
            return 0

    def save_high_score(self, score):
        try:
            if score > self.high_score:
                with open('highscore.txt', 'w') as f:
                    f.write(str(score))
                self.high_score = score
                print(colours.GREEN + f"\nNew High Score: {score}!" + colours.RESET_ALL)


        except (FileNotFoundError, ValueError) as e:
            print(colours.RED + f"\nCould not load high score: {e}" + colours.RESET_ALL)
            return 0

    def show_menu(self):
        self.clear_screen()
        styling.print_header(None)

        menu_text = """
Select Option:

» 1 «  Nightmare Mode
    └─ 34 entities, one life, infinite levels
    
» 2 «  Normal Mode
    └─ Standard gameplay with entities
    
» 3 «  Load Game
    └─ Continue from a saved game
    
» 0 «  Quit Game
    └─ Exit to desktop"""

        print(styling.box_text(menu_text.strip(), 55, colours.MAGENTA, colours.WHITE))

        try:
            choice = input(f"\n{colours.CYAN}▶ Enter your choice (0-3):{colours.RESET_ALL} ").strip()

            if choice == "0":
                print(colours.YELLOW + "\nThank you for playing Liminal: Lucid Dreams. Goodbye!" + colours.RESET_ALL)
                time.sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')
                sys.exit(0)
            elif choice == "1":
                os.system('cls' if os.name == 'nt' else 'clear')
                self.game_mode = "nightmare"
                print(colours.RED + f"\n╔════════════════════════════════════╗")
                print(f"║  Current High Score: {self.high_score:>10} levels  ║")
                print("╚════════════════════════════════════╝" + colours.RESET_ALL)
            elif choice == "3":
                if self.show_load_menu():
                    return
                os.system('cls' if os.name == 'nt' else 'clear')
                self.show_menu()
                return
            elif choice == "2":
                os.system('cls' if os.name == 'nt' else 'clear')
                submenu_text = """
Select Normal Mode Type:

» 1 «  Coma Mode
    └─ Standard game
    
» 2 «  Dreaming Mode
    └─ No entities, special ending"""
                print(styling.box_text(submenu_text.strip(), 45, colours.YELLOW, colours.WHITE))
                try:
                    sub_choice = input("\nEnter your choice (1-2): ").strip()
                    if sub_choice == "1":
                        os.system('cls' if os.name == 'nt' else 'clear')
                        self.game_mode = "coma"
                    elif sub_choice == "2":
                        os.system('cls' if os.name == 'nt' else 'clear')
                        self.game_mode = "dreaming" 
                    else:
                        print(colours.YELLOW + "\nInvalid choice. Defaulting to Coma Mode." + colours.RESET_ALL)
                        self.game_mode = "coma"
                except (EOFError, KeyboardInterrupt):
                    print(colours.RED + "\nInput interrupted. Returning to main menu." + colours.RESET_ALL)
                    self.show_menu()
                    return
            else:
                print(colours.RED + "\nInvalid choice. Please try again." + colours.RESET_ALL)
                time.sleep(1)
                self.show_menu()
                return
        except (EOFError, KeyboardInterrupt):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(colours.RED + "\nInput interrupted. Exiting game." + colours.RESET_ALL)
            sys.exit(0)

        self.initialize_game()

    def check_nightmare_death(self):
        if self.game_mode == "nightmare" and self.player is not None:
            for entity in self.entities:
                if (entity['pos'] == (self.player.x, self.player.y, self.player.z) and 
                    not entity.get('friendly', False)):
                    self.animate_text(colours.RED + f"\n{entity['name']} found you. Game Over." + colours.RESET_ALL)
                    self.save_high_score(self.player.level)
                    self.running = False
                    return True
        return False

    def move_entities(self):
        if self.game_mode == "nightmare" and self.player is not None:
            for entity in self.entities:
                if random.random() < entity['speed']:
                    dx = self.player.x - entity['pos'][0]
                    dy = self.player.y - entity['pos'][1]
                    dz = self.player.z - entity['pos'][2]

                    # Move towards player with some randomness to avoid clustering
                    x, y, z = entity['pos']
                    directions = []
                    if dx != 0:
                        directions.append(('x', 1 if dx > 0 else -1))
                    if dy != 0:
                        directions.append(('y', 1 if dy > 0 else -1))
                    if dz != 0:
                        directions.append(('z', 1 if dz > 0 else -1))

                    if directions:
                        axis, step = random.choice(directions)
                        if axis == 'x':
                            x += step
                        elif axis == 'y':
                            y += step
                        else:
                            z += step

                        entity['pos'] = (x, y, z)

    def generate_entities(self):
        if self.game_mode == "nightmare":
            self.entities = []

            # Get theme-specific entities from data
            theme_entities_data = data_loader.get_nightmare_entities_for_theme(self.level_theme)
            
            # Default limbo entities
            default_entities = [
                {'name': 'Shadow Walker', 'speed': 0.4, 'friendly': False, 'theme': 'limbo'},
                {'name': 'Mind Eater', 'speed': 0.6, 'friendly': False, 'theme': 'limbo'},
                {'name': 'Lost Soul', 'speed': 0.3, 'friendly': True, 'theme': 'limbo'},
                {'name': 'Void Stalker', 'speed': 0.5, 'friendly': False, 'theme': 'limbo'},
                {'name': 'The angel', 'speed': 0.4, 'friendly': False, 'theme': 'limbo'},
                {'name': 'The demon', 'speed': 0.5, 'friendly': False, 'theme': 'limbo'},
                {'name': 'The shadow', 'speed': 0.3, 'friendly': False, 'theme': 'limbo'},
                {'name': 'The watcher', 'speed': 0.6, 'friendly': False, 'theme': 'limbo'},
                {'name': 'Your friend', 'speed': 0.4, 'friendly': True, 'theme': 'limbo'},
                {'name': 'Your worst dream','speed': 0.5, 'friendly': False, 'theme': 'limbo'},
            ]

            # Create entity list - use theme-specific if available, otherwise use default
            if theme_entities_data:
                all_entities = theme_entities_data + default_entities
            else:
                all_entities = default_entities

            # Higher player level means more entities and they're faster
            if self.player:
                num_entities = min(34, 20 + (self.player.level // 5))
                level_speed_boost = min(0.2, self.player.level * 0.01)
            else:
                num_entities = 20
                level_speed_boost = 0

            for _ in range(num_entities):
                entity_type = random.choice(all_entities).copy()

                # Apply level-based speed boost
                entity_type['speed'] = min(0.9, entity_type['speed'] + level_speed_boost)

                # Position the entity
                entity_type['pos'] = (
                    random.randint(X_MIN, X_MAX),
                    random.randint(Y_MIN, Y_MAX),
                    random.randint(Z_MIN, Z_MAX)
                )

                # Make sure entity isn't placed directly on the player
                if self.player:
                    if entity_type['pos'] == (self.player.x, self.player.y, self.player.z):
                        # Reposition if on player
                        entity_type['pos'] = (
                            random.randint(X_MIN, X_MAX),
                            random.randint(Y_MIN, Y_MAX),
                            random.randint(Z_MIN, Z_MAX)
                        )

                self.entities.append(entity_type)

    def initialize_game(self):
        try:
            print(colours.CYAN + "\nEnter your character's name:" + colours.RESET_ALL)
            name = input("> ").strip()
            if not name:
                name = "Unknown"

            start_z = random.randint(Z_MIN, Z_MAX)
            self.player = Player(name=name, x=0, y=0, z=start_z)
            self.generate_level()
            self.print_intro()
        except (EOFError, KeyboardInterrupt):
            print(colours.RED + "\nGame initialization interrupted. Returning to menu." + colours.RESET_ALL)
            self.player = None
            time.sleep(1)
            try:
                self.show_menu()
            except Exception as e:
                print(colours.RED + f"\nError returning to menu: {str(e)}" + colours.RESET_ALL)
                sys.exit(1)
        except Exception as e:
            print(colours.RED + f"\nError during game initialization: {str(e)}" + colours.RESET_ALL)
            self.player = None
            time.sleep(1)
            try:
                self.show_menu()
            except Exception as e:
                print(colours.RED + f"\nError returning to menu: {str(e)}" + colours.RESET_ALL)
                sys.exit(1)

    def generate_level(self):
        # Use data_loader to get theme for this level
        self.level_theme = data_loader.get_theme_for_level(self.player.level if self.player else 1)

        # Generate the exit far from the player
        while True:
            self.exit = (
                random.randint(X_MIN, X_MAX),
                random.randint(Y_MIN, Y_MAX),
                random.randint(Z_MIN, Z_MAX)
            )

            # Make sure exit is far enough from player
            if self.player:
                distance = abs(self.exit[0] - self.player.x) + abs(self.exit[1] - self.player.y) + abs(self.exit[2] - self.player.z)
                if distance >= 10:  # Minimum distance to make it challenging
                    break
            else:
                break

        # Generate special door for heaven/hell endings
        if self.player is not None and self.player.level >= 50:  # Special door appears after level 50
            z = 5 if random.random() < 0.5 else -5  # Top or bottom floor
            x = random.randint(X_MIN, X_MAX)
            y = random.randint(Y_MIN, Y_MAX)
            while abs(x - self.player.x) + abs(y - self.player.y) < MIN_HEAVEN_DOOR_DISTANCE:
                x = random.randint(X_MIN, X_MAX)
                y = random.randint(Y_MIN, Y_MAX)
            self.special_door = (x, y, z)
        else:
            self.special_door = None

        # Pre-generate some rooms to create consistency in the world
        # This creates a more coherent "tiled map" feeling
        self.discovered_areas = set()  # Reset discovered areas
        self.room_map = {}  # Store pre-generated rooms

        # Get level for room generation
        level = self.player.level if self.player else 1

        # Generate a number of predefined rooms
        num_predefined = min(50, 20 + (level // 2))  # More rooms at higher levels
        for _ in range(num_predefined):
            pos = (
                random.randint(X_MIN, X_MAX),
                random.randint(Y_MIN, Y_MAX),
                random.randint(Z_MIN, Z_MAX)
            )
            if pos not in self.room_map:
                self.room_map[pos] = Room(theme=self.level_theme, level=level)

        # Add specific room at exit location
        self.room_map[self.exit] = Room(theme='limbo', level=level)  # Exit is always limbo-themed

        # If there's a special door, make that room special too
        if self.special_door:
            special_room = Room(theme='limbo', level=level)
            # Make sure it's a special room with visible distinctions
            special_room.description = colours.WHITE + "A room with a strange door that glows with otherworldly energy." + colours.RESET_ALL
            self.room_map[self.special_door] = special_room

    def print_intro(self):
        styling.print_header(None)

        self.clear_screen()
        if self.player is not None:
            print(colours.MAGENTA + f"\nWelcome, {self.player.name}, to where reality bends and perception ends..." + colours.RESET_ALL)
        else:
            print(colours.MAGENTA + "\nWelcome to where reality bends and perception ends..." + colours.RESET_ALL)
        print("\nType /help for a list of commands.\n")

    def check_endings(self):
        if self.player is None:
            return False

        current_pos = (self.player.x, self.player.y, self.player.z)

        # Wall of photos ending (Real ending)
        if (self.current_room and 
            "wall of photos" in self.current_room.description.lower() and 
            random.random() < 0.05):
            self.wake_up_ending()
            return True

        # Heaven/Hell endings
        if self.special_door and current_pos == self.special_door:
            if self.player.sanity > 70:
                self.heaven_ending()
            else:
                self.hell_ending()
            return True

        # Exit to next level
        if current_pos == self.exit:
            self.next_level()
            return False  # Not a game ending, just level progression

        return False

    def wake_up_ending(self):
        self.clear_screen()
        self.animate_text(colours.CYAN + "\nYou stare at the wall of photos. Memories flood back...")
        time.sleep(1)
        self.animate_text(colours.YELLOW + "\nA car accident. A hospital room. Machines beeping.")
        time.sleep(1)
        self.animate_text(colours.GREEN + "\nYou've been in a coma. This was all in your mind.")
        time.sleep(1)
        self.animate_text(colours.WHITE + "\nYou feel yourself pulled back to reality.")
        time.sleep(2)
        self.animate_text(colours.MAGENTA + "\nYour eyes open. A doctor smiles down at you.")
        time.sleep(1)
        self.animate_text(colours.CYAN + "\n\"Welcome back,\" she says.")
        time.sleep(1)
        self.animate_text(colours.YELLOW + "\nYou see all your family members around your bed.")
        time.sleep(1)
        self.animate_text(colours.WHITE + "\nYou start tearing along your family's faces.")
        time.sleep(1)
        self.animate_text(colours.GREEN + "\nYOU WOKE UP - THE REAL ENDING" + colours.RESET_ALL)
        self.running = False
        return True

    def heaven_ending(self):
        self.clear_screen()
        self.animate_text(colours.CYAN + "\nYou step through the door into blinding light...")
        time.sleep(1)
        self.animate_text(colours.YELLOW + "\nYou realise your body is no longer heavy.")
        time.sleep(1)
        self.animate_text(colours.YELLOW + "\nA sense of peace washes over you.")
        time.sleep(1)
        self.animate_text(colours.WHITE + "\nYou see familiar faces. People you once knew.")
        time.sleep(1)
        self.animate_text(colours.MAGENTA + "\nThey welcome you with open arms.")
        time.sleep(1)
        self.animate_text(colours.CYAN + "\nYou realize you've been here before.")
        time.sleep(1)
        self.animate_text(colours.YELLOW + "\nYou're finally home.")
        time.sleep(1)
        self.animate_text(colours.WHITE + "\nHEAVEN ENDING - You found peace" + colours.RESET_ALL)
        self.running = False
        return True

    def hell_ending(self):
        self.clear_screen()
        self.animate_text(colours.RED + "\nYou step through the door into smothering darkness...")
        time.sleep(1)
        self.animate_text(colours.YELLOW + "\nThe air is hot and sulfurous.")
        time.sleep(1)
        self.animate_text(colours.RED + "\nYou hear screams in the distance.")
        time.sleep(1)
        self.animate_text(colours.MAGENTA + "\nShadowy figures surround you.")
        time.sleep(1)
        self.animate_text(colours.RED + "\nYou try to run, but there's nowhere to go.")
        time.sleep(1)
        self.animate_text(colours.YELLOW + "\nYou realize this is your fate.")
        time.sleep(1)
        self.animate_text(colours.RED + "\nHELL ENDING - Your sanity was too low" + colours.RESET_ALL)
        self.running = False
        return True

    def dreaming_ending(self):
        self.clear_screen()
        self.animate_text(colours.CYAN + "\nYou sit on your bed, looking out the window...")
        time.sleep(1)
        self.animate_text(colours.YELLOW + "\nThe dream is ending, but you know you can return.")
        time.sleep(1)
        self.animate_text(colours.GREEN + "\nYou close your eyes, ready to wake up.")
        time.sleep(1)
        self.animate_text(colours.WHITE + "\nWhen you open them, you're back in your room.")
        time.sleep(1)
        self.animate_text(colours.MAGENTA + "\nIt was all a dream, but the memories remain.")
        time.sleep(1)
        self.animate_text(colours.CYAN + "\nYou can always return to this place.")
        time.sleep(1)
        self.animate_text(colours.RED + "\nYou know you can ALWAYS return...")
        time.sleep(1)
        self.animate_text(colours.CYAN + "\nAnd you know you can go back whenever you want.")
        time.sleep(1)
        self.animate_text(colours.GREEN + "\nDREAMING ENDING - You can always return" + colours.RESET_ALL)
        self.running = False
        return True

    def next_level(self):
        if self.player is None:
            return

        self.player.level += 1
        self.player.sanity = min(self.player.sanity + 15, SANITY_MAX)  # Reward for completing a level

        print(colours.GREEN + f"\nYou found the exit! Moving to level {self.player.level}." + colours.RESET_ALL)
        print(colours.CYAN + f"Sanity restored to {self.player.sanity}." + colours.RESET_ALL)

        # Add a random item to inventory sometimes
        if random.random() < 0.3:
            item = random.choice(list(items.keys()))
            if item != 'sanity':  # Don't add sanity as an item
                self.player.inventory.append(item)
                print(colours.YELLOW + f"You found a {item}!" + colours.RESET_ALL)

        self.generate_level()
        self.generate_entities()
        time.sleep(2)

    def display_room(self):
        if self.player is None:
            return

        current_pos = (self.player.x, self.player.y, self.player.z)

        # Use the room from our tiled map if it exists, otherwise create a new one
        if hasattr(self, 'room_map') and current_pos in self.room_map:
            self.current_room = self.room_map[current_pos]
        elif current_pos not in self.discovered_areas:
            # Create a new room using the level theme
            level = self.player.level if self.player else 1
            theme = self.level_theme if hasattr(self, 'level_theme') else None
            self.current_room = Room(theme=theme, level=level)

            # Add to discovered areas and room map
            self.discovered_areas.add(current_pos)
            if hasattr(self, 'room_map'):
                self.room_map[current_pos] = self.current_room

        # Make sure current_room is set
        if self.current_room is None:
            self.current_room = Room(theme=self.level_theme if hasattr(self, 'level_theme') else None, 
                                     level=self.player.level if self.player else 1)

        # Display room description with theme information
        theme_colors = {
            'hospital': colours.CYAN,
            'school': colours.YELLOW,
            'home': colours.GREEN,
            'limbo': colours.MAGENTA,
            'mall': colours.BLUE
        }

        # Show theme info at higher levels when player has more experience
        if self.player and self.player.level > 5 and hasattr(self.current_room, 'theme') and self.current_room.theme:
            theme_color = theme_colors.get(self.current_room.theme, colours.WHITE)
            theme_name = self.current_room.theme.upper()
            print(f"\n{theme_color}[{theme_name} ZONE - LEVEL {self.player.level}]{colours.RESET_ALL}")

        # Display room description with null checks
        if hasattr(self.current_room, 'description') and self.current_room.description:
            print(f"\n{self.current_room.description}")
        else:
            print("\nAn undefined space that feels wrong somehow.")

        if hasattr(self.current_room, 'stairs') and self.current_room.stairs:
            print(f"{self.current_room.stairs}")
        else:
            print("There are no visible stairs or elevators.")

        if hasattr(self.current_room, 'paths') and self.current_room.paths:
            print(f"{self.current_room.paths}")
        else:
            print("Paths extend in unpredictable directions.")

        # Display interactable if present with null checks
        if hasattr(self.current_room, 'interactable') and self.current_room.interactable and isinstance(self.current_room.interactable, tuple) and len(self.current_room.interactable) > 0:
            print(colours.YELLOW + f"\n{self.current_room.interactable[0]}" + colours.RESET_ALL)

        # Display any nearby entities in nightmare mode
        if self.game_mode == "nightmare" and hasattr(self, 'entities'):
            nearby_entities = []
            for entity in self.entities:
                ex, ey, ez = entity['pos']
                distance = abs(ex - self.player.x) + abs(ey - self.player.y) + abs(ez - self.player.z)

                if distance <= 3:  # Close enough to sense
                    if hasattr(self.player, 'has_light') and self.player.has_light:  # Can see clearly with light
                        entity_name = entity['name']
                        entity_theme = entity.get('theme', 'unknown')
                        # Show more detail about entities when player has a light
                        nearby_entities.append(f"{entity_name} ({entity_theme}) is nearby.")
                    else:  # Can only sense
                        nearby_entities.append("Something moves in the darkness.")

            if nearby_entities:
                print(colours.RED + "\nDanger:" + colours.RESET_ALL)
                for entity_msg in nearby_entities:
                    print(colours.RED + f" - {entity_msg}" + colours.RESET_ALL)

        # Show if this is the exit
        if hasattr(self, 'exit') and current_pos == self.exit:
            print(colours.GREEN + "\nThis room has a door that feels different. It might be the exit." + colours.RESET_ALL)

        # Show special door if present
        if hasattr(self, 'special_door') and self.special_door and current_pos == self.special_door:
            if self.player.sanity > 70:
                print(colours.WHITE + "\nA radiant door pulses with warm light. It calls to you." + colours.RESET_ALL)
            else:
                print(colours.RED + "\nA dark door emanates dread. Something waits beyond." + colours.RESET_ALL)

        # Display minimap for player with adjacency information
        if hasattr(self.player, 'has_light') and self.player.has_light and hasattr(self, 'room_map'):  # Only show minimap if player has light
            print(colours.CYAN + "\nAdjacent Rooms:" + colours.RESET_ALL)
            for direction, (dx, dy, dz) in directions.items():
                adjacent_pos = (self.player.x + dx, self.player.y + dy, self.player.z + dz)
                if adjacent_pos in self.room_map:
                    adj_room = self.room_map[adjacent_pos]
                    if hasattr(adj_room, 'theme') and adj_room.theme:
                        print(f" - {direction}: {theme_colors.get(adj_room.theme, colours.WHITE)}{adj_room.theme.capitalize()} area{colours.RESET_ALL}")
                    else:
                        print(f" - {direction}: Unknown area")

    def show_help(self):
        help_text = """
MOVEMENT
  /right, /left, /forward, /backward
  /upstairs, /downstairs
  /move [direction]

INTERACTION
  /examine    - Look around the room
  /use [item] - Use an item from inventory
  /take       - Pick up items

INFORMATION
  /inventory /i - View your items
  /stats         - View your status

SAVE/LOAD
  /save [slot] - Save game (1-5)
  /load [slot] - Load game (1-5)

OTHER
  /exit /quit - Leave the game
  /help        - Show this message"""
        
        print(styling.decorated_title("COMMANDS", 40, colours.CYAN))
        print(styling.box_text(help_text.strip(), 45, colours.CYAN, colours.WHITE))

    def show_stats(self):
        if self.player is None:
            print(colours.RED + "\nNo active player." + colours.RESET_ALL)
            return

        # Determine colors based on values
        sanity_color = colours.GREEN
        if self.player.sanity < 30:
            sanity_color = colours.RED
        elif self.player.sanity < 70:
            sanity_color = colours.YELLOW
            
        reality_color = colours.CYAN
        if self.player.reality_coherence < 30:
            reality_color = colours.RED
        elif self.player.reality_coherence < 70:
            reality_color = colours.YELLOW
            
        memory_color = colours.LIGHTBLUE_EX
        if self.player.memory_stability < 30:
            memory_color = colours.RED
        elif self.player.memory_stability < 70:
            memory_color = colours.YELLOW
        
        # Create progress bars
        sanity_bar = styling.progress_bar(self.player.sanity, 100, 20, sanity_color)
        reality_bar = styling.progress_bar(self.player.reality_coherence, 100, 20, reality_color)
        memory_bar = styling.progress_bar(self.player.memory_stability, 100, 20, memory_color)
        
        stats_text = f"""
Name:    {self.player.name}
Level:   {self.player.level}
Position: ({self.player.x}, {self.player.y}, {self.player.z})

{sanity_color}SANITY:{colours.RESET_ALL}   {self.player.sanity:3d}/100 {sanity_bar}
{reality_color}REALITY:{colours.RESET_ALL} {self.player.reality_coherence:3d}/100 {reality_bar}
{memory_color}MEMORY:{colours.RESET_ALL}   {self.player.memory_stability:3d}/100 {memory_bar}

Psychological State: {self.player.psychological_state}"""
        
        if self.game_mode == "nightmare":
            stats_text += f"\n{colours.RED}Game Mode: Nightmare{colours.RESET_ALL}"
        elif self.game_mode == "coma":
            stats_text += f"\n{colours.YELLOW}Game Mode: Coma{colours.RESET_ALL}"
        else:
            stats_text += f"\n{colours.GREEN}Game Mode: Dreaming{colours.RESET_ALL}"
        
        print(styling.decorated_title("PLAYER STATS", 45, colours.CYAN))
        print(styling.box_text(stats_text.strip(), 50, colours.CYAN, colours.WHITE))

    def show_inventory(self):
        if self.player is None:
            print(colours.RED + "\nNo active player." + colours.RESET_ALL)
            return

        if not self.player.inventory:
            print(colours.YELLOW + "\nYour inventory is empty." + colours.RESET_ALL)
            return

        print(colours.CYAN + "\n=== INVENTORY ===" + colours.RESET_ALL)
        for item in self.player.inventory:
            print(f"{item}: {items.get(item, 'Unknown item')}")

    def move(self, direction):
        if self.player is None:
            print(colours.RED + "\nNo active player." + colours.RESET_ALL)
            return

        # Normalize direction - add slash prefix if not present for lookup
        if not direction.startswith('/'):
            direction = '/' + direction

        if direction not in directions:
            print(colours.RED + f"Invalid direction. Use: {', '.join([d.replace('/', '') for d in directions.keys()])}" + colours.RESET_ALL)
            return

        # Make sure current_room is set
        if not hasattr(self, 'current_room') or self.current_room is None:
            self.current_room = Room(theme=self.level_theme if hasattr(self, 'level_theme') else None, 
                                     level=self.player.level if self.player else 1)

        # Check if the direction is available in the current room
        if not hasattr(self.current_room, 'available_directions') or not self.current_room.available_directions.get(direction, False):
            print(colours.RED + f"You can't go {direction} from here." + colours.RESET_ALL)
            return

        dx, dy, dz = directions[direction]
        self.player.x += dx
        self.player.y += dy
        self.player.z += dz

        # Constrain to world bounds
        self.player.x = max(X_MIN, min(X_MAX, self.player.x))
        self.player.y = max(Y_MIN, min(Y_MAX, self.player.y))
        self.player.z = max(Z_MIN, min(Z_MAX, self.player.z))

        # Sanity loss on movement
        sanity_loss = 1
        if hasattr(self.player, 'has_light') and self.player.has_light:
            sanity_loss = 0.5

        # Round down to int for sanity
        self.player.sanity = int(max(0, self.player.sanity - sanity_loss))

        print(f"Moving {direction}...")

        # If you moved, entities might move too
        if hasattr(self, 'move_entities') and callable(getattr(self, 'move_entities')):
            self.move_entities()

        # Check if player died by entity
        if hasattr(self, 'check_nightmare_death') and callable(getattr(self, 'check_nightmare_death')):
            if self.check_nightmare_death():
                return

        # Check if new position triggers an ending
        if hasattr(self, 'check_endings') and callable(getattr(self, 'check_endings')):
            if not self.check_endings():
                self.display_room()

        # Warn if sanity is low
        if hasattr(self.player, 'sanity'):
            if self.player.sanity < 20:
                print(colours.RED + "\nYour sanity is dangerously low!" + colours.RESET_ALL)
            elif self.player.sanity < 50:
                print(colours.YELLOW + "\nYour sanity is getting low." + colours.RESET_ALL)

    def interact(self, action):
        if self.player is None:
            print(colours.RED + "\nNo active player." + colours.RESET_ALL)
            return

        if not self.current_room:
            print(colours.RED + "\nNo current room to interact with." + colours.RESET_ALL)
            return

        if action == "examine":
            if (hasattr(self.current_room, 'interactable') and 
                self.current_room.interactable and 
                isinstance(self.current_room.interactable, tuple) and 
                len(self.current_room.interactable) > 1):

                print(colours.CYAN + f"\n{self.current_room.interactable[1]}" + colours.RESET_ALL)

                # Sometimes interacting gives sanity
                if random.random() < 0.3:
                    gain = random.randint(5, 15)
                    self.player.sanity = int(min(SANITY_MAX, self.player.sanity + gain))
                    print(colours.GREEN + f"You feel a bit better. +{gain} sanity." + colours.RESET_ALL)
            else:
                print("There's nothing interesting to examine here.")

        elif action == "take":
            if (hasattr(self.current_room, 'interactable') and 
                self.current_room.interactable and 
                isinstance(self.current_room.interactable, tuple)):

                # Higher chance of finding something to test inventory properly
                if random.random() < 0.9:  
                    item = random.choice(list(items.keys()))
                    if item != 'sanity':  # Don't add sanity as an item
                        self.player.inventory.append(item)
                        print(colours.YELLOW + f"You found a {item}!" + colours.RESET_ALL)
                    else:
                        print("There's nothing useful to take.")
                else:
                    print("There's nothing useful to take.")
            else:
                print("There's nothing useful to take.")

        elif action.startswith("use "):
            item = action[4:].strip()
            if item in self.player.inventory:
                self.use_item(item)
            else:
                print(colours.RED + f"You don't have a {item}." + colours.RESET_ALL)

        else:
            print(colours.RED + "Unknown action. Try 'examine', 'take', or 'use [item]'." + colours.RESET_ALL)

    def use_item(self, item):
        if self.player is None:
            print(colours.RED + "\nNo active player." + colours.RESET_ALL)
            return

        if item == 'battery':
            gain = random.randint(10, 20)
            self.player.sanity = int(min(SANITY_MAX, self.player.sanity + gain))
            print(colours.GREEN + f"You use the battery to power your devices. +{gain} sanity." + colours.RESET_ALL)
            self.player.inventory.remove(item)

        elif item == 'flashlight':
            self.player.has_light = True
            print(colours.YELLOW + "You turn on the flashlight. It will help you see and preserve sanity." + colours.RESET_ALL)
            if 'battery' not in self.player.inventory:
                print("The flashlight will eventually need batteries.")

        elif item == 'mysterious key':
            current_pos = (self.player.x, self.player.y, self.player.z)
            if current_pos == self.exit:
                print(colours.GREEN + "The key fits the exit door! You can now proceed to the next level." + colours.RESET_ALL)
                self.next_level()
            elif self.special_door and current_pos == self.special_door:
                print(colours.CYAN + "The key fits the mysterious door. You open it..." + colours.RESET_ALL)
                if self.player.sanity > 70:
                    self.heaven_ending()
                else:
                    self.hell_ending()
            else:
                print("You try the key, but there's no lock here that it fits.")

        elif item == 'old map':
            # Show nearby points of interest
            print(colours.CYAN + "\nThe map reveals:" + colours.RESET_ALL)

            # Show exit direction
            if self.exit is not None:
                exit_x, exit_y, exit_z = self.exit
                dx = exit_x - self.player.x
                dy = exit_y - self.player.y
                dz = exit_z - self.player.z
            else:
                print("The map seems to be blank or damaged.")
                return

            if abs(dx) > abs(dy) and abs(dx) > abs(dz):
                direction = "east" if dx > 0 else "west"
            elif abs(dy) > abs(dx) and abs(dy) > abs(dz):
                direction = "north" if dy > 0 else "south"
            else:
                direction = "up" if dz > 0 else "down"

            print(f"- The exit appears to be to the {direction}.")

            # Sometimes reveal special door
            if self.special_door and random.random() < 0.5:
                print("- A special door is marked with a strange symbol.")

            # In nightmare mode, reveal nearby entities
            if self.game_mode == "nightmare":
                nearby_count = 0
                for entity in self.entities:
                    ex, ey, ez = entity['pos']
                    distance = abs(ex - self.player.x) + abs(ey - self.player.y) + abs(ez - self.player.z)
                    if distance <= 5:
                        nearby_count += 1

                if nearby_count > 0:
                    print(colours.RED + f"- {nearby_count} entities are nearby." + colours.RESET_ALL)

        elif item == 'strange coin':
            # Warns about nearby entities
            if self.game_mode == "nightmare":
                danger_level = 0
                for entity in self.entities:
                    ex, ey, ez = entity['pos']
                    distance = abs(ex - self.player.x) + abs(ey - self.player.y) + abs(ez - self.player.z)
                    if distance <= 3 and not entity.get('friendly', False):
                        danger_level += 1

                if danger_level == 0:
                    print("The coin is silent. No immediate danger.")
                elif danger_level <= 2:
                    print(colours.YELLOW + "The coin hums softly. Danger is near." + colours.RESET_ALL)
                else:
                    print(colours.RED + "The coin vibrates violently! Immediate danger!" + colours.RESET_ALL)
            else:
                print("The coin seems inert in this reality.")

        elif item == 'polaroid camera':
            print("You take a photo. It develops slowly...")
            time.sleep(1)

            photo_descriptions = [
                "The photo shows this room, but with someone standing behind you who isn't there.",
                "The photo is completely black except for two glowing eyes.",
                "The photo shows you, but your face is blurred and distorted.",
                "The photo reveals hidden writing on the walls that says 'WAKE UP'.",
                "The photo shows the exit door glowing faintly.",
                "The photo is normal, but as you watch, your figure in it begins to move."
            ]

            print(colours.CYAN + random.choice(photo_descriptions) + colours.RESET_ALL)

            # Small chance to reveal exit
            if random.random() < 0.2 and self.exit is not None:
                exit_x, exit_y, exit_z = self.exit
                print(colours.GREEN + f"You notice coordinates in the corner: ({exit_x}, {exit_y}, {exit_z})" + colours.RESET_ALL)

        elif item == 'music box':
            gain = random.randint(15, 30)
            self.player.sanity = int(min(SANITY_MAX, self.player.sanity + gain))
            print(colours.GREEN + f"The gentle melody soothes your mind. +{gain} sanity." + colours.RESET_ALL)

            # In nightmare mode, entities are attracted to the sound
            if self.game_mode == "nightmare":
                print(colours.RED + "But the sound might attract unwanted attention..." + colours.RESET_ALL)
                for entity in self.entities:
                    if random.random() < 0.3:
                        ex, ey, ez = entity['pos']
                        # Move entity closer to player
                        if ex < self.player.x:
                            ex += 1
                        elif ex > self.player.x:
                            ex -= 1
                        if ey < self.player.y:
                            ey += 1
                        elif ey > self.player.y:
                            ey -= 1
                        if ez < self.player.z:
                            ez += 1
                        elif ez > self.player.z:
                            ez -= 1
                        entity['pos'] = (ex, ey, ez)

        elif item == 'compass':
            # Points to exit or special door
            if self.special_door and self.player.level >= 50 and random.random() < 0.3:
                sx, sy, sz = self.special_door
                dx = sx - self.player.x
                dy = sy - self.player.y
                dz = sz - self.player.z

                if abs(dx) > abs(dy) and abs(dx) > abs(dz):
                    direction = "east" if dx > 0 else "west"
                elif abs(dy) > abs(dx) and abs(dy) > abs(dz):
                    direction = "north" if dy > 0 else "south"
                else:
                    direction = "up" if dz > 0 else "down"

                print(colours.MAGENTA + f"The compass needle spins wildly, then points {direction} with a strange glow." + colours.RESET_ALL)
            else:
                if self.exit is not None:
                    ex, ey, ez = self.exit
                    dx = ex - self.player.x
                    dy = ey - self.player.y
                    dz = ez - self.player.z

                    if abs(dx) > abs(dy) and abs(dx) > abs(dz):
                        direction = "east" if dx > 0 else "west"
                    elif abs(dy) > abs(dx) and abs(dy) > abs(dz):
                        direction = "north" if dy > 0 else "south"
                    else:
                        direction = "up" if dz > 0 else "down"

                    print(colours.CYAN + f"The compass needle points {direction}." + colours.RESET_ALL)
                else:
                    print(colours.CYAN + "The compass needle spins erratically, as if confused." + colours.RESET_ALL)

        elif item == 'pills':
            gain = random.randint(30, 50)
            self.player.sanity = int(min(SANITY_MAX, self.player.sanity + gain))
            print(colours.GREEN + f"You take the pills. Your mind clears significantly. +{gain} sanity." + colours.RESET_ALL)
            self.player.inventory.remove(item)

        else:
            print(f"You're not sure how to use the {item}.")

    def save(self, slot_number=None):
        if self.player is None:
            print(colours.RED + "\nNo active player to save." + colours.RESET_ALL)
            return False

        if slot_number is None:
            print(colours.CYAN + "\nSave slots:" + colours.RESET_ALL)
            for slot in range(1, MAX_SLOTS + 1):
                save_data = save_load.load_save(slot)
                if save_data is not None:
                    player = save_data['player']
                    print(f"{slot}. {player.name} - Level {player.level} - Sanity: {player.sanity}")
                else:
                    print(f"{slot}. [Empty]")

            slot_number = input("\nEnter slot number (1-5): ").strip()
            if not slot_number.isdigit() or int(slot_number) < 1 or int(slot_number) > MAX_SLOTS:
                print(colours.RED + f"Invalid slot number. Choose 1-{MAX_SLOTS}." + colours.RESET_ALL)
                return False

        try:
            save_data = {
                'player': self.player,
                'exit': self.exit,
                'special_door': self.special_door,
                'discovered_areas': self.discovered_areas,
                'game_mode': self.game_mode,
                'entities': self.entities,
                'current_room': self.current_room
            }

            save_load.save_game(int(slot_number), save_data)

            print(colours.GREEN + f"Game saved to slot {slot_number}." + colours.RESET_ALL)
            return True
        except Exception as e:
            print(colours.RED + f"Error saving game: {e}" + colours.RESET_ALL)
            return False

    def load(self, slot_number):
        try:
            save_data = save_load.load_save(int(slot_number))
            if save_data is None:
                print(colours.RED + f"Save slot {slot_number} is empty." + colours.RESET_ALL)
                return False

            self.player = save_data['player']
            self.exit = save_data['exit']
            self.special_door = save_data['special_door']
            self.discovered_areas = save_data['discovered_areas']
            self.game_mode = save_data['game_mode']
            self.entities = save_data['entities']
            self.current_room = save_data['current_room']

            print(colours.GREEN + f"Game loaded from slot {slot_number}." + colours.RESET_ALL)
            self.display_room()
            return True
        except Exception as e:
            print(colours.RED + f"Error loading game: {e}" + colours.RESET_ALL)
            return False

    def process_command(self, command):
        if not command:
            return

        if command in directions:
            self.move(command)

        elif command == '/help':
            self.show_help()

        elif command in ['/inventory', '/i']:
            self.show_inventory()

        elif command == '/stats':
            self.show_stats()

        elif command.startswith('/save'):
            parts = command.split()
            slot = None
            if len(parts) > 1:
                try:
                    slot = int(parts[1])
                except (ValueError, TypeError):
                    print(colours.RED + "Invalid save slot number." + colours.RESET_ALL)
            self.save(slot)

        elif command.startswith('/load'):
            parts = command.split()
            if len(parts) > 1:
                try:
                    slot = int(parts[1])
                    self.load(slot)
                except (ValueError, TypeError):
                    print(colours.RED + "Invalid save slot number." + colours.RESET_ALL)
            else:
                self.show_load_menu()

        elif command in ['/exit', '/quit']:
            confirm = input("Are you sure you want to quit? Progress will be lost unless saved. (y/n): ")
            if confirm and confirm.lower().startswith('y'):
                print("Thanks for playing!")
                self.running = False

        elif command in ['/examine', '/take'] or command.startswith('/use '):
            # Remove the slash for internal processing
            cmd = command[1:] if command.startswith('/') else command
            self.interact(cmd)

        # Add support for '/move direction' command
        elif command.startswith('/move '):
            direction = command[6:].strip()
            if f'/{direction}' in directions or direction in directions:
                self.move(direction)
            else:
                print(colours.RED + f"Invalid direction. Use: {', '.join([d.replace('/', '') for d in directions.keys()])}" + colours.RESET_ALL)

        else:
            print(colours.RED + "Unknown command. Type /help for commands." + colours.RESET_ALL)

    def game_loop(self):
        if not self.player:
            return

        self.display_room()

        while self.running:
            # Check for game over due to low sanity
            if self.player.sanity <= 0:
                print(colours.RED + "\nYour sanity has completely eroded. You are lost in the liminal space forever." + colours.RESET_ALL)
                if self.game_mode == "nightmare":
                    self.save_high_score(self.player.level)
                self.running = False
                break

            try:
                command = input("\n> ").strip().lower()
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen after each command
                self.process_command(command)
            except EOFError:
                print(colours.RED + "\nInput error occurred. Exiting game." + colours.RESET_ALL)
                time.sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')
                self.running = False
                break
            except KeyboardInterrupt:
                print(colours.YELLOW + "\nGame interrupted. Goodbye!" + colours.RESET_ALL)
                os.system('cls' if os.name == 'nt' else 'clear')
                self.running = False
                break

            # Dreaming mode check for special ending
            if self.game_mode == "dreaming" and self.player.level >= 10 and random.random() < 0.05:
                self.dreaming_ending()

def main():
    try:
        game = Game()
        game.show_menu()  # Show menu explicitly first
        game.game_loop()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
    except EOFError:
        print("\nInput error occurred. Exiting game.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

