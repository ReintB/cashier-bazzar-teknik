import pyglet
from pyglet.window import key, mouse

# Daftar menu
menu = {
    '• Kelapa': 10000,
    '• Ricebowl': 15000,
    '• Bakmi B2': 15000,
    '• Es Susu Soda Gembira': 7000,
    '• Thai Tea/Green Tea': 5000
}

# Data yang akan dimasukkan oleh kasir
nama_pembeli = ''
tanggal_beli = ''
selected_item = ''
selected_jumlah = 0
total_harga = 0
input_mode = 'nama' 
transaction_done = False 

# Data pembelian
pembelian = []

# Window untuk kasir
window_kasir = pyglet.window.Window(caption="Kasir - WARTEK XII-4", width=640, height=480)

# Window untuk pembeli
window_pembeli = pyglet.window.Window(caption="Pembeli - WARTEK XII-4", width=640, height=480)

item_positions = {
    '• Kelapa': (20, 280),
    '• Ricebowl': (20, 250),
    '• Bakmi B2': (20, 220),
    '• Es Susu Soda Gembira': (20, 190),
    '• Thai Tea/Green Tea': (20, 160)
}

jumlah_positions = {
    1: (20, 120), 2: (70, 120), 3: (120, 120), 4: (170, 120),
    5: (220, 120), 6: (270, 120), 7: (320, 120), 8: (370, 120),
    9: (420, 120), 10: (470, 120)
}

# Posisi untuk memilih tanggal
tanggal_positions = {
    'Kamis, 24 Oktober 2024': (20, 340),
    'Jumat, 25 Oktober 2024': (20, 310)
}

def update_pembeli_window():
    window_pembeli.clear()
    
    label_judul = pyglet.text.Label(f'SELAMAT DATANG DI WARUNG TEKNIK (WARTEK)', x=20, y=450, font_size=14, bold = True)
    label_judul.draw()
    label_nama = pyglet.text.Label(f'Nama Pembeli: {nama_pembeli}', x=20, y=420, font_size=14)
    label_nama.draw()
    label_tanggal = pyglet.text.Label(f'Tanggal Pembelian: {tanggal_beli}', x=20, y=390, font_size=14)
    label_tanggal.draw()
    
    y_pos = 360
    for item, jumlah, harga in pembelian:
        label_item = pyglet.text.Label(f'{item}: {jumlah} x Rp {harga//jumlah} = Rp {harga}', x=20, y=y_pos, font_size=12)
        label_item.draw()
        y_pos -= 30
    
    total_label = pyglet.text.Label(f'Total Harga: Rp {total_harga}', x=20, y=y_pos - 30, font_size=14, bold=True)
    total_label.draw()

def reset_data():
    global nama_pembeli, tanggal_beli, selected_item, selected_jumlah, total_harga, input_mode, pembelian, show_alert
    nama_pembeli = ''
    tanggal_beli = ''
    selected_item = ''
    selected_jumlah = 0
    total_harga = 0
    input_mode = 'nama'
    pembelian.clear()

@window_kasir.event
def on_draw():
    window_kasir.clear()
    pyglet.text.Label('Data transaksi:', x=20, y=450, font_size=14).draw()
    
    pyglet.text.Label(f'Nama Pembeli: {nama_pembeli}', x=20, y=400, font_size=12).draw()
    pyglet.text.Label(f'Tanggal: {tanggal_beli}', x=20, y=370, font_size=12).draw()
    
    if input_mode == 'nama':
        pyglet.text.Label('Masukkan nama pembeli:', x=20, y=320, font_size=12).draw()
    elif input_mode == 'tanggal':
        pyglet.text.Label('Pilih tanggal pembelian:', x=20, y=280, font_size=12).draw()
        for tanggal, pos in tanggal_positions.items():
            pyglet.text.Label(tanggal, x=pos[0], y=pos[1], font_size=12).draw()
    elif input_mode == 'item':
        pyglet.text.Label('Pilih item dengan mengetik atau klik item:', x=20, y=320, font_size=12).draw()
        y_pos = 280
        for item in menu.keys():
            pyglet.text.Label(item, x=20, y=y_pos, font_size=12).draw()
            y_pos -= 30
    elif input_mode == 'jumlah':
        pyglet.text.Label(f'Item dipilih: {selected_item}', x=20, y=320, font_size=12).draw()
        pyglet.text.Label('Pilih jumlah item (1-10) dengan mengklik angka:', x=20, y=290, font_size=12).draw()
        for jumlah, pos in jumlah_positions.items():
            jumlah_x, jumlah_y = pos
            pyglet.text.Label(str(jumlah), x=jumlah_x, y=jumlah_y, font_size=14).draw()
    
    pyglet.shapes.Rectangle(300, 80, 100, 30, color=(50, 150, 50)).draw()
    pyglet.text.Label('Selesai', x=320, y=90, font_size=14, bold=True, color=(255, 255, 255, 255)).draw()

    pyglet.shapes.Rectangle(420, 80, 100, 30, color=(150, 50, 50)).draw()
    pyglet.text.Label('Batal', x=440, y=90, font_size=14, bold=True, color=(255, 255, 255, 255)).draw()

@window_kasir.event
def on_text(text):
    global nama_pembeli, tanggal_beli, selected_jumlah, input_mode

    if input_mode == 'nama':
        if text.isalpha() or text.isspace():
            nama_pembeli += text
    elif input_mode == 'tanggal':
        pass

@window_kasir.event
def on_key_press(symbol, modifiers):
    global input_mode
    if symbol == key.ENTER and input_mode == 'nama':
        input_mode = 'tanggal'
    elif symbol == key.ENTER and input_mode == 'tanggal':
        input_mode = 'item'

@window_kasir.event
def on_mouse_press(x, y, button, modifiers):
    global selected_item, selected_jumlah, input_mode, total_harga, transaction_done, show_alert, alert_time, tanggal_beli
    if button == mouse.LEFT:
        if input_mode == 'tanggal':
            for tanggal, pos in tanggal_positions.items():
                if pos[1] <= y <= pos[1] + 20:
                    tanggal_beli = tanggal
                    input_mode = 'item' 
                    break
        elif input_mode == 'item':
            for item, pos in item_positions.items():
                item_x, item_y = pos
                if item_x <= x <= item_x + 200 and item_y <= y <= item_y + 20:
                    selected_item = item
                    input_mode = 'jumlah'
                    break
        elif input_mode == 'jumlah':
            for jumlah, pos in jumlah_positions.items():
                jumlah_x, jumlah_y = pos
                if jumlah_x <= x <= jumlah_x + 30 and jumlah_y <= y <= jumlah_y + 30:
                    selected_jumlah = jumlah
                    harga_total = menu[selected_item] * selected_jumlah
                    pembelian.append((selected_item, selected_jumlah, harga_total))
                    total_harga += harga_total
                    selected_item = ''
                    selected_jumlah = 0
                    input_mode = 'item'

        # Tombol "Selesai"
        if 300 <= x <= 400 and 80 <= y <= 110:
            if nama_pembeli and tanggal_beli and pembelian:
                transaction_done = True 
                reset_data()
                update_pembeli_window()

        # Tombol "Batal"
        elif 420 <= x <= 520 and 80 <= y <= 110:
            reset_data()  # Reset data ketika dibatalkan

@window_pembeli.event
def on_draw():
    update_pembeli_window()

def main():
    pyglet.app.run()

if __name__ == '__main__':
    main()