import os
import utilities.colours as colours

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(self):
    game_title ="""
█░░ █ █▀▄▀█ █ █▄░█ ▄▀█ █░░ ▄  █░░ █░█ █▀ █ █▀▄  █▀▄ █▀█ ▄▀ ▄▀█ █▀▄▀█ █▀▀
█░░ █ █░█░█ █ █░██ █ █ █      █   █ █ █  █ █ █  █ █ █▄█ █▄ █ █ █░█░█ █▄▄
█▄▄ █ █░ ░█ █ █░░█ █▀█ █▄▄ ▄  █▄▄ █▄█ █▄ █ █▄▀  █▄▀ █▀▄ █▄ █▀█ █░ ░█ ▄▄█
"""

    clear_screen() 
    print(f"{'=' * 50}")
    print(colours.CYAN + game_title + colours.END)
    print(f"{'=' * 50}\n")

def progress_bar(current, total, length=20, color=colours.CYAN):
    """Create a visual progress bar"""
    filled = int(length * current / total)
    bar = '█' * filled + '░' * (length - filled)
    percentage = int(100 * current / total)
    return f"{color}[{bar}]{colours.RESET_ALL} {percentage}%"

def box_text(text, width=60, border_color=colours.WHITE, text_color=colours.RESET):
    """Wrap text in an ASCII box"""
    lines = text.split('\n')
    wrapped_lines = []
    
    for line in lines:
        while len(line) > width - 4:
            wrapped_lines.append(line[:width - 4])
            line = line[width - 4:]
        wrapped_lines.append(line)
    
    border = border_color + '┌' + '─' * (width - 2) + '┐' + colours.RESET_ALL
    bottom = border_color + '└' + '─' * (width - 2) + '┘' + colours.RESET_ALL
    
    result = [border]
    for line in wrapped_lines:
        result.append(f"{border_color}│{colours.RESET} {text_color}{line:<{width - 3}}{colours.RESET} {border_color}│{colours.RESET}")
    result.append(bottom)
    
    return '\n'.join(result)

def section_divider(char='─', length=50, color=colours.LIGHTBLACK_EX):
    """Create a section divider line"""
    return f"{color}{char * length}{colours.RESET_ALL}"

def status_bar(player, show_box=True):
    """Create a status bar showing player stats"""
    # Determine colors based on values
    sanity_color = colours.GREEN
    if player.sanity < 30:
        sanity_color = colours.RED
    elif player.sanity < 60:
        sanity_color = colours.YELLOW
        
    reality_color = colours.CYAN
    if player.reality_coherence < 30:
        reality_color = colours.RED
    elif player.reality_coherence < 60:
        reality_color = colours.YELLOW
        
    memory_color = colours.LIGHTBLUE_EX
    if player.memory_stability < 30:
        memory_color = colours.RED
    elif player.memory_stability < 60:
        memory_color = colours.YELLOW
    
    # Create progress bars
    sanity_bar = progress_bar(player.sanity, 100, 15, sanity_color)
    reality_bar = progress_bar(player.reality_coherence, 100, 15, reality_color)
    memory_bar = progress_bar(player.memory_stability, 100, 15, memory_color)
    
    # Format the status bar
    status = f"""
{sanity_color}SANITY:{colours.RESET_ALL} {player.sanity:3d}/100 {sanity_bar}
{reality_color}REALITY:{colours.RESET_ALL} {player.reality_coherence:3d}/100 {reality_bar}
{memory_color}MEMORY:{colours.RESET_ALL} {player.memory_stability:3d}/100 {memory_bar}"""
    
    if show_box:
        return box_text(f"Level: {player.level} | Pos: ({player.x}, {player.y}, {player.z})\n" + 
                       f"Psychological State: {player.psychological_state}" + status, 
                       55, colours.CYAN)
    return f"Level: {player.level} | Pos: ({player.x}, {player.y}, {player.z})\n" + status

def decorated_title(title, width=50, color=colours.MAGENTA):
    """Create a decorated section title"""
    padding = (width - len(title) - 2) // 2
    return f"""
{color}╔{'═' * (len(title) + padding * 2)}╗{colours.RESET}
{color}║{' ' * padding}{title}{' ' * padding}║{colours.RESET}
{color}╚{'═' * (len(title) + padding * 2)}╝{colours.RESET}"""

def menu_option(number, description, color=colours.WHITE, selected=False):
    """Format a menu option with nice styling"""
    if selected:
        return f"  {color}► {number}. {description} ◄{colours.RESET}"
    return f"    {color}{number}. {description}{colours.RESET}"

def centered_text(text, width=50, color=colours.WHITE):
    """Center text within a given width"""
    padding = (width - len(text)) // 2
    return f"{color}{' ' * padding}{text}{' ' * padding}{colours.RESET_ALL}"

def print_atmosphere(room, width=55):
    """Display room atmosphere with color coding"""
    if not hasattr(room, 'atmosphere_intensity'):
        return ""
    
    atmosphere = []
    if room.atmosphere_intensity > 0.8:
        atmosphere.append(f"{colours.RED}{colours.BRIGHT}⚠ The air feels thick and oppressive...{colours.RESET_ALL}")
    elif room.atmosphere_intensity > 0.5:
        atmosphere.append(f"{colours.YELLOW}⚡ An unsettling tension permeates the space.{colours.RESET_ALL}")
        
    if room.temporal_stability < 0.3:
        atmosphere.append(f"{colours.MAGENTA}{colours.BRIGHT}⏱ Time seems to stutter around you...{colours.RESET_ALL}")
    elif room.temporal_stability < 0.6:
        atmosphere.append(f"{colours.LIGHTMAGENTA_EX}⏳ The flow of time feels inconsistent...{colours.RESET_ALL}")
        
    if room.reality_coherence < 0.4:
        atmosphere.append(f"{colours.BACK_RED}{colours.WHITE}◊ Reality flickers like a damaged screen...{colours.RESET_ALL}")
    elif room.reality_coherence < 0.7:
        atmosphere.append(f"{colours.LIGHTBLACK_EX}∼ The edges of your vision seem to blur...{colours.RESET_ALL}")
    
    if atmosphere:
        return '\n'.join([f"  {line}" for line in atmosphere])
    return ""

def danger_indicator(entity_count, max_distance=3):
    """Show danger level indicator"""
    if entity_count == 0:
        return f"  {colours.GREEN}✓ No immediate threats detected{colours.RESET_ALL}"
    elif entity_count <= 2:
        return f"  {colours.YELLOW}⚠ WARNING: {entity_count} entity(s) nearby!{colours.RESET_ALL}"
    else:
        return f"  {colours.RED}{colours.BRIGHT}☠ CRITICAL: {entity_count} entities very close!{colours.RESET_ALL}"
