/**
 * Liminal: Lucid Dreams - Browser Version
 * A text-based adventure game - Terminal Style Demo
 */

// ==================== DATA ====================

// Game settings (same as Python version)
const SETTINGS = {
    world_bounds: {
        x_min: -100, x_max: 100,
        y_min: -100, y_max: 100,
        z_min: -10, z_max: 10
    },
    player_stats: {
        sanity_max: 100,
        reality_max: 100,
        memory_max: 100
    },
    gameplay: {
        min_heaven_door_distance: 10,
        entity_spawn_chance: 0.15,
        anomaly_chance: 0.25,
        memory_fragment_chance: 0.20,
        dimensional_rift_chance: 0.08,
        echo_event_chance: 0.15,
        phantom_interaction_chance: 0.12
    }
};

// Theme data (loaded from JSON in full version, embedded here for demo)
const THEMES = {
    hospital: {
        descriptions: [
            ["A sterile hospital room where IV drips count down to unknown procedures.", ["door1", "door2"]],
            ["A blood-stained operating theater where surgical lights swing hypnotically.", ["door1", "door2"]],
            ["An endless hospital corridor where wheelchair tracks lead in circles.", ["door1", "door2", "door3"]],
            ["A morgue where toe tags write themselves, listing deaths that haven't happened yet.", ["door2", "door4"]]
        ],
        features: [
            "There's an emergency stairwell leading up.",
            "A service elevator shaft descends into darkness.",
            "Both the patient and staff stairwells are accessible."
        ],
        paths: [
            "Hospital corridors extend in all directions.",
            "Only the patient wing and administration area are accessible.",
            "A single hallway continues forward."
        ],
        interactables: [
            ["A patient's chart hangs on the wall.", "The chart has your name on it..."],
            ["A medical monitor flickers with vitals.", "The heartbeat matches your own exactly..."],
            ["A wheelchair sits empty in the corner.", "It slowly begins to move on its own..."]
        ]
    },
    school: {
        descriptions: [
            ["A classroom where chalk writes equations that solve themselves.", ["door1", "door4"]],
            ["A gymnasium where sneakers squeak on phantom feet.", ["door1", "door3"]],
            ["A library where books rewrite their endings based on who's reading.", ["door1", "door3", "door4"]],
            ["An abandoned prom hall where decorations sway to music only the dead can hear.", ["door2", "door3"]]
        ],
        features: [
            "There's a staircase to the upper floor classrooms.",
            "A dark stairwell leads to the basement level.",
            "Both main and emergency staircases are visible."
        ],
        paths: [
            "School hallways extend in all directions.",
            "Only forward to the gym and backward to the entrance are clear.",
            "A single hallway continues forward."
        ],
        interactables: [
            ["An old yearbook lies open on a desk.", "Your photo is on every page, getting older..."],
            ["A chalkboard covered in equations.", "The math solves a problem about your life..."],
            ["A detention slip with your name on it.", "It details a crime you don't remember committing..."]
        ]
    },
    home: {
        descriptions: [
            ["A child's bedroom where stuffed animals whisper bedtime stories.", ["door1"]],
            ["An attic where photo albums chronicle a family that grows older in reverse.", ["door1", "door4"]],
            ["A basement where the walls bleed condensation shaped like unspoken confessions.", ["door1", "door2"]],
            ["A nursery that prepares itself for children who will never be born.", ["door1", "door4"]]
        ],
        features: [
            "There's a carpeted staircase leading to the upper floor.",
            "A cellar door opens to stairs descending below.",
            "Both the main stairs and a ladder to the attic are visible."
        ],
        paths: [
            "Doorways lead to other rooms in all directions.",
            "Only forward to the living room and backward to the foyer are clear.",
            "A single doorway continues forward."
        ],
        interactables: [
            ["An old TV flickers with static.", "The TV shows glimpses of your past..."],
            ["A rusty music box sits on a table.", "The melody brings tears to your eyes..."],
            ["A dusty photo album lies open.", "The photos show memories you'd forgotten..."]
        ]
    },
    limbo: {
        descriptions: [
            ["A mirrored labyrinth where each reflection shows a different choice you could have made.", ["door1", "door2", "door3"]],
            ["An infinite void where fragments of consciousness float like islands.", ["door1", "door2", "door3", "door4"]],
            ["A library of unwritten books where empty pages fill themselves with stories.", ["door1", "door2", "door3", "door4"]],
            ["A waiting room for the afterlife where appointment numbers are called.", ["door2", "door3"]]
        ],
        features: [
            "There's a floating staircase suspended in midair.",
            "A dark pit seems to lead downward forever.",
            "Staircases spiral both upward and downward impossibly."
        ],
        paths: [
            "Impossible pathways extend in all directions.",
            "Only forward and backward seem to lead somewhere tangible.",
            "A single shimmering path continues forward."
        ],
        interactables: [
            ["A mirror reflects a different room.", "Your reflection seems wrong somehow..."],
            ["A broken clock ticks erratically.", "Time seems distorted here..."],
            ["A locked chest sits in the corner.", "It hums with mysterious energy..."]
        ]
    },
    mall: {
        descriptions: [
            ["An endless corridor with doors that seem to breathe.", ["door1", "door2", "door3", "door4"]],
            ["An overgrown indoor garden where plants whisper secrets.", ["door1", "door3"]],
            ["A toy store where the toys observe you carefully.", ["door2", "door3"]],
            ["A cinema playing movies of your life you don't remember.", ["door1", "door2"]]
        ],
        features: [
            "There's an escalator leading to the upper level.",
            "A down escalator leads to the lower concourse.",
            "Both up and down escalators are operational."
        ],
        paths: [
            "Shopping concourses extend in all directions.",
            "Only the main concourse and entrance are clear.",
            "A single walkway continues forward."
        ],
        interactables: [
            ["A store mannequin in an unusual pose.", "Its head turns slightly to watch you..."],
            ["A mall directory with a 'You Are Here' marker.", "The marker moves when you look away..."],
            ["A shopping cart that rolls away on its own.", "It seems to be leading you somewhere..."]
        ]
    },
    Train_station: {
        descriptions: [
            ["A train station with trains that never arrive.", ["door1", "door2"]],
            ["A platform where the echoes of footsteps linger.", ["door1", "door3"]],
            ["A waiting room with chairs that shift positions.", ["door1", "door4"]],
            ["An underground tunnel that seems to stretch forever.", ["door1", "door3"]]
        ],
        features: [
            "There's a staircase leading to the platform above.",
            "A dark stairwell leads to the underground tracks.",
            "Both main and emergency staircases are visible."
        ],
        paths: [
            "Train platforms extend in all directions.",
            "Only the main platform and entrance are clear.",
            "A single walkway continues forward."
        ],
        interactables: [
            ["A train schedule board with your name.", "The next train is always 'now'..."],
            ["A ticket machine that dispenses blank tickets.", "The tickets show places you've never been..."],
            ["A station clock that ticks backward.", "Time seems to unravel around it..."]
        ]
    }
};

