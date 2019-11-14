import time
from liquid_crystal.driver import LiquidCrystalDriver

lcd = LiquidCrystalDriver('/dev/i2c-1')

lcd.set_blacklight(on=False)
time.sleep(1)
lcd.set_blacklight(on=True)

# lcd.clear()
# lcd.display_at_position('hello', 2, 0)
# lcd.display_at_position('hello', 3, 0)
lcd.display_at_position('how are you', 0, 0)
lcd.display_at_position('how are you', 1, 0)
lcd.display_at_position('how are you', 2, 0)
lcd.display_at_position('how are you', 3, 0)
time.sleep(1)
# for _ in range(5):
#     lcd.scroll_display_right()
# lcd.set_blink(on=True)
# # mylcd.lcd_display_string_pos("255.255.255.255", 2, 0)
# mylcd.lcd_display_string_pos("hi", 1, 0)
# mylcd.backlight(1)
