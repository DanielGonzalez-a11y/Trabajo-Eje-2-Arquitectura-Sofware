import webbrowser
import os
import threading
from datetime import datetime, timedelta
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from typing import List
from models.entities import Material, CentroReciclaje, Noticia, Recordatorio

Window.size = (360, 640)


class BaseScreen(Screen):
    """Clase base para todas las pantallas con funcionalidades comunes"""

    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        # Fondo verde claro para todas las pantallas
        with self.canvas.before:
            Color(0.9, 0.96, 0.9, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos


class RoundedButton(Button):
    """Botón personalizado con bordes redondeados y transparencia"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.18, 0.49, 0.20, 0.8)
        self.background_normal = ''
        self.color = (1, 1, 1, 1)
        self.font_size = '16sp'
        self.halign = 'center'
        self.valign = 'middle'
        self.text_size = (None, None)  # Permitir auto-ajuste
        self.shorten = True  # Acortar texto si es muy largo
        self.markup = True  # Permitir markup

        # Bordes redondeados
        with self.canvas.before:
            Color(0.18, 0.49, 0.20, 0.8)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


class MainScreen(BaseScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(controller, **kwargs)
        self._crear_ui()

    def _crear_ui(self):
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
            btn = RoundedButton(
                text=text,
                size_hint_y=None,
                height=80
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


class MaterialesScreen(BaseScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(controller, **kwargs)
        self.controller.set_on_materiales_loaded(self._on_materiales_loaded)
        self._crear_ui()

    def _crear_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10)

        # Botón volver
        back_btn = RoundedButton(
            text='Volver',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.8, 0.8, 0.8)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        # Título
        self.title_label = Label(
            text='Base de datos de materiales',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        layout.add_widget(self.title_label)

        # Lista de materiales
        self.scroll = ScrollView()
        self.content_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        self.scroll.add_widget(self.content_layout)
        layout.add_widget(self.scroll)

        self.add_widget(layout)

    def on_enter(self):
        self.controller.cargar_materiales()

    def _on_materiales_loaded(self, materiales: List[Material]):
        self._actualizar_ui(materiales)

    def _actualizar_ui(self, materiales: List[Material]):
        self.content_layout.clear_widgets()

        if not materiales:
            error_label = Label(
                text='No se pudieron cargar los materiales\nVerifica la conexión a la base de datos',
                font_size='16sp',
                color=(1, 0, 0, 1)
            )
            self.content_layout.add_widget(error_label)
            return

        # Agrupar materiales por categoría
        materiales_agrupados = self.controller.get_materiales_agrupados()

        for categoria, materiales_cat in materiales_agrupados.items():
            # Título de categoría
            cat_label = Label(
                text=f'[b]{categoria}[/b]',
                size_hint_y=None,
                height=40,
                font_size='18sp',
                markup=True,
                color=(0.2, 0.4, 0.2, 1)
            )
            self.content_layout.add_widget(cat_label)

            # Materiales de esta categoría
            for material in materiales_cat:
                btn = RoundedButton(
                    text=f'{material.nombre_material}\n{material.descripcion}',
                    size_hint_y=None,
                    height=80,
                    background_color=(0.18, 0.49, 0.20, 0.7),
                    halign="center"
                )
                btn.bind(on_press=lambda instance, mid=material.id_material:
                self._mostrar_detalle_material(mid))
                self.content_layout.add_widget(btn)

    def _mostrar_detalle_material(self, id_material: int):
        # Usar la pantalla existente en lugar de crear una nueva
        material_detail_screen = self.manager.get_screen('material_detail')
        material_detail_screen.cargar_material(id_material)
        self.manager.current = 'material_detail'

    def go_back(self, instance):
        self.manager.current = 'main'


class MaterialDetailScreen(BaseScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(controller, **kwargs)
        self._crear_ui()

    def _crear_ui(self):
        self.layout = BoxLayout(orientation='vertical', padding=15)

        # Botón volver
        back_btn = RoundedButton(
            text='Volver a materiales',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.8, 0.8, 0.8)
        )
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.scroll = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        self.scroll.add_widget(self.content_layout)
        self.layout.add_widget(self.scroll)

        self.add_widget(self.layout)

    def cargar_material(self, id_material: int):
        material = self.controller.get_material_by_id(id_material)
        self._mostrar_material(material)

    def _mostrar_material(self, material: Material):
        self.content_layout.clear_widgets()

        if not material:
            error_label = Label(
                text='Material no encontrado',
                font_size='18sp',
                color=(1, 0, 0, 1)
            )
            self.content_layout.add_widget(error_label)
            return

        # Título
        title = Label(
            text=f'{material.nombre_material}',
            size_hint_y=None,
            height=40,
            font_size='22sp',
            bold=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(title)

        # Categoría
        cat_label = Label(
            text=f'Categoria: {material.nombre_categoria}',
            size_hint_y=None,
            height=30,
            font_size='16sp',
            color=(0.4, 0.4, 0.4, 1)
        )
        self.content_layout.add_widget(cat_label)

        # Descripción
        desc_label = Label(
            text=f'[b]Descripcion:[/b]\n{material.descripcion}',
            size_hint_y=None,
            height=80,
            font_size='16sp',
            markup=True,
            text_size=(300, None),
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(desc_label)

        # Tiempo de descomposición
        tiempo_label = Label(
            text=f'[b]Tiempo de descomposicion:[/b]\n{material.tiempo_descomposicion}',
            size_hint_y=None,
            height=60,
            font_size='16sp',
            markup=True,
            text_size=(300, None),
            color = (0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(tiempo_label)

        # Información adicional
        info_label = Label(
            text='[b]Instrucciones de reciclaje:[/b]\n\n• Limpia el material antes de reciclar\n• Separa por tipo de material\n• Compacta para ahorrar espacio\n• Sigue las indicaciones locales',
            size_hint_y=None,
            height=120,
            font_size='14sp',
            markup=True,
            text_size=(300, None),
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(info_label)

    def go_back(self, instance):
        self.manager.current = 'materiales'


class GuiaScreen(BaseScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(controller, **kwargs)
        self._crear_ui()

    def _crear_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10)

        # Botón volver
        back_btn = RoundedButton(
            text='Volver',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.8, 0.8, 0.8)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        # Título
        title = Label(
            text='Guía de separación de residuos',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        layout.add_widget(title)

        # Contenido desplazable
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None, padding=10)
        content.bind(minimum_height=content.setter('height'))

        # Sección de colores de bolsas/canecas
        colores_title = Label(
            text='[b]Codigo de colores para separacion:[/b]',
            size_hint_y=None,
            height=40,
            font_size='18sp',
            markup=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        content.add_widget(colores_title)

        # Bolsa Blanca - Residuos aprovechables
        blanca_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80)
        with blanca_layout.canvas.before:
            Color(1, 1, 1, 1)  # Blanco
            Rectangle(size=blanca_layout.size, pos=blanca_layout.pos)
        blanca_layout.bind(size=self._update_rect_white, pos=self._update_rect_white)

        blanca_label = Label(
            text='[color=000000]Bolsa o caneca BLANCA\nResiduos aprovechables[/color]',
            markup=True,
            font_size='14sp',
            halign="center"
        )
        blanca_layout.add_widget(blanca_label)
        content.add_widget(blanca_layout)

        # Bolsa Verde - Orgánicos aprovechables
        verde_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80)
        with verde_layout.canvas.before:
            Color(0, 0.5, 0, 1)  # Verde
            Rectangle(size=verde_layout.size, pos=verde_layout.pos)
        verde_layout.bind(size=self._update_rect_green, pos=self._update_rect_green)

        verde_label = Label(
            text='Bolsa o caneca VERDE\nResiduos organicos aprovechables',
            color=(1, 1, 1, 1),
            font_size='14sp',
            halign="center"
        )
        verde_layout.add_widget(verde_label)
        content.add_widget(verde_layout)

        # Bolsa Negra - No aprovechables
        negra_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80)
        with negra_layout.canvas.before:
            Color(0, 0, 0, 1)  # Negro
            Rectangle(size=negra_layout.size, pos=negra_layout.pos)
        negra_layout.bind(size=self._update_rect_black, pos=self._update_rect_black)

        negra_label = Label(
            text='Bolsa o caneca NEGRA\nResiduos no aprovechables',
            color=(1, 1, 1, 1),
            font_size='14sp',
            halign="center"
        )
        negra_layout.add_widget(negra_label)
        content.add_widget(negra_layout)

        # Bolsa Roja - Peligrosos
        roja_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80)
        with roja_layout.canvas.before:
            Color(1, 0, 0, 1)  # Rojo
            Rectangle(size=roja_layout.size, pos=roja_layout.pos)
        roja_layout.bind(size=self._update_rect_red, pos=self._update_rect_red)

        roja_label = Label(
            text='Bolsa o caneca ROJA\nResiduos peligrosos',
            color=(1, 1, 1, 1),
            font_size='14sp',
            halign="center"
        )
        roja_layout.add_widget(roja_label)
        content.add_widget(roja_layout)

        # Información adicional
        info_label = Label(
            text='\n[b]Que va en cada bolsa?[/b]\n\n'
                 '[b]BLANCA:[/b] Plastico, vidrio, metal, papel, carton\n'
                 '[b]VERDE:[/b] Restos de comida, podas, papel sucio\n'
                 '[b]NEGRA:[/b] Papel higienico, servilletas, icopor\n'
                 '[b]ROJA:[/b] Pilas, medicamentos, productos quimicos',
            size_hint_y=None,
            height=150,
            font_size='14sp',
            markup=True,
            text_size=(300, None),
            color=(0.2, 0.4, 0.2, 1)
        )
        content.add_widget(info_label)

        # Consejos
        consejos_label = Label(
            text='[b]Consejos para una mejor separacion:[/b]\n\n'
                 '• Enjuaga los envases antes de reciclar\n'
                 '• Aplasta las botellas y latas para ahorrar espacio\n'
                 '• Separa los materiales por tipo\n'
                 '• No mezcles residuos peligrosos con los comunes\n'
                 '• Consulta los horarios de recoleccion en tu localidad',
            size_hint_y=None,
            height=140,
            font_size='14sp',
            markup=True,
            text_size=(300, None),
            color=(0.2, 0.4, 0.2, 1)
        )
        content.add_widget(consejos_label)

        scroll.add_widget(content)
        layout.add_widget(scroll)

        self.add_widget(layout)

    def _update_rect_white(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(size=instance.size, pos=instance.pos)

    def _update_rect_green(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0, 0.5, 0, 1)
            Rectangle(size=instance.size, pos=instance.pos)

    def _update_rect_black(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(size=instance.size, pos=instance.pos)

    def _update_rect_red(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(1, 0, 0, 1)
            Rectangle(size=instance.size, pos=instance.pos)

    def go_back(self, instance):
        self.manager.current = 'main'


class MapaScreen(BaseScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(controller, **kwargs)
        self.controller.set_on_centros_loaded(self._on_centros_loaded)
        self.mapa_path = None
        self._crear_ui()

    def _crear_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10)

        # Botón volver
        back_btn = RoundedButton(
            text='Volver',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.8, 0.8, 0.8)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        # Título
        self.title_label = Label(
            text='Mapa de Puntos de Reciclaje',
            size_hint=(1, 0.08),
            font_size='20sp',
            bold=True,
            halign='center',
            color=(0.2, 0.4, 0.2, 1)
        )
        layout.add_widget(self.title_label)

        # Controles del mapa
        controles_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.12),
            spacing=10,
            padding=10
        )

        # Botón para abrir mapa en navegador
        self.abrir_mapa_btn = RoundedButton(
            text='Abrir Mapa Interactivo',
            size_hint=(0.6, 1),
            background_color=(0.2, 0.6, 0.8, 0.7)
        )
        self.abrir_mapa_btn.bind(on_press=self._abrir_mapa_navegador)
        self.abrir_mapa_btn.disabled = True

        # Botón para actualizar
        actualizar_btn = RoundedButton(
            text='Generar Mapa',
            size_hint=(0.4, 1)
        )
        actualizar_btn.bind(on_press=self._actualizar_mapa)

        controles_layout.add_widget(self.abrir_mapa_btn)
        controles_layout.add_widget(actualizar_btn)
        layout.add_widget(controles_layout)

        # Área de información del mapa
        self.info_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.3),
            padding=10
        )

        # Mensaje inicial
        self.mapa_info_label = Label(
            text='[b]Mapa Interactivo de Centros de Reciclaje[/b]\n\n'
                 '• Presiona "Generar Mapa" para crear el mapa\n'
                 '• Luego "Abrir Mapa Interactivo" para verlo\n'
                 '• El mapa se abrira en tu navegador web\n'
                 '• Podras hacer zoom y click en los marcadores',
            font_size='14sp',
            markup=True,
            text_size=(350, None),
            halign='center',
            valign='top',
            color=(0.2, 0.4, 0.2, 1)
        )
        self.info_container.add_widget(self.mapa_info_label)

        layout.add_widget(self.info_container)

        # Lista de centros (scrollable)
        self.centros_scroll = ScrollView(size_hint=(1, 0.5))
        self.centros_layout = BoxLayout(
            orientation='vertical',
            spacing=8,
            size_hint_y=None,
            padding=10
        )
        self.centros_layout.bind(minimum_height=self.centros_layout.setter('height'))
        self.centros_scroll.add_widget(self.centros_layout)
        layout.add_widget(self.centros_scroll)

        self.add_widget(layout)

        # Verificar si ya existe un mapa
        self._verificar_mapa_existente()

    def _verificar_mapa_existente(self):
        """Verifica si ya existe un mapa generado"""
        mapa_existente = self.controller.get_ruta_mapa_actual()
        if mapa_existente:
            self.mapa_path = mapa_existente
            self.mapa_info_label.text = '[b]Mapa disponible[/b]\n\nPresiona "Abrir Mapa Interactivo" para ver el mapa actual.\nO "Generar Mapa" para crear uno nuevo.'
            self.abrir_mapa_btn.disabled = False

    def on_enter(self):
        # Cargar centros cuando se entra a la pantalla
        self.controller.cargar_centros_reciclaje()

    def _on_centros_loaded(self, centros: List[CentroReciclaje]):
        self._actualizar_lista_centros(centros)

    def _generar_mapa_fondo(self, centros):
        """Genera el mapa en un hilo separado"""
        try:
            self.mapa_path = self.controller.generar_mapa_centros(centros)
            # Actualizar UI en el hilo principal
            Clock.schedule_once(lambda dt: self._mapa_generado())
        except Exception as e:
            print(f"Error generando mapa: {e}")
            Clock.schedule_once(lambda dt: self._error_mapa())

    def _mapa_generado(self):
        """Callback cuando el mapa está listo"""
        if self.mapa_path:
            self.mapa_info_label.text = '[b]Mapa generado exitosamente![/b]\n\nPresiona "Abrir Mapa Interactivo" para explorar los centros de reciclaje en Bogota.'
            self.abrir_mapa_btn.disabled = False
        else:
            self.mapa_info_label.text = '[b]Error generando el mapa[/b]\n\nVerifica que tengas conexion a internet e intenta nuevamente.'

    def _error_mapa(self):
        """Callback cuando hay error generando el mapa"""
        self.mapa_info_label.text = '[b]Error generando el mapa[/b]\n\nVerifica que tengas las dependencias instaladas:\npip install folium branca'

    def _abrir_mapa_navegador(self, instance):
        """Abre el mapa HTML en el navegador predeterminado"""
        if self.mapa_path and os.path.exists(self.mapa_path):
            try:
                # Convertir ruta a formato file://
                absolute_path = os.path.abspath(self.mapa_path)
                webbrowser.open(f'file://{absolute_path}')
                self.mapa_info_label.text = '[b]Mapa abierto en navegador[/b]\n\n• Navega por el mapa interactivo\n• Haz click en los marcadores\n• Usa zoom para ver mas detalles'
            except Exception as e:
                print(f"Error abriendo mapa: {e}")
                self.mapa_info_label.text = '[b]Error abriendo el mapa[/b]\n\nNo se pudo abrir el navegador.'
        else:
            self.mapa_info_label.text = '[b]El mapa no esta disponible[/b]\n\nPresiona "Generar Mapa" para crear uno nuevo.'

    def _actualizar_mapa(self, instance):
        """Forza la generación de un nuevo mapa"""
        self.mapa_info_label.text = '[b]Generando nuevo mapa...[/b]\n\nEsto puede tomar unos segundos.'
        self.abrir_mapa_btn.disabled = True

        centros = self.controller._centros_cache
        if centros:
            # Generar mapa en segundo plano
            threading.Thread(
                target=self._generar_mapa_fondo,
                args=(centros,),
                daemon=True
            ).start()
        else:
            self.mapa_info_label.text = '[b]No hay centros cargados[/b]\n\nPrimero carga los centros de reciclaje.'

    def _actualizar_lista_centros(self, centros: List[CentroReciclaje]):
        """Actualiza la lista de centros en la UI"""
        self.centros_layout.clear_widgets()

        # Contador de centros
        contador_label = Label(
            text=f'[b]Centros encontrados: {len(centros)}[/b]',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            markup=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        self.centros_layout.add_widget(contador_label)

        for centro in centros:
            centro_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=90,
                padding=5
            )

            with centro_layout.canvas.before:
                Color(0.95, 0.95, 0.95, 1)
                Rectangle(size=centro_layout.size, pos=centro_layout.pos)
            centro_layout.bind(size=self._update_rect_centro, pos=self._update_rect_centro)

            # Nombre del centro
            nombre_label = Label(
                text=f'[b]{centro.nombre_centro}[/b]',
                size_hint_y=None,
                height=25,
                font_size='14sp',
                markup=True,
                color=(0, 0, 0, 1)
            )
            centro_layout.add_widget(nombre_label)

            # Dirección
            direccion_label = Label(
                text=f'Direccion: {centro.direccion}',
                size_hint_y=None,
                height=20,
                font_size='11sp',
                color=(0.3, 0.3, 0.3, 1),
                text_size=(340, None)
            )
            centro_layout.add_widget(direccion_label)

            # Información en línea
            info_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=20)

            horario_label = Label(
                text=f'Horario: {centro.horario_atencion[:20]}...',
                font_size='10sp',
                color=(0.5, 0.5, 0.5, 1)
            )
            info_layout.add_widget(horario_label)

            materiales_label = Label(
                text=f'Materiales: {len(centro.materiales)}',
                font_size='10sp',
                color=(0.2, 0.5, 0.2, 1)
            )
            info_layout.add_widget(materiales_label)

            centro_layout.add_widget(info_layout)

            # Teléfono
            telefono_label = Label(
                text=f'Telefono: {centro.telefono}',
                size_hint_y=None,
                height=20,
                font_size='10sp',
                color=(0.4, 0.4, 0.4, 1)
            )
            centro_layout.add_widget(telefono_label)

            self.centros_layout.add_widget(centro_layout)

    def _update_rect_centro(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            Rectangle(size=instance.size, pos=instance.pos)

    def go_back(self, instance):
        self.manager.current = 'main'


class EmpresasScreen(BaseScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(controller, **kwargs)
        self.controller.set_on_centros_loaded(self._on_centros_loaded)
        self._crear_ui()

    def _crear_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10)

        # Botón volver
        back_btn = RoundedButton(
            text='Volver',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.8, 0.8, 0.8)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        # Título
        self.title_label = Label(
            text='Directorio de Empresas y Centros',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        layout.add_widget(self.title_label)

        # Lista de centros
        self.scroll = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, padding=10)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        self.scroll.add_widget(self.content_layout)
        layout.add_widget(self.scroll)

        self.add_widget(layout)

    def on_enter(self):
        self.controller.cargar_centros_reciclaje()

    def _on_centros_loaded(self, centros: List[CentroReciclaje]):
        self._actualizar_lista_centros(centros)

    def _actualizar_lista_centros(self, centros: List[CentroReciclaje]):
        self.content_layout.clear_widgets()

        if not centros:
            error_label = Label(
                text='No se pudieron cargar los centros\nVerifica la conexion a la base de datos',
                font_size='16sp',
                color=(1, 0, 0, 1)
            )
            self.content_layout.add_widget(error_label)
            return

        # Contador
        contador_label = Label(
            text=f'[b]Centros disponibles: {len(centros)}[/b]',
            size_hint_y=None,
            height=40,
            font_size='16sp',
            markup=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(contador_label)

        for centro in centros:
            centro_btn = RoundedButton(
                text=f'{centro.nombre_centro}\nDireccion: {centro.direccion[:30]}...',
                size_hint_y=None,
                height=100,
                background_color=(0.18, 0.49, 0.20, 0.7)
            )
            centro_btn.bind(on_press=lambda instance, cid=centro.id_centro:
            self._mostrar_detalle_centro(cid))
            self.content_layout.add_widget(centro_btn)

    def _mostrar_detalle_centro(self, id_centro: int):
        # Usar la pantalla existente en lugar de crear una nueva
        centro_detalle_screen = self.manager.get_screen('centro_detalle')
        centro_detalle_screen.cargar_centro(id_centro)
        self.manager.current = 'centro_detalle'

    def go_back(self, instance):
        self.manager.current = 'main'


class CentroDetalleScreen(BaseScreen):
    def __init__(self, controller, **kwargs):  # Quitamos el id_centro del constructor
        super().__init__(controller, **kwargs)
        self.id_centro = None
        self._crear_ui()

    def _crear_ui(self):
        self.layout = BoxLayout(orientation='vertical', padding=15)

        # Botón volver
        back_btn = RoundedButton(
            text='Volver al directorio',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.8, 0.8, 0.8)
        )
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.scroll = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        self.scroll.add_widget(self.content_layout)
        self.layout.add_widget(self.scroll)

        self.add_widget(self.layout)

    def cargar_centro(self, id_centro: int):
        """Método para cargar el centro desde fuera"""
        self.id_centro = id_centro
        self._cargar_datos()

    def _cargar_datos(self):
        if self.id_centro:
            centro = self.controller.get_centro_by_id(self.id_centro)
            if centro:
                self._mostrar_centro(centro)

    def _mostrar_centro(self, centro: CentroReciclaje):
        self.content_layout.clear_widgets()

        if not centro:
            error_label = Label(
                text='Centro no encontrado',
                font_size='18sp',
                color=(1, 0, 0, 1)
            )
            self.content_layout.add_widget(error_label)
            return

        # Nombre
        nombre_label = Label(
            text=f'[b]{centro.nombre_centro}[/b]',
            size_hint_y=None,
            height=40,
            font_size='20sp',
            markup=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(nombre_label)

        # Dirección
        direccion_label = Label(
            text=f'[b]Dirección:[/b]\n{centro.direccion}',
            size_hint_y=None,
            height=60,
            font_size='16sp',
            markup=True,
            text_size=(300, None),
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(direccion_label)

        # Teléfono
        telefono_label = Label(
            text=f'[b]Teléfono:[/b] {centro.telefono}',
            size_hint_y=None,
            height=30,
            font_size='16sp',
            markup=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(telefono_label)

        # Horario
        horario_label = Label(
            text=f'[b]Horario de atención:[/b]\n{centro.horario_atencion}',
            size_hint_y=None,
            height=50,
            font_size='16sp',
            markup=True,
            text_size=(300, None),
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(horario_label)

        # Materiales aceptados - MOSTRAR CANTIDAD CORRECTA
        num_materiales = len(centro.materiales) if centro.materiales else 0
        materiales_label = Label(
            text=f'[b]Materiales aceptados ({num_materiales}):[/b]',
            size_hint_y=None,
            height=30,
            font_size='16sp',
            markup=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(materiales_label)

        # Lista de materiales - VERIFICAR SI HAY MATERIALES
        if centro.materiales:
            for material in centro.materiales:
                material_layout = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=40,
                    padding=5
                )

                with material_layout.canvas.before:
                    Color(0.9, 0.95, 0.9, 1)
                    Rectangle(size=material_layout.size, pos=material_layout.pos)
                material_layout.bind(size=self._update_rect_material, pos=self._update_rect_material)

                material_label = Label(
                    text=f'• {material.nombre_material}',
                    font_size='14sp',
                    color=(0.2, 0.4, 0.2, 1)
                )
                material_layout.add_widget(material_label)

                self.content_layout.add_widget(material_layout)
        else:
            # Mensaje si no hay materiales
            sin_materiales_label = Label(
                text='No hay información de materiales disponibles',
                size_hint_y=None,
                height=30,
                font_size='14sp',
                color=(0.5, 0.5, 0.5, 1),
                italic=True
            )
            self.content_layout.add_widget(sin_materiales_label)

    def _update_rect_material(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.9, 0.95, 0.9, 1)
            Rectangle(size=instance.size, pos=instance.pos)

    def go_back(self, instance):
        if self.manager:
            self.manager.current = 'empresas'


class NoticiasScreen(BaseScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(controller, **kwargs)
        self.controller.set_on_noticias_loaded(self._on_noticias_loaded)
        self._crear_ui()

    def _crear_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10)

        # Botón volver
        back_btn = RoundedButton(
            text='Volver',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.8, 0.8, 0.8)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        # Título
        self.title_label = Label(
            text='Noticias y Tips de Reciclaje',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        layout.add_widget(self.title_label)

        # Lista de noticias
        self.scroll = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None, padding=10)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        self.scroll.add_widget(self.content_layout)
        layout.add_widget(self.scroll)

        self.add_widget(layout)

    def on_enter(self):
        self.controller.cargar_noticias()

    def _on_noticias_loaded(self, noticias: List[Noticia]):
        self._actualizar_lista_noticias(noticias)

    def _actualizar_lista_noticias(self, noticias: List[Noticia]):
        self.content_layout.clear_widgets()

        if not noticias:
            error_label = Label(
                text='No se pudieron cargar las noticias',
                font_size='16sp',
                color=(1, 0, 0, 1)
            )
            self.content_layout.add_widget(error_label)
            return

        # Contador
        contador_label = Label(
            text=f'[b]Últimas noticias: {len(noticias)}[/b]',
            size_hint_y=None,
            height=40,
            font_size='16sp',
            markup=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(contador_label)

        for noticia in noticias:
            # Limitar longitud del texto para que quepa bien
            titulo = noticia.titulo
            if len(titulo) > 45:
                titulo = titulo[:42] + '...'

            resumen = noticia.resumen
            if len(resumen) > 55:
                resumen = resumen[:52] + '...'

            # Crear botón mejorado
            noticia_btn = Button(
                text=f'[b]{titulo}[/b]\n\n📅 {noticia.fecha_publicacion} | 📰 {noticia.fuente}\n\n{resumen}\n\n[b]Toca para leer más →[/b]',
                size_hint_y=None,
                height=150,
                background_color=(0.2, 0.4, 0.6, 0.8),
                background_normal='',
                color=(1, 1, 1, 1),
                font_size='13sp',
                halign='left',
                valign='top',
                markup=True,
                text_size=(320, None),
                padding=(15, 10)
            )

            # Agregar bordes redondeados al botón
            with noticia_btn.canvas.before:
                Color(0.2, 0.4, 0.6, 0.8)
                noticia_btn.rect = RoundedRectangle(
                    size=noticia_btn.size,
                    pos=noticia_btn.pos,
                    radius=[15]
                )
            noticia_btn.bind(
                size=self._update_btn_rect,
                pos=self._update_btn_rect,
                on_press=lambda instance, nid=noticia.id_noticia: self._mostrar_detalle_noticia(nid)
            )

            self.content_layout.add_widget(noticia_btn)

    def _update_btn_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.2, 0.4, 0.6, 0.8)
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[15])

    def _mostrar_detalle_noticia(self, id_noticia: int):
        # Usar la pantalla existente en lugar de crear una nueva
        noticia_detalle_screen = self.manager.get_screen('noticia_detalle')
        noticia_detalle_screen.cargar_noticia(id_noticia)
        self.manager.current = 'noticia_detalle'

    def go_back(self, instance):
        self.manager.current = 'main'



class NoticiaDetalleScreen(BaseScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(controller, **kwargs)
        self.id_noticia = None
        self._crear_ui()

    def _crear_ui(self):
        self.layout = BoxLayout(orientation='vertical', padding=15)

        # volver
        back_btn = RoundedButton(
            text='Volver a noticias',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.8, 0.8, 0.8)
        )
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.scroll = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        self.scroll.add_widget(self.content_layout)
        self.layout.add_widget(self.scroll)

        self.add_widget(self.layout)

    def cargar_noticia(self, id_noticia: int):
        """Método para cargar la noticia desde fuera"""
        self.id_noticia = id_noticia
        self._cargar_datos()

    def _cargar_datos(self):
        if self.id_noticia:
            noticia = self.controller.get_noticia_by_id(self.id_noticia)
            if noticia:
                self._mostrar_noticia(noticia)

    def _mostrar_noticia(self, noticia: Noticia):
        self.content_layout.clear_widgets()

        if not noticia:
            error_label = Label(
                text='Noticia no encontrada',
                font_size='18sp',
                color=(1, 0, 0, 1)
            )
            self.content_layout.add_widget(error_label)
            return

        # Título
        titulo_label = Label(
            text=f'[b]{noticia.titulo}[/b]',
            size_hint_y=None,
            height=60,
            font_size='20sp',
            markup=True,
            text_size=(300, None),
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(titulo_label)

        # Fecha y fuente
        meta_label = Label(
            text=f'Fecha: {noticia.fecha_publicacion} | Fuente: {noticia.fuente}',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            color=(0.5, 0.5, 0.5, 1)
        )
        self.content_layout.add_widget(meta_label)

        # Resumen
        resumen_label = Label(
            text=f'[b]Resumen:[/b]\n{noticia.resumen}',
            size_hint_y=None,
            height=80,
            font_size='16sp',
            markup=True,
            text_size=(300, None),
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(resumen_label)

        # Contenido
        contenido_label = Label(
            text=f'{noticia.contenido}',
            size_hint_y=None,
            height=200,
            font_size='14sp',
            text_size=(300, None),
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(contenido_label)

    def go_back(self, instance):
        if self.manager:
            self.manager.current = 'noticias'


class RecordatoriosScreen(BaseScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(controller, **kwargs)
        self.controller.set_on_recordatorios_loaded(self._on_recordatorios_loaded)
        self._crear_ui()

    def _crear_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10)

        # Botón volver
        back_btn = RoundedButton(
            text='Volver al Inicio',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.8, 0.8, 0.8)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        # Título
        title_label = Label(
            text='Recordatorios de Reciclaje',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        layout.add_widget(title_label)

        # Botón para agregar recordatorio
        agregar_btn = RoundedButton(
            text='Agregar Nuevo Recordatorio',
            size_hint=(1, 0.1),
            background_color=(0.18, 0.49, 0.20, 0.9)
        )
        agregar_btn.bind(on_press=self._mostrar_formulario)
        layout.add_widget(agregar_btn)

        # Lista de recordatorios
        self.scroll = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', spacing=12, size_hint_y=None, padding=[10, 15, 10, 15])
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        self.scroll.add_widget(self.content_layout)
        layout.add_widget(self.scroll)

        self.add_widget(layout)

    def on_enter(self):
        self.controller.cargar_recordatorios()

    def _on_recordatorios_loaded(self, recordatorios: List[Recordatorio]):
        self._actualizar_lista_recordatorios(recordatorios)

    def _actualizar_lista_recordatorios(self, recordatorios: List[Recordatorio]):
        self.content_layout.clear_widgets()

        if not recordatorios:
            # Mensaje cuando no hay recordatorios
            vacio_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=180,
                padding=20
            )

            with vacio_layout.canvas.before:
                Color(0.95, 0.95, 0.95, 1)
                vacio_layout.rect = RoundedRectangle(size=vacio_layout.size, pos=vacio_layout.pos, radius=[15])
            vacio_layout.bind(size=self._update_vacio_rect, pos=self._update_vacio_rect)

            mensaje_label = Label(
                text='No tienes recordatorios programados\n\nPresiona "Agregar Nuevo Recordatorio"\npara crear tu primer recordatorio',
                font_size='14sp',
                text_size=(300, None),
                halign='center',
                valign='middle',
                size_hint_y=None,
                height=120
            )
            vacio_layout.add_widget(mensaje_label)

            self.content_layout.add_widget(vacio_layout)
            return

        # Contador
        contador_label = Label(
            text=f'[b]Recordatorios activos: {len(recordatorios)}[/b]',
            size_hint_y=None,
            height=40,
            font_size='16sp',
            markup=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        self.content_layout.add_widget(contador_label)

        for recordatorio in recordatorios:
            # Layout principal del recordatorio
            recordatorio_layout = BoxLayout(
                orientation='horizontal',  # Cambiamos a horizontal
                size_hint_y=None,
                height=120,
                padding=[10, 10, 10, 10],
                spacing=10
            )

            # Contenido del recordatorio (lado izquierdo)
            contenido_layout = BoxLayout(
                orientation='vertical',
                size_hint_x=0.8,
                spacing=3
            )

            # Fondo con color según si es recurrente o no
            color_fondo = (0.9, 0.95, 0.9, 1) if not recordatorio.repetir_semanal else (0.9, 0.92, 0.98, 1)

            with contenido_layout.canvas.before:
                Color(*color_fondo)
                contenido_layout.rect = RoundedRectangle(
                    size=contenido_layout.size,
                    pos=contenido_layout.pos,
                    radius=[12]
                )
            contenido_layout.bind(size=self._update_rect_recordatorio, pos=self._update_rect_recordatorio)

            # Header con título y badge de repetición
            header_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=25
            )

            titulo_label = Label(
                text=f'[b]{recordatorio.titulo}[/b]',
                size_hint_x=0.7,
                font_size='14sp',
                markup=True,
                color=(0, 0, 0, 1),
                text_size=(200, None),
                halign='left'
            )
            header_layout.add_widget(titulo_label)

            # Badge de repetición
            repeticion_text = 'Semanal' if recordatorio.repetir_semanal else 'Una vez'
            repeticion_label = Label(
                text=repeticion_text,
                size_hint_x=0.3,
                font_size='10sp',
                color=(0.5, 0.5, 0.5, 1),
                halign='right'
            )
            header_layout.add_widget(repeticion_label)

            contenido_layout.add_widget(header_layout)

            # Fecha y hora
            fecha_hora_label = Label(
                text=f'Fecha: {recordatorio.fecha_recordatorio}  Hora: {recordatorio.hora_recordatorio}',
                size_hint_y=None,
                height=20,
                font_size='12sp',
                color=(0.4, 0.4, 0.4, 1),
                text_size=(250, None),
                halign='left'
            )
            contenido_layout.add_widget(fecha_hora_label)

            # Descripción
            desc_label = Label(
                text=recordatorio.descripcion,
                size_hint_y=None,
                height=40,
                font_size='12sp',
                color=(0.3, 0.3, 0.3, 1),
                text_size=(250, None),
                halign='left',
                valign='top'
            )
            contenido_layout.add_widget(desc_label)

            # Estado
            estado_label = Label(
                text='Activo' if recordatorio.activo else 'Inactivo',
                size_hint_y=None,
                height=15,
                font_size='10sp',
                color=(0.2, 0.6, 0.2, 1) if recordatorio.activo else (0.8, 0.2, 0.2, 1)
            )
            contenido_layout.add_widget(estado_label)

            # Botón de eliminar (lado derecho)
            eliminar_btn = Button(
                text='Eliminar',
                size_hint_x=0.2,
                background_color=(0.8, 0.2, 0.2, 0.9),
                background_normal='',
                color=(1, 1, 1, 1),
                font_size='12sp'
            )

            # Agregar bordes redondeados al botón de eliminar
            with eliminar_btn.canvas.before:
                Color(0.8, 0.2, 0.2, 0.9)
                eliminar_btn.rect = RoundedRectangle(
                    size=eliminar_btn.size,
                    pos=eliminar_btn.pos,
                    radius=[8]
                )
            eliminar_btn.bind(
                size=self._update_eliminar_btn_rect,
                pos=self._update_eliminar_btn_rect,
                on_press=lambda instance, rid=recordatorio.id_recordatorio: self._eliminar_recordatorio(rid)
            )

            # Agregar ambos layouts al layout principal
            recordatorio_layout.add_widget(contenido_layout)
            recordatorio_layout.add_widget(eliminar_btn)

            self.content_layout.add_widget(recordatorio_layout)

    def _update_eliminar_btn_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.8, 0.2, 0.2, 0.9)
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[8])

    def _eliminar_recordatorio(self, id_recordatorio: int):
        """Elimina un recordatorio"""
        # Aquí podrías agregar un diálogo de confirmación
        resultado = self.controller.eliminar_recordatorio(id_recordatorio)
        if not resultado:
            print("Error al eliminar el recordatorio")

    def _update_rect_recordatorio(self, instance, value):
        instance.canvas.before.clear()
        color_fondo = (0.9, 0.95, 0.9, 1)
        with instance.canvas.before:
            Color(*color_fondo)
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[12])

    def _update_vacio_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[15])

    def _mostrar_formulario(self, instance):
        # Crear pantalla de formulario (en lugar de usar una existente)
        formulario_screen = FormularioRecordatorioScreen(
            self.controller,
            name='formulario_recordatorio'
        )
        self.manager.add_widget(formulario_screen)
        self.manager.current = 'formulario_recordatorio'

    def go_back(self, instance):
        self.manager.current = 'main'


class FormularioRecordatorioScreen(BaseScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(controller, **kwargs)
        self._crear_ui()

    def _crear_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10)

        # Botón volver
        back_btn = RoundedButton(
            text='Cancelar y Volver',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.8, 0.8, 0.8)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        # Título
        titulo_label = Label(
            text='Crear Nuevo Recordatorio',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True,
            color=(0.2, 0.4, 0.2, 1)
        )
        layout.add_widget(titulo_label)

        # Formulario
        self.scroll = ScrollView()
        form_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None, padding=[20, 10, 20, 20])
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Título del recordatorio
        titulo_container = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        titulo_container.add_widget(Label(
            text='Título del recordatorio:',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            color=(0.2, 0.4, 0.2, 1)
        ))
        self.titulo_input = TextInput(
            hint_text='Ej: Sacar la basura reciclable',
            size_hint_y=None,
            height=40,
            background_color=(1, 1, 1, 0.9),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 8]
        )
        titulo_container.add_widget(self.titulo_input)
        form_layout.add_widget(titulo_container)

        # Descripción
        desc_container = BoxLayout(orientation='vertical', size_hint_y=None, height=120)
        desc_container.add_widget(Label(
            text='Descripción:',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            color=(0.2, 0.4, 0.2, 1)
        ))
        self.descripcion_input = TextInput(
            hint_text='Ej: Separar plásticos, vidrios y cartones para reciclaje',
            size_hint_y=None,
            height=80,
            multiline=True,
            background_color=(1, 1, 1, 0.9),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 8]
        )
        desc_container.add_widget(self.descripcion_input)
        form_layout.add_widget(desc_container)

        # Fecha y Hora en una sola fila
        fecha_hora_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, spacing=10)

        # Fecha
        fecha_container = BoxLayout(orientation='vertical', size_hint_x=0.5)
        fecha_container.add_widget(Label(
            text='Fecha:',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            color=(0.2, 0.4, 0.2, 1)
        ))
        self.fecha_input = TextInput(
            hint_text='AAAA-MM-DD',
            size_hint_y=None,
            height=40,
            background_color=(1, 1, 1, 0.9),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 8]
        )
        fecha_container.add_widget(self.fecha_input)
        fecha_hora_layout.add_widget(fecha_container)

        # Hora
        hora_container = BoxLayout(orientation='vertical', size_hint_x=0.5)
        hora_container.add_widget(Label(
            text='Hora:',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            color=(0.2, 0.4, 0.2, 1)
        ))
        self.hora_input = TextInput(
            hint_text='HH:MM',
            size_hint_y=None,
            height=40,
            background_color=(1, 1, 1, 0.9),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 8]
        )
        hora_container.add_widget(self.hora_input)
        fecha_hora_layout.add_widget(hora_container)

        form_layout.add_widget(fecha_hora_layout)

        # Repetición
        repeticion_container = BoxLayout(orientation='vertical', size_hint_y=None, height=70)
        repeticion_container.add_widget(Label(
            text='Repetición:',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            color=(0.2, 0.4, 0.2, 1)
        ))

        repeticion_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=35, spacing=20)

        self.repetir_toggle = ToggleButton(
            text='Semanalmente',
            size_hint_x=0.5,
            group='repeticion'
        )

        no_repetir_btn = ToggleButton(
            text='Una sola vez',
            size_hint_x=0.5,
            group='repeticion',
            state='down'
        )

        repeticion_layout.add_widget(no_repetir_btn)
        repeticion_layout.add_widget(self.repetir_toggle)
        repeticion_container.add_widget(repeticion_layout)
        form_layout.add_widget(repeticion_container)

        # Botón guardar
        guardar_btn = RoundedButton(
            text='Guardar Recordatorio',
            size_hint_y=None,
            height=50,
            background_color=(0.18, 0.49, 0.20, 0.9)
        )
        guardar_btn.bind(on_press=self._guardar_recordatorio)
        form_layout.add_widget(guardar_btn)

        self.scroll.add_widget(form_layout)
        layout.add_widget(self.scroll)

        self.add_widget(layout)

    def _guardar_recordatorio(self, instance):
        titulo = self.titulo_input.text.strip()
        descripcion = self.descripcion_input.text.strip()
        fecha = self.fecha_input.text.strip()
        hora = self.hora_input.text.strip()
        repetir = self.repetir_toggle.state == 'down'

        # Validaciones básicas
        if not titulo:
            self._mostrar_error('Por favor ingresa un título')
            return

        if not descripcion:
            self._mostrar_error('Por favor ingresa una descripción')
            return

        if not fecha:
            self._mostrar_error('Por favor ingresa una fecha')
            return

        if not hora:
            self._mostrar_error('Por favor ingresa una hora')
            return

        # Guardar recordatorio
        resultado = self.controller.guardar_recordatorio(titulo, descripcion, fecha, hora, repetir)

        if resultado:
            self.go_back(None)
        else:
            self._mostrar_error('Error al guardar el recordatorio')

    def _mostrar_error(self, mensaje):
        # Podrías implementar un popup de error aquí
        print(f"Error: {mensaje}")

    def go_back(self, instance):
        if self.manager:
            self.manager.current = 'recordatorios'