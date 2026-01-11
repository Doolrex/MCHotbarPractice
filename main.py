import pygame
import sys
from config import *
from classes import Hotbar

def main():
    pygame.init()
    pygame.mixer.init()
    
    initial_w = BASE_WIDTH * INITIAL_SCALE
    initial_h = BASE_HEIGHT * INITIAL_SCALE
    
    try:
        program_icon = pygame.image.load("assets/icon.png")
        pygame.display.set_icon(program_icon)
    except:
        pass
    
    screen = pygame.display.set_mode((initial_w, initial_h), pygame.RESIZABLE)
    pygame.display.set_caption("Minecraft Hotbar Trainer")
    
    aspect_ratio = BASE_WIDTH / BASE_HEIGHT
    clock = pygame.time.Clock()
    game = Hotbar()
    game.recalculate_scale(initial_w, initial_h)

    time_accumulator = 0
    
    running = True
    while running:
        dt = clock.tick(60)
        time_accumulator += dt
        
        title_text = "Hotbar Practice v1.0 | "
        if game.f3_mode:
            if game.editing_slot is not None:
                title_text += f"Editor Mode - Assigning Key to Slot {game.editing_slot + 1}..."
            else:
                title_text += "Editor Mode"
        else:
            title_text += f"Score: {game.score}"
            if game.reaction_limit_ticks >= 0:
                ticks_left = game.reaction_limit_ticks - game.slot_ticks_elapsed
                title_text += f" | Time: {ticks_left} ticks"
            
        pygame.display.set_caption(title_text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.VIDEORESIZE:
                new_w = event.w
                new_h = int(new_w / aspect_ratio)
                screen = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)
                game.recalculate_scale(new_w, new_h)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: game.handle_click(event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    game.toggle_f3()
                elif game.editing_slot is not None:
                    game.assign_new_key(event.key)
                else:
                    game.register_input_buffer(event.key)

        if game.editing_slot is None:
            while time_accumulator >= MS_PER_TICK:
                game.process_tick()
                time_accumulator -= MS_PER_TICK
        else:
            time_accumulator = 0 

        screen.fill((30, 30, 30))
        game.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()