# kütüphaneleri import etme
import random
from pygame import mixer
import customtkinter as ctk
import os
from PIL import Image
import math
mixer.init()
# pencere teması
ctk.set_appearance_mode("dark")
# pencere oluşturma
pencere = ctk.CTk()
pencere.title("Rus Ruleti")
pencere.iconbitmap("tamburaicon.ico")
pencere.geometry("600x600")
# şarjör
mermi = random.randint(1, 6)
# soru ve yazı
sayi = ctk.CTkEntry(pencere, placeholder_text="1 ile 6 arasında bir sayı seç!", width=200)
sayi.pack(pady=10)
yazi = ctk.CTkLabel(pencere, text="")
yazi.pack(pady=20)
# animasyon
img = Image.open("tambura.png").convert("RGBA")
label = ctk.CTkLabel(pencere, text="")
label.pack(pady=20)
duration = 3000  # ms
fps = 60
frames = duration // (1000 // fps)
diag = int(math.ceil(math.hypot(img.width, img.height)))
def animate(frame=0, on_finish=None):
    t = frame / frames
    eased = 2 - 2 * math.cos(math.pi * t)
    angle = eased * 360
    rotated = img.rotate(-angle, expand=True)

    # sabit boyutlu şeffaf bir tuval oluştur, döndürülmüş resmi ortasına yapıştır
    canvas = Image.new("RGBA", (diag, diag), (0, 0, 0, 0))
    offset = ((diag - rotated.width) // 2, (diag - rotated.height) // 2)
    canvas.paste(rotated, offset, rotated if rotated.mode == "RGBA" else None)

    ctk_img = ctk.CTkImage(light_image=canvas, dark_image=canvas, size=(diag, diag))
    label.configure(image=ctk_img)
    label.image = ctk_img

    if frame < frames:
        pencere.after(1000 // fps, animate, frame + 1, on_finish)
    else:
        if on_finish:
            on_finish()
# ateş etme
def ates_et():
    mixer.music.stop()
    if os.path.exists("silah.mp3"):
        mixer.music.load("silah.mp3")
        mixer.music.play()

    secim = int(sayi.get())
    if secim < 1 or secim > 6:
        yazi.configure(text="1 ile 6 arasında sayı seçiniz lütfen.")
    elif secim == mermi:
        yazi.configure(text="Öldünüz.")
    else:
        yazi.configure(text="Tebrikler! Hayattasınız.")

    buton.configure(state="normal")
# rulet
def rulet():
    if not sayi.get().strip().isdigit() or not (1 <= int(sayi.get()) <= 6):
        yazi.configure(text="Lütfen 1 ile 6 arasında bir sayı giriniz.")
        return
    buton.configure(state="disabled")
    if os.path.exists("spin.mp3"):
        mixer.music.load("spin.mp3")
        mixer.music.play()
    animate(on_finish=ates_et)
# kontrol
buton = ctk.CTkButton(pencere, text="Şarjörü Çevir ve Tetiği Çek", command=rulet)
buton.pack(pady=10)
pencere.mainloop()