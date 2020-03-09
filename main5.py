#!/usr/bin/env python3
import urwid, sys
import time
from Needlman import  Needle_Spell, Dictionary

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

def BigTxt(TXT):
    txt = urwid.BigText(
                TXT, urwid.font.HalfBlock5x4Font())
    view = urwid.Padding(txt, 'center', width='clip')
    view = urwid.AttrMap(view, 'body')
    return urwid.Columns([view])

class QuestionBox(urwid.Padding):
    def keypress(self, size, key):
        global edit_w,Num
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        if edit.edit_text == 'q':
            raise urwid.ExitMainLoop()
        edit_w = urwid.Edit(u"Box1\n")
        #self.original_widget = QuestionBox(edit_w)
        Num, Result1, Result2 = Needle_Spell.main(edit.edit_text,DB,Num) # main function
        Head_w1.contents[0] = (BigTxt(Result1), Head_w1.options())
        Head_w2.contents[0] = (BigTxt(Result2), Head_w2.options())
        edit2.contents[0] = (QuestionBox_2(edit_w), edit2.options())
        Dic_widge.contents[0] = (urwid.Text(Dictionary.Dic_WB(Result2)), Dic_widge.options())

class QuestionBox_2(urwid.Padding):
    def keypress(self, size, key):
        global edit,Num
        if key != 'enter':
            return super(QuestionBox_2, self).keypress(size, key)
        if edit_w.edit_text == 'q':
            raise urwid.ExitMainLoop()
        edit = urwid.Edit(u"Box2\n")
        #self.original_widget = QuestionBox(edit)
        Num, Result1, Result2 = Needle_Spell.main(edit_w.edit_text,DB,Num) # main function
        Head_w1.contents[0] = (BigTxt(Result1), Head_w1.options())
        Head_w2.contents[0] = (BigTxt(Result2), Head_w2.options())
        edit2.contents[0] = (QuestionBox(edit), edit2.options())
        Dic_widge.contents[0] = (urwid.Text(Dictionary.Dic_WB(Result2)), Dic_widge.options())

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
    ('body',         'black',      'light gray', 'standout'),
    ('header',       'white',      'dark red',   'bold'),
    ('button normal','light gray', 'dark blue', 'standout'),
    ('button select','white',      'dark green'),
    ('button disabled','dark gray','dark blue'),
    ('edit',         'light gray', 'dark blue'),
    ('bigtext',      'white',      'black'),
    ('chars',        'light gray', 'black'),
    ('exit',         'white',      'dark cyan'),
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
Dic_widge = urwid.Columns([urwid.Text(Dictionary.Dic_WB('happy'))])


W = urwid.Pile([Head_w1,Head_w2])

W2 = urwid.Columns([edit2,Dic_widge])
W = urwid.Pile([W,W2])
fill = urwid.Filler(W)
loop = urwid.MainLoop(fill, unhandled_input=exit_on_q)
loop.run()
