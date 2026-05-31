from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.utils import get_color_from_hex
import socket
import re
import requests
import threading

# ========== НАСТРОЙКИ (ТВОИ ДАННЫЕ) ==========
PC_MAC = "08:62:66:2C:D8:93"      # ← ТВОЙ MAC
PC_IP = "192.168.0.115"           # ← ТВОЙ IP (потом заменишь)
# =============================================

def send_wol(mac):
    mac = re.sub(r'[:\-.]', '', mac).upper()
    if len(mac) != 12:
        return False
    data = bytes.fromhex('FF' * 6 + mac * 16)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(data, ('255.255.255.255', 9))
    sock.close()
    return True

class JarvisApp(App):
    def build(self):
        self.title = "Jarvis Controller"
        
        # Главный контейнер
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Тёмный фон
        with main_layout.canvas.before:
            Color(0.03, 0.05, 0.12, 1)
            self.bg_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
            main_layout.bind(size=self.update_bg, pos=self.update_bg)
        
        # Верхняя неоновая линия
        top_line = Label(size_hint_y=0.01)
        with top_line.canvas:
            Color(0.0, 0.8, 1.0, 1)
            Rectangle(size=(main_layout.width, 2))
        
        # Заголовок
        title_label = Label(
            text="[color=00ccff]J.A.R.V.I.S.[/color]\n[color=0088aa]v.2.0[/color]",
            markup=True,
            font_size='28sp',
            size_hint_y=0.15,
            halign='center'
        )
        
        # Контейнер для кнопок
        buttons_layout = BoxLayout(orientation='vertical', spacing=25, size_hint_y=None)
        buttons_layout.bind(minimum_height=buttons_layout.setter('height'))
        
        # Кнопка 1 - Включить ПК
        self.btn_power = Button(
            text="🔵 АКТИВИРОВАТЬ СИСТЕМУ",
            size_hint=(1, None),
            height=80,
            background_color=(0.0, 0.5, 0.9, 0.9),
            color=(1, 1, 1, 1),
            font_size='18sp'
        )
        self.btn_power.bind(on_release=self.power_on_pc)
        
        # Кнопка 2 - Запустить CS
        self.btn_cs = Button(
            text="🎮 ЗАПУСТИТЬ КОНТР-СТРАЙК",
            size_hint=(1, None),
            height=80,
            background_color=(0.0, 0.5, 0.9, 0.9),
            color=(1, 1, 1, 1),
            font_size='18sp'
        )
        self.btn_cs.bind(on_release=self.launch_cs)
        
        buttons_layout.add_widget(self.btn_power)
        buttons_layout.add_widget(self.btn_cs)
        
        # Скролл для кнопок
        scroll = ScrollView()
        scroll.add_widget(buttons_layout)
        
        # Статусная строка
        self.status_label = Label(
            text="● ONLINE. READY, SIR.",
            color=(0.0, 1.0, 0.7, 1),
            size_hint_y=0.08,
            font_size='14sp',
            halign='center'
        )
        
        # Нижняя неоновая линия
        bottom_line = Label(size_hint_y=0.01)
        with bottom_line.canvas:
            Color(0.0, 0.8, 1.0, 0.7)
            Rectangle(size=(main_layout.width, 1))
        
        # Собираем всё вместе
        main_layout.add_widget(top_line)
        main_layout.add_widget(title_label)
        main_layout.add_widget(scroll)
        main_layout.add_widget(self.status_label)
        main_layout.add_widget(bottom_line)
        
        # Анимации
        Clock.schedule_interval(self.pulse_status, 0.8)
        Clock.schedule_once(lambda dt: self.welcome_message(), 0.5)
        self.animate_buttons()
        
        return main_layout
    
    def update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos
    
    def animate_buttons(self):
        anim = Animation(opacity=1, duration=0.5) + Animation(opacity=0.9, duration=0.3) * 2
        anim.start(self.btn_power)
        anim.start(self.btn_cs)
    
    def pulse_status(self, dt):
        text = self.status_label.text
        if "●" in text:
            self.status_label.text = text.replace("●", "○")
        else:
            self.status_label.text = text.replace("○", "●")
    
    def welcome_message(self):
        self.status_label.text = "◉ INITIALIZING JARVIS..."
        Clock.schedule_once(lambda dt: self.set_status_ready(), 1.5)
    
    def set_status_ready(self):
        self.status_label.text = "● ONLINE. READY, SIR."
    
    def power_on_pc(self, instance):
        self.status_label.text = "⟳ ОТПРАВКА СИГНАЛА... STAND BY."
        
        # Анимация кнопки
        instance.background_color = (0.0, 0.3, 0.6, 1)
        Clock.schedule_once(lambda dt: self.reset_button_color(instance), 0.2)
        
        if send_wol(PC_MAC):
            self.status_label.text = "✓ СИГНАЛ ОТПРАВЛЕН. АКТИВАЦИЯ..."
            Clock.schedule_once(lambda dt: self.set_status_ready(), 3)
        else:
            self.status_label.text = "✗ ОШИБКА. НЕВЕРНЫЙ MAC"
            Clock.schedule_once(lambda dt: self.set_status_ready(), 3)
    
    def reset_button_color(self, button):
        button.background_color = (0.0, 0.5, 0.9, 0.9)
    
    def launch_cs(self, instance):
        self.status_label.text = "⟳ ЗАПУСК КОНТР-СТРАЙКА..."
        
        # Анимация кнопки
        instance.background_color = (0.0, 0.3, 0.6, 1)
        Clock.schedule_once(lambda dt: self.reset_button_color(instance), 0.2)
        
        try:
            response = requests.get(f"http://{PC_IP}:8888/cs", timeout=3)
            if response.status_code == 200:
                self.status_label.text = "✓ КОНТР-СТРАЙК ЗАПУЩЕН"
                Clock.schedule_once(lambda dt: self.set_status_ready(), 3)
            else:
                self.status_label.text = "✗ ОШИБКА СЕРВЕРА"
                Clock.schedule_once(lambda dt: self.set_status_ready(), 3)
        except:
            self.status_label.text = "✗ СВЯЗЬ ПОТЕРЯНА"
            Clock.schedule_once(lambda dt: self.set_status_ready(), 3)

if __name__ == "__main__":
    JarvisApp().run()