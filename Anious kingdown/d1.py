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

# 加载背景动图帧
background_frames = [pygame.image.load(f"f{i}.jpg").convert() for i in range(1, 17)]  # 假设动图有16帧
background_frames = [pygame.transform.scale(frame, (WIDTH, HEIGHT)) for frame in background_frames]  # 调整大小
current_frame = 0

def draw_gradient_background(start_color, end_color):
    for i in range(HEIGHT):
        r = start_color[0] + (end_color[0] - start_color[0]) * i // HEIGHT
        g = start_color[1] + (end_color[1] - start_color[1]) * i // HEIGHT
        b = start_color[2] + (end_color[2] - start_color[2]) * i // HEIGHT
        pygame.draw.line(screen, (r, g, b), (0, i), (WIDTH, i))

# 按钮绘制及交互
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

def game_start_screen():
    global current_frame
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # 绘制背景动图
        screen.blit(background_frames[current_frame], (0, 0))
        current_frame = (current_frame + 1) % len(background_frames)  # 更新帧索引以循环播放动图

        # 绘制按钮
        draw_button(WIDTH // 4, HEIGHT // 2 - 90, WIDTH // 2, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR, "开始游戏", 36, start_game)
        draw_button(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR, "设置", 36, settings)
        draw_button(WIDTH // 4, HEIGHT // 2 + 90, WIDTH // 2, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR, "退出游戏", 36, quit_game)

        pygame.display.flip()
        clock.tick(FPS)  # 控制帧率

# 各个按钮对应的功能函数
def start_game():
    print("开始游戏")
    main()  # 进入游戏主循环

def settings():
    print("打开设置界面")
    # 设置选项界面（未来扩展）

def quit_game():
    pygame.quit()
    exit()

# 游戏主逻辑 (和之前相同)
def main():
    board = create_board()
    selected = []
    selected_tiles = set()
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
                if board[row][col] is not None:
                    if (row, col) in selected_tiles:
                        selected.remove((row, col))
                        selected_tiles.remove((row, col))
                    else:
                        if len(selected) < 6:
                            selected.append((row, col))
                            selected_tiles.add((row, col))
                        else:
                            print("已达到最大选择数量，游戏结束！")
                            running = False

                if len(selected) == 3:
                    check_match(board, selected, selected_tiles)

        screen.fill(BG_COLOR)
        draw_board(board, selected_tiles)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    game_start_screen()