// Items
const ITEMS = {
    'battery': 'Restores sanity slightly',
    'flashlight': 'Reveals hidden paths and increases sanity recovery',
    'mysterious key': 'May unlock special doors',
    'old map': 'Shows nearby points of interest',
    'strange coin': 'Makes unusual sounds when danger is near',
    'polaroid camera': 'Captures evidence of the impossible',
    'music box': 'Calms the mind, restoring sanity',
    'compass': 'Points to... something',
    'pills': 'Restores significant sanity'
};

// ==================== GAME STATE ====================

let gameState = {
    player: null,
    gameMode: null,
    currentRoom: null,
    exit: null,
    specialDoor: null,
    levelTheme: null,
    roomMap: {},
    entities: [],
    discoveredAreas: new Set(),
    running: false
};

// Directions
const DIRECTIONS = {
    '/right': { dx: 1, dy: 0, dz: 0 },
    '/left': { dx: -1, dy: 0, dz: 0 },
    '/forward': { dx: 0, dy: 1, dz: 0 },
    '/backward': { dx: 0, dy: -1, dz: 0 },
    '/upstairs': { dx: 0, dy: 0, dz: 1 },
    '/downstairs': { dx: 0, dy: 0, dz: -1 }
};

// ==================== CLASSES ====================

class Player {
    constructor(name) {
        this.name = name;
        this.x = 0;
        this.y = 0;
        this.z = Math.floor(Math.random() * 20) - 10;
        this.inventory = [];
        this.sanity = SETTINGS.player_stats.sanity_max;
        this.reality = SETTINGS.player_stats.reality_max;
        this.memory = SETTINGS.player_stats.memory_max;
        this.level = 1;
        this.hasLight = false;
    }
}

