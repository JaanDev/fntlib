import fntlib
import random

def test_main():
    print()
    
    with open(r"D:\Dev\Python\Python_3.7\Programs\PyCharmProjects\fntlib\tests\bigFont-uhd.fnt", 'rb') as f:
        fnt = fntlib.load(f)
        print(fnt)
        # print(fnt.info)
        # print(fnt.common)
        # print(fnt.pages)
        # print(fnt.chars)
        # print(fnt.kernings)
        
        fnt.info.aa = False
        fnt.info.face = "Hello Python! 110101001"
        fnt.info.size = 100500
        fnt.info.stretch_h = 101
        fnt.info.padding.down = 99
        
        fnt.common.alpha_channel = fntlib.ChannelInfo.GLYPH_AND_OUTLINE
        fnt.common.blue_channel = fntlib.ChannelInfo.ONE
        # fnt.common.packed = True
        fnt.common.scale_w = 228
        
        print(fnt.common, fnt.info)
        
        for c in fnt.chars:
            c.xadvance = random.randint(-100, 100)
            c.x = fnt.chars.index(c) * 10
            c.y = fnt.chars.index(c) * 10
            
            c.chnl = fntlib.Channel.ALL
            
            c.id = random.randint(-1, 10)
            
        fnt.kernings = fnt.kernings[5:20]
        print(fnt.kernings)
            
        # fnt2 = fntlib.FNT()
        # print(fnt2)
        
    with open(r"D:\Dev\Python\Python_3.7\Programs\PyCharmProjects\fntlib\tests\bigFont-uhd-2.fnt", 'wb') as f:
        fntlib.dump(fnt, f)