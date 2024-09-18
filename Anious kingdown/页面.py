import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("压了个牙")

# 加载图片
image = pygame.image.load('end.jpg')  # 替换为你的图片路径
image = pygame.transform.scale(image, (WIDTH, HEIGHT))  # 调整图片大小以适应屏幕

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 绘制图片
    screen.blit(image, (0, 0))

    # 更新显示
    pygame.display.flip()

