import pygame
import random

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 100
ROWS, COLS = 6, 6
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (255, 255, 255)  # 背景颜色
SELECTED_COLOR = (255, 0, 0)  # 选中提示颜色
BUTTON_COLOR = (0, 128, 0)  # 按钮颜色
BUTTON_HOVER_COLOR = (0, 255, 0)  # 按钮悬停颜色
BUTTON_TEXT_COLOR = WHITE

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("羊了个羊小游戏")

# 加载图案图片
try:
    patterns = [pygame.image.load(f"{i}.jpg") for i in range(1, 7)]
    patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]
except pygame.error as e:
    print(f"图像加载失败: {e}")
    pygame.quit()
    exit()

# 加载背景动图帧
try:
    background_frames = [pygame.image.load(f"f{i}.jpg").convert() for i in range(1, 17)]
    background_frames = [pygame.transform.scale(frame, (WIDTH, HEIGHT)) for frame in background_frames]
except pygame.error as e:
    print(f"背景图像加载失败: {e}")
    pygame.quit()
    exit()

current_frame = 0
clock = pygame.time.Clock()

def draw_button(x, y, width, height, color, hover_color, text, font_size, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def check_match(board, selected, selected_tiles):
    if len(selected) == 3:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        r3, c3 = selected[2]
        
        if (r1, c1) == (r2, c2) or (r1, c1) == (r3, c3) or (r2, c2) == (r3, c3):
            selected.clear()
            return
        
        if board[r1][c1] == board[r2][c2] == board[r3][c3]:
            board[r1][c1] = None
            board[r2][c2] = None
            board[r3][c3] = None
            selected_tiles.discard((r1, c1))
            selected_tiles.discard((r2, c2))
            selected_tiles.discard((r3, c3))
        
        selected.clear()

def game_start_screen():
    global current_frame
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.blit(background_frames[current_frame], (0, 0))
        current_frame = (current_frame + 1) % len(background_frames)

        draw_button(WIDTH // 4, HEIGHT // 2 - 90, WIDTH // 2, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR, "try it", 36, start_game)
        draw_button(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR, "choose", 36, settings)
        draw_button(WIDTH // 4, HEIGHT // 2 + 90, WIDTH // 2, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR, "quit", 36, quit_game)

        pygame.display.flip()
        clock.tick(FPS)

def start_game():
    print("游戏开始")
    main()

def settings():
    pygame.quit()
    # 引入外部模块需要确保路径正确，或将 game 文件中的函数导入
    import game
    game.level_selection()

def quit_game():
    pygame.quit()
    exit()

def create_board():
    board = []
    for row in range(ROWS):
        board_row = []
        for col in range(COLS):
            tile = random.choice(patterns)
            board_row.append(tile)
        board.append(board_row)
    return board

def draw_board(board, selected_tiles):
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))
            if (row, col) in selected_tiles:
                pygame.draw.rect(screen, SELECTED_COLOR, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

def main():
    board = create_board()
    selected = []
    selected_tiles = set()
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // TILE_SIZE, y // TILE_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS and board[row][col] is not None:
                    if (row, col) in selected_tiles:
                        selected.remove((row, col))
                        selected_tiles.remove((row, col))
                    else:
                        if len(selected) < 6:
                            selected.append((row, col))
                            selected_tiles.add((row, col))
                        else:
                            print("游戏结束")
                            running = False

                if len(selected) == 3:
                    check_match(board, selected, selected_tiles)

        screen.fill(BG_COLOR)
        draw_board(board, selected_tiles)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    game_start_screen()