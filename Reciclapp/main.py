# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from controllers.app_controller import AppController
from views import (
    MainScreen, MaterialesScreen, MaterialDetailScreen,
    GuiaScreen, MapaScreen, EmpresasScreen,
    NoticiasScreen, RecordatoriosScreen,CentroDetalleScreen,
    NoticiaDetalleScreen
)


class ReciclApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = AppController()

    def build(self):
        sm = ScreenManager()

        # Pantallas principales
        sm.add_widget(MainScreen(self.controller, name='main'))
        sm.add_widget(MaterialesScreen(self.controller, name='materiales'))
        sm.add_widget(MaterialDetailScreen(self.controller, name='material_detail'))
        sm.add_widget(GuiaScreen(self.controller, name='guia'))
        sm.add_widget(MapaScreen(self.controller, name='mapa'))
        sm.add_widget(EmpresasScreen(self.controller, name='empresas'))
        sm.add_widget(NoticiasScreen(self.controller, name='noticias'))
        sm.add_widget(RecordatoriosScreen(self.controller, name='recordatorios'))
        sm.add_widget(CentroDetalleScreen(self.controller, name='centro_detalle'))
        sm.add_widget(NoticiaDetalleScreen(self.controller, name='noticia_detalle'))


        return sm

    def on_stop(self):
        self.controller.cerrar_aplicacion()


if __name__ == '__main__':
    ReciclApp().run()