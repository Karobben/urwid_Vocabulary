#!/usr/bin/env python3
import urwid, sys
import time
from Needlman import  Needle_Spell, Dictionary

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

def on_exit_clicked(button):
    raise urwid.ExitMainLoop()

def BigTxt(TXT):
    txt = urwid.BigText(
                ('banner',TXT), urwid.font.HalfBlock5x4Font())
    view = urwid.Padding(txt, 'center', width='clip')
    #view = urwid.AttrMap(view, 'body')
    return urwid.Columns([view])

def Fresh_Qbox(Result1, Result2,ResultT,Num,):
    Dic_widge.contents[0] = (urwid.Text(Dictionary.Dic_WB(Result2)), Dic_widge.options())
    if ResultT == "True":
        Tdr_txt = urwid.Text(('banner',"YOUR ARE RIGHT!!! "+str(Num)),align='center')
        Tdr_pattern = 'Green_BG'
    else:
        Tdr_txt = urwid.Text(('banner',"Your are wrong... Please Check again"),align='center')
        Tdr_pattern = 'Green_RG'
    Tdr.contents[0] = ( urwid.AttrWrap(Tdr_txt,Tdr_pattern), Tdr.options())
    Head_w1.contents[0] = (urwid.AttrWrap(BigTxt(Result1),Tdr_pattern), Head_w1.options())
    Head_w2.contents[0] = (urwid.AttrWrap(BigTxt(Result2),Tdr_pattern), Head_w2.options())
    #Head_w1.contents[0] = (BigTxt(Result1), Head_w1.options())
    #Head_w2.contents[0] = (BigTxt(Result2), Head_w2.options())

class QuestionBox(urwid.Padding):
    def keypress(self, size, key):
        global edit_w,Num
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        if edit.edit_text == 'q':
            raise urwid.ExitMainLoop()
        edit_w = urwid.Edit(u"Box1\n")
        #self.original_widget = QuestionBox(edit_w)
        Num, Result1, Result2, ResultT = Needle_Spell.main(edit.edit_text,DB,Num) # main function
        edit2.contents[0] = (QuestionBox_2(edit_w), edit2.options())
        Fresh_Qbox(Result1, Result2,ResultT,Num)

class QuestionBox_2(urwid.Padding):
    def keypress(self, size, key):
        global edit,Num
        if key != 'enter':
            return super(QuestionBox_2, self).keypress(size, key)
        if edit_w.edit_text == 'q':
            raise urwid.ExitMainLoop()
        edit = urwid.Edit(u"Box2\n")
        #self.original_widget = QuestionBox(edit)
        Num, Result1, Result2, ResultT = Needle_Spell.main(edit_w.edit_text,DB,Num) # main function
        edit2.contents[0] = (QuestionBox(edit), edit2.options())
        Fresh_Qbox(Result1, Result2,ResultT,Num)

'''
reading Words List
'''

DB = Needle_Spell.read_DB(open(sys.path[0] +'/Needlman/Word',"r"))
Num = 0
#Num, Result = Needle_Spell.main("biology",DB,Num) # main function

'''
Main Page
'''

palette = [
    ('banner', 'black', 'light gray'),
    ('body',         'black',      'light gray', 'standout'),
    ('header',       'white',      'light gray',   'bold'),
    ('Green_BG',       'white',      'dark green',   'bold'),
    ('Green_RG',       'white',      'dark red',   'bold'),
    ('button normal','light gray', 'dark blue', 'standout'),
    ('button select','white',      'dark green'),
    ('button disabled','dark gray','dark blue'),
    ('edit',         'light gray', 'dark blue'),
    ('bigtext',      'white',      'black'),
    ('chars',        'light gray', 'black'),
    ('exit',         'white',      'dark cyan'),
    ('Yellow_Text',    'yellow',      '',  'bold')
    ]


Head_w1 = BigTxt('Hello')
Head_w2 = BigTxt('World')

#Head_w1 = urwid.Columns([Head_w1])
#Head_w2 = urwid.Columns([Head_w2])
edit = urwid.Edit(u"What is your name?\n")
edit2 = urwid.Columns([QuestionBox(edit)])



'''
Dictionary
'''
#print(Dictionary.Dic_WB('biology'))
#time.sleep(2)
'''
Dic_widge = urwid.Columns([urwid.Text(Dictionary.Dic_WB('happy'))])


W = urwid.Pile([Head_w1,Head_w2])

W2 = urwid.Columns([edit2,Dic_widge])
W = urwid.Pile([W,W2])
fill = urwid.Filler(W)
fiil = urwid.Frame(header=Head_w1,body=fill)
loop = urwid.MainLoop(fill, unhandled_input=exit_on_q)
loop.run()
'''


Dic_widge = urwid.Columns([urwid.Text(Dictionary.Dic_WB('happy'))])


W = urwid.Pile([Head_w1,Head_w2])

W2 = urwid.Columns([edit2,Dic_widge])

button = urwid.Button(("Green_RG",u'Exit'))
urwid.connect_signal(button, 'click', on_exit_clicked)

W = urwid.Pile([W,W2,button])


fill = urwid.Filler(W)

hdr = urwid.Text("背單詞 v.10 type 'q' to quite the program", align='center')
hdr = urwid.AttrMap(hdr,'header')
Tdr = urwid.Text("What the heck again??", align='center')
Tdr = urwid.Columns([Tdr])
fill = urwid.Frame(header=hdr,body=fill, footer=Tdr)
loop = urwid.MainLoop(fill, palette, unhandled_input=exit_on_q)
loop.run()
