print("\nGO!")

from machine import Pin, I2C, SPI, PWM, Timer
import framebuf
import time
import gc

print(gc.mem_free())

print("GOT IMPORTS!")

#Pin definition  引脚定义
I2C_SDA = 8
I2C_SDL = 9
I2C_INT = 40
I2C_RST = 39

DC = 14
CS = 10
SCK = 12
MOSI = 11
MISO = 13
RST = 48

BL = 47

#LCD Driver  LCD驱动
class LCD_1inch28(framebuf.FrameBuffer):
    def __init__(self): #SPI initialization  SPI初始化
        self.width = 240
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1,100_000_000,polarity=0, phase=0,bits= 8,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        #Define color, Micropython fixed to BRG format  定义颜色，Micropython固定为BRG格式
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        self.brown =   0X8430
        
        self.fill(self.white) #Clear screen  清屏
        self.show()#Show  显示

        self.pwm = PWM(Pin(BL))
        self.pwm.freq(5000) #Turn on the backlight  开背光
        
    def write_cmd(self, cmd): #Write command  写命令
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf): #Write data  写数据
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)
        
    def set_bl_pwm(self,duty): #Set screen brightness  设置屏幕亮度
        self.pwm.duty_u16(duty)#max 65535
        
    def init_display(self): #LCD initialization  LCD初始化
        """Initialize dispaly"""  
        self.rst(1)
        time.sleep(0.01)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        time.sleep(0.05)
        
        self.write_cmd(0xEF)
        self.write_cmd(0xEB)
        self.write_data(0x14) 
        
        self.write_cmd(0xFE) 
        self.write_cmd(0xEF) 

        self.write_cmd(0xEB)
        self.write_data(0x14) 

        self.write_cmd(0x84)
        self.write_data(0x40) 

        self.write_cmd(0x85)
        self.write_data(0xFF) 

        self.write_cmd(0x86)
        self.write_data(0xFF) 

        self.write_cmd(0x87)
        self.write_data(0xFF)

        self.write_cmd(0x88)
        self.write_data(0x0A)

        self.write_cmd(0x89)
        self.write_data(0x21) 

        self.write_cmd(0x8A)
        self.write_data(0x00) 

        self.write_cmd(0x8B)
        self.write_data(0x80) 

        self.write_cmd(0x8C)
        self.write_data(0x01) 

        self.write_cmd(0x8D)
        self.write_data(0x01) 

        self.write_cmd(0x8E)
        self.write_data(0xFF) 

        self.write_cmd(0x8F)
        self.write_data(0xFF) 


        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(0x20)

        self.write_cmd(0x36)
        self.write_data(0x98)

        self.write_cmd(0x3A)
        self.write_data(0x05) 


        self.write_cmd(0x90)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08) 

        self.write_cmd(0xBD)
        self.write_data(0x06)
        
        self.write_cmd(0xBC)
        self.write_data(0x00)

        self.write_cmd(0xFF)
        self.write_data(0x60)
        self.write_data(0x01)
        self.write_data(0x04)

        self.write_cmd(0xC3)
        self.write_data(0x13)
        self.write_cmd(0xC4)
        self.write_data(0x13)

        self.write_cmd(0xC9)
        self.write_data(0x22)

        self.write_cmd(0xBE)
        self.write_data(0x11) 

        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)

        self.write_cmd(0xDF)
        self.write_data(0x21)
        self.write_data(0x0c)
        self.write_data(0x02)

        self.write_cmd(0xF0)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF1)    
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37)  
        self.write_data(0x6F)


        self.write_cmd(0xF2)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF3)   
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37) 
        self.write_data(0x6F)

        self.write_cmd(0xED)
        self.write_data(0x1B) 
        self.write_data(0x0B) 

        self.write_cmd(0xAE)
        self.write_data(0x77)
        
        self.write_cmd(0xCD)
        self.write_data(0x63)


        self.write_cmd(0x70)
        self.write_data(0x07)
        self.write_data(0x07)
        self.write_data(0x04)
        self.write_data(0x0E) 
        self.write_data(0x0F) 
        self.write_data(0x09)
        self.write_data(0x07)
        self.write_data(0x08)
        self.write_data(0x03)

        self.write_cmd(0xE8)
        self.write_data(0x34)

        self.write_cmd(0x62)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x71)
        self.write_data(0xED)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x0F)
        self.write_data(0x71)
        self.write_data(0xEF)
        self.write_data(0x70) 
        self.write_data(0x70)

        self.write_cmd(0x63)
        self.write_data(0x18)
        self.write_data(0x11)
        self.write_data(0x71)
        self.write_data(0xF1)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x13)
        self.write_data(0x71)
        self.write_data(0xF3)
        self.write_data(0x70) 
        self.write_data(0x70)

        self.write_cmd(0x64)
        self.write_data(0x28)
        self.write_data(0x29)
        self.write_data(0xF1)
        self.write_data(0x01)
        self.write_data(0xF1)
        self.write_data(0x00)
        self.write_data(0x07)

        self.write_cmd(0x66)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0xCD)
        self.write_data(0x67)
        self.write_data(0x45)
        self.write_data(0x45)
        self.write_data(0x10)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_cmd(0x67)
        self.write_data(0x00)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x54)
        self.write_data(0x10)
        self.write_data(0x32)
        self.write_data(0x98)

        self.write_cmd(0x74)
        self.write_data(0x10)
        self.write_data(0x85)
        self.write_data(0x80)
        self.write_data(0x00) 
        self.write_data(0x00) 
        self.write_data(0x4E)
        self.write_data(0x00)
        
        self.write_cmd(0x98)
        self.write_data(0x3e)
        self.write_data(0x07)

        self.write_cmd(0x35)
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)
    
    #设置窗口    
    def setWindows(self,Xstart,Ystart,Xend,Yend): 
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(Xstart)
        self.write_data(0x00)
        self.write_data(Xend-1)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(Ystart)
        self.write_data(0x00)
        self.write_data(Yend-1)
        
        self.write_cmd(0x2C)
     
    #Show  显示   
    def show(self): 
        self.setWindows(0,0,self.width,self.height)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
    '''
        Partial display, the starting point of the local
        display here is reduced by 10, and the end point
        is increased by 10
    '''
    #Partial display, the starting point of the local display here is reduced by 10, and the end point is increased by 10
    #局部显示，这里的局部显示起点减少10，终点增加10
    def Windows_show(self,Xstart,Ystart,Xend,Yend):
        if Xstart > Xend:
            data = Xstart
            Xstart = Xend
            Xend = data
            
        if (Ystart > Yend):        
            data = Ystart
            Ystart = Yend
            Yend = data
            
        if Xstart <= 10:
            Xstart = 10
        if Ystart <= 10:
            Ystart = 10
            
        Xstart -= 10;Xend += 10
        Ystart -= 10;Yend += 10
        
        self.setWindows(Xstart,Ystart,Xend,Yend)      
        self.cs(1)
        self.dc(1)
        self.cs(0)
        for i in range (Ystart,Yend-1):             
            Addr = (Xstart * 2) + (i * 240 * 2)                
            self.spi.write(self.buffer[Addr : Addr+((Xend-Xstart)*2)])
        self.cs(1)
        
    #Write characters, size is the font size, the minimum is 1  
    #写字符，size为字体大小,最小为1
    def write_text(self,text,x,y,size,color):
        ''' Method to write Text on OLED/LCD Displays
            with a variable font size

            Args:
                text: the string of chars to be displayed
                x: x co-ordinate of starting position
                y: y co-ordinate of starting position
                size: font size of text
                color: color of text to be displayed
        '''
        background = self.pixel(x,y)
        info = []
        # Creating reference charaters to read their values
        self.text(text,x,y,color)
        for i in range(x,x+(8*len(text))):
            for j in range(y,y+8):
                # Fetching amd saving details of pixels, such as
                # x co-ordinate, y co-ordinate, and color of the pixel
                px_color = self.pixel(i,j)
                info.append((i,j,px_color)) if px_color == color else None
        # Clearing the reference characters from the screen
        self.text(text,x,y,background)
        # Writing the custom-sized font characters on screen
        for px_info in info:
            self.fill_rect(size*px_info[0] - (size-1)*x , size*px_info[1] - (size-1)*y, size, size, px_info[2]) 
    
        
