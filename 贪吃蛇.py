import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 颜色定义
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# 修改游戏设置部分
# 将固定窗口大小替换屏幕信息获取
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20  # 固定方块大小
GAME_SPEED = 5

# 修改创建游戏窗口部分，移除全屏模式
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇游戏')
clock = pygame.time.Clock()

# 修改字体加载部分，使其更稳定
def init_fonts():
    """初始化字体"""
    try:
        # 使用固定字体大小
        large_font_size = 48
        normal_font_size = 24
        
        font_path = "C:/Windows/Fonts/simhei.ttf"
        return pygame.font.Font(font_path, large_font_size), pygame.font.Font(font_path, normal_font_size)
    except Exception as e:
        print(f"加载中文字体失败: {e}")
        print("使用系统默认字体")
        return pygame.font.Font(None, large_font_size), pygame.font.Font(None, normal_font_size)

# 初始化字体
font_big, font_normal = init_fonts()

# 添加难度设置
DIFFICULTY_SETTINGS = {
    '简单': {'speed': 5, 'color': GREEN},
    '中等': {'speed': 8, 'color': YELLOW},
    '困难': {'speed': 12, 'color': RED}
}

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.direction = 'RIGHT'
        self.body = [(self.x, self.y)]
        self.length = 1
        self.score = 0
    
    def move(self):
        # 根据方向移动蛇头
        if self.direction == 'UP':
            self.y -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            self.y += BLOCK_SIZE
        elif self.direction == 'LEFT':
            self.x -= BLOCK_SIZE
        elif self.direction == 'RIGHT':
            self.x += BLOCK_SIZE
        
        # 穿墙（考虑BLOCK_SIZE以确保完全穿墙）
        self.x = (self.x + WINDOW_WIDTH) % WINDOW_WIDTH
        self.y = (self.y + WINDOW_HEIGHT) % WINDOW_HEIGHT
        
        # 更新蛇身
        self.body.insert(0, (self.x, self.y))
        if len(self.body) > self.length:
            self.body.pop()
    
    def check_collision(self):
        # 检查是否撞到自己
        return (self.x, self.y) in self.body[1:]
    
    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE-2, BLOCK_SIZE-2))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()
    
    def spawn(self):
        max_x = (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE
        max_y = (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE
        self.position = (
            random.randrange(0, max_x) * BLOCK_SIZE,
            random.randrange(0, max_y) * BLOCK_SIZE
        )
    
    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], BLOCK_SIZE-2, BLOCK_SIZE-2))

def draw_button(text, color, y_pos, hover=False):
    """绘制一个按钮"""
    font = font_normal
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, y_pos))
    
    # 使用固定按钮大小
    button_width = 200
    button_height = 40
    
    button_rect = pygame.Rect(
        WINDOW_WIDTH//2 - button_width//2,
        y_pos - button_height//2,
        button_width,
        button_height
    )
    
    if hover:
        pygame.draw.rect(screen, color, button_rect, border_radius=10)
        text_surface = font.render(text, True, BLACK)
    else:
        pygame.draw.rect(screen, color, button_rect, 2, border_radius=10)
    
    screen.blit(text_surface, text_rect)
    return button_rect

