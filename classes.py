import pygame
import random
import json
import os
from config import *

class Hotbar:
    def __init__(self):
        raw_hotbar_temp = pygame.image.load(PATH_HOTBAR).convert_alpha()
        raw_selector_temp = pygame.image.load(PATH_SELECTOR).convert_alpha()
        self.raw_item = pygame.image.load(PATH_ITEM).convert_alpha()

        try:
            self.sound_success = pygame.mixer.Sound(PATH_SOUND_SUCCESS)
            self.sound_error = pygame.mixer.Sound(PATH_SOUND_ERROR)
            self.sound_success.set_volume(0.5)
            self.sound_error.set_volume(0.5)
        except Exception:
            self.sound_success = None
            self.sound_error = None

        self.raw_hotbar = self._reduce_base(raw_hotbar_temp)
        self.raw_selector = self._reduce_base(raw_selector_temp)
        
        self.assigned_keys = []
        self.reaction_limit_ticks = DEFAULT_LIMIT_TICKS
        self.load_config()
        
        self.f3_mode = False
        self.editing_slot = None
        self.active_slot = random.randint(0, 8)
        self.selected_slot = 0
        self.score = 0
        
        self.input_buffer = set()
        self.slot_ticks_elapsed = 0
        
        self.img_hotbar = None
        self.img_selector = None
        self.img_item = None
        self.base_x = 0
        self.base_y = 0
        self.current_scale = 1
        self.key_font = None

    def load_config(self):
        self.assigned_keys = list(DEFAULT_KEYS)
        self.reaction_limit_ticks = DEFAULT_LIMIT_TICKS

        if not os.path.exists(CONFIG_FILE):
            self.save_config()
            return

        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                ticks_val = data.get("reaction_limit_ticks")
                if ticks_val is not None:
                    self.reaction_limit_ticks = int(ticks_val)

                keys_dict = data.get("keys_mapping", {})
                if keys_dict:
                    new_keys = []
                    for i in range(1, 10):
                        key_name = keys_dict.get(f"slot_{i}", str(i))
                        key_code = pygame.key.key_code(key_name)
                        new_keys.append(key_code)
                    self.assigned_keys = new_keys
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")

    def save_config(self):
        keys_mapping = {}
        for i, code in enumerate(self.assigned_keys):
            keys_mapping[f"slot_{i+1}"] = pygame.key.name(code)

        data = {
            "_comment_info": "Configuration file for Minecraft Hotbar Trainer",
            "_comment_assets": "You can replace files in the 'assets' folder with custom ones, provided you keep the original filenames.",
            "_comment_ticks": "reaction_limit_ticks controls the reaction window in ticks (20 ticks = 1 sec). Set to -1 for infinite time.",
            "reaction_limit_ticks": self.reaction_limit_ticks,
            "_comment_keys": "Key assignments for each slot.",
            "keys_mapping": keys_mapping
        }

        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e: pass

    def _reduce_base(self, img):
        return pygame.transform.scale(img, (int(img.get_width() * 0.5), int(img.get_height() * 0.5)))

    def recalculate_scale(self, win_w, win_h):
        self.current_scale = max(0.5, win_w / BASE_WIDTH)
        self.img_hotbar = self._scale_img(self.raw_hotbar)
        self.img_selector = self._scale_img(self.raw_selector)
        self.img_item = self._scale_img(self.raw_item)
        
        self.base_x = (win_w - self.img_hotbar.get_width()) // 2
        self.base_y = (win_h - self.img_hotbar.get_height()) // 2
        
        font_size = int(8 * self.current_scale)
        try:
            self.key_font = pygame.font.Font(PATH_FONT, font_size)
        except:
            self.key_font = pygame.font.SysFont("Arial", font_size, bold=True)

    def _scale_img(self, img):
        nw = int(img.get_width() * self.current_scale)
        nh = int(img.get_height() * self.current_scale)
        return pygame.transform.scale(img, (nw, nh))

    def handle_click(self, mouse_pos):
        if not self.f3_mode: return False
        
        mx, my = mouse_pos
        if not (self.base_y <= my <= self.base_y + self.img_hotbar.get_height()):
            self.editing_slot = None
            return False
        
        if mx < self.base_x: return False
        
        real_slot_width = 20 * self.current_scale
        idx = int((mx - self.base_x) / real_slot_width)

        if 0 <= idx <= 8:
            self.editing_slot = idx
            return True
        return False

    def assign_new_key(self, key_code):
        if self.editing_slot is not None:
            self.assigned_keys[self.editing_slot] = key_code
            self.save_config()
            self.editing_slot = None
            return True
        return False
    
    def toggle_f3(self):
        self.f3_mode = not self.f3_mode
        if not self.f3_mode: self.editing_slot = None

    def get_slot_from_key(self, key_code):
        try: return self.assigned_keys.index(key_code)
        except: return None
        
    def register_input_buffer(self, key_code):
        slot = self.get_slot_from_key(key_code)
        if slot is not None: self.input_buffer.add(slot)
        
    def play_sound(self, type_str):
        if type_str == 'success' and self.sound_success: self.sound_success.play()
        elif type_str == 'error' and self.sound_error: self.sound_error.play()
        
    def move_selector(self, idx):
        self.selected_slot = idx
        
    def change_slot(self):
        candidates = list(range(9))
        if self.active_slot in candidates: candidates.remove(self.active_slot)
        if self.selected_slot in candidates: candidates.remove(self.selected_slot)
        self.active_slot = random.choice(candidates)

    def process_tick(self):
        self.slot_ticks_elapsed += 1
        
        winner_slot = max(self.input_buffer) if self.input_buffer else None
        
        self.input_buffer.clear() 
        
        if winner_slot is not None:
            self.move_selector(winner_slot)
            if winner_slot == self.active_slot:
                self.score += 1
                self.play_sound('success')
                self.change_slot()
                self.slot_ticks_elapsed = 0
            else:
                self.score -= 1

        if self.reaction_limit_ticks >= 0:
            if self.slot_ticks_elapsed >= self.reaction_limit_ticks:
                self.change_slot()
                self.score -= 1
                self.play_sound('error')
                self.slot_ticks_elapsed = 0

    def draw(self, screen):
        # Hotbar
        screen.blit(self.img_hotbar, (self.base_x, self.base_y))
        
        real_slot_width = 20 * self.current_scale
        
        # F3 TEXT
        if self.f3_mode:
            for i in range(9):
                x = self.base_x + (i * real_slot_width)
                y = self.base_y + (1.25 * self.current_scale)
                
                text_str = ""
                color = COLOR_TEXT
                
                if i == self.editing_slot:
                    text_str = "?"
                    color = COLOR_EDITING
                else:
                    key_name = pygame.key.name(self.assigned_keys[i])
                    text_str = key_name[:3].upper() if len(key_name) > 2 else key_name.upper()
                
                txt_surf = self.key_font.render(text_str, False, color)
                shadow_surf = self.key_font.render(text_str, False, COLOR_SHADOW)
                
                txt_surf.set_alpha(128)
                shadow_surf.set_alpha(128)
                
                pos_txt_x = x + (4 * self.current_scale)
                pos_txt_y = y + (2 * self.current_scale)
                offset = max(1, 1 * self.current_scale * 0.5)
                
                screen.blit(shadow_surf, (pos_txt_x + offset, pos_txt_y + offset))
                screen.blit(txt_surf, (pos_txt_x, pos_txt_y))

        # ITEM
        item_x = self.base_x + (self.active_slot * real_slot_width)
        center_off_x = (real_slot_width - self.img_item.get_width()) / 2
        center_off_y = (self.img_hotbar.get_height() - self.img_item.get_height()) / 2
        
        item_correction_x = 1.0 * self.current_scale 
        
        final_item_x = int(item_x + center_off_x + item_correction_x)
        final_item_y = int(self.base_y + center_off_y)
        screen.blit(self.img_item, (final_item_x, final_item_y))

        # SELECTOR
        sel_x = self.base_x + (self.selected_slot * real_slot_width)
        center_sel_x = (real_slot_width - self.img_selector.get_width()) / 2
        center_sel_y = (self.img_hotbar.get_height() - self.img_selector.get_height()) / 2
        
        sel_adjust_x = 1.0 * self.current_scale
        
        final_sel_x = int(sel_x + center_sel_x + sel_adjust_x)
        final_sel_y = int(self.base_y + center_sel_y)
        screen.blit(self.img_selector, (final_sel_x, final_sel_y))