import time

from liquid_crystal.i2c import I2C

# LCD Commands
# ---------------------------------------------------------------------------
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
# ---------------------------------------------------------------------------
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off and cursor control
# ---------------------------------------------------------------------------
LCD_DISPLAYON = 0x04
LCD_CURSORON = 0x02
LCD_BLINKON = 0x01

# flags for display/cursor shift
# ---------------------------------------------------------------------------
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
# ---------------------------------------------------------------------------
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# Define COMMAND and DATA LCD Rs (used by send method).
# ---------------------------------------------------------------------------
COMMAND = 0
DATA = 1
FOUR_BITS = 2

LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

# Microseconds
HOME_CLEAR_EXEC = 2000
EXEC_TIME = 37

En = 0b00000100  # Enable bit
Rw = 0b00000010  # Read/Write bit
Rs = 0b00000001  # Register select bit

cursor_row_offset = [0x0, 0x40, 0x14, 0x54]


class LiquidCrystalDriver:
    def __init__(self, i2c_path: str, i2c_address: int = 0x27):
        self.i2c_device = I2C(i2c_path, i2c_address)
        self.__write(0x03)
        self.__write(0x03)
        self.__write(0x03)
        self.__write(0x02)

        self.__write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
        self.__write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        self.__write(LCD_CLEARDISPLAY)
        self.__write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)

    def clear(self):
        self.i2c_device.write_command(LCD_CLEARDISPLAY)
        self.i2c_device.write_command(LCD_RETURNHOME)

    def __write_four_bits(self, data: int):
        self.i2c_device.write_command(data | LCD_BACKLIGHT)
        self.i2c_device.write_command(data | En | LCD_BACKLIGHT)
        time.sleep(.0005)
        self.i2c_device.write_command(((data & ~En) | LCD_BACKLIGHT))
        time.sleep(.0001)

    def __write(self, command: int, mode: int = COMMAND):
        self.__write_four_bits(mode | (command & 0xF0))
        self.__write_four_bits(mode | ((command << 4) & 0xF0))

    def set_cursor(self, row: int, col: int):
        cursor_position = LCD_SETDDRAMADDR + col + cursor_row_offset[row % len(cursor_row_offset)]
        self.__write(cursor_position)

    def display_at_position(self, display: str, row: int, col: int):
        self.set_cursor(row, col)
        for char in display:
            self.__write(ord(char), Rs)

    def display(self, display: str):
        for char in display:
            self.__write(ord(char), Rs)

    def set_blacklight(self, on: bool):
        self.i2c_device.write_command(LCD_BACKLIGHT if on else LCD_NOBACKLIGHT)

    def set_blink(self, on: bool):
        self.__write((LCD_DISPLAYCONTROL & ~LCD_DISPLAYON) | (LCD_DISPLAYON if on else 0))

    def scroll_display_right(self):
        self.__write(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)