def show_start_screen():
    # 创建渐变背景
    for i in range(WINDOW_HEIGHT):
        color = (0, int(50 * (1 - i/WINDOW_HEIGHT)), int(100 * (1 - i/WINDOW_HEIGHT)))
        pygame.draw.line(screen, color, (0, i), (WINDOW_WIDTH, i))
    
    # 绘制标题
    title = font_big.render('贪吃蛇游戏', True, GREEN)
    title_shadow = font_big.render('贪吃蛇游戏', True, BLACK)
    title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4))
    
    # 添加标题阴影效果
    screen.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
    screen.blit(title, title_rect)
    
    # 添加装饰线
    pygame.draw.line(screen, GREEN, 
                    (WINDOW_WIDTH//4, WINDOW_HEIGHT//3),
                    (WINDOW_WIDTH*3//4, WINDOW_HEIGHT//3), 3)
    
    # 显示游戏说明
    instructions = [
        "游戏说明:",
        "使用方向键控制蛇的移动",
        "吃到食物可以增加长度和分数",
        "撞到自己会导致游戏结束"
    ]
    
    for i, text in enumerate(instructions):
        inst_text = font_normal.render(text, True, WHITE)
        screen.blit(inst_text, (WINDOW_WIDTH//4, WINDOW_HEIGHT//2 + i*30))
    
    # 初始化按钮矩形
    start_rect = draw_button("开始游戏 (空格)", GREEN, WINDOW_HEIGHT*3//4, False)
    quit_rect = draw_button("退出游戏 (Q)", RED, WINDOW_HEIGHT*3//4 + 60, False)
    
    # 添加版本信息
    version_text = font_normal.render("v1.0", True, WHITE)
    screen.blit(version_text, (WINDOW_WIDTH - 60, WINDOW_HEIGHT - 30))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    waiting = False
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        # 更新按钮悬停效果
        mouse_pos = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse_pos) or quit_rect.collidepoint(mouse_pos):
            # 重新绘制开始界面
            screen.fill(BLACK)
            # 重新创建渐变背景
            for i in range(WINDOW_HEIGHT):
                color = (0, int(50 * (1 - i/WINDOW_HEIGHT)), int(100 * (1 - i/WINDOW_HEIGHT)))
                pygame.draw.line(screen, color, (0, i), (WINDOW_WIDTH, i))
            
            # 重新绘制所有元素
            screen.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
            screen.blit(title, title_rect)
            
            pygame.draw.line(screen, GREEN, 
                        (WINDOW_WIDTH//4, WINDOW_HEIGHT//3),
                        (WINDOW_WIDTH*3//4, WINDOW_HEIGHT//3), 3)
            
            for i, text in enumerate(instructions):
                inst_text = font_normal.render(text, True, WHITE)
                screen.blit(inst_text, (WINDOW_WIDTH//4, WINDOW_HEIGHT//2 + i*30))
            
            # 更新按钮状态
            start_rect = draw_button("开始游戏 (空格)", GREEN, 
                                WINDOW_HEIGHT*3//4,
                                start_rect.collidepoint(mouse_pos))
            
            quit_rect = draw_button("退出游戏 (Q)", RED,
                               WINDOW_HEIGHT*3//4 + 60,
                               quit_rect.collidepoint(mouse_pos))
            
            screen.blit(version_text, (WINDOW_WIDTH - 60, WINDOW_HEIGHT - 30))
            pygame.display.flip()

def show_score(score):
    score_text = font_normal.render(f'得分: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

def show_game_over(score):
    game_over = font_big.render('游戏结束!', True, RED)
    score_text = font_normal.render(f'最终得分: {score}', True, YELLOW)
    restart_text = font_normal.render('按R键重新开始', True, WHITE)
    quit_text = font_normal.render('按Q键退出游戏', True, WHITE)
    
    # 计算文本位置使其居中显示
    game_over_rect = game_over.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
    quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100))
    
    # 绘制半透明背景
    s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    s.set_alpha(128)
    s.fill(BLACK)
    screen.blit(s, (0,0))
    
    # 绘制文本
    screen.blit(game_over, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(quit_text, quit_rect)

def show_settings_screen():
    """显示游戏设置界面"""
    screen.fill(BLACK)
    
    # 绘制标题
    title = font_big.render('游戏设置', True, WHITE)
    title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//6))
    screen.blit(title, title_rect)
    
    # 添加装饰线
    pygame.draw.line(screen, WHITE, 
                    (WINDOW_WIDTH//4, WINDOW_HEIGHT//4),
                    (WINDOW_WIDTH*3//4, WINDOW_HEIGHT//4), 2)
    
    button_rects = {}
    settings_options = {
        '难度设置': {
            '简单': {'color': GREEN, 'desc': '速度: 5'},
            '中等': {'color': YELLOW, 'desc': '速度: 8'},
            '困难': {'color': RED, 'desc': '速度: 12'}
        },
        '返回': {'color': WHITE, 'desc': '返回主菜单'}
    }
    
    y_pos = WINDOW_HEIGHT//3
    
    # 绘制所有设置选项
    for option, details in settings_options.items():
        if option == '难度设置':
            # 显示难度设置标题
            text = font_normal.render('难度设置:', True, WHITE)
            screen.blit(text, (WINDOW_WIDTH//4, y_pos))
            y_pos += 50
            
            # 显示难度选项
            for difficulty, diff_details in details.items():
                button_rects[difficulty] = draw_button(
                    f"{difficulty} ({diff_details['desc']})",
                    diff_details['color'], y_pos, False
                )
                y_pos += 60
        else:
            # 绘制返回按钮
            y_pos += 30
            button_rects[option] = draw_button(
                option,
                details['color'], y_pos, False
            )
    
    pygame.display.flip()
    
    # 等待用户选择
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for option, rect in button_rects.items():
                    if rect.collidepoint(event.pos):
                        if option in ['简单', '中等', '困难']:
                            return option  # 返回选择的难度
                        elif option == '返回':
                            return None  # 返回主菜单
            
            # 更新按钮悬停效果
            mouse_pos = pygame.mouse.get_pos()
            hover_update = False
            for option, rect in button_rects.items():
                if rect.collidepoint(mouse_pos):
                    if option in ['简单', '中等', '困难']:
                        color = settings_options['难度设置'][option]['color']
                        desc = settings_options['难度设置'][option]['desc']
                        draw_button(f"{option} ({desc})", color, rect.centery, True)
                    else:
                        draw_button(option, settings_options[option]['color'], rect.centery, True)
                    hover_update = True
                else:
                    if option in ['简单', '中等', '困难']:
                        color = settings_options['难度设置'][option]['color']
                        desc = settings_options['难度设置'][option]['desc']
                        draw_button(f"{option} ({desc})", color, rect.centery, False)
                    else:
                        draw_button(option, settings_options[option]['color'], rect.centery, False)
            
            if hover_update:
                pygame.display.flip()

def main():
    difficulty = '简单'
    game_speed = DIFFICULTY_SETTINGS[difficulty]['speed']
    
    running = True
    while running:
        show_start_screen()
        
        while running:
            snake = Snake()
            food = Food()
            game_over = False
            
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    if event.type == pygame.KEYDOWN:
                        if game_over:
                            if event.key == pygame.K_r:
                                snake = Snake()
                                food = Food()
                                game_over = False
                                break
                            elif event.key == pygame.K_q:
                                running = False
                                break
                        else:
                            if event.key == pygame.K_UP and snake.direction != 'DOWN':
                                snake.direction = 'UP'
                            elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                                snake.direction = 'DOWN'
                            elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                                snake.direction = 'LEFT'
                            elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                                snake.direction = 'RIGHT'
                
                if not game_over:
                    snake.move()
                    
                    if snake.x == food.position[0] and snake.y == food.position[1]:
                        snake.length += 1
                        snake.score += 1
                        food.spawn()
                    
                    if snake.check_collision():
                        game_over = True
                    
                    screen.fill(BLACK)
                    snake.draw()
                    food.draw()
                    score_text = font_normal.render(f'难度: {difficulty} | 得分: {snake.score}', True, WHITE)
                    screen.blit(score_text, (10, 10))
                
                if game_over:
                    show_game_over(snake.score)
                
                pygame.display.flip()
                clock.tick(game_speed)
                
                if not running:
                    break
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        pygame.quit()
        sys.exit() 