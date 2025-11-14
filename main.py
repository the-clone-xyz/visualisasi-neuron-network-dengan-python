import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches # Diperlukan untuk kotak

# -------------------------------------------------------------------
# Konfigurasi Arsitektur dan Warna yang Disempurnakan
# -------------------------------------------------------------------
num_neurons_input = 3
num_neurons_hidden = 4
num_neurons_output = 1

x_input, x_hidden, x_output = 1.5, 4.5, 7.5 # Memberi lebih banyak ruang

# Palet Warna Baru
color_input_base = '#FFDAB9' # PeachPuff
color_hidden_base = '#ADD8E6' # LightBlue
color_output_base = '#D8BFD8' # Thistle

color_input_box = '#FFDAB9'
color_hidden_box = '#ADD8E6'
color_output_box = '#D8BFD8'

color_active = 'orange'
color_text = '#333333' # Abu-abu gelap, lebih lembut dari hitam
color_connection = 'grey'
color_connection_active = '#007BFF' # Biru cerah

# -------------------------------------------------------------------
# Fungsi Pembantu (Dengan Penambahan Kotak)
# -------------------------------------------------------------------
def draw_layer_static(ax, x_pos, num_neurons, base_color, box_color, layer_name):
    y_positions = np.linspace(-num_neurons/2 + 0.5, num_neurons/2 - 0.5, num_neurons)
    
    # --- BARU: Hitung dan gambar kotak latar belakang ---
    min_y = min(y_positions)
    max_y = max(y_positions)
    box_height = (max_y - min_y) + 1.2 # 1.2 = (0.4 radius * 2) + (0.2 padding * 2)
    box_width = 1.2
    
    # Jika hanya 1 neuron, y_positions = [0], min_y=0, max_y=0
    if num_neurons == 1:
        box_height = 1.2

    box_x_corner = x_pos - box_width / 2
    box_y_corner = min_y - box_height / 2 + (0.5 if num_neurons == 1 else 0.5)
    if num_neurons == 1:
        box_y_corner = y_positions[0] - box_height / 2
    else:
        box_y_corner = min_y - 0.6 # 0.4 radius + 0.2 padding
        
    # Gambar Kotak
    rect = patches.Rectangle((box_x_corner, box_y_corner), box_width, box_height,
                             linewidth=1, edgecolor='black', facecolor=box_color, 
                             alpha=0.2, zorder=0) # zorder=0 (paling belakang)
    ax.add_patch(rect)
    # --- Selesai Bagian Baru ---

    neurons_coords = []
    circles = []
    texts = []
    
    for i, y_pos in enumerate(y_positions):
        circle = plt.Circle((x_pos, y_pos), radius=0.4, color=base_color, alpha=0.9, 
                            edgecolor='black', zorder=3) # zorder=3 (di atas garis)
        ax.add_patch(circle)
        circles.append(circle)
        neurons_coords.append((x_pos, y_pos))
        
        # Label statis
        if layer_name == "Input Layer" and i == 0:
            ax.text(x_pos, y_pos, 'Input\nneuron', ha='center', va='center', fontsize=9, color=color_text, zorder=4)
        elif layer_name == "Output Layer" and i == 0:
            ax.text(x_pos, y_pos, 'Output\nneuron', ha='center', va='center', fontsize=9, color=color_text, zorder=4)
            
        # Teks untuk nilai aktivasi
        activation_text = ax.text(x_pos, y_pos, '', ha='center', va='center', fontsize=9, 
                                  color='black', fontweight='bold', zorder=4) # zorder=4 (paling atas)
        texts.append(activation_text)
            
    # Nama Lapisan
    ax.text(x_pos, box_y_corner + box_height + 0.2, layer_name, 
            ha='center', va='bottom', fontsize=12, fontweight='bold', color=color_text)
    
    return neurons_coords, y_positions, circles, texts

def draw_connections_static(ax, layer1_neurons_coords, layer2_neurons_coords):
    lines = []
    arrows = []
    for i, (x1, y1) in enumerate(layer1_neurons_coords):
        for j, (x2, y2) in enumerate(layer2_neurons_coords):
            line, = ax.plot([x1 + 0.4, x2 - 0.4], [y1, y2], color=color_connection, 
                            linewidth=0.8, zorder=1) # zorder=1 (di atas kotak)
            lines.append(line)
            
            # Label W_1 dan W_n
            if i == 0 and j == 0:
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                ax.text(mid_x, mid_y + 0.2, f'$W_1$', ha='center', va='bottom', fontsize=10, color=color_text, zorder=2)
            elif i == len(layer1_neurons_coords)-1 and j == len(layer2_neurons_coords)-1:
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                ax.text(mid_x, mid_y - 0.2, f'$W_n$', ha='center', va='top', fontsize=10, color=color_text, zorder=2)
                
            # Panah (awalnya tidak terlihat)
            arrow_patch = ax.annotate('', xy=(x2 - 0.4, y2), xytext=(x1 + 0.4, y1),
                                      arrowprops=dict(facecolor=color_connection_active, edgecolor='none',
                                                      shrink=0.1, width=1.5, headwidth=6, headlength=6, alpha=0.0),
                                      zorder=2) # zorder=2 (di atas garis, di bawah neuron)
            arrows.append(arrow_patch)
            
    return lines, arrows

# -------------------------------------------------------------------
# Persiapan Plot Statis Awal
# -------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 8)) # Ukuran plot lebih besar
ax.set_aspect('equal')
ax.axis('off')

