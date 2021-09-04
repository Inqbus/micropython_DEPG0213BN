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

# Rotaion
ROTATION_0 = const(0)
ROTATION_90 = const(1)
ROTATION_180 = const(2)
ROTATION_270 = const(3)


LUT_SIZE_TTGO_DKE_PART = 153

PART_UPDATE_LUT_TTGO_DKE = bytearray([
    0x0, 0x40, 0x0, 0x0, 0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x80, 0x80, 0x0, 0x0, 0x0, 0x0,  0x0, 0x0,
    0x0, 0x0,  0x0, 0x0, 0x40, 0x40, 0x0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x0,  0x0,  0x0, 0x0, 0x0, 0x80, 0x0, 0x0,
    0x0, 0x0,  0x0, 0x0, 0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x0,  0x0,  0x0, 0x0, 0x0, 0x0,  0x0, 0x0,
    0xF, 0x0,  0x0, 0x0, 0x0,  0x0,  0x0,  0x1,  0x0,  0x0,  0x0, 0x0, 0x0,  0x0,  0x0, 0x0, 0x0, 0x0,  0x0, 0x0,
    0x0, 0x0,  0x0, 0x0, 0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x0,  0x0,  0x0, 0x0, 0x0, 0x0,  0x0, 0x0,
    0x0, 0x0,  0x0, 0x0, 0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x0,  0x0,  0x0, 0x0, 0x0, 0x0,  0x0, 0x0,
    0x0, 0x0,  0x1, 0x0, 0x0,  0x0,  0x0,  0x0,  0x0,  0x1,  0x0, 0x0, 0x0,  0x0,  0x0, 0x0, 0x0, 0x0,  0x0, 0x0,
    0x0, 0x0,  0x0, 0x0, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x0, 0x0, 0x0
    ])
                                     

class EPD(framebuf.FrameBuffer):
    def __init__(self, spi, cs, dc, rst, busy, rotation=ROTATION_0):
        self.init_spi(spi, cs, dc, rst, busy)
        self.init_buffer(rotation)

    def init_buffer(self, rotation):
        self._rotation = rotation
        size = EPD_WIDTH * EPD_HEIGHT // 8
        self.buffer = bytearray(size)

        if self._rotation == ROTATION_0 or self._rotation == ROTATION_180:
            self.width = EPD_WIDTH
            self.height = EPD_HEIGHT
        else:
            self.width = EPD_HEIGHT
            self.height = EPD_WIDTH       
        
        print('width:{}, height:{}'.format(self.width, self.height))
        
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HLSB)
        self.hard_reset()

    def init_spi(self, spi, cs, dc, rst, busy):
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
      
      
# void GxDEPG0213BN::_SetRamArea(uint8_t Xstart, uint8_t Xend, uint8_t Ystart, uint8_t Ystart1, uint8_t Yend, uint8_t Yend1)
# {
#     _writeCommand(0x44);
#     _writeData(Xstart + 1);
#     _writeData(Xend + 1);
#     _writeCommand(0x45);
#     _writeData(Ystart);
#     _writeData(Ystart1);
#     _writeData(Yend);
#     _writeData(Yend1);
# }
# 
# void GxDEPG0213BN::_SetRamPointer(uint8_t addrX, uint8_t addrY, uint8_t addrY1)
# {
#     _writeCommand(0x4e);
#     _writeData(addrX + 1);
#     _writeCommand(0x4f);
#     _writeData(addrY);
#     _writeData(addrY1);
# }
   
