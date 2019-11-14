import struct
from fcntl import ioctl

# Linux command constant to specify setting the slave
I2C_SLAVE = 0x0703


class I2C:

    def __init__(self, i2c_path: str, i2c_address: int = 0x27):
        self.__path = i2c_path
        self.__device = open(i2c_path, 'r+b', buffering=0)
        ioctl(self.__device.fileno(), I2C_SLAVE, i2c_address & 0x7F)

    def write_command_arg(self, command: int, arg: int):
        self.__device.write(struct.pack('>HH', command, arg))

    def write_command(self, command: int):
        self.__device.write(struct.pack('>H', command))

    def read(self) -> int:
        (value,) = struct.unpack('>H', self.__device.read(1))
        return value

    def read_data(self, command: int) -> int:
        self.__device.write(struct.pack('>H', command))
        (value,) = struct.unpack('>H', self.__device.read(1))
        return value
