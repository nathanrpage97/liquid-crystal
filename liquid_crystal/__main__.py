from liquid_crystal.i2c import I2C

i2c = I2C('/dev/i2c-1')

i2c.read(0)
