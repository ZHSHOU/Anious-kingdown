import pygame
import random

# 游戏设置
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 100
ROWS, COLS = 6, 6
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SELECTED_COLOR = (255, 0, 0)  # 选中提示颜色
BG_COLOR = (255, 255, 255)  # 背景颜色

# 按钮绘制及交互
def draw_button(screen, x, y, width, height, color, hover_color, text, font_size, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# 创建游戏板
def create_board(patterns):
    total_tiles = ROWS * COLS
    num_patterns = len(patterns)

    # 确保总数是3的倍数
    if total_tiles % 3 != 0:
        raise ValueError("总的方块数量必须是3的倍数")

    # 确保每种图案的出现次数是3的倍数
    pattern_counts = [3] * num_patterns
    total_needed = sum(pattern_counts)
    if total_needed > total_tiles:
        raise ValueError("图案数量超出总方块数量")

    # 调整图案的分布，确保每种图案的数量为3的倍数
    board = []
    available_tiles = []
    for pattern, count in zip(patterns, pattern_counts):
        available_tiles.extend([pattern] * count)

    # 确保总数符合要求
    while len(available_tiles) < total_tiles:
        available_tiles.append(random.choice(patterns))

    random.shuffle(available_tiles)

    # 创建游戏板
    for row in range(ROWS):
        board_row = available_tiles[row * COLS:(row + 1) * COLS]
        board.append(board_row)

    return board

# 绘制游戏板
def draw_board(screen, board, selected_tiles):
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))
            if (row, col) in selected_tiles:
                pygame.draw.rect(screen, SELECTED_COLOR, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

# 检查匹配
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

# 根据关卡选择加载图案
def load_patterns(level):
    if level == 1:
        patterns = [pygame.image.load(f"{i}.jpg") for i in range(1, 7)]
    elif level == 2:
        patterns = [pygame.image.load(f"{i}.jpg") for i in range(1, 12)]
    elif level == 3:
        patterns = [pygame.image.load(f"{i}.jpg") for i in range(1, 13)]
    else:
        raise ValueError("Invalid level")

    return [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

# 游戏主逻辑
def main(level):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("游戏")
    clock = pygame.time.Clock()

    try:
        patterns = load_patterns(level)
        board = create_board(patterns)
    except Exception as e:
        print(f"游戏初始化失败: {e}")
        pygame.quit()
        return

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
        draw_board(screen, board, selected_tiles)
        pygame.display.flip()

    pygame.quit()

# 游戏开始界面
def game_start_screen():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("游戏开始")
    clock = pygame.time.Clock()

    def start_game():
        main(1)  # 开始关卡1

    def settings():
        level_selection()  # 跳转到关卡选择界面

    def quit_game():
        pygame.quit()
        exit()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(BG_COLOR)
        draw_button(screen, WIDTH // 4, HEIGHT // 2 - 90, WIDTH // 2, 60, (0, 128, 0), (0, 255, 0), "游戏开始", 36, start_game)
        draw_button(screen, WIDTH // 4, HEIGHT // 2, WIDTH // 2, 60, (0, 128, 0), (0, 255, 0), "设置", 36, settings)
        draw_button(screen, WIDTH // 4, HEIGHT // 2 + 90, WIDTH // 2, 60, (0, 128, 0), (0, 255, 0), "退出", 36, quit_game)

        pygame.display.flip()
        clock.tick(FPS)

# 关卡选择界面
def level_selection():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("关卡选择")
    clock = pygame.time.Clock()
    
    def level1():
        main(1)  # 开始关卡1
    
    def level2():
        main(2)  # 开始关卡2
    
    def level3():
        main(3)  # 开始关卡3

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(BG_COLOR)
        draw_button(screen, WIDTH // 4, HEIGHT // 2 - 90, WIDTH // 2, 60, (0, 128, 0), (0, 255, 0), "Level 1", 36, level1)
        draw_button(screen, WIDTH // 4, HEIGHT // 2, WIDTH // 2, 60, (0, 128, 0), (0, 255, 0), "Level 2", 36, level2)
        draw_button(screen, WIDTH // 4, HEIGHT // 2 + 90, WIDTH // 2, 60, (0, 128, 0), (0, 255, 0), "Level 3", 36, level3)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    game_start_screen()



