from micropython import const
from time import sleep_ms
import framebuf

# Display resolution
EPD_WIDTH = const(128)
EPD_HEIGHT = const(250)

# Some command OP-Codes
WRITE_RAM = b'\x24'
DISPLAY_UPDATE_CONTROL_1 = b'\x21'
DISPLAY_UPDATE_CONTROL_2 = b'\x22'


class EPD(framebuf.FrameBuffer):
    def __init__(self, spi, cs, dc, rst, busy):
        self.spi = spi
        self.spi.init()
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN, value=0)

        size = EPD_WIDTH * EPD_HEIGHT // 8
        self.buffer = memoryview(bytearray(size))
        super().__init__(self.buffer, EPD_WIDTH, EPD_HEIGHT, framebuf.MONO_HLSB)
        self.hard_reset()

    def _command(self, command, data=None):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(command)
        self.cs(1)
        if data is not None:
            self._data(data)

    def _data(self, data):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def _wait_until_idle(self):
        while self.busy.value() == 1:
            sleep_ms(10)

    def hard_reset(self):
        self.rst(1)
        sleep_ms(1)
        self.rst(0)
        sleep_ms(10)
        self.rst(1)
      
            
    def update(self):

#  this->command(0x12);
#  this->wait_until_idle_();
        self._command(b'\x12')
        self._wait_until_idle()
        
#  this->command(0x11);
#  this->data(0x03);
        self._command(b'\x11', b'\x03')

#  this->command(0x44);
#  this->data(1);
#  this->data(this->get_width_internal() / 8);
        self._command(b'\x44', b'\x01\x10')

#  this->command(0x45);
#  this->data(0);
#  this->data(0);
#  this->data(this->get_height_internal());
#  this->data(0);
        self._command(b'\x45', b'\x00\x00\xf9\x00'
                      )
#  this->command(0x4e);
#  this->data(1);
        self._command(b'\x4e', b'\x01')

#  this->command(0x4f);
#  this->data(0);
#  this->data(0);
        self._command(b'\x4f', b'\x00\x00')
        
#    // send data
#    this->command(0x24);
#    this->start_data_();
#    this->write_array(this->buffer_, this->get_buffer_length_());
#    this->end_data_();        
        self._command(WRITE_RAM, self.buffer)

#    // commit
#    this->command(0x20);
#    this->wait_until_idle_();
        self._command(b'\x20')
        self._wait_until_idle()
