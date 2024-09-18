import pygame
import game

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 100
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

# 加载背景动图帧
background_frames = [pygame.image.load(f"f{i}.jpg").convert() for i in range(1, 17)]  # 假设动图有16帧
background_frames = [pygame.transform.scale(frame, (WIDTH, HEIGHT)) for frame in background_frames]  # 调整大小
current_frame = 0

# 绘制渐变背景函数
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

    try:
        font = pygame.font.Font('msyh.ttf', font_size)
    except FileNotFoundError:
        font = pygame.font.Font(None, font_size)

    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# 开始游戏界面
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
        draw_button(WIDTH // 4, HEIGHT // 2 - 90, WIDTH // 2, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR, "game begin", 36, lambda: start_game(1))
        draw_button(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR, "setting", 36, settings)
        draw_button(WIDTH // 4, HEIGHT // 2 + 90, WIDTH // 2, 60, BUTTON_COLOR, BUTTON_HOVER_COLOR, "quit", 36, quit_game)

        pygame.display.flip()
        clock.tick(FPS)  # 控制帧率

# 各个按钮对应的功能函数
def start_game(level):
    pygame.quit()
    import game
    game.main(level)  # 调用 game.py 的 main 函数并传递关卡参数

def settings():
    pygame.quit()
    import game
    game.level_selection()  # 调用 game.py 的 level_selection 函数

def quit_game():
    pygame.quit()
    exit()

if __name__ == "__main__":
    game_start_screen()