#Touch drive  触摸驱动
class Touch_CST816T(object):
    #Initialize the touch chip  初始化触摸芯片
    def __init__(self,address=0x15,mode=0,i2c_num=1,i2c_sda=I2C_SDA,i2c_scl=I2C_SDL,int_pin=I2C_INT,rst_pin=I2C_RST,LCD=None):
        self._bus = I2C(i2c_num,scl=Pin(i2c_scl),sda=Pin(i2c_sda),freq=400_000) #Initialize I2C 初始化I2C
        self._address = address #Set slave address  设置从机地址
        self.int=Pin(int_pin,Pin.IN, Pin.PULL_UP)     
        self.tim = Timer(0)   
        self.rst=Pin(rst_pin,Pin.OUT)
        self.Reset()
        bRet=self.WhoAmI()
        if bRet :
            print("Success:Detected CST816T.")
            Rev= self.Read_Revision()
            print("CST816T Revision = {}".format(Rev))
            self.Stop_Sleep()
        else    :
            print("Error: Not Detected CST816T.")
            return None
        self.Mode = mode
        self.Gestures="None"
        self.Flag = self.Flgh =self.l = 0
        self.X_point = self.Y_point = 0
        self.int.irq(handler=self.Int_Callback,trigger=Pin.IRQ_FALLING)
      
    def _read_byte(self,cmd):
        rec=self._bus.readfrom_mem(int(self._address),int(cmd),1)
        return rec[0]
    
    def _read_block(self, reg, length=1):
        rec=self._bus.readfrom_mem(int(self._address),int(reg),length)
        return rec
    
    def _write_byte(self,cmd,val):
        self._bus.writeto_mem(int(self._address),int(cmd),bytes([int(val)]))

    def WhoAmI(self):
        if (0xB5) != self._read_byte(0xA7):
            return False
        return True
    
    def Read_Revision(self):
        return self._read_byte(0xA9)
      
    #Stop sleeping  停止睡眠
    def Stop_Sleep(self):
        self._write_byte(0xFE,0x01)
    
    #Reset  复位    
    def Reset(self):
        self.rst(0)
        time.sleep_ms(1)
        self.rst(1)
        time.sleep_ms(50)
    
    #Set mode  设置模式   
    def Set_Mode(self,mode,callback_time=10,rest_time=5): 
        # mode = 0 gestures mode 
        # mode = 1 point mode 
        # mode = 2 mixed mode 
        if (mode == 1):      
            self._write_byte(0xFA,0X41)
            
        elif (mode == 2) :
            self._write_byte(0xFA,0X71)
            
        else:
            self._write_byte(0xFA,0X11)
            self._write_byte(0xEC,0X01)
     
    #Get the coordinates of the touch  获取触摸的坐标
    def get_point(self):
        xy_point = self._read_block(0x03,4)
        
        x_point= ((xy_point[0]&0x0f)<<8)+xy_point[1]
        y_point= ((xy_point[2]&0x0f)<<8)+xy_point[3]
        
        self.X_point=x_point
        self.Y_point=y_point
    
    #Draw line and show  画线并显示  
    def Touch_HandWriting(self):
        x = y = data = 0
        color = 0
        self.Flgh = 0
        self.Flag = 0
        self.Mode = 1
        self.Set_Mode(self.Mode)
        
        LCD.fill(LCD.white)
        LCD.rect(0, 0, 35, 208,LCD.red,True)
        LCD.rect(0, 0, 208, 35,LCD.green,True)
        LCD.rect(205, 0, 240, 240,LCD.blue,True)
        LCD.rect(0, 205, 240, 240,LCD.brown,True)
        LCD.show()
        
        self.tim.init(period=1, callback=self.Timer_callback)
        try:
            while True:
                if self.Flgh == 0 and self.X_point != 0:
                    self.Flgh = 1
                    x = self.X_point
                    y = self.Y_point
                    
                if self.Flag == 1:
                    if (self.X_point > 34 and self.X_point < 205) and (self.Y_point > 34 and self.Y_point < 205):
                        self.Flgh = 3
                    else:
                        if (self.X_point > 0 and self.X_point < 33) and (self.Y_point > 0 and self.Y_point < 208):
                            color = LCD.red
                            
                        if (self.X_point > 0 and self.X_point < 208) and (self.Y_point > 0 and self.Y_point < 33):
                            color = LCD.green
                            
                        if (self.X_point > 208 and self.X_point < 240) and (self.Y_point > 0 and self.Y_point < 240):
                            color = LCD.blue
                            
                        if (self.X_point > 0 and self.X_point < 240) and (self.Y_point > 208 and self.Y_point < 240):
                            LCD.fill(LCD.white)
                            LCD.rect(0, 0, 35, 208,LCD.red,True)
                            LCD.rect(0, 0, 208, 35,LCD.green,True)
                            LCD.rect(205, 0, 240, 240,LCD.blue,True)
                            LCD.rect(0, 205, 240, 240,LCD.brown,True)
                            LCD.show()
                        self.Flgh = 4
                        
                    if self.Flgh == 3:
                        time.sleep(0.001) #Prevent disconnection  防止断触
                        if self.l < 25:           
                            self.Flag = 0
                            LCD.line(x,y,self.X_point,self.Y_point,color)
                            LCD.Windows_show(x,y,self.X_point,self.Y_point)
                            self.l=0
                        else:
                            self.Flag = 0
                            LCD.pixel(self.X_point,self.Y_point,color)
                            LCD.Windows_show(x,y,self.X_point,self.Y_point)
                            self.l=0
                            
                        x = self.X_point
                        y = self.Y_point
        except KeyboardInterrupt:
            pass
    
    #Gesture  手势
    def Touch_Gesture(self):
        self.Mode = 0
        self.Set_Mode(self.Mode)
        LCD.write_text('Gesture test',70,90,1,LCD.black)
        LCD.write_text('Complete as prompted',35,120,1,LCD.black)
        LCD.show()
        time.sleep(1)
        LCD.fill(LCD.white)
        while self.Gestures != 0x01:
            LCD.fill(LCD.white)
            LCD.write_text('UP',100,110,3,LCD.black)
            LCD.show()

        print("a")
            
        while self.Gestures != 0x02:
            LCD.fill(LCD.white)
            LCD.write_text('DOWM',70,110,3,LCD.black)
            LCD.show()

        print("b")
            
        while self.Gestures != 0x03:
            LCD.fill(LCD.white)
            LCD.write_text('LEFT',70,110,3,LCD.black)
            LCD.show()
            
        while self.Gestures != 0x04:
            LCD.fill(LCD.white)
            LCD.write_text('RIGHT',60,110,3,LCD.black)
            LCD.show()
            
        while self.Gestures != 0x0C:
            LCD.fill(LCD.white)
            LCD.write_text('Long Press',40,110,2,LCD.black)
            LCD.show()
            
        while self.Gestures != 0x0B:
            LCD.fill(LCD.white)
            LCD.write_text('Double Click',25,110,2,LCD.black)
            LCD.show() 
        
    def Int_Callback(self,pin):
        if self.Mode == 0 :
            self.Gestures = self._read_byte(0x01)

        elif self.Mode == 1:           
            self.Flag = 1
            self.get_point()

    def Timer_callback(self,t):
        self.l += 1
        if self.l > 100:
            self.l = 50
            
if __name__=='__main__':
    print("RUNNING MAIN!")
    LCD = LCD_1inch28()
    LCD.set_bl_pwm(65535)

    Touch=Touch_CST816T(mode=1,LCD=LCD)

    Touch.Touch_Gesture()
    Touch.Touch_HandWriting()













