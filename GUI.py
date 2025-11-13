import pygame
import sys
import math
import tictactoe

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 540
BOARD_OFFSET_Y = 100
CELL_SIZE = BOARD_SIZE // 3
LINE_WIDTH = 5
CROSS_WIDTH = 15
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15

# Colors
BG_COLOR = (20, 20, 40)
LINE_COLOR = (40, 40, 80)
CROSS_COLOR = (255, 50, 50)
CROSS_GLOW = (255, 100, 100)
CIRCLE_COLOR = (50, 150, 255)
CIRCLE_GLOW = (100, 180, 255)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (60, 60, 100)
BUTTON_HOVER = (80, 80, 140)
POPUP_BG = (30, 30, 60)
POPUP_BORDER = (100, 100, 200)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.Font(None, 80)
menu_font = pygame.font.Font(None, 50)
message_font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 40)

# Game state
game_mode = None  # None, "Player vs Player (PVP)", "Player vs Computer (PVC)"
current_player = "X"
game_over = False
winner_message = ""
animation_time = 0


def draw_grid():
    """Draw the tic-tac-toe grid."""
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, 
                     (CELL_SIZE + 30, BOARD_OFFSET_Y + 30), 
                     (CELL_SIZE + 30, BOARD_OFFSET_Y + BOARD_SIZE - 30), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, 
                     (2 * CELL_SIZE + 30, BOARD_OFFSET_Y + 30), 
                     (2 * CELL_SIZE + 30, BOARD_OFFSET_Y + BOARD_SIZE - 30), LINE_WIDTH)
    
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, 
                     (30, BOARD_OFFSET_Y + CELL_SIZE + 30), 
                     (BOARD_SIZE + 30, BOARD_OFFSET_Y + CELL_SIZE + 30), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, 
                     (30, BOARD_OFFSET_Y + 2 * CELL_SIZE + 30), 
                     (BOARD_SIZE + 30, BOARD_OFFSET_Y + 2 * CELL_SIZE + 30), LINE_WIDTH)