class Room {
    constructor(theme = 'limbo', level = 1) {
        this.theme = theme;
        this.level = level;
        
        // Get theme data
        const themeData = THEMES[theme] || THEMES.limbo;
        
        this.descriptions = themeData.descriptions;
        this.features = themeData.features;
        this.paths = themeData.paths;
        this.interactables = themeData.interactables;
        
        // Generate room content
        this.atmosphereIntensity = Math.random() * 0.7 + 0.3;
        this.temporalStability = Math.random() * 0.5 + 0.5;
        this.realityCoherence = Math.random() * 0.6 + 0.4;
        
        this.generateDescription();
    }
    
    generateDescription() {
        const desc = randomChoice(this.descriptions);
        this.description = desc[0];
        this.doors = desc[1];
        
        this.stairs = randomChoice(this.features);
        this.pathsText = randomChoice(this.paths);
        
        // Higher levels have more disturbing descriptions
        if (this.level > 25) {
            this.description += " Something feels very wrong here.";
        }
        
        this.interactable = randomChoice(this.interactables);
        
        // Available directions
        this.availableDirections = {
            '/up': this.stairs.toLowerCase().includes('up') || Math.random() < 0.5,
            '/down': this.stairs.toLowerCase().includes('down') || Math.random() < 0.5,
            '/forward': Math.random() < 0.8,
            '/backward': Math.random() < 0.8,
            '/left': Math.random() < 0.7,
            '/right': Math.random() < 0.7
        };
    }
}

// ==================== UTILITY FUNCTIONS ====================

