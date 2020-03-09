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
    ('important','dark blue','light gray',('standout','underline')),
    ]

text_intro = [('important', u"Text"),
    u" widgets are the most common in "
    u"any urwid program.  This Text widget was created "
    u"without setting the wrap or align mode, so it "
    u"defaults to left alignment with wrapping on space "
    u"characters.  ",
    ('important', u"Change the window width"),
    u" to see how the widgets on this page react.  "
    u"This Text widget is wrapped with a ",
    ('important', u"Padding"),
    u" widget to keep it indented on the left and right."]

W = urwid.Text(('header', u" Hello World "), align='center')
fill = urwid.Filler(W)
loop = urwid.MainLoop(fill,palette, unhandled_input=exit_on_q)
loop.run()
