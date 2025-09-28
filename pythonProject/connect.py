# connect.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# Importar el backend desde main
from main import DatabaseManager

# Configurar tamaño de ventana
Window.size = (360, 640)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = App.get_running_app().db

        # Layout principal
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Header
        header = BoxLayout(orientation='vertical', size_hint=(1, 0.15))
        with header.canvas.before:
            Color(0.18, 0.49, 0.20, 1)
            self.rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=self._update_rect, pos=self._update_rect)

        title = Label(
            text='ReciclApp',
            font_size='24sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        header.add_widget(title)
        main_layout.add_widget(header)

        # Contenido desplazable
        scroll = ScrollView()
        content = GridLayout(cols=1, spacing=15, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        sections = [
            ('Base de datos de materiales', 'materiales'),
            ('Guía de separación de residuos', 'guia'),
            ('Mapa de puntos de reciclaje', 'mapa'),
            ('Directorio de empresas', 'empresas'),
            ('Noticias y tips', 'noticias'),
            ('Recordatorios y avisos', 'recordatorios')
        ]

        for text, screen_name in sections:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=80,
                background_color=(0.18, 0.49, 0.20, 1),
                background_normal='',
                color=(1, 1, 1, 1),
                font_size='16sp'
            )
            btn.bind(on_press=lambda instance, sn=screen_name:
            self.switch_to_screen(sn))
            content.add_widget(btn)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def switch_to_screen(self, screen_name):
        self.manager.current = screen_name


class MaterialesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = App.get_running_app().db

        layout = BoxLayout(orientation='vertical', padding=10)

        # Botón volver
        back_btn = Button(
            text='← Volver',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.8, 0.8, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        # Título
        title = Label(
            text='Base de datos de materiales',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True
        )
        layout.add_widget(title)

        # Lista de materiales
        self.scroll = ScrollView()
        self.content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter('height'))

        self.scroll.add_widget(self.content)
        layout.add_widget(self.scroll)

        self.add_widget(layout)

    def on_enter(self):
        # Cargar materiales cuando se entra a la pantalla
        self.cargar_materiales()

    def cargar_materiales(self):
        self.content.clear_widgets()
        materiales = self.db.get_materiales()

        if not materiales:
            error_label = Label(
                text='No se pudieron cargar los materiales\nVerifica la conexión a la base de datos',
                font_size='16sp',
                color=(1, 0, 0, 1)
            )
            self.content.add_widget(error_label)
            return

        categoria_actual = ""
        for material in materiales:
            id_material, categoria, nombre, descripcion, tiempo = material

            # Agregar título de categoría si cambió
            if categoria != categoria_actual:
                categoria_actual = categoria
                cat_label = Label(
                    text=f'[b]{categoria}[/b]',
                    size_hint_y=None,
                    height=40,
                    font_size='18sp',
                    markup=True,
                    color=(0.2, 0.4, 0.2, 1)
                )
                self.content.add_widget(cat_label)

            # Botón del material
            btn = Button(
                text=f'{nombre}\n{descripcion}',
                size_hint_y=None,
                height=80,
                background_color=(0.18, 0.49, 0.20, 0.8),
                background_normal='',
                color=(1, 1, 1, 1),
                font_size='14sp',
                halign='left',
                valign='center'
            )
            btn.bind(on_press=lambda instance, mid=id_material:
            self.show_material_detail(mid))
            self.content.add_widget(btn)

    def go_back(self, instance):
        self.manager.current = 'main'

    def show_material_detail(self, id_material):
        self.manager.get_screen('material_detail').set_material(id_material)
        self.manager.current = 'material_detail'


class MaterialDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = App.get_running_app().db
        self.layout = BoxLayout(orientation='vertical', padding=15)

        # Botón volver
        back_btn = Button(
            text='← Volver a materiales',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.8, 0.8, 1)
        )
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.scroll = ScrollView()
        self.content = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter('height'))

        self.scroll.add_widget(self.content)
        self.layout.add_widget(self.scroll)

        self.add_widget(self.layout)

    def set_material(self, id_material):
        self.content.clear_widgets()
        material = self.db.get_material_by_id(id_material)

        if not material:
            error_label = Label(
                text='Material no encontrado',
                font_size='18sp',
                color=(1, 0, 0, 1)
            )
            self.content.add_widget(error_label)
            return

        id_material, categoria, nombre, descripcion, tiempo = material

        # Título
        title = Label(
            text=f'# {nombre}',
            size_hint_y=None,
            height=40,
            font_size='22sp',
            bold=True
        )
        self.content.add_widget(title)

        # Categoría
        cat_label = Label(
            text=f'Categoría: {categoria}',
            size_hint_y=None,
            height=30,
            font_size='16sp',
            color=(0.4, 0.4, 0.4, 1)
        )
        self.content.add_widget(cat_label)

        # Descripción
        desc_label = Label(
            text=f'[b]Descripción:[/b]\n{descripcion}',
            size_hint_y=None,
            height=80,
            font_size='16sp',
            markup=True,
            text_size=(300, None)
        )
        self.content.add_widget(desc_label)

        # Tiempo de descomposición
        tiempo_label = Label(
            text=f'[b]Tiempo de descomposición:[/b]\n{tiempo}',
            size_hint_y=None,
            height=60,
            font_size='16sp',
            markup=True,
            text_size=(300, None)
        )
        self.content.add_widget(tiempo_label)

        # Información adicional
        info_label = Label(
            text='[b]Instrucciones de reciclaje:[/b]\n\n• Limpia el material antes de reciclar\n• Separa por tipo de material\n• Compacta para ahorrar espacio\n• Sigue las indicaciones locales',
            size_hint_y=None,
            height=120,
            font_size='14sp',
            markup=True,
            text_size=(300, None)
        )
        self.content.add_widget(info_label)

    def go_back(self, instance):
        self.manager.current = 'materiales'


