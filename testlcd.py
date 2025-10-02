import utime
import gc9a01
import tft_config
import vga1_bold_16x32 as font

BLACK = 0x0000
WHITE = 0xFFFF

print("go")

tft = tft_config.config()
tft.init()
tft.fill(BLACK)
utime.sleep(1)

tft.text(font, "Hello", 40, 104, WHITE)
print("done")