# void GxDEPG0213BN::_writeToWindow(uint16_t xs, uint16_t ys, uint16_t xd, uint16_t yd, uint16_t w, uint16_t h)
# {
#     //Serial.printf("_writeToWindow(%d, %d, %d, %d, %d, %d)\n", xs, ys, xd, yd, w, h);
#     // the screen limits are the hard limits
#     if (xs >= GxDEPG0213BN_WIDTH) return;
#     if (ys >= GxDEPG0213BN_HEIGHT) return;
#     if (xd >= GxDEPG0213BN_WIDTH) return;
#     if (yd >= GxDEPG0213BN_HEIGHT) return;
#     w = gx_uint16_min(w, GxDEPG0213BN_WIDTH - xs);
#     w = gx_uint16_min(w, GxDEPG0213BN_WIDTH - xd);
#     h = gx_uint16_min(h, GxDEPG0213BN_HEIGHT - ys);
#     h = gx_uint16_min(h, GxDEPG0213BN_HEIGHT - yd);
#     uint16_t xds_d8 = xd / 8;
#     uint16_t xde_d8 = (xd + w - 1) / 8;
#     uint16_t yde = yd + h - 1;
#     // soft limits, must send as many bytes as set by _SetRamArea
#     uint16_t xse_d8 = xs / 8 + xde_d8 - xds_d8;
#     uint16_t yse = ys + h - 1;
#     _SetRamArea(xds_d8, xde_d8, yd % 256, yd / 256, yde % 256, yde / 256); // X-source area,Y-gate area
#     _SetRamPointer(xds_d8, yd % 256, yd / 256); // set ram
#     _waitWhileBusy(0, 100); // needed ?
#     _writeCommand(0x24);
#     for (int16_t y1 = ys; y1 <= yse; y1++) {
#         for (int16_t x1 = xs / 8; x1 <= xse_d8; x1++) {
#             uint16_t idx = y1 * (GxDEPG0213BN_WIDTH / 8) + x1;
#             uint8_t data = (idx < sizeof(_buffer)) ? _buffer[idx] : 0x00;
#             _writeData(~data);
#         }
#     }
# }
# 
# void GxDEPG0213BN::updateToWindow(uint16_t xs, uint16_t ys, uint16_t xd, uint16_t yd, uint16_t w, uint16_t h, bool using_rotation)
# {
#     if (using_rotation) {
#         switch (getRotation()) {
#         case 1:
#             swap(xs, ys);
#             swap(xd, yd);
#             swap(w, h);
#             xs = GxDEPG0213BN_WIDTH - xs - w - 1;
#             xd = GxDEPG0213BN_WIDTH - xd - w - 1;
#             break;
#         case 2:
#             xs = GxDEPG0213BN_WIDTH - xs - w - 1;
#             ys = GxDEPG0213BN_HEIGHT - ys - h - 1;
#             xd = GxDEPG0213BN_WIDTH - xd - w - 1;
#             yd = GxDEPG0213BN_HEIGHT - yd - h - 1;
#             break;
#         case 3:
#             swap(xs, ys);
#             swap(xd, yd);
#             swap(w, h);
#             ys = GxDEPG0213BN_HEIGHT - ys  - h - 1;
#             yd = GxDEPG0213BN_HEIGHT - yd  - h - 1;
#             break;
#         }
#     }
#     _Init_Part(0x03);
#     _writeToWindow(xs, ys, xd, yd, w, h);
#     _Update_Part();
#     delay(GxDEPG0213BN_PU_DELAY);
#     // update erase buffer
#     _writeToWindow(xs, ys, xd, yd, w, h);
#     delay(GxDEPG0213BN_PU_DELAY);
# }
#    
# 
#     def update_window(xs, ys, xd, yd, w, h)
# 
#         if self._rotation != ROTATION_0
#             return
#         switch (getRotation()) {
#         case 1:
#             swap(xs, ys);
#             swap(xd, yd);
#             swap(w, h);
#             xs = GxDEPG0213BN_WIDTH - xs - w - 1;
#             xd = GxDEPG0213BN_WIDTH - xd - w - 1;
#             break;
#         case 2:
#             xs = GxDEPG0213BN_WIDTH - xs - w - 1;
#             ys = GxDEPG0213BN_HEIGHT - ys - h - 1;
#             xd = GxDEPG0213BN_WIDTH - xd - w - 1;
#             yd = GxDEPG0213BN_HEIGHT - yd - h - 1;
#             break;
#         case 3:
#             swap(xs, ys);
#             swap(xd, yd);
#             swap(w, h);
#             ys = GxDEPG0213BN_HEIGHT - ys  - h - 1;
#             yd = GxDEPG0213BN_HEIGHT - yd  - h - 1;
#             break;
#         _Init_Part(0x03);
#         _writeToWindow(xs, ys, xd, yd, w, h);
#         _Update_Part();
#         delay(GxDEPG0213BN_PU_DELAY);
#         // update erase buffer
#         _writeToWindow(xs, ys, xd, yd, w, h);
#         delay(GxDEPG0213BN_PU_DELAY);



    def update_comon(self):

#  this->command(0x12);
#  this->wait_until_idle_();
        self._command(b'\x12')
        self._wait_until_idle()
        
