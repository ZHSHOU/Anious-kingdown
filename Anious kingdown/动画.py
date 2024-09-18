import pygame
import random

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 100
ROWS, COLS = 6, 6
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (200, 100, 200)  # 背景颜色
SELECTED_COLOR = (255, 0, 0)  # 选中提示颜色
BUTTON_COLOR = (0, 128, 0)  # 按钮颜色
BUTTON_HOVER_COLOR = (0, 255, 0)  # 按钮悬停颜色
BUTTON_TEXT_COLOR = WHITE

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("羊了个羊小游戏")

# 加载图案图片
patterns = [pygame.image.load(f"{i}.jpg") for i in range(1, 7)]
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

def create_board():
    # 确保每张图片出现的次数为 3 的倍数
    num_patterns = len(patterns)
    tiles_needed = ROWS * COLS
    tiles_per_pattern = (tiles_needed // num_patterns) // 3 * 3  # 每种图案出现的次数为 3 的倍数

    # 创建包含每张图片所需数量的图案列表
    tiles = []
    for pattern in patterns:
        tiles.extend([pattern] * tiles_per_pattern)

    # 如果tiles的数量不足以填满游戏板，我们需要添加更多的图案（为了确保每张图片的数量是3的倍数）
    if len(tiles) < tiles_needed:
        extra_tiles_needed = tiles_needed - len(tiles)
        additional_patterns = random.choices(patterns, k=extra_tiles_needed)
        tiles.extend(additional_patterns)

    # 打乱图案列表
    random.shuffle(tiles)

    # 创建游戏板
    return [tiles[i * COLS:(i + 1) * COLS] for i in range(ROWS)]

def draw_button(x, y, width, height, color, text):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def game_start_screen():
    # 游戏开始页面
    running = True
    button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 - 30, WIDTH // 2, 60)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return

        # 绘制背景和按钮
        screen.fill(BG_COLOR)
        draw_button(button_rect.x, button_rect.y, button_rect.width, button_rect.height, BUTTON_COLOR, "开始游戏")

        # 检测鼠标悬停
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            draw_button(button_rect.x, button_rect.y, button_rect.width, button_rect.height, BUTTON_HOVER_COLOR, "开始游戏")
        
        pygame.display.flip()

def draw_board(board, selected_tiles):
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))
            # 如果瓷砖在选中列表中，用另一种颜色或样式显示
            if (row, col) in selected_tiles:
                pygame.draw.rect(screen, SELECTED_COLOR, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 5)

def check_match(board, selected, selected_tiles):
    if len(selected) == 3:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        r3, c3 = selected[2]
        
        # 确保三个选中的瓷砖不是同一个
        if (r1, c1) == (r2, c2) or (r1, c1) == (r3, c3) or (r2, c2) == (r3, c3):
            selected.clear()
            return
        
        # 如果三个瓷砖匹配，移除它们
        if board[r1][c1] == board[r2][c2] == board[r3][c3]:
            board[r1][c1] = None
            board[r2][c2] = None
            board[r3][c3] = None
            selected_tiles.discard((r1, c1))
            selected_tiles.discard((r2, c2))
            selected_tiles.discard((r3, c3))
        
        selected.clear()

# 主游戏逻辑
def main():
    game_start_screen()

    board = create_board()
    selected = []
    selected_tiles = set()  # 记录已选中的瓷砖位置

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // TILE_SIZE, y // TILE_SIZE
                
                # 只在瓷砖没有被移除的情况下添加到选中列表
                if board[row][col] is not None:
                    if (row, col) in selected_tiles:
                        # 如果已选中的瓷砖被再次点击，取消选中
                        selected.remove((row, col))
                        selected_tiles.remove((row, col))
                    else:
                        # 如果当前选中的瓷砖数量少于6张，添加到选中列表
                        if len(selected) < 6:
                            selected.append((row, col))
                            selected_tiles.add((row, col))
                        else:
                            print("已达到最大选择数量，游戏结束！")
                            running = False
                
                # 当选中三个瓷砖时检查是否匹配
                if len(selected) == 3:
                    check_match(board, selected, selected_tiles)

        screen.fill(BG_COLOR)
        draw_board(board, selected_tiles)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