# Otras pantallas (simplificadas)
class GuiaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20)

        back_btn = Button(
            text='← Volver',
            size_hint=(1, 0.1),
            background_color=(0.8, 0.8, 0.8, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        content = Label(
            text='Guía de separación de residuos\n\nAprende a separar correctamente tus residuos según el tipo de material.',
            font_size='18sp'
        )
        layout.add_widget(content)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'main'


class MapaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20)

        back_btn = Button(
            text='← Volver',
            size_hint=(1, 0.1),
            background_color=(0.8, 0.8, 0.8, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        content = Label(
            text='Mapa de puntos de reciclaje\n\nEncuentra los centros de reciclaje más cercanos a tu ubicación.',
            font_size='18sp'
        )
        layout.add_widget(content)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'main'


class EmpresasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20)

        back_btn = Button(
            text='← Volver',
            size_hint=(1, 0.1),
            background_color=(0.8, 0.8, 0.8, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        content = Label(
            text='Directorio de empresas\n\nEncuentra empresas de recolección y reciclaje en tu área.',
            font_size='18sp'
        )
        layout.add_widget(content)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'main'


class NoticiasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20)

        back_btn = Button(
            text='← Volver',
            size_hint=(1, 0.1),
            background_color=(0.8, 0.8, 0.8, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        content = Label(
            text='Noticias y tips\n\nMantente informado sobre las últimas novedades en reciclaje.',
            font_size='18sp'
        )
        layout.add_widget(content)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'main'


class RecordatoriosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20)

        back_btn = Button(
            text='← Volver',
            size_hint=(1, 0.1),
            background_color=(0.8, 0.8, 0.8, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        content = Label(
            text='Recordatorios y avisos\n\nConfigura recordatorios para tus días de reciclaje.',
            font_size='18sp'
        )
        layout.add_widget(content)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'main'


class ReciclApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseManager()

    def build(self):
        sm = ScreenManager()

        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(MaterialesScreen(name='materiales'))
        sm.add_widget(MaterialDetailScreen(name='material_detail'))
        sm.add_widget(GuiaScreen(name='guia'))
        sm.add_widget(MapaScreen(name='mapa'))
        sm.add_widget(EmpresasScreen(name='empresas'))
        sm.add_widget(NoticiasScreen(name='noticias'))
        sm.add_widget(RecordatoriosScreen(name='recordatorios'))

        return sm

    def on_stop(self):
        # Cerrar conexión a la base de datos al salir
        self.db.close()


if __name__ == '__main__':
    ReciclApp().run()