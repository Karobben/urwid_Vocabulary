#!/usr/bin/env python3
import urwid
import time
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
        global edit_w
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        if edit.edit_text == 'q':
            raise urwid.ExitMainLoop()
        #edit_w = urwid.Edit(u"Box1\n")
        #self.original_widget = QuestionBox(edit_w)
        Head_w1.contents[0] = (BigTxt(edit.edit_text), Head_w1.options())
        edit2.contents[0] = (QuestionBox(urwid.Edit(u"Box1\n")), edit2.options())

class QuestionBox_2(urwid.Padding):
    def keypress(self, size, key):
        global edit
        if key != 'enter':
            return super(QuestionBox_2, self).keypress(size, key)
        if edit_w.edit_text == 'q':
            raise urwid.ExitMainLoop()
        edit = urwid.Edit(u"Box2\n")
        #self.original_widget = QuestionBox(edit)
        Head_w1.contents[0] = (BigTxt(edit_w.edit_text), Head_w1.options())
        edit2.contents[0] = (QuestionBox(edit), edit2.options())

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


Head_w1 = BigTxt('test')
Head_w2 = BigTxt('tast')

#Head_w1 = urwid.Columns([Head_w1])
#Head_w2 = urwid.Columns([Head_w2])
edit = urwid.Edit(u"What is your name?\n")
edit2 = urwid.Columns([QuestionBox(edit)])


W = urwid.Pile([Head_w1,Head_w2,edit2])
fill = urwid.Filler(W)
loop = urwid.MainLoop(fill, unhandled_input=exit_on_q)
loop.run()