# Gambar lapisan (sekarang dengan kotak)
input_neurons_coords, _, input_circles, input_texts = draw_layer_static(ax, x_input, num_neurons_input, color_input_base, color_input_box, "Input Layer")
hidden_neurons_coords, _, hidden_circles, hidden_texts = draw_layer_static(ax, x_hidden, num_neurons_hidden, color_hidden_base, color_hidden_box, "Hidden Layer")
output_neurons_coords, _, output_circles, output_texts = draw_layer_static(ax, x_output, num_neurons_output, color_output_base, color_output_box, "Output Layer")

# Gambar koneksi
input_hidden_lines, input_hidden_arrows = draw_connections_static(ax, input_neurons_coords, hidden_neurons_coords)
hidden_output_lines, hidden_output_arrows = draw_connections_static(ax, hidden_neurons_coords, output_neurons_coords)

# Teks penjelasan animasi
animation_explanation = ax.text(x_hidden, max(num_neurons_input, num_neurons_hidden, num_neurons_output)/2 + 2.0, 
                                '', ha='center', va='bottom', fontsize=14, color='darkred', fontweight='bold')

# Visualisasi input data
input_data_arrows = []
for i, (x_n, y_n) in enumerate(input_neurons_coords):
    arrow = ax.annotate(f'Data {i+1}', xy=(x_n - 0.4, y_n), xytext=(x_n - 1.5, y_n),
                        arrowprops=dict(facecolor='purple', edgecolor='none', shrink=0.1, width=1, headwidth=5, headlength=5, alpha=0.0),
                        fontsize=9, color='purple', ha='right', va='center', alpha=0.0)
    input_data_arrows.append(arrow)

# Atur batas plot
ax.set_xlim(0, x_output + 2)
ax.set_ylim(-max(num_neurons_input, num_neurons_hidden, num_neurons_output)/2 - 1.5,
             max(num_neurons_input, num_neurons_hidden, num_neurons_output)/2 + 3)

fig.suptitle("Visualisasi Cara Kerja Jaringan Saraf Tiruan", fontsize=18, fontweight='bold')

# -------------------------------------------------------------------
# Fungsi Animasi (Tidak perlu diubah)
# -------------------------------------------------------------------
def update(frame):
    # Reset semua warna dan teks aktivasi
    for circle in input_circles: circle.set_color(color_input_base)
    for text in input_texts: text.set_text('')
    for arrow in input_data_arrows:
        arrow.set_alpha(0.0)
        arrow.arrow_patch.set_alpha(0.0)

    for circle in hidden_circles: circle.set_color(color_hidden_base)
    for text in hidden_texts: text.set_text('')

    for circle in output_circles: circle.set_color(color_output_base)
    for text in output_texts: text.set_text('')
        
    for line in input_hidden_lines + hidden_output_lines: line.set_color(color_connection)
    for arrow_patch in input_hidden_arrows + hidden_output_arrows:
        arrow_patch.arrow_patch.set_alpha(0.0)

    updated_artists = []

    # Fase 0: Input data masuk
    if frame == 0:
        animation_explanation.set_text("Fase 1: Data Input Masuk")
        for i in range(num_neurons_input):
            input_data_arrows[i].set_alpha(1.0)
            input_data_arrows[i].arrow_patch.set_alpha(1.0)
            updated_artists.extend([input_data_arrows[i], input_data_arrows[i].arrow_patch])

    # Fase 1: Input Layer Aktif
    elif frame == 1:
        animation_explanation.set_text("Fase 2: Neuron Input Aktif")
        for i in range(num_neurons_input):
            input_circles[i].set_color(color_active)
            input_texts[i].set_text(f'{np.random.rand():.2f}') # Angka acak sebagai aktivasi
            updated_artists.extend([input_circles[i], input_texts[i]])

    # Fase 2: Koneksi Input ke Hidden Aktif
    elif frame == 2:
        animation_explanation.set_text("Fase 3: Aktivasi Mengalir ke Hidden Layer")
        for line in input_hidden_lines:
            line.set_color(color_connection_active)
            updated_artists.append(line)
        for arrow_patch in input_hidden_arrows:
            arrow_patch.arrow_patch.set_alpha(1.0)
            updated_artists.append(arrow_patch.arrow_patch)
        
    # Fase 3: Hidden Layer Aktif
    elif frame == 3:
        animation_explanation.set_text("Fase 4: Komputasi Internal di Hidden Layer")
        for circle in hidden_circles:
            circle.set_color(color_active)
            updated_artists.append(circle)
        for text in hidden_texts:
            text.set_text(f'{np.random.rand():.2f}')
            updated_artists.append(text)

    # Fase 4: Koneksi Hidden ke Output Aktif
    elif frame == 4:
        animation_explanation.set_text("Fase 5: Aktivasi Mengalir ke Output Layer")
        for line in hidden_output_lines:
            line.set_color(color_connection_active)
            updated_artists.append(line)
        for arrow_patch in hidden_output_arrows:
            arrow_patch.arrow_patch.set_alpha(1.0)
            updated_artists.append(arrow_patch.arrow_patch)
    
    # Fase 5: Output Layer Aktif dan Hasil
    elif frame == 5:
        animation_explanation.set_text("Fase 6: Menghasilkan Output")
        for circle in output_circles:
            circle.set_color(color_active)
            updated_artists.append(circle)
        for text in output_texts:
            text.set_text(f'{np.random.rand():.2f}')
            updated_artists.append(text)

    updated_artists.append(animation_explanation)
    return updated_artists

# -------------------------------------------------------------------
# Jalankan Animasi
# -------------------------------------------------------------------
ani = FuncAnimation(fig, update, frames=range(6), interval=1000, blit=False, repeat=True)
plt.show()

# Untuk menyimpan animasi
# ani.save('neural_network_perfected.gif', writer='pillow', fps=1)