import pyglet

window  = pyglet.window.Window()    
label = pyglet.text.Label('Window 1',
font_name='Times New Roman',
font_size=36,
x=window.width//2, 
y=window.height//2,
anchor_x='center', 
anchor_y='center')  

@window.event
def on_draw():
    window.clear()
    label.draw()

window1  = pyglet.window.Window()
label1 = pyglet.text.Label('Window 2',
font_name='Times New Roman',
font_size=36,
x=window1.width//2,
y=window1.height//2,
anchor_x='center', 
anchor_y='center')

@window1.event
def on_draw():
    window1.clear()
    label1.draw()
    
pyglet.app.run()