function randomChoice(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function distance(pos1, pos2) {
    return Math.abs(pos1.x - pos2.x) + Math.abs(pos1.y - pos2.y) + Math.abs(pos1.z - pos2.z);
}

function getKey(x, y, z) {
    return `${x},${y},${z}`;
}

function parseKey(key) {
    const [x, y, z] = key.split(',').map(Number);
    return { x, y, z };
}

// ==================== GAME FUNCTIONS ====================

function startGame(mode) {
    const name = prompt("Enter your character's name:", "Unknown") || "Unknown";
    
    gameState.player = new Player(name);
    gameState.gameMode = mode;
    gameState.running = true;
    
    // Generate level
    generateLevel();
    
    // Show game screen
    document.getElementById('main-menu').classList.add('hidden');
    document.getElementById('game-screen').style.display = 'block';
    
    // Clear terminal and display initial room
    document.getElementById('game-output').innerHTML = '';
    
    displayRoom();
    
    log("Welcome to where reality bends and perception ends...", "info");
    log("Type /help for commands.", "info");
    
    // Focus input
    document.getElementById('terminal-input').focus();
}

function generateLevel() {
    const themes = Object.keys(THEMES);
    
    // Theme selection based on level
    const level = gameState.player.level;
    let themeWeights;
    
    if (level < 10) {
        themeWeights = { hospital: 5, school: 1, home: 5, limbo: 1, mall: 2, Train_station: 1 };
    } else if (level < 25) {
        themeWeights = { hospital: 3, school: 4, home: 3, limbo: 2, mall: 4, Train_station: 2 };
    } else if (level < 40) {
        themeWeights = { hospital: 2, school: 3, home: 2, limbo: 5, mall: 3, Train_station: 2 };
    } else {
        themeWeights = { hospital: 1, school: 2, home: 1, limbo: 10, mall: 1, Train_station: 3 };
    }
    
    // Weighted random selection
    const weightedThemes = [];
    for (const [theme, weight] of Object.entries(themeWeights)) {
        for (let i = 0; i < weight; i++) {
            weightedThemes.push(theme);
        }
    }
    gameState.levelTheme = randomChoice(weightedThemes);
    
    // Generate exit
    while (true) {
        gameState.exit = {
            x: randomInt(SETTINGS.world_bounds.x_min, SETTINGS.world_bounds.x_max),
            y: randomInt(SETTINGS.world_bounds.y_min, SETTINGS.world_bounds.y_max),
            z: randomInt(SETTINGS.world_bounds.z_min, SETTINGS.world_bounds.z_max)
        };
        
        const dist = distance(gameState.player, gameState.exit);
        if (dist >= 10) break;
    }
    
    // Generate special door for high levels
    if (gameState.player.level >= 50 && Math.random() < 0.5) {
        gameState.specialDoor = {
            x: randomInt(SETTINGS.world_bounds.x_min, SETTINGS.world_bounds.x_max),
            y: randomInt(SETTINGS.world_bounds.y_min, SETTINGS.world_bounds.y_max),
            z: Math.random() < 0.5 ? 5 : -5
        };
    } else {
        gameState.specialDoor = null;
    }
    
    // Reset room map
    gameState.roomMap = {};
    gameState.discoveredAreas = new Set();
    
    // Pre-generate rooms
    const numRooms = Math.min(50, 20 + Math.floor(level / 2));
    for (let i = 0; i < numRooms; i++) {
        const x = randomInt(SETTINGS.world_bounds.x_min, SETTINGS.world_bounds.x_max);
        const y = randomInt(SETTINGS.world_bounds.y_min, SETTINGS.world_bounds.y_max);
        const z = randomInt(SETTINGS.world_bounds.z_min, SETTINGS.world_bounds.z_max);
        const key = getKey(x, y, z);
        
        if (!gameState.roomMap[key]) {
            gameState.roomMap[key] = new Room(gameState.levelTheme, level);
        }
    }
    
    // Exit is always limbo-themed
    const exitKey = getKey(gameState.exit.x, gameState.exit.y, gameState.exit.z);
    gameState.roomMap[exitKey] = new Room('limbo', level);
    
    // Generate entities for nightmare mode
    if (gameState.gameMode === 'nightmare') {
        generateEntities();
    }
}

function generateEntities() {
    gameState.entities = [];
    
    const numEntities = Math.min(34, 20 + Math.floor(gameState.player.level / 5));
    
    for (let i = 0; i < numEntities; i++) {
        const entity = {
            name: randomChoice([
                'Shadow Walker', 'Mind Eater', 'Lost Soul', 'Void Stalker',
                'The Angel', 'The Demon', 'The Shadow', 'The Watcher'
            ]),
            speed: 0.4 + Math.random() * 0.2,
            friendly: Math.random() < 0.2,
            pos: {
                x: randomInt(SETTINGS.world_bounds.x_min, SETTINGS.world_bounds.x_max),
                y: randomInt(SETTINGS.world_bounds.y_min, SETTINGS.world_bounds.y_max),
                z: randomInt(SETTINGS.world_bounds.z_min, SETTINGS.world_bounds.z_max)
            }
        };
        
        // Don't spawn on player
        if (distance(entity.pos, gameState.player) > 5) {
            gameState.entities.push(entity);
        }
    }
}

function displayRoom() {
    const key = getKey(gameState.player.x, gameState.player.y, gameState.player.z);
    
    // Get or create room
    if (!gameState.roomMap[key]) {
        gameState.roomMap[key] = new Room(gameState.levelTheme, gameState.player.level);
    }
    
    gameState.currentRoom = gameState.roomMap[key];
    gameState.discoveredAreas.add(key);
    
    // Output as text lines
    log("", "info");
    log(`[${gameState.currentRoom.theme.toUpperCase()} ZONE - LEVEL ${gameState.player.level}]`, "info");
    log(gameState.currentRoom.description, "info");
    log(gameState.currentRoom.stairs, "info");
    log(gameState.currentRoom.pathsText, "info");
    
    if (gameState.currentRoom.interactable) {
        log(gameState.currentRoom.interactable[0], "warning");
    }
    
    // Danger (nightmare mode)
    if (gameState.gameMode === 'nightmare') {
        const nearby = gameState.entities.filter(e => distance(e.pos, gameState.player) <= 3);
        if (nearby.length > 0) {
            log("DANGER NEARBY:", "danger");
            nearby.forEach(e => {
                if (gameState.player.hasLight) {
                    log(`  - ${e.name} is nearby`, "danger");
                } else {
                    log(`  - Something moves in the darkness`, "danger");
                }
            });
        }
    }
    
    // Exit indicator
    const currentPos = { x: gameState.player.x, y: gameState.player.y, z: gameState.player.z };
    if (distance(currentPos, gameState.exit) <= 2) {
        log("This room has a door that feels different. It might be the exit.", "success");
    }
    
    // Special door
    if (gameState.specialDoor && distance(currentPos, gameState.specialDoor) <= 2) {
        if (gameState.player.sanity > 70) {
            log("A radiant door pulses with warm light. It calls to you.", "success");
        } else {
            log("A dark door emanates dread. Something waits beyond.", "danger");
        }
    }
    
    // Show position
    log(`Position: (${gameState.player.x}, ${gameState.player.y}, ${gameState.player.z})`, "info");
    log(`Sanity: ${gameState.player.sanity}/100 | Level: ${gameState.player.level}`, "info");
}

function move(direction) {
    if (!gameState.running || !gameState.player) return;
    
    // Normalize direction
    let dir = direction;
    if (!dir.startsWith('/')) {
        dir = '/' + dir;
    }
    
    // Handle aliases
    const aliases = {
        'f': '/forward', 'b': '/backward', 'l': '/left', 'r': '/right',
        'u': '/upstairs', 'd': '/downstairs',
        'forward': '/forward', 'backward': '/backward', 'back': '/backward',
        'left': '/left', 'right': '/right',
        'up': '/upstairs', 'down': '/downstairs',
        'upstairs': '/upstairs', 'downstairs': '/downstairs'
    };
    
    dir = aliases[dir] || dir;
    
    if (!DIRECTIONS[dir]) {
        log("Invalid direction. Use: forward, backward, left, right, upstairs, downstairs", "error");
        return;
    }
    
    // Check if direction is available
    if (!gameState.currentRoom.availableDirections[dir]) {
        log(`You can't go ${dir.replace('/', '')} from here.`, "error");
        return;
    }
    
    const d = DIRECTIONS[dir];
    gameState.player.x += d.dx;
    gameState.player.y += d.dy;
    gameState.player.z += d.dz;
    
    // Constrain to bounds
    gameState.player.x = Math.max(SETTINGS.world_bounds.x_min, Math.min(SETTINGS.world_bounds.x_max, gameState.player.x));
    gameState.player.y = Math.max(SETTINGS.world_bounds.y_min, Math.min(SETTINGS.world_bounds.y_max, gameState.player.y));
    gameState.player.z = Math.max(SETTINGS.world_bounds.z_min, Math.min(SETTINGS.world_bounds.z_max, gameState.player.z));
    
    // Sanity loss
    const sanityLoss = gameState.player.hasLight ? 0.5 : 1;
    gameState.player.sanity = Math.max(0, Math.floor(gameState.player.sanity - sanityLoss));
    
    log(`Moving ${dir.replace('/', '')}...`, "info");
    
    // Move entities in nightmare mode
    if (gameState.gameMode === 'nightmare') {
        moveEntities();
        checkNightmareDeath();
    }
    
    // Check endings
    if (!checkEndings()) {
        displayRoom();
    }
    
    // Check sanity
    if (gameState.player.sanity < 20) {
        log("Your sanity is dangerously low!", "warning");
    } else if (gameState.player.sanity < 50) {
        log("Your sanity is getting low.", "warning");
    }
}

function moveEntities() {
    for (const entity of gameState.entities) {
        if (Math.random() < entity.speed) {
            const dx = gameState.player.x - entity.pos.x;
            const dy = gameState.player.y - entity.pos.y;
            const dz = gameState.player.z - entity.pos.z;
            
            const moves = [];
            if (dx !== 0) moves.push({ axis: 'x', dir: dx > 0 ? 1 : -1 });
            if (dy !== 0) moves.push({ axis: 'y', dir: dy > 0 ? 1 : -1 });
            if (dz !== 0) moves.push({ axis: 'z', dir: dz > 0 ? 1 : -1 });
            
            if (moves.length > 0) {
                const move = randomChoice(moves);
                if (move.axis === 'x') entity.pos.x += move.dir;
                else if (move.axis === 'y') entity.pos.y += move.dir;
                else entity.pos.z += move.dir;
            }
        }
    }
}

function checkNightmareDeath() {
    for (const entity of gameState.entities) {
        if (entity.pos.x === gameState.player.x && 
            entity.pos.y === gameState.player.y && 
            entity.pos.z === gameState.player.z &&
            !entity.friendly) {
            
            log(`${entity.name} found you. GAME OVER.`, "error");
            log(`Final Level: ${gameState.player.level}`, "info");
            gameState.running = false;
            return true;
        }
    }
    return false;
}

function checkEndings() {
    const pos = { x: gameState.player.x, y: gameState.player.y, z: gameState.player.z };
    
    // Wall of photos ending
    if (gameState.currentRoom.description.toLowerCase().includes('wall of photos') && Math.random() < 0.05) {
        triggerWakeUpEnding();
        return true;
    }
    
    // Heaven/Hell endings
    if (gameState.specialDoor && distance(pos, gameState.specialDoor) === 0) {
        if (gameState.player.sanity > 70) {
            triggerHeavenEnding();
        } else {
            triggerHellEnding();
        }
        return true;
    }
    
    // Exit to next level
    if (distance(pos, gameState.exit) === 0) {
        nextLevel();
        return true;
    }
    
    // Sanity game over
    if (gameState.player.sanity <= 0) {
        log("Your sanity has completely eroded. You are lost in the liminal space forever.", "error");
        log(`Final Level: ${gameState.player.level}`, "info");
        gameState.running = false;
        return true;
    }
    
    return false;
}

function nextLevel() {
    gameState.player.level++;
    gameState.player.sanity = Math.min(gameState.player.sanity + 15, SETTINGS.player_stats.sanity_max);
    
    log(`You found the exit! Moving to level ${gameState.player.level}.`, "success");
    log(`Sanity restored to ${gameState.player.sanity}.`, "success");
    
    // Random item
    if (Math.random() < 0.3) {
        const itemKeys = Object.keys(ITEMS);
        const item = randomChoice(itemKeys);
        gameState.player.inventory.push(item);
        log(`You found a ${item}!`, "success");
    }
    
    generateLevel();
    
    if (gameState.gameMode === 'nightmare') {
        generateEntities();
    }
    
    displayRoom();
}

function triggerWakeUpEnding() {
    const messages = [
        "You stare at the wall of photos. Memories flood back...",
        "A car accident. A hospital room. Machines beeping.",
        "You've been in a coma. This was all in your mind.",
        "You feel yourself pulled back to reality.",
        "Your eyes open. A doctor smiles down at you.",
        "\"Welcome back,\" she says.",
        "=== YOU WOKE UP - THE REAL ENDING ==="
    ];
    
    displayEnding(messages, "#00ff00");
}

function triggerHeavenEnding() {
    const messages = [
        "You step through the door into blinding light...",
        "You realise your body is no longer heavy.",
        "A sense of peace washes over you.",
        "You see familiar faces. People you once knew.",
        "They welcome you with open arms.",
        "You realize you've been here before.",
        "You're finally home.",
        "=== HEAVEN ENDING - You found peace ==="
    ];
    
    displayEnding(messages, "#00ffff");
}

function triggerHellEnding() {
    const messages = [
        "You step through the door into smothering darkness...",
        "The air is hot and sulfurous.",
        "You hear screams in the distance.",
        "Shadowy figures surround you.",
        "You try to run, but there's nowhere to go.",
        "You realize this is your fate.",
        "=== HELL ENDING - Your sanity was too low ==="
    ];
    
    displayEnding(messages, "#ff0000");
}

function displayEnding(messages, color) {
    gameState.running = false;
    
    log("", "info");
    messages.forEach(msg => {
        log(msg, "success");
    });
}

// ==================== ACTIONS ====================

function examine() {
    if (!gameState.currentRoom.interactable) {
        log("There's nothing interesting to examine here.", "info");
        return;
    }
    
    const [, description] = gameState.currentRoom.interactable;
    log(description, "info");
    
    // Chance to gain sanity
    if (Math.random() < 0.3) {
        const gain = randomInt(5, 15);
        gameState.player.sanity = Math.min(SETTINGS.player_stats.sanity_max, gameState.player.sanity + gain);
        log(`You feel a bit better. +${gain} sanity.`, "success");
    }
}

function take() {
    if (!gameState.currentRoom.interactable) {
        log("There's nothing useful to take.", "info");
        return;
    }
    
    if (Math.random() < 0.9) {
        const itemKeys = Object.keys(ITEMS);
        const item = randomChoice(itemKeys);
        gameState.player.inventory.push(item);
        log(`You found a ${item}!`, "success");
    } else {
        log("There's nothing useful to take.", "info");
    }
}

function showInventory() {
    if (gameState.player.inventory.length === 0) {
        log("Your inventory is empty.", "info");
        return;
    }
    
    log("=== INVENTORY ===", "info");
    gameState.player.inventory.forEach(item => {
        log(`  ${item}: ${ITEMS[item] || 'Unknown item'}`, "info");
    });
}

function showStats() {
    log("=== STATUS ===", "info");
    log(`Name: ${gameState.player.name}`, "info");
    log(`Level: ${gameState.player.level}`, "info");
    log(`Position: (${gameState.player.x}, ${gameState.player.y}, ${gameState.player.z})`, "info");
    log(`Sanity: ${gameState.player.sanity}/100`, "info");
    log(`Reality: ${gameState.player.reality}/100`, "info");
    log(`Memory: ${gameState.player.memory}/100`, "info");
    log(`Game Mode: ${gameState.gameMode}`, "info");
}

function showHelp() {
    log("=== COMMANDS ===", "info");
    log("Movement: forward, backward, left, right, upstairs, downstairs", "info");
    log("Shortcuts: f, b, l, r, u, d", "info");
    log("Actions:", "info");
    log("  /examine - Look around", "info");
    log("  /take - Pick up items", "info");
    log("  /inventory (or /i) - Check items", "info");
    log("  /stats - View status", "info");
    log("  /help - This help", "info");
}

// ==================== UI ====================

function log(message, type = 'info') {
    const output = document.getElementById('game-output');
    const line = document.createElement('div');
    line.className = `terminal-line ${type}`;
    line.textContent = message;
    output.appendChild(line);
    
    // Keep only last 100 entries
    while (output.children.length > 100) {
        output.removeChild(output.firstChild);
    }
    
    // Scroll to bottom
    const terminal = document.getElementById('terminal');
    terminal.scrollTop = terminal.scrollHeight;
}

function useItem(item) {
    if (!gameState.player.inventory.includes(item)) {
        log(`You don't have a ${item}.`, "error");
        return;
    }
    
    switch(item) {
        case 'battery':
            const batteryGain = randomInt(10, 20);
            gameState.player.sanity = Math.min(SETTINGS.player_stats.sanity_max, gameState.player.sanity + batteryGain);
            log(`You use the battery. +${batteryGain} sanity.`, "success");
            gameState.player.inventory = gameState.player.inventory.filter(i => i !== item);
            break;
            
        case 'flashlight':
            gameState.player.hasLight = true;
            log("You turn on the flashlight. It will help you see.", "success");
            break;
            
        case 'pills':
            const pillsGain = randomInt(30, 50);
            gameState.player.sanity = Math.min(SETTINGS.player_stats.sanity_max, gameState.player.sanity + pillsGain);
            log(`You take the pills. +${pillsGain} sanity.`, "success");
            gameState.player.inventory = gameState.player.inventory.filter(i => i !== item);
            break;
            
        case 'music box':
            const musicGain = randomInt(15, 30);
            gameState.player.sanity = Math.min(SETTINGS.player_stats.sanity_max, gameState.player.sanity + musicGain);
            log(`The gentle melody soothes your mind. +${musicGain} sanity.`, "success");
            break;
            
        default:
            log(`You're not sure how to use the ${item}.`, "info");
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        processCommand();
    }
}

function processCommand() {
    const input = document.getElementById('terminal-input');
    const cmd = input.value.trim().toLowerCase();
    input.value = '';
    
    if (!cmd) return;
    
    // Echo command
    log(`> ${cmd}`, "info");
    
    // Movement commands
    if (['forward', 'backward', 'left', 'right', 'upstairs', 'downstairs', 'f', 'b', 'l', 'r', 'u', 'd'].includes(cmd)) {
        move(cmd);
        return;
    }
    
    // Slash commands
    switch(cmd) {
        case '/help':
        case 'help':
            showHelp();
            break;
        case '/inventory':
        case '/i':
        case 'inventory':
        case 'i':
            showInventory();
            break;
        case '/stats':
        case 'stats':
            showStats();
            break;
        case '/examine':
        case 'examine':
            examine();
            break;
        case '/take':
        case 'take':
            take();
            break;
        default:
            log("Unknown command. Type /help for commands.", "error");
    }
}

// Initialize
console.log("Liminal: Lucid Dreams - Browser Version Loaded");