def draw_cross(row, col, glow=False):
    """Draw an X with glowing effect."""
    center_x = col * CELL_SIZE + CELL_SIZE // 2 + 30
    center_y = row * CELL_SIZE + CELL_SIZE // 2 + BOARD_OFFSET_Y + 30
    offset = 50
    
    if glow:
        # Glow effect
        for i in range(3):
            alpha = 50 - i * 15
            glow_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            width = CROSS_WIDTH + (3 - i) * 3
            pygame.draw.line(glow_surface, (*CROSS_GLOW, alpha), 
                           (CELL_SIZE // 2 - offset, CELL_SIZE // 2 - offset),
                           (CELL_SIZE // 2 + offset, CELL_SIZE // 2 + offset), width)
            pygame.draw.line(glow_surface, (*CROSS_GLOW, alpha),
                           (CELL_SIZE // 2 + offset, CELL_SIZE // 2 - offset),
                           (CELL_SIZE // 2 - offset, CELL_SIZE // 2 + offset), width)
            screen.blit(glow_surface, (col * CELL_SIZE + 30, row * CELL_SIZE + BOARD_OFFSET_Y + 30))
    
    # Main cross
    pygame.draw.line(screen, CROSS_COLOR, 
                     (center_x - offset, center_y - offset),
                     (center_x + offset, center_y + offset), CROSS_WIDTH)
    pygame.draw.line(screen, CROSS_COLOR,
                     (center_x + offset, center_y - offset),
                     (center_x - offset, center_y + offset), CROSS_WIDTH)


def draw_circle(row, col, glow=False):
    """Draw an O with glowing effect."""
    center_x = col * CELL_SIZE + CELL_SIZE // 2 + 30
    center_y = row * CELL_SIZE + CELL_SIZE // 2 + BOARD_OFFSET_Y + 30
    
    if glow:
        # Glow effect
        for i in range(3):
            alpha = 50 - i * 15
            glow_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*CIRCLE_GLOW, alpha), 
                             (CELL_SIZE // 2, CELL_SIZE // 2), 
                             CIRCLE_RADIUS + (3 - i) * 3, CIRCLE_WIDTH + (3 - i) * 2)
            screen.blit(glow_surface, (col * CELL_SIZE + 30, row * CELL_SIZE + BOARD_OFFSET_Y + 30))
    
    # Main circle
    pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), 
                      CIRCLE_RADIUS, CIRCLE_WIDTH)


def draw_board():
    """Draw all marks on the board."""
    for i in range(9):
        row = i // 3
        col = i % 3
        if tictactoe.board[i] == "X":
            draw_cross(row, col, glow=True)
        elif tictactoe.board[i] == "O":
            draw_circle(row, col, glow=True)


def draw_button(text, x, y, w, h, mouse_pos):
    """Draw a button and return if it's hovered."""
    rect = pygame.Rect(x, y, w, h)
    is_hovered = rect.collidepoint(mouse_pos)
    color = BUTTON_HOVER if is_hovered else BUTTON_COLOR
    
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, POPUP_BORDER, rect, 3, border_radius=10)
    
    text_surf = button_font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    
    return is_hovered


def draw_popup(message):
    """Draw centered popup with message and buttons."""
    popup_width = 450
    popup_height = 280
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2
    
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    # Popup background
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    pygame.draw.rect(screen, POPUP_BG, popup_rect, border_radius=15)
    pygame.draw.rect(screen, POPUP_BORDER, popup_rect, 4, border_radius=15)
    
    # Message
    msg_surf = message_font.render(message, True, TEXT_COLOR)
    msg_rect = msg_surf.get_rect(center=(WIDTH // 2, popup_y + 80))
    screen.blit(msg_surf, msg_rect)
    
    # Buttons
    mouse_pos = pygame.mouse.get_pos()
    button_y = popup_y + 160
    
    rematch_hover = draw_button("Rematch", WIDTH // 2 - 200, button_y, 180, 60, mouse_pos)
    menu_hover = draw_button("Menu", WIDTH // 2 + 20, button_y, 180, 60, mouse_pos)
    
    return rematch_hover, menu_hover


def draw_menu():
    """Draw the main menu."""
    screen.fill(BG_COLOR)
    
    # Title with glow
    glow_offset = abs(math.sin(animation_time * 2)) * 5
    for i in range(3):
        alpha = 30 - i * 10
        glow_surf = title_font.render("TIC TAC TOE", True, (*CIRCLE_GLOW, alpha))
        glow_rect = glow_surf.get_rect(center=(WIDTH // 2 + i, 120 + i))
        screen.blit(glow_surf, glow_rect)
    
    title_surf = title_font.render("TIC TAC TOE", True, TEXT_COLOR)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 120))
    screen.blit(title_surf, title_rect)
    
    # Menu buttons
    mouse_pos = pygame.mouse.get_pos()
    
    pvp_hover = draw_button("Player vs Player", WIDTH // 2 - 150, 250, 300, 70, mouse_pos)
    pvc_hover = draw_button("Player vs Computer", WIDTH // 2 - 150, 350, 300, 70, mouse_pos)
    quit_hover = draw_button("Quit", WIDTH // 2 - 150, 450, 300, 70, mouse_pos)
    
    return pvp_hover, pvc_hover, quit_hover


def get_cell_from_pos(pos):
    """Convert mouse position to board cell index."""
    x, y = pos
    if 30 <= x <= BOARD_SIZE + 30 and BOARD_OFFSET_Y + 30 <= y <= BOARD_OFFSET_Y + BOARD_SIZE + 30:
        col = (x - 30) // CELL_SIZE
        row = (y - BOARD_OFFSET_Y - 30) // CELL_SIZE
        return row * 3 + col
    return None


def main():
    global game_mode, current_player, game_over, winner_message, animation_time
    
    running = True
    show_menu = True
    
    while running:
        dt = clock.tick(60) / 1000.0
        animation_time += dt
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_menu:
                    # Menu interaction
                    pvp_h, pvc_h, quit_h = draw_menu()
                    if pvp_h:
                        game_mode = "PVP"
                        show_menu = False
                        tictactoe.reset_board()
                        current_player = "X"
                        game_over = False
                    elif pvc_h:
                        game_mode = "PVC"
                        show_menu = False
                        tictactoe.reset_board()
                        current_player = "X"
                        game_over = False
                    elif quit_h:
                        running = False
                
                elif game_over:
                    # Popup interaction
                    rematch_h, menu_h = draw_popup(winner_message)
                    if rematch_h:
                        tictactoe.reset_board()
                        current_player = "X"
                        game_over = False
                        winner_message = ""
                    elif menu_h:
                        show_menu = True
                        game_over = False
                        winner_message = ""
                        game_mode = None
                
                elif game_mode and not game_over:
                    # Game interaction
                    if game_mode == "PVP" or (game_mode == "PVC" and current_player == "X"):
                        cell = get_cell_from_pos(mouse_pos)
                        if cell is not None and tictactoe.board[cell] == " ":
                            tictactoe.make_move(cell, current_player)
                            
                            if tictactoe.is_winner(current_player):
                                if game_mode == "PVP":
                                    winner_message = f"Player {current_player} Wins!"
                                else:
                                    winner_message = "You Win!"
                                game_over = True
                            elif tictactoe.is_draw():
                                winner_message = "It's a Draw!"
                                game_over = True
                            else:
                                current_player = "O" if current_player == "X" else "X"
        
        # Computer move (PVC mode)
        if game_mode == "PVC" and current_player == "O" and not game_over and not show_menu:
            pygame.time.wait(500)  #  Pause for better UX
            move = tictactoe.get_computer_move()
            tictactoe.make_move(move, "O")
            
            if tictactoe.is_winner("O"):
                winner_message = "Computer Wins!"
                game_over = True
            elif tictactoe.is_draw():
                winner_message = "It's a Draw!"
                game_over = True
            else:
                current_player = "X"
        
        screen.fill(BG_COLOR)
        
        if show_menu:
            draw_menu()
        else:
            if game_mode == "PVP":
                header_text = f"Player {current_player}'s Turn"
            elif game_mode == "PVC":
                header_text = "Your Turn" if current_player == "X" else "Computer's Turn"
            else:
                header_text = ""
            
            header_surf = menu_font.render(header_text, True, TEXT_COLOR)
            header_rect = header_surf.get_rect(center=(WIDTH // 2, 50))
            screen.blit(header_surf, header_rect)
            
            #Draw Game Board
            draw_grid()
            draw_board()
            
            if game_over:
                draw_popup(winner_message)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()