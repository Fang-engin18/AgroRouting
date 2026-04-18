import os
import math
import tkinter as tk
import random
import mercantile
import serial
import serial.tools.list_ports
import time
import urllib.request
import io
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
from cairo import ImageSurface, FORMAT_ARGB32, Context
from tkinter import font


class ImageButton(tk.Canvas):
    def __init__(self, parent, normal_img, hover_img=None, pressed_img=None,
                 command=None, width=None, height=None, **kwargs):
        kwargs.setdefault('bg', '#160B0B')
        kwargs.setdefault('highlightthickness', 0)
        super().__init__(parent, **kwargs)
        self.command = command
        self.state = "normal"
        # Загрузка изображений
        self.normal_img = self.load_image(normal_img, width, height)
        self.hover_img = self.load_image(hover_img, width, height) if hover_img else self.normal_img
        self.pressed_img = self.load_image(pressed_img, width, height) if pressed_img else self.normal_img

        # Создание кнопки
        self.image_item = self.create_image(0, 0, anchor=tk.NW, image=self.normal_img)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

        # Установка размеров
        if width and height:
            self.config(width=width, height=height)
        else:
            self.config(width=self.normal_img.width(), height=self.normal_img.height())

    def load_image(self, path, width=None, height=None):
        try:
            img = Image.open(path)
            if width and height:
                img = img.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            # Создаем простую кнопку-заглушку
            img = Image.new("RGBA", (100, 40), "#cccccc")
            draw = ImageDraw.Draw(img)
            draw.text((10, 10), "Button", fill="black")
            return ImageTk.PhotoImage(img)

    def on_enter(self, event):
        self.state = "hover"
        self.itemconfig(self.image_item, image=self.hover_img)

    def on_leave(self, event):
        self.state = "normal"
        self.itemconfig(self.image_item, image=self.normal_img)

    def on_press(self, event):
        self.state = "pressed"
        self.itemconfig(self.image_item, image=self.pressed_img)

    def on_release(self, event):
        if self.state == "pressed":
            self.state = "hover"
            self.itemconfig(self.image_item, image=self.hover_img)
            if self.command:
                self.command()

    def disable(self):
        """Делает кнопку неактивной"""
        self.config(state=tk.DISABLED)
        self.itemconfig(self.image_item, image=self.normal_img)  # Можно добавить серое изображение

    def enable(self):
        """Делает кнопку активной"""
        self.config(state=tk.NORMAL)
        self.itemconfig(self.image_item, image=self.normal_img)


class GifLoadingScreen:
    def __init__(self, root, app_class):
        self.root = root
        self.root.title("Загрузка")
        self.root.configure(bg='#222222')
        self.root.geometry("1280x720")
        self.root.resizable(False, False)

        self.app_class = app_class
        self.frames = []
        self.current_frame = 0
        self.setup_ui()
        self.root.after(0, self.animate_gif)

    def setup_ui(self):
        # Загрузка GIF-изображения
        try:
            gif_path = "gifka.gif"  # Укажите путь к вашему GIF-файлу
            with Image.open(gif_path) as gif:
                # Извлекаем все кадры из GIF
                for frame in range(0, gif.n_frames):
                    gif.seek(frame)
                    frame_image = ImageTk.PhotoImage(gif.copy())
                    self.frames.append(frame_image)
        except Exception as e:
            print(f"Ошибка загрузки GIF: {e}")
            # Создаем простую заставку, если GIF не загрузился
            self.create_fallback_loading()

        # Создаем холст для отображения GIF
        self.canvas = tk.Canvas(self.root, width=1280, height=720, bg='#160B0B', highlightthickness=0)
        self.canvas.pack()

    def animate_gif(self):
        i = 0
        if self.frames:
            self.canvas.delete("all")
            self.canvas.create_image(640, 360, image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)

            self.root.after(500, self.animate_gif)  # 10 FPS
            self.root.after(5000, self.transition_to_app)

    def transition_to_app(self):
        self.canvas.destroy()
        self.app_class(self.root)


class ImageButton(tk.Canvas):
    def __init__(self, parent, normal_img, hover_img=None, pressed_img=None,
                 command=None, width=None, height=None, **kwargs):
        kwargs.setdefault('bg', '#160B0B')
        kwargs.setdefault('highlightthickness', 0)
        super().__init__(parent, **kwargs)
        self.command = command
        self.state = "normal"

        # Загрузка изображений
        self.normal_img = self.load_image(normal_img, width, height)
        self.hover_img = self.load_image(hover_img, width, height) if hover_img else self.normal_img
        self.pressed_img = self.load_image(pressed_img, width, height) if pressed_img else self.normal_img

        # Создание кнопки
        self.image_item = self.create_image(0, 0, anchor=tk.NW, image=self.normal_img)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

        # Установка размеров
        if width and height:
            self.config(width=width, height=height)
        else:
            self.config(width=self.normal_img.width(), height=self.normal_img.height())

    def load_image(self, path, width=None, height=None):
        try:
            img = Image.open(path)
            if width and height:
                img = img.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            img = Image.new("RGBA", (100, 40), "#cccccc")
            draw = ImageDraw.Draw(img)
            draw.text((10, 10), "Button", fill="black")
            return ImageTk.PhotoImage(img)

    def on_enter(self, event):
        self.state = "hover"
        self.itemconfig(self.image_item, image=self.hover_img)

    def on_leave(self, event):
        self.state = "normal"
        self.itemconfig(self.image_item, image=self.normal_img)

    def on_press(self, event):
        self.state = "pressed"
        self.itemconfig(self.image_item, image=self.pressed_img)

    def on_release(self, event):
        if self.state == "pressed":
            self.state = "hover"
            self.itemconfig(self.image_item, image=self.hover_img)
            if self.command:
                self.command()


