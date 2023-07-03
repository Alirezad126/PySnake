from Pygame_env import *

x = int(input("Enter X size of Game: "))
y = int(input("Enter Y size of Game: "))
cell_size = int(input("Enter cell size of Game: "))
difficulty = int(input("Enter FPS of Game: "))

snake_env = SnakeEnv(x,y,cell_size)
fps_controller = pygame.time.Clock()
check_errors = pygame.init()

pygame.display.set_caption("SNAKE GAME")

last_action = None

while True:

    
    
    # Human Input
    for event in pygame.event.get():

        snake_env.action = snake_env.human_step(event)

        if snake_env.action !=None:
            last_action = snake_env.action
             

    # Check direction and move

    snake_env.direction = snake_env.change_direction(snake_env.action, snake_env.direction)
    snake_env.snake_pos = snake_env.move(snake_env.direction, snake_env.snake_pos)

    # Check if we ate food

    snake_env.snake_body.insert(0, list(snake_env.snake_pos))
    
    if snake_env.eat():
        snake_env.score +=1
        snake_env.food_spawn = False
    else:
        #Remove the last element in the snake's body position (moving in grid)
        snake_env.snake_body.pop()


    # Check if spawn new food

    if not snake_env.food_spawn:
        snake_env.food_pos = snake_env.spawn_food()

    snake_env.food_spawn = True

    # Drawing the snake

    snake_env.game_window.fill(GRAY)
    pygame.draw.rect(snake_env.game_window, DARK_GRAY, pygame.Rect(0, 0, snake_env.frame_size_x, snake_env.cell_size))
    pygame.draw.rect(snake_env.game_window, DARK_GRAY, pygame.Rect(0, snake_env.frame_size_y - snake_env.cell_size, snake_env.frame_size_x, snake_env.cell_size))
    pygame.draw.rect(snake_env.game_window, DARK_GRAY, pygame.Rect(0, 0, snake_env.cell_size, snake_env.frame_size_y))
    pygame.draw.rect(snake_env.game_window, DARK_GRAY, pygame.Rect(snake_env.frame_size_x - snake_env.cell_size, 0, snake_env.cell_size, snake_env.frame_size_y))
    
    for x in range(snake_env.cell_size, snake_env.frame_size_x, snake_env.cell_size):
        pygame.draw.line(snake_env.game_window, WHITE, (x, 0), (x, snake_env.frame_size_y))
        
    for y in range(snake_env.cell_size, snake_env.frame_size_y, snake_env.cell_size):
        pygame.draw.line(snake_env.game_window, WHITE, (0, y), (snake_env.frame_size_x, y))
        
    for pos in snake_env.snake_body:
        if pos == snake_env.snake_body[0]:
            pygame.draw.rect(snake_env.game_window, LIGHT_GREEN, pygame.Rect(pos[0], pos[1],
                                                                             snake_env.cell_size,
                                                                               snake_env.cell_size))
        else:
            pygame.draw.rect(snake_env.game_window, DARK_GREEN, pygame.Rect(pos[0], pos[1],
                                                                              snake_env.cell_size,
                                                                                snake_env.cell_size))
            pygame.draw.rect(snake_env.game_window, GRAY, pygame.Rect(pos[0], pos[1],
                                                                       snake_env.cell_size,
                                                                         snake_env.cell_size), 1)

        

    # Drawing of food

    pygame.draw.rect(snake_env.game_window, RED, pygame.Rect(snake_env.food_pos[0],
                                                                snake_env.food_pos[1], snake_env.cell_size
                                                                , snake_env.cell_size))
    pygame.draw.rect(snake_env.game_window, GRAY, pygame.Rect(snake_env.food_pos[0],
                                                            snake_env.food_pos[1], snake_env.cell_size, snake_env.cell_size), 1)


    # Check if end game

    game_over = snake_env.game_over()
    
    if game_over:

        # Display game over message
        font = pygame.font.Font(None, 20)
        text = font.render("You lost! Play again? (Y/N)", True, (255, 255, 255))
        text_rect = text.get_rect(center=(snake_env.game_window.get_width() // 2,
                                           snake_env.game_window.get_height() // 2))
        snake_env.game_window.blit(text, text_rect)
        pygame.display.flip()

        # Wait for user input
        waiting = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        # User wants to play again
                        waiting = False
                        playing = True
                    elif event.key == pygame.K_n:
                        # User doesn't want to play again
                        playing = False
                        waiting = False
        
        if not waiting and playing:
            snake_env.reset()
        else:
            snake_env.end_game()

    # Refresh game screen

    snake_env.display_score(WHITE, "consolas", 20)

    #if event.type == pygame.KEYDOWN:
    #        last_key = event.key
    #        last_key_text = pygame.key.name(last_key)
    #        snake_env.display_action(last_key_text,WHITE, "consolas", 20)

    pygame.display.update()
    fps_controller.tick(difficulty)
    img = array3d(snake_env.game_window)
    
