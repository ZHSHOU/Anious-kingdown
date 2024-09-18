import pygame
from title import start_game, settings, quit_game, background_frames, WIDTH, HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, FPS, clock
from utils import draw_button

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

# 屏幕尺寸
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# 游戏主逻辑
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

          # 当选中三个瓷砖时检查是否匹配
                if len(selected) == 3:
                    check_match(board, selected, selected_tiles)

        screen.fill(BG_COLOR)
        draw_board(board, selected_tiles)
        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    game_start_screen()