class StatusBar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg='#160B0B', height=50, bd=0, relief=tk.FLAT)

        # Контейнер для GNSS индикатора
        gnss_frame = tk.Frame(self, bg='#160B0B')
        gnss_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Canvas для полосок сигнала
        self.signal_canvas = tk.Canvas(gnss_frame, width=50, height=30, bg='#160B0B', highlightthickness=0)
        self.signal_canvas.pack(side=tk.LEFT)

        # Параметры полосок
        self.bar_width = 6
        self.gap = 4
        self.heights = [6, 12, 18, 24, 30]
        self.bars = []

        # Создаем полоски
        for i, h in enumerate(self.heights):
            x0 = i * (self.bar_width + self.gap)
            y0 = 30 - h
            x1 = x0 + self.bar_width
            y1 = 30
            rect = self.signal_canvas.create_rectangle(x0, y0, x1, y1, fill='gray', outline='')
            self.bars.append(rect)

        # Надпись GNSS
        self.gnss_label = tk.Label(gnss_frame, text="GNSS", bg='#160B0B', fg='white', font=('Arial', 12, 'bold'))
        self.gnss_label.pack(side=tk.LEFT, padx=(8, 0), pady=5)

        # Текущее время
        self.time_label = tk.Label(self, text="", bg='#160B0B', fg='white', font=('Arial', 12))
        self.time_label.pack(side=tk.LEFT, padx=15)
        self.update_time()

        # Индикатор статуса
        self.status_canvas = tk.Canvas(self, width=20, height=20, bg='#160B0B', highlightthickness=0)
        self.status_canvas.pack(side=tk.LEFT, padx=(10, 0))
        self.status_canvas.create_oval(5, 5, 15, 15, fill='limegreen')

        # Запускаем анимацию сигнала
        self.update_signal()

    def update_signal(self):
        active_bars = random.randint(3, 5)
        for i, bar_id in enumerate(self.bars):
            if i < active_bars:
                self.signal_canvas.itemconfig(bar_id, fill='limegreen')
            else:
                self.signal_canvas.itemconfig(bar_id, fill='gray')
        delay = random.randint(500, 2000)
        self.after(delay, self.update_signal)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(500, self.update_time)


class TractorSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Траектория движения трактора")
        self.root.geometry("1600x950")
        self.root.configure(bg='#160B0B')

        # Параметры интерфейса
        self.field_width = 1120
        self.field_height = 700
        self.initial_zoom = 3

        # Параметры трактора
        self.TRACTOR_WIDTH = 15
        self.TRACTOR_LENGTH = 25
        self.MAX_SPEED = 0.35
        self.TURN_RATE = 2.25
        self.ANGLE_OFFSET = -90
        self.TRACTOR_SIZE = 15

        # Инициализация переменных
        self.original_image = None
        self.image = None
        self.image_tk = None
        self.image_id = None
        self.scale_factor = 1.0
        self.image_offset_x = 0
        self.image_offset_y = 0
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.is_dragging = False
        self.is_panning = False
        self.selection_points = []
        self.trajectory_points = []
        self.current_target_index = 0
        self.tractor = None
        self.tractor_img = None
        self.tractor_id = None
        self.simulation_active = False
        self.simulation_paused = False
        self.polygon_mode = False
        self.position_refining = False
        self.start_button = None

        # Статус бар
        self.statuse_bar = tk.Label(self.root, text="Готов к работе", bd=1, bg="#160B0B",
                                    fg='white', relief=tk.SUNKEN, anchor=tk.W)
        self.statuse_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Создание виджетов
        self.create_widgets()
        self.create_tractor_image()

        # Инициализация порта для ардуино
        self.arduino_port = None
        self.arduino_connected = False
        self.arduino_error = ""
        self.init_arduino_connection()

    def create_widgets(self):
        """Создает элементы интерфейса"""
        # Главный контейнер
        self.main_frame = tk.Frame(self.root, bg='#160B0B')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Левая панель - карта
        self.map_frame = tk.Frame(self.main_frame, width=self.field_width, height=self.field_height,
                                  bg='#160B0B', relief=tk.SUNKEN, borderwidth=2)
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Холст для карты
        self.canvas = tk.Canvas(self.map_frame, bg="white", cursor="crosshair", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.load_image()

        # Правая панель - управление (увеличена до 400px)
        self.control_frame = tk.Frame(self.main_frame, width=400, padx=10, pady=10, bg='#160B0B')
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Стиль для групп кнопок
        group_style = {
            'bg': '#160B0B',
            'fg': 'white',
            'padx': 5,
            'pady': 5,
            'relief': tk.RIDGE,
            'borderwidth': 2,
            'font': ('Arial', 10)
        }

        # Группа управления полигоном
        polygon_frame = tk.LabelFrame(self.control_frame, text=" Управление полигоном и траекторией ", **group_style)
        polygon_frame.pack(fill=tk.X, pady=5)

        # Кнопки управления полигоном (теперь в две колонки)
        buttons_frame = tk.Frame(polygon_frame, bg='#160B0B')
        buttons_frame.pack(fill=tk.X)

        self.polygon_button = ImageButton(
            buttons_frame,
            normal_img="Buttons/WhiteButtons/ZPoligonA.png",
            pressed_img="Buttons/WhiteButtons/ZPoligonD.png",
            command=self.toggle_polygon_mode
        )
        self.polygon_button.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.X, expand=True)

        ImageButton(
            buttons_frame,
            normal_img="Buttons/WhiteButtons/OPoligonA.png",
            pressed_img="Buttons/WhiteButtons/OPoligonD.png",
            command=self.clear_polygon
        ).pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.X, expand=True)

        ImageButton(
            polygon_frame,
            normal_img="Buttons/WhiteButtons/ClearA.png",
            pressed_img="Buttons/WhiteButtons/ClearD.png",
            command=self.clear_trajectory
        ).pack(pady=2, anchor='center', expand=True)

        # Группа ввода начальных координат
        coord_frame = tk.LabelFrame(self.control_frame, text=" Начальные координаты ", **group_style)
        coord_frame.pack(fill=tk.X, anchor="center", pady=5)

        self.manual_button = ImageButton(
            coord_frame,
            normal_img="Buttons/WhiteButtons/CoordsA.png",
            pressed_img="Buttons/WhiteButtons/CoordsD.png",
            command=self.set_start_coords_manually
        )

        self.manual_button.pack(side=tk.LEFT, padx=5, anchor='center')

        # Вертикальный стек для полей X и Y (теперь через grid)
        coord_entry_frame = tk.Frame(coord_frame, bg='#160B0B')
        coord_entry_frame.pack(side=tk.LEFT, padx=10, anchor='center')

        # Метки и поля координат с выравниванием по сетке
        tk.Label(coord_entry_frame, text="X:", fg='white', bg='#160B0B', font=('Comic Sans MS', 14)).grid(row=0,
                                                                                                          column=0,
                                                                                                          sticky="e",
                                                                                                          pady=2)
        self.entry_x = tk.Entry(coord_entry_frame, width=15, bg='#222222', fg='white', font=('Comic Sans MS', 14))
        self.entry_x.grid(row=0, column=1, pady=2)

        tk.Label(coord_entry_frame, text="Y:", fg='white', bg='#160B0B', font=('Comic Sans MS', 14)).grid(row=1,
                                                                                                          column=0,
                                                                                                          sticky="e",
                                                                                                          pady=2)
        self.entry_y = tk.Entry(coord_entry_frame, width=15, bg='#222222', fg='white', font=('Comic Sans MS', 14))
        self.entry_y.grid(row=1, column=1, pady=2)

        # Группа управления симуляцией
        sim_frame = tk.LabelFrame(self.control_frame, text=" Управление симуляцией ", **group_style)
        sim_frame.pack(fill=tk.X, pady=5)

        # Вложенный фрейм для кнопок возобновить/остановить
        sim_buttons_frame = tk.Frame(sim_frame, bg='#160B0B')
        sim_buttons_frame.pack(fill=tk.X, pady=5)

        ImageButton(
            sim_buttons_frame,
            normal_img="Buttons/WhiteButtons/ResumeA.png",
            pressed_img="Buttons/WhiteButtons/ResumeD.png",
            command=self.resume_simulation
        ).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        ImageButton(
            sim_buttons_frame,
            normal_img="Buttons/WhiteButtons/StopA.png",
            pressed_img="Buttons/WhiteButtons/StopD.png",
            command=self.stop_simulation
        ).pack(side=tk.RIGHT, padx=2, fill=tk.X, expand=True)

        self.start_button = ImageButton(
            sim_frame,
            normal_img="Buttons/WhiteButtons/StartSimA.png",
            pressed_img="Buttons/WhiteButtons/StartSimD.png",
            command=self.start_simulation
        )
        self.start_button.pack(pady=5, anchor='center', expand=True)

        # Группа управления масштабом
        zoom_frame = tk.LabelFrame(self.control_frame, text=" Управление масштабом ", **group_style)
        zoom_frame.pack(fill=tk.X, pady=5)

        # Фрейм для кнопок масштабирования (две колонки)
        zoom_buttons_frame = tk.Frame(zoom_frame, bg='#160B0B')
        zoom_buttons_frame.pack(fill=tk.X)

        ImageButton(
            zoom_buttons_frame,
            normal_img="Buttons/WhiteButtons/ScopePA.png",
            pressed_img="Buttons/WhiteButtons/ScopePD.png",
            command=lambda: self.zoom_image(1.2)
        ).pack(side=tk.LEFT, padx=2, pady=2, fill=tk.X, expand=True)

        ImageButton(
            zoom_buttons_frame,
            normal_img="Buttons/WhiteButtons/ScopeMA.png",
            pressed_img="Buttons/WhiteButtons/ScopeMD.png",
            command=lambda: self.zoom_image(0.8)
        ).pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.X, expand=True)

        ImageButton(
            zoom_frame,
            normal_img="Buttons/WhiteButtons/ResetA.png",
            pressed_img="Buttons/WhiteButtons/ResetD.png",
            command=self.reset_zoom
        ).pack(pady=5, anchor='center', expand=True)

        # Группа информации
        info_frame = tk.LabelFrame(self.control_frame, text=" Инструкция ", **group_style)
        info_frame.pack(fill=tk.X, pady=5)

        instructions = [
            "1. Нажмите 'Задать полигон'",
            "2. Отметьте 4 угла поля (клик левой кнопкой)",
            "3. Укажите начальную точку внутри поля",
            "   - можно кликнуть на карте",
            "   - или ввести координаты вручную",
            "4. Нажмите 'Старт симуляции'",
            "",
            "Управление картой:",
            "- Масштаб: колесо мыши",
            "- Перемещение: средняя кнопка мыши"
        ]

        for step in instructions:
            tk.Label(info_frame, text=step, anchor=tk.W, justify=tk.LEFT,
                     bg='#160B0B', fg='white', font=('Arial', 10)).pack(fill=tk.X, padx=5, pady=2)

        # Статус бар
        self.status_bar = StatusBar(self.main_frame, width=300)
        self.status_bar.place(x=self.field_width - 300, y=0, width=300, height=50)
        self.status_bar.lift()

        # Привязка событий
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Button-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.on_pan)
        self.canvas.bind("<ButtonRelease-2>", self.end_pan)

    def init_arduino_connection(self):
        """Автоматически ищет и подключается к Arduino"""
        try:
            ports = list(serial.tools.list_ports.comports())
            for port in ports:
                if 'Arduino' in port.description or 'CH340' in port.description or 'USB-SERIAL' in port.description:
                    self.arduino_port = serial.Serial(port.device, 9600, timeout=1)
                    time.sleep(2)  # Дать время Arduino на перезапуск
                    self.arduino_connected = True
                    # self.statuse_bar.config(text=f"Arduino подключена: {port.device}")
                    return
            self.arduino_connected = False
            # self.statuse_bar.config(text="Arduino не найдена")
        except Exception as e:
            self.arduino_connected = False
            self.arduino_error = str(e)
            self.statuse_bar.config(text=f"Ошибка подключения Arduino: {self.arduino_error}")

    def send_angle_to_arduino(self, angle_diff):
        """Отправляет угол поворота на Arduino, если соединение установлено"""
        if self.arduino_connected and self.arduino_port:
            try:
                msg = f"{angle_diff:.2f}\n"
                self.arduino_port.write(msg.encode('utf-8'))
                # Можно добавить чтение ответа от Arduino для подтверждения
                # response = self.arduino_port.readline().decode().strip()
                # self.statuse_bar.config(text=f"Отправлено: {msg.strip()} | Ответ: {response}")
            except Exception as e:
                self.statuse_bar.config(text=f"Ошибка передачи: {e}")
                self.arduino_connected = False
        else:
            self.statuse_bar.config(text="Arduino не подключена")

    def set_start_coords_manually(self):
        """Устанавливает начальные координаты трактора вручную через текстовые поля"""
        if len(self.selection_points) != 4:
            self.statuse_bar.config(text="Сначала задайте полигон (4 точки)")
            return
        try:
            # Получаем координаты из полей ввода
            x = float(self.entry_x.get())
            y = float(self.entry_y.get())

            # Проверяем, что точка внутри полигона
            polygon = self.selection_points
            if not self.point_in_polygon((x, y), polygon):
                self.statuse_bar.config(text="Точка находится вне полигона!")
                return

            # Устанавливаем начальные координаты
            self.start_x = x
            self.start_y = y

            # Отрисовываем траекторию
            self.draw_trajectory()

            # Отображаем трактор в начальной точке
            if not hasattr(self, 'tractor'):
                self.tractor = {
                    'orig_x': x,
                    'orig_y': y,
                    'angle': self.calculate_initial_angle(),
                    'speed': 0,
                    'target_index': 0
                }
            else:
                self.tractor['orig_x'] = x
                self.tractor['orig_y'] = y
                self.tractor['angle'] = self.calculate_initial_angle()

            self.redraw_all()
            self.statuse_bar.config(text=f"Начальная точка установлена: ({x:.1f}, {y:.1f})")

        except ValueError:
            self.statuse_bar.config(text="Ошибка: введите числовые координаты")

    def toggle_polygon_mode(self):
        """Переключает режим задания полигона"""
        self.polygon_mode = not self.polygon_mode
        if self.polygon_mode:
            self.statuse_bar.config(text="Режим задания полигона: кликните по 4 точкам границы поля")
            self.selection_points = []  # Очищаем предыдущие точки
            self.redraw_all()
        else:
            self.statuse_bar.config(text="Готов к работе")
            if len(self.selection_points) == 4:
                self.statuse_bar.config(text="Полигон задан. Укажите начальную точку внутри поля")

    def clear_polygon(self):
        """Очищает текущий полигон"""
        self.selection_points = []
        self.polygon_mode = False
        self.redraw_all()
        self.statuse_bar.config(text="Полигон очищен. Готов к работе")

    def stop_simulation(self):
        """Останавливает симуляцию движения трактора"""
        self.simulation_paused = True
        self.position_refining = False
        self.statuse_bar.config(text="Симуляция остановлена")
        self.start_button.config(state=tk.NORMAL)

    def clear_trajectory(self):
        """Очищает текущую траекторию"""
        self.selection_points = []
        self.trajectory_points = []
        self.tractor = None
        self.simulation_active = False
        self.simulation_paused = False
        self.polygon_mode = False
        self.position_refining = False
        self.start_button.config(state=tk.NORMAL)
        self.canvas.delete("all")
        self.load_image()
        self.statuse_bar.config(text="Траектория очищена. Готов к новой работе")

    def resume_simulation(self):
        """Возобновляет симуляцию движения трактора"""
        if self.simulation_paused and self.tractor:
            self.simulation_paused = False
            self.animate_tractor()
            self.statuse_bar.config(text="Симуляция продолжается")

    def load_image(self):
        """Загружает изображение карты с обработкой ошибок"""
        try:
            self.canvas.delete("all")
            self.original_image = Image.open("map.png") if os.path.exists("map.png") else self.create_blank_map()
            self.image = self.original_image.copy()

            # Масштабируем до размеров холста
            img_width, img_height = self.original_image.size
            ratio = min(self.field_width / img_width, self.field_height / img_height) * self.initial_zoom
            self.scale_factor = ratio

            self.image = self.image.resize(
                (int(img_width * ratio), int(img_height * ratio)),
                Image.LANCZOS
            )

            self.image_tk = ImageTk.PhotoImage(self.image)
            self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.center_image()
            self.statuse_bar.config(text="Карта успешно загружена")

        except Exception as e:
            self.statuse_bar.config(text=f"Ошибка загрузки карты: {str(e)}")
            self.create_blank_map()

    def create_blank_map(self):
        """Создает пустую карту, если файл не найден"""
        self.original_image = Image.new("RGB", (1000, 800), color="white")
        draw = ImageDraw.Draw(self.original_image)
        draw.text((100, 100), "Карта не найдена\nСоздана пустая карта", fill="black")
        return self.original_image

    def start_pan(self, event):
        """Начинает перемещение карты"""
        self.is_panning = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.canvas.config(cursor="fleur")

    def on_pan(self, event):
        """Обрабатывает перемещение карты"""
        if self.is_panning:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y

            self.image_offset_x += dx
            self.image_offset_y += dy
            self.canvas.move(self.image_id, dx, dy)

            self.drag_start_x = event.x
            self.drag_start_y = event.y
            self.redraw_all()

    def end_pan(self, event):
        """Завершает перемещение карты"""
        self.is_panning = False
        self.canvas.config(cursor="")

    def create_tractor_image(self):
        """Создает изображение трактора из PNG"""
        try:
            if os.path.exists("Tratata.png"):
                self.original_tractor_img = Image.open("Tratata.png").convert("RGBA")
            else:
                raise FileNotFoundError("Файл Tratata.png не найден")
        except Exception as e:
            print(f"Ошибка загрузки изображения трактора: {e}")
            self.original_tractor_img = Image.new("RGBA", (30, 30), (0, 0, 0, 0))  # Пустое прозрачное изображение
            draw = ImageDraw.Draw(self.original_tractor_img)
            draw.rectangle([5, 5, 25, 25], fill="red")  # Просто красный квадрат как заглушка

    def draw_tractor(self):
        if not self.tractor or not self.original_tractor_img:
            return

        # Кэширование повернутого изображения
        angle = self.tractor['angle'] + self.ANGLE_OFFSET
        cache_key = f"{angle}_{self.scale_factor}"

        if not hasattr(self, 'tractor_cache'):
            self.tractor_cache = {}

        if cache_key not in self.tractor_cache:
            # Масштабирование и поворот только при изменении параметров
            scaled_size = int(self.TRACTOR_SIZE * self.scale_factor)
            aspect = self.original_tractor_img.width / self.original_tractor_img.height
            scaled_img = self.original_tractor_img.resize(
                (int(scaled_size * aspect), scaled_size),
                Image.LANCZOS
            )
            rotated_img = scaled_img.rotate(angle, expand=True, resample=Image.BICUBIC)
            self.tractor_cache[cache_key] = ImageTk.PhotoImage(rotated_img)

        # Используем кэшированное изображение
        x, y = self.transform_coords(self.tractor['orig_x'], self.tractor['orig_y'])
        if self.tractor_id:
            self.canvas.delete(self.tractor_id)
        self.tractor_id = self.canvas.create_image(
            x, y,
            image=self.tractor_cache[cache_key],
            tags="tractor",
            anchor=tk.CENTER
        )

    def zoom_image(self, factor):
        """Масштабирует изображение с центром на текущей позиции мыши"""
        if not self.original_image:
            return

        # Сохраняем предыдущий масштаб
        old_scale = self.scale_factor

        # Применяем новый масштаб
        self.scale_factor *= factor
        self.scale_factor = max(0.1, min(self.scale_factor, 5.0))  # Ограничиваем масштаб

        # Вычисляем новые размеры
        width = int(self.original_image.width * self.scale_factor)
        height = int(self.original_image.height * self.scale_factor)

        # Масштабируем изображение
        self.image = self.original_image.resize((width, height), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

        # Обновляем изображение на холсте
        self.canvas.itemconfig(self.image_id, image=self.image_tk)

        # Корректируем положение, чтобы масштабирование происходило относительно центра
        self.image_offset_x *= self.scale_factor / old_scale
        self.image_offset_y *= self.scale_factor / old_scale
        self.canvas.coords(self.image_id, self.image_offset_x, self.image_offset_y)

        self.redraw_all()

    def reset_zoom(self):
        """Сбрасывает масштаб и положение изображения"""
        if not self.original_image:
            return

        self.scale_factor = 1.0
        self.image_offset_x = 0
        self.image_offset_y = 0

        self.image = self.original_image.copy()
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.image_id, image=self.image_tk)
        self.canvas.coords(self.image_id, 0, 0)

        self.redraw_all()

    def redraw_all(self):
        """Перерисовывает все элементы"""
        self.canvas.delete("point")
        self.canvas.delete("line")
        self.canvas.delete("tractor")

        # Только если нужно перерисовать точки и линии
        for point in self.selection_points:
            x, y = self.transform_coords(*point)
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="green", tags="point")

        if len(self.selection_points) == 4:
            self.draw_boundary()

        if len(self.trajectory_points) > 1:
            self.draw_trajectory_lines()

        if hasattr(self, 'tractor'):
            self.draw_tractor()

    def transform_coords(self, orig_x, orig_y):
        """Преобразует координаты с учетом масштаба и смещения"""
        return (
            orig_x * self.scale_factor + self.image_offset_x,
            orig_y * self.scale_factor + self.image_offset_y
        )

    def inverse_transform_coords(self, canvas_x, canvas_y):
        """Обратное преобразование координат"""
        return (
            (canvas_x - self.image_offset_x) / self.scale_factor,
            (canvas_y - self.image_offset_y) / self.scale_factor
        )

    def on_click(self, event):
        """Обработчик клика мыши"""
        if self.is_dragging or self.is_panning:
            return

        orig_x, orig_y = self.inverse_transform_coords(event.x, event.y)

        if self.polygon_mode and len(self.selection_points) < 4:
            self.selection_points.append((orig_x, orig_y))
            x, y = self.transform_coords(orig_x, orig_y)
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="green", tags="point")

            if len(self.selection_points) == 4:
                self.draw_boundary()
                self.polygon_mode = False
                self.statuse_bar.config(text="Полигон задан. Укажите начальную точку внутри поля")

        elif len(self.selection_points) == 4 and not self.polygon_mode:
            self.start_x = orig_x
            self.start_y = orig_y
            self.draw_trajectory()

    def draw_boundary(self):
        """Рисует границы участка"""
        points = [self.transform_coords(p[0], p[1]) for p in self.selection_points]
        for i in range(4):
            self.canvas.create_line(
                points[i][0], points[i][1],
                points[(i + 1) % 4][0], points[(i + 1) % 4][1],
                fill="red", width=2, tags="line"
            )

    def prepare_working_grid(self):
        """Создает рабочую сетку на основе полигона"""
        polygon = self.selection_points
        self.working_grid = []

        min_x = min(p[0] for p in polygon)
        max_x = max(p[0] for p in polygon)
        min_y = min(p[1] for p in polygon)
        max_y = max(p[1] for p in polygon)

        step = self.TRACTOR_WIDTH  # Используем ширину трактора как шаг

        for y in range(int(min_y), int(max_y), int(step)):
            row = []
            for x in range(int(min_x), int(max_x), int(step)):
                center_x = x + step // 2
                center_y = y + step // 2
                if self.point_in_polygon((center_x, center_y), polygon):
                    row.append((x, y, False))
                else:
                    row.append(None)
            self.working_grid.append(row)

    def find_nearest_grid_cell(self, x, y):
        min_dist = float('inf')
        nearest = (None, None)

        for row_idx, row in enumerate(self.working_grid):
            for col_idx, cell in enumerate(row):
                if cell and not cell[2]:
                    cell_x = cell[0] + self.TRACTOR_WIDTH // 2
                    cell_y = cell[1] + self.TRACTOR_WIDTH // 2
                    dist = math.hypot(x - cell_x, y - cell_y)
                    if dist < min_dist:
                        min_dist = dist
                        nearest = (col_idx, row_idx)
        return nearest

    def build_trajectory(self):
        if not hasattr(self, 'start_x') or not self.working_grid:
            return

        start_col, start_row = self.find_nearest_grid_cell(self.start_x, self.start_y)
        if start_col is None:
            return

        self.trajectory_points = [(self.start_x, self.start_y)]
        rows = len(self.working_grid)
        cols = len(self.working_grid[0]) if rows > 0 else 0

        moving_right = start_col < cols // 2

        row_queue = [start_row]
        processed_rows = {start_row}

        while row_queue:
            current_row = row_queue.pop(0)

            col_range = range(cols) if moving_right else reversed(range(cols))
            row_has_cells = False

            for col in col_range:
                cell = self.working_grid[current_row][col]
                if cell and not cell[2]:
                    x, y, _ = cell
                    center = (x + self.TRACTOR_WIDTH // 2, y + self.TRACTOR_WIDTH // 2)

                    if self.trajectory_points:
                        last_point = self.trajectory_points[-1]
                        if abs(last_point[1] - center[1]) > self.TRACTOR_WIDTH // 2:
                            self.trajectory_points.append((last_point[0], center[1]))

                    self.trajectory_points.append(center)
                    self.working_grid[current_row][col] = (x, y, True)
                    row_has_cells = True

                    for dy in [-1, 1]:
                        new_row = current_row + dy
                        if 0 <= new_row < rows and new_row not in processed_rows:
                            if any(c and not c[2] for c in self.working_grid[new_row]):
                                row_queue.append(new_row)
                                processed_rows.add(new_row)

            if row_has_cells:
                moving_right = not moving_right

    def smooth_trajectory(self):
        if len(self.trajectory_points) < 2:
            self.smoothed_trajectory = self.trajectory_points.copy()
            return

        self.smoothed_trajectory = [self.trajectory_points[0]]

        for i in range(1, len(self.trajectory_points) - 1):
            prev = self.trajectory_points[i - 1]
            curr = self.trajectory_points[i]
            next = self.trajectory_points[i + 1]

            # Пропустить сглаживание для самого первого поворота
            if i == 1:
                self.smoothed_trajectory.append(curr)
                continue

            dx1, dy1 = curr[0] - prev[0], curr[1] - prev[1]
            dx2, dy2 = next[0] - curr[0], next[1] - curr[1]

            if (dx1 * dy2 - dy1 * dx2) != 0:
                self.add_turn(prev, curr, next)
            else:
                self.smoothed_trajectory.append(curr)

        self.smoothed_trajectory.append(self.trajectory_points[-1])

    def add_turn(self, prev, turn, next):
        dx1, dy1 = turn[0] - prev[0], turn[1] - prev[1]
        dx2, dy2 = next[0] - turn[0], next[1] - turn[1]
        cross = dx1 * dy2 - dy1 * dx2
        angle1 = math.atan2(dy1, dx1)
        angle2 = math.atan2(dy2, dx2)
        angle_diff = angle2 - angle1

        if angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        elif angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        # Новая проверка: если поворот почти 180 градусов, не рисуем дугу
        if abs(angle_diff) > math.radians(160):
            self.smoothed_trajectory.append(turn)
            return

        if abs(angle_diff) > 0.1:
            radius = self.TRACTOR_WIDTH / 2
            if cross > 0:
                cx = turn[0] - radius * math.sin(angle1)
                cy = turn[1] + radius * math.cos(angle1)
            else:
                cx = turn[0] + radius * math.sin(angle1)
                cy = turn[1] - radius * math.cos(angle1)

            start_angle = math.atan2(prev[1] - cy, prev[0] - cx)
            end_angle = math.atan2(next[1] - cy, next[0] - cx)

            if cross > 0 and end_angle < start_angle:
                end_angle += 2 * math.pi
            elif cross < 0 and end_angle > start_angle:
                end_angle -= 2 * math.pi

            steps = 10
            for i in range(1, steps):
                t = i / steps
                angle = start_angle + t * (end_angle - start_angle)
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                self.smoothed_trajectory.append((x, y))
        else:
            self.smoothed_trajectory.append(turn)

    def draw_trajectory(self):
        if len(self.selection_points) != 4 or not hasattr(self, 'start_x'):
            return

        if not self.point_in_polygon((self.start_x, self.start_y), self.selection_points):
            return

        self.prepare_working_grid()
        self.build_trajectory()
        self.smooth_trajectory()

        self.trajectory_points = self.smoothed_trajectory
        self.draw_trajectory_lines()

    def simplify_trajectory(self):
        """Упрощает траекторию, удаляя лишние точки"""
        if len(self.trajectory_points) < 3:
            return

        simplified = [self.trajectory_points[0]]
        for i in range(1, len(self.trajectory_points) - 1):
            x1, y1 = simplified[-1]
            x2, y2 = self.trajectory_points[i]
            x3, y3 = self.trajectory_points[i + 1]

            area = abs(0.5 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)))
            if area >= 0.1:
                simplified.append(self.trajectory_points[i])

        simplified.append(self.trajectory_points[-1])
        self.trajectory_points = simplified

    def draw_trajectory_lines(self):
        """Рисует линии траектории"""
        if len(self.trajectory_points) < 2:
            return

        points = [self.transform_coords(p[0], p[1]) for p in self.trajectory_points]
        for i in range(1, len(points)):
            self.canvas.create_line(
                points[i - 1][0], points[i - 1][1],
                points[i][0], points[i][1],
                fill="green", width=2, tags="line"
            )

    def point_in_polygon(self, point, polygon):
        """Проверяет, находится ли точка внутри полигона"""
        x, y = point
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def on_mousewheel(self, event):
        """Обработчик колесика мыши для масштабирования"""
        if event.num == 5 or (hasattr(event, 'delta') and event.delta < 0):
            self.zoom_image(0.9)
        elif event.num == 4 or (hasattr(event, 'delta') and event.delta > 0):
            self.zoom_image(1.1)

    def simulate_position_refining(self):
        """Симулирует процесс уточнения местоположения"""
        if not self.position_refining:
            return

        # Случайное изменение координат трактора (имитация уточнения)
        if self.tractor:
            self.tractor['orig_x'] += random.uniform(-5, 5)
            self.tractor['orig_y'] += random.uniform(-5, 5)
            self.redraw_all()

        # Продолжаем уточнение или завершаем
        if self.position_refining_steps > 0:
            self.position_refining_steps -= 1
            self.statuse_bar.config(text=f"Уточнение местоположения... Осталось: {self.position_refining_steps} сек")
            self.root.after(1000, self.simulate_position_refining)
        else:
            self.position_refining = False
            self.start_button.config(state=tk.NORMAL)
            self.statuse_bar.config(text="Местоположение уточнено. Готов к работе")
            self.start_simulation_after_refining()

    def start_simulation_after_refining(self):
        """Начинает симуляцию после уточнения местоположения"""
        if len(self.trajectory_points) < 2:
            return

        self.tractor = {
            'orig_x': self.trajectory_points[0][0],
            'orig_y': self.trajectory_points[0][1],
            'angle': self.calculate_initial_angle(),
            'speed': self.MAX_SPEED,
            'target_index': 1
        }

        self.simulation_active = True
        self.simulation_paused = False
        self.animate_tractor()

    def start_simulation(self):
        """Начинает процесс симуляции с уточнением местоположения"""
        if len(self.trajectory_points) < 2:
            return

        # Блокируем кнопку старта
        self.start_button.config(state=tk.DISABLED)
        self.statuse_bar.config(text="Начато уточнение местоположения...")

        # Устанавливаем параметры уточнения
        self.position_refining = True
        self.position_refining_steps = random.randint(2, 5)  # Случайное время уточнения (3-7 сек)

        # Создаем начальное положение трактора с некоторой ошибкой
        self.tractor = {
            'orig_x': self.trajectory_points[0][0] + random.uniform(-20, 20),
            'orig_y': self.trajectory_points[0][1] + random.uniform(-20, 20),
            'angle': self.calculate_initial_angle() + random.uniform(-30, 30),
            'speed': 0,  # На время уточнения скорость = 0
            'target_index': 1
        }

        # Запускаем процесс уточнения
        self.simulate_position_refining()

    def center_image(self):
        """Центрирует изображение на холсте"""
        if not self.image:
            return

        self.image_offset_x = (self.field_width - self.image.width) // 2
        self.image_offset_y = (self.field_height - self.image.height) // 2
        self.canvas.coords(self.image_id, self.image_offset_x, self.image_offset_y)

    def calculate_initial_angle(self):
        """Вычисляет начальный угол направления"""
        if len(self.trajectory_points) < 2:
            return 0

        x1, y1 = self.trajectory_points[0]
        x2, y2 = self.trajectory_points[1]
        dx = x2 - x1
        dy = y2 - y1
        return math.degrees(math.atan2(-dy, dx))

    def animate_tractor(self):
        if not self.tractor or self.tractor['target_index'] >= len(self.trajectory_points) or self.simulation_paused:
            return

        # 1. Получаем текущие координаты и цель
        current_x, current_y = self.tractor['orig_x'], self.tractor['orig_y']
        target_x, target_y = self.trajectory_points[self.tractor['target_index']]

        # 2. Вычисляем вектор к цели
        dx = target_x - current_x
        dy = target_y - current_y
        distance = math.hypot(dx, dy)

        # 3. Рассчитываем углы
        desired_angle = math.degrees(math.atan2(-dy, dx))
        current_angle = self.tractor['angle']

        # 4. Вычисляем разницу углов (оптимальное направление)
        angle_diff = (desired_angle - current_angle + 180) % 360 - 180

        # === Расчёт угла поворота руля ===
        MAX_STEERING_ANGLE = 90
        STEERING_RETURN_RATE = 2.5  # градусов за кадр
        STEERING_SCALE = 3
        current_steering = self.tractor.get('steering_angle', 0)

        if abs(angle_diff) > 5:
            target_steering_angle = max(
                -MAX_STEERING_ANGLE,
                min(MAX_STEERING_ANGLE, angle_diff * STEERING_SCALE)
            )
            # target_steering_angle = max(-MAX_STEERING_ANGLE, min(MAX_STEERING_ANGLE, (angle_diff / 180) * MAX_STEERING_ANGLE))
            SMOOTHING_FACTOR = 0.15
            self.tractor['steering_angle'] = (
                    current_steering * (1 - SMOOTHING_FACTOR) + target_steering_angle * SMOOTHING_FACTOR
            )
        else:
            # Плавное возвращение к нулю
            if abs(current_steering) <= STEERING_RETURN_RATE:
                self.tractor['steering_angle'] = 0
            else:
                self.tractor['steering_angle'] = current_steering - STEERING_RETURN_RATE * (
                    1 if current_steering > 0 else -1)

        servo_angle = int(90 + self.tractor['steering_angle'])
        servo_angle = max(0, min(180, servo_angle))  # гарантируем диапазон 0–180
        print(servo_angle)
        self.send_angle_to_arduino(servo_angle)

        # ================================
        # 5. Логика поворота
        if abs(angle_diff) > 5:
            turn_direction = 1 if angle_diff > 0 else -1
            turn_amount = min(self.TURN_RATE, abs(angle_diff))
            self.tractor['angle'] = (current_angle + turn_direction * turn_amount) % 360

        update_delay = 16  # ~60 FPS

        # 6. Движение вперед
        angle_rad = math.radians(self.tractor['angle'])
        self.tractor['orig_x'] += self.tractor['speed'] * math.cos(angle_rad)
        self.tractor['orig_y'] -= self.tractor['speed'] * math.sin(angle_rad)

        # 7. Переход к следующей точке
        if distance < self.TRACTOR_WIDTH * 0.7:
            self.tractor['target_index'] += 1

        # 8. Обновление камеры и отрисовка
        self.cinematic_camera_follow()
        self.redraw_all()
        self.root.after(update_delay, self.animate_tractor)

    def cinematic_camera_follow(self):
        if not self.tractor:
            return

        # Более агрессивные параметры слежения
        ZOOM_TARGET = 3.0
        SMOOTHING = 0.5

        # Упрощенный расчет координат
        tractor_x, tractor_y = self.transform_coords(
            self.tractor['orig_x'],
            self.tractor['orig_y']
        )

        # Оптимизированный расчет смещения
        target_offset_x = self.image_offset_x + (self.field_width / 2 - tractor_x) * 1.3
        target_offset_y = self.image_offset_y + (self.field_height / 2 - tractor_y) * 1.3

        # Оптимизация масштабирования
        if not hasattr(self, 'last_scale_update'):
            self.last_scale_update = time.time()

        # Обновляем масштаб реже (не каждый кадр)
        if time.time() - self.last_scale_update > 0.1:  # 10 раз в секунду
            target_scale = min(ZOOM_TARGET, 3.0 + self.tractor['speed'] * 0.2)
            self.scale_factor += (target_scale - self.scale_factor) * SMOOTHING
            self.last_scale_update = time.time()

        # Плавное перемещение камеры
        self.image_offset_x += (target_offset_x - self.image_offset_x) * SMOOTHING * 2
        self.image_offset_y += (target_offset_y - self.image_offset_y) * SMOOTHING * 2

        # Оптимизированное обновление карты
        self._update_map_image()

    def _update_map_image(self):
        """Оптимизированное обновление изображения карты"""
        if not hasattr(self, 'last_scale') or abs(self.last_scale - self.scale_factor) > 0.01:
            width = int(self.original_image.width * self.scale_factor)
            height = int(self.original_image.height * self.scale_factor)

            # Используем более быстрый метод ресайза для больших изображений
            resample_method = Image.NEAREST if self.scale_factor > 2 else Image.LANCZOS

            self.image = self.original_image.resize((width, height), resample_method)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.last_scale = self.scale_factor

        self.canvas.itemconfig(self.image_id, image=self.image_tk)
        self.canvas.coords(self.image_id, self.image_offset_x, self.image_offset_y)

    def end_pan(self, event):
        """Завершает перемещение карты"""
        self.is_panning = False
        self.canvas.config(cursor="")

    def on_drag(self, event):
        """Обработчик перетаскивания"""
        if not self.is_dragging and len(self.selection_points) < 1:
            self.is_dragging = True
            self.drag_start_x = event.x
            self.drag_start_y = event.y
        elif self.is_dragging:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y

            self.image_offset_x += dx
            self.image_offset_y += dy
            self.canvas.coords(self.image_id, self.image_offset_x, self.image_offset_y)

            self.drag_start_x = event.x
            self.drag_start_y = event.y

            self.redraw_all()

    def on_release(self, event):
        """Обработчик отпускания кнопки мыши"""
        self.is_dragging = False
        self.is_panning = False


if __name__ == "__main__":
    root = tk.Tk()
    GifLoadingScreen(root, TractorSimulator)
    root.mainloop()