#  this->command(0x11);
#  this->data(0x03);
        # Set RAM entry mode 3 (x increase, y increase : normal mode)
        self._command(b'\x11', b'\x03')

#  this->command(0x44);
#  this->data(1);
#  this->data(this->get_width_internal() / 8);
#        self._command(b'\x44', b'\x01\x10')
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
        
    def update(self):        
        self.update_comon()
        
#    // send data
#    this->command(0x24);
#    this->start_data_();
#    this->write_array(this->buffer_, this->get_buffer_length_());
#    this->end_data_();        
        self._command(WRITE_RAM, self._get_rotated_buffer())

#    // commit
#    this->command(0x20);
#    this->wait_until_idle_();
        self._command(b'\x20')
        self._wait_until_idle()

    def update_partial(self):        
        self.update_comon()
        
#https://github.com/lewisxhe/GxEPD/blob/master/src/GxDEPG0213BN/GxDEPG0213BN.cpp
        
        
#     // set up partial update
#    this->command(0x32);
#    for (uint8_t v : PART_UPDATE_LUT_TTGO_DKE)
#      this->data(v);
        self._command(b'\x32', PART_UPDATE_LUT_TTGO_DKE)

#    this->command(0x3F);
#    this->data(0x22);
        self._command(b'\x3F', b'\x22')

#    this->command(0x03);
#    this->data(0x17);
        self._command(b'\x03', b'\x17')

#    this->command(0x04);
#    this->data(0x41);
#    this->data(0x00);
#    this->data(0x32);
        self._command(b'\x04', b'\x41\x00\x32')


#    this->command(0x2C);
#    this->data(0x32);
        self._command(b'\x2C', b'\x32')

#    this->command(0x37);
#    this->data(0x00);
#    this->data(0x00);
#    this->data(0x00);
#    this->data(0x00);
#    this->data(0x00);
#    this->data(0x40);
#    this->data(0x00);
#    this->data(0x00);
#    this->data(0x00);
#    this->data(0x00);
        self._command(b'\x37', b'\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00')

#    this->command(0x3C);
#    this->data(0x80);
        self._command(b'\x3C', b'\x80')

#    this->command(0x22);
#    this->data(0xC0);
        self._command(b'\x22', b'\xC0')

#    this->command(0x20);
#    this->wait_until_idle_();

        self._command(b'\x20')
        self._wait_until_idle()

#        return
    
#    // send data
#    this->command(0x24);
#    this->start_data_();
#    this->write_array(this->buffer_, this->get_buffer_length_());
#    this->end_data_();

        self._command(WRITE_RAM, self._get_rotated_buffer())

#    // commit as partial
#    this->command(0x22);
#    this->data(0xCF);
        self._command(b'\x22', b'\xCF')


#    this->command(0x20);
#    this->wait_until_idle_();
        self._command(b'\x20')
        self._wait_until_idle()

#    // data must be sent again on partial update
#    delay(300);  // NOLINT
#    this->command(0x24);
#    this->start_data_();
#    this->write_array(this->buffer_, this->get_buffer_length_());
#    this->end_data_();
#    delay(300);  // NOLINT

        self._command(b'\x24')
        sleep_ms(300)
        self._command(WRITE_RAM, self._get_rotated_buffer())
        sleep_ms(300)
        
#    @micropython.native
    def _get_rotated_buffer(self):
        # no need to rotate
        if self._rotation == ROTATION_0:
            return self.buffer
        # create buffer and rotate
        size = EPD_WIDTH * EPD_HEIGHT // 8
        fbuffer = memoryview(bytearray(size))
        frame = framebuf.FrameBuffer(
            fbuffer, EPD_WIDTH, EPD_HEIGHT, framebuf.MONO_HLSB)
        # copy buffer
        if self._rotation == ROTATION_270:
            for x in range(self.width):
                for y in range(self.height):
                    frame.pixel(y, EPD_HEIGHT-x-1, self.pixel(x, y))
        if self._rotation == ROTATION_90:
            for x in range(self.width):
                for y in range(self.height):
                    frame.pixel(EPD_WIDTH-y-1, x, self.pixel(x, y))
            frame.scroll(-6, 0)
        if self._rotation == ROTATION_180:
            for i in range(size):
                fbuffer[size-i-1] = self.buffer[i]
            frame.scroll(-6, 0)
        return fbuffer