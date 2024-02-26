from kivy.app import App
from kivy.utils import get_hex_from_color as unhex
from kivy.utils import get_color_from_hex as hexed
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage, Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.filechooser import FileChooserIconView
from recursos.data.lector import Modificacion_BDD
import random, os, win32api
import inspect

LabelBase.register(name="rubik",fn_regular="recursos/fonts/Rubik/Rubik-Regular.ttf")

#Experimento actual: 
#Experimento logrado: Popups de un Popup
#Experimento logrado: cambiar el color del fondo de todas las pantallas
#Experimento logrado: iterar creación de widgets
#Experimento logrado: pintar el botón presionado y decolorear el resto
#Experimento logrado: que se grabe el botón coloreado y la pregunta para comparar
#Experimento logrado: iterar creación de widgets con distintas funciones
#Experimento logrado: colocar una imagen de fondo que se adapte a la ventana
#Experimento logrado: Lograr cargar un archivo de con FileChooser y que lea su excel

BDD = Modificacion_BDD()

def adapt_text_size(widget):
    screen_res = [win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1)]
    text_size = []
    text_size.append((widget.size_hint[0]-0.01)*screen_res[0])
    return int(text_size[0])

def pophexed(hex_color:str):
    cal = hexed(hex_color)
    result = []
    for a in cal:
        result.append(7*a)
    return result

class Add_question(Popup):
    current_frame = inspect.currentframe()
    callframe = inspect.getouterframes(current_frame, 2)
    father = callframe[1][3]
    print(type(father))
    widgets = []
    def __init__(self, **kwargs):
        super(Add_question,self).__init__(**kwargs)

        mainframe = BoxLayout(orientation="vertical", padding="5dp")
        question_label = Label(text="Ingrese los datos")
        question_set = Label(text="Ingrese su pregunta")
        question = TextInput()
        mainframe.add_widget(question_label)
        mainframe.add_widget(question_set)
        mainframe.add_widget(question)
        text = ["A", "B", "C"]
        answers_box = GridLayout(cols=2)
        mainframe.add_widget(answers_box)
        for a in text:
            label = Label(text=a, size_hint=[.5,None])
            answer = TextInput()
            answers_box.add_widget(label)
            answers_box.add_widget(answer)
            self.widgets.append(answer)
        action = Button(text="Guardar")
        salir = Button(text="Cancelar", on_release=self.dismiss)
        answers_box.add_widget(action)
        answers_box.add_widget(salir)
        self.add_widget(mainframe)
class File_explorer(Popup): #Explorador de archivos - Se debe corregir el tamaño
    def __init__(self, **kwargs):
        super(File_explorer, self).__init__(**kwargs)

        mainframe = BoxLayout(orientation="vertical", padding="5dp")
        self.direction = TextInput(size_hint=[1,None],height="30dp")
        self.direction.bind(text=self.actual_path)
        self.fichero = FileChooserIconView(size_hint=[1,2.5], dirselect=True) # Se cambio el sector Y por 2
        self.fichero.path = os.path.expanduser("~\\Onedrive\\Desktop")
        self.fichero.bind(selection=self.selected_path)
        subframe = BoxLayout()
        self.selected = TextInput(multiline=False, size_hint=[.8, None], height="30dp")
        send = Button(text="Seleccionar" ,size_hint=[.2, None], height="30dp")
        send.bind(on_release=self.send_path)
        subframe.add_widget(Label(text="Achivo: ", size_hint=[.3,None], height="30dp"))
        subframe.add_widget(self.selected)
        subframe.add_widget(send)
        mainframe.add_widget(self.direction)
        mainframe.add_widget(self.fichero)
        mainframe.add_widget(subframe)
        self.add_widget(mainframe)
    
    def actual_path(self, widget, text):
        self.fichero.path = text
        return

    def selected_path(self, widget:object, val):
        self.selected.text = str(val[0])
        return

    def send_path(self, widget:object):
        App.get_running_app().managersc.get_screen(name="gestion").ruta = self.selected.text
        App.get_running_app().managersc.get_screen(name="gestion").excelsior.text = f"Cargar Excel: '{self.selected.text}'"
        return
    
    def on_touch(self,touch):
        if self.fichero.selection:
            self.direction.text = str(self.fichero.selection[0])
        return super().on_touch(touch)
    
class CRUD(Screen):

    def gestionar(self, widget):
        """
        Este es el widget más complejo de toda la app, contiene 8 popups en su interior; un movimiento en falso y puede darte interrminables
        errores, dependiendo del widget que llame esta función se ejecutara de diferentes maneras, identifica el widget gracias a su posición
        en la lista "widgets"
        """
        popup = Popup(size_hint=[None, .8],width=500)
        popup.title = widget.text
        tantrum = BoxLayout(orientation="vertical")
        lower = BoxLayout(spacing="1dp", padding="1dp", size_hint_y=(0.1))
        accion = Button(background_normal="", background_color=hexed("#6644ff"), color=hexed("#00e6bf"))
        salir = Button(text="Cancelar",background_normal="", background_color=hexed("#6644ff"), color=hexed("#00e6bf"))
        lower.add_widget(accion)
        lower.add_widget(salir)
        salir.bind(on_press=popup.dismiss)
        if self.widgets[0] == widget or self.widgets[1] == widget:
            tantrum.add_widget(Label(text="Ingrese el tema", size_hint=[None,0.3], halign="center"))
            getter = TextInput(size_hint=(None, 0.1), halign="center")
            tantrum.add_widget(getter)
            if self.widgets[0] == widget: # Añadir tema - programado - probado
                accion.text = "Ingresar"
                def función(*args):
                    Modificacion_BDD().agregar_tema(getter.text)
                    popup.dismiss()
            elif self.widgets[1] == widget: # Buscar tema - programado - probado
                accion.text = "Buscar"
                encuentro = Label(text="...Esperando ingreso...")
                tantrum.add_widget(encuentro)
                def función(*args):
                    coincidencias = []
                    temas = Modificacion_BDD().temas
                    for a in temas:
                        if getter.text in a:
                            coincidencias.append(a)
                    if coincidencias.count == 0 or getter.text == "":
                        encuentro.text= "Coincdencias: 0"
                    else:    
                        encuentro.text = "Encontrados: \n" + ",\n".join(coincidencias)
            getter.bind(text=función)
            popup.content = tantrum
        else:
            temas = BDD.temas
            selector = Spinner(text="Seleccione su tema", values=temas,
                                background_normal="", background_color=hexed("#00cfff"),color=hexed("#6644ff"),
                                size_hint=[.5,None], height="30dp",sync_height=True,
                                pos_hint={"center_x":.5})
            tantrum.add_widget(selector)
            if self.widgets[2] == widget: #Modificar tema - programado - no probado
                getter = TextInput(size_hint=(None,0.1), halign="center")
                accion.text="Modificar"
                tantrum.add_widget(getter)
                def modif():
                    BDD.editar_tema(selector.text, getter.text)
                accion.bind(on_release=modif)
            elif self.widgets[3] == widget: #Eliminar tema - Programado - No probado
                accion.text="Eliminar"
                def elimi():
                    BDD.borrar_tema(selector.text)
                accion.bind(on_release=elimi)
            elif self.widgets[4] == widget:
                Add_question(size_hint=[None,None], size=[500,700]).open()
            elif self.widgets[5] == widget:  #Buscar preguntas - en proceso
                getter = TextInput(size_hint=(None, 0.1))
                accion.text = "Detalles"
                encuentro = Label(text="...Esperando ingreso...")
                tantrum.add_widget(encuentro)
                def función_prep(*args):
                    coincidencias = []
                    temas = Modificacion_BDD().preguntasDelTema(selector.text)
                    for a in temas:
                        if getter.text in a:
                            coincidencias.append(a)
                    if coincidencias.count == 0 or getter.text == "":
                        encuentro.text= "Coincdencias: 0"
                    else:    
                        encuentro.text = "Encontrados: \n" + ",\n".join(coincidencias)
                getter.bind(text=función_prep)
            elif "Modificar" in widget.text:
                pass
            elif "Eliminar" in widget.text:
                pass
            popup.content = tantrum

        tantrum.add_widget(lower)
        popup.open()

    def pop(self, widget):
        Popup(title="boton presionado", content=Label(text=widget.text), size_hint=[None,None], size=[400,200]).open()

    def file_explorer(self, widget):
        chamaco = File_explorer(size_hint=[None,None],size=[700,600])
        chamaco.open()

    def use_path(self, widget):
        try:
            BDD.traducir_excel(self.ruta)
        except:
            Popup(title="Error", content=Label(text="Archivo o ruta no valida"), size_hint=[None,None], size=[300,200]).open()

    widgets = []
    def __init__(self, **kwargs):
        texto  = StringProperty()
        self.ruta = ""
        super(CRUD, self).__init__(**kwargs)
        self.main = BoxLayout(orientation="vertical")
        cruds = ["Temas","Preguntas"]
        opciones = ["Agregar","Buscar","Modificar","Eliminar"]
        volvere = Button(text="X", background_normal="", background_color=hexed("#de3090"), color=hexed("#ffbb33"),          
                        size_hint=[None,None],size=["60dp","60dp"],
                        pos_hint={"center_x":.9})
        volvere.bind(on_release=CuestionarioApp.menu)
        self.main.add_widget(volvere)

        for a in cruds:
            texto = "Gestionar " + a
            self.main.add_widget(Label(text=texto, 
                                       size_hint=[None,.2], pos_hint={"center_x":.5}
                                       ,color=hexed("#00e6bf")))
            grid = GridLayout(cols=2, spacing="10dp", padding="15dp")
            self.main.add_widget(grid)
            for b in opciones:
                texto = b + " " + a
                boton = Button(text=(texto), background_color=hexed("#6644ff"), background_normal="",color=hexed("#000066"),
                               size_hint=[.5,None], height="60dp",
                               pos_hint={"center_x":.5})
                self.widgets.append(boton)
                boton.bind(on_press = self.gestionar)
                grid.add_widget(boton)
        self.excelsior = Button(text=f"Cargar excel: '{self.ruta}' ", size_hint=[.7,None], pos_hint={"center_x":.5}, halign="center")
        self.excelsior.text_size = (adapt_text_size(self.excelsior),None)
        self.excelsior.bind(on_release=self.use_path)
        #self.excelsior.bind(width=lambda *x: self.excelsior.setter('text_size')(self.excelsior, (self.excelsior.width, None)))
        selector = Button(text="Buscar Archivo", size_hint=[.7,None], pos_hint={"center_x":.5})
        selector.bind(on_release=self.file_explorer)
        self.main.add_widget(self.excelsior)        
        self.main.add_widget(selector)
        self.add_widget(self.main)   

class Menu(Screen):    

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.temas = BDD.temas

        parent = BoxLayout(orientation="vertical", spacing="5dp",padding="5dp")
        titulo_app = Label(text="Concurso", color=hexed("#6644ff"), font_size="120dp",
                           size_hint=[1,None])
        sup = BoxLayout(orientation="horizontal", size_hint=[1,None])
        sup.add_widget(AsyncImage(source="recursos/img/B- isologo municipal y comunal unidos/dgdd_logo.png",
                                  size_hint=[.1,3], pos_hint={"center_y":0}, fit_mode="contain"))
        sup.add_widget(Label(size_hint=[.8,None]))
        agregar = Button(text="+", background_normal="", background_color=hexed("#6644ff"), color=hexed("#00e6bf"),
                         size_hint=[None,None], size=["60dp","60dp"])
        agregar.bind(on_release=self.abrir_ingreso)
        
        sup.add_widget(agregar)
        parent.add_widget(sup)
        #parent.add_widget(titulo_app)
        parent.add_widget(AsyncImage(source="recursos/img/Emerson-01.png", size=["70dp","70dp"]))
        
        caja_tema = BoxLayout(orientation="vertical", size_hint=[.9, .9], pos_hint={"center_x":.5})
        titulo_tema = Label(text="Elija su tema:", color=hexed("#000066"), size_hint=[1,.2], font_size="30dp")
        self.elegidor_tema = GridLayout(cols=3, spacing="5dp")
        self.elegido = []
        for a in self.temas:
            boton = Button(text="{}".format(a), color=hexed("#6644ff"), background_normal="", background_color=hexed("#ffbb33"),
                           size_hint=[1, None], height="90dp", font_size="40dp")
            boton.bind(on_release=self.pintar)
            self.elegidor_tema.add_widget(boton)
            self.elegido.append(boton)

        caja_tema.add_widget(titulo_tema)
        caja_tema.add_widget(self.elegidor_tema)
        parent.add_widget(caja_tema)
        
        iniciar = Button(text="Iniciar Concurso", 
                         background_color=hexed("#0053cc"), color=hexed("#00e6bf"), background_normal="", 
                         size_hint=[.4, None], pos_hint={"center_x":0.5}, font_size="40dp")
        iniciar.bind(on_release=self.refresh_plus)
        salir = Button(text="Salir", 
                       background_color=hexed("#0053cc"), color=hexed("#00e6bf"), background_normal="", 
                       size_hint=[None,None], pos_hint={"center_x":0.5}, size=["120dp","60dp"], font_size="40dp")
        salir.bind(on_release= CuestionarioApp.salir)
        parent.add_widget(iniciar)
        sup.add_widget(salir)
        self.add_widget(Image(source="recursos/img/fondos/Fondo.png", fit_mode="fill"))
        self.add_widget(parent) 

    def refresh_plus(self, *args):
        self.refresh()
        for a in self.elegido:
            if a.color == hexed("#ffbb33"):
                    self.recargar_plus()      
            else:
                pass
            a.color = hexed("#6644ff")
            a.background_color = hexed("#ffbb33")

    def pintar(self, *args):
        b = [*args]
        if b[0].color == hexed("#6644ff"):
            for a in self.elegido:
                a.color = hexed("#6644ff")
                a.background_color = hexed("#ffbb33")
            b[0].color = hexed("#ffbb33")
            b[0].background_color = hexed("#6644ff")
        else:
            b[0].color = hexed("#6644ff")
            b[0].background_color = hexed("#ffbb33")

    def recargar_plus(self, *args):
        for a in self.elegido:
            if a.color == hexed("#ffbb33"):
                patata = a.text
        preguntas = []
        preguntas.extend(BDD.preguntasDelTema(patata))
        random.shuffle(preguntas)
        try:
            App.get_running_app().managersc.get_screen(name="quizz").titulo.text = preguntas[0]["pregunta"]
            App.get_running_app().managersc.get_screen(name="quizz").progreso.max = len(preguntas)
            App.get_running_app().managersc.get_screen(name="quizz").checkup = preguntas[0]["respuesta_correcta"]
            for a in range(3):
                App.get_running_app().managersc.get_screen(name="quizz").tepts[a].text = preguntas[0]["respuestas"][a]
            preguntas.pop(0)
            App.get_running_app().managersc.get_screen(name="quizz").preguntas =  preguntas
            
        except IndexError:
            App.get_running_app().managersc.get_screen(name="quizz").titulo.text = "- Pregunta no cargada -"
            App.get_running_app().managersc.get_screen(name="quizz").progreso.max = 0
            for a in range(3):
                App.get_running_app().managersc.get_screen(name="quizz").tepts[a].text = str(a)

    def recargar(self, *args):
        """
        Aqui se asignan los valores correspondientes, rescatando el nombre del tema y luego sacando todas las 
        preguntas asociadas a ese tema, sus respuestas correctas y las respuestas totales
        """
        for a in self.elegido:
            if a.color == hexed("#ffbb33"):
                patata = a.text
        preguntas = Modificacion_BDD().preguntasDelTema(patata)
        ying = []
        yang = []
        equilibrium = {}
        for a,b in preguntas[0].items():
            ying.append(a) 
            yang.append(b)
        random.shuffle(ying)
        random.shuffle(yang)
        for c,d in preguntas[1].items():
            equilibrium[c] = d
        try:
            App.get_running_app().managersc.get_screen(name="quizz").titulo.text = ying[0]
            App.get_running_app().managersc.get_screen(name="quizz").progreso.max = len(ying)
            App.get_running_app().managersc.get_screen(name="quizz").preguntas =  preguntas[0]
            App.get_running_app().managersc.get_screen(name="quizz").checkup = equilibrium
            for a in range(3):
                App.get_running_app().managersc.get_screen(name="quizz").tepts[a].text = preguntas[0][ying[0]][a]
            preguntas[0].pop(ying[0])
            ying.pop(0)
            App.get_running_app().managersc.get_screen(name="quizz").preguntas_label = ying
        except IndexError:
            App.get_running_app().managersc.get_screen(name="quizz").titulo.text = "- Pregunta no cargada -"
            App.get_running_app().managersc.get_screen(name="quizz").progreso.max = 0
            for a in range(3):
                App.get_running_app().managersc.get_screen(name="quizz").tepts[a].text = str(a)
        
    def refresh(self, *args):
        for a in self.elegido:
            if a.color == hexed("#ffbb33"):
                texto = a.text
                break
            else:
                texto = "nada"
        if texto in self.temas:
            CuestionarioApp.quizz(self)
        else:
            Popup(title="Error", content=Label(text="¡No has elegido un tema!"),
                  size_hint=[None,None], size=[400,200], 
                  separator_color=[.9,.4,.2,1], background_color=pophexed("#de3090")).open()
       
    def abrir_ingreso(self, *args):

        patata = GridLayout(cols=2,padding="15dp" , spacing="20dp")
        patata.add_widget(Label(text="Usuario: "))
        user = TextInput()
        user.multiline = False
        patata.add_widget(user)
        patata.add_widget(Label(text="Contraseña: "))
        passw = TextInput()
        passw.multiline = False
        patata.add_widget(passw)

        ingresar = Button(text="Ingresar")
        salir = Button(text="Salir")
        
        patata.add_widget(ingresar)
        patata.add_widget(salir)

        popup = Popup(title="Iniciar Sesión", content=patata, auto_dismiss=False, 
                      size_hint=(None,None), size=(600,320))
        
        def ingresar_usr(self, *args):
            if passw.text == "" and user.text == "":
                Popup(title="Faltan datos", content=Label(text="Por favor, rellene los datos antes de continuar"),
                      size_hint=(None,None), size=(450,200)).open()
            elif user.text != "a" or passw.text != "b":
                Popup(title="Datos incorrectos", content=Label(text="Usuario o contraseña incorrectos"),
                      size_hint=(None,None), size=[450,200]).open()
            else:
                App.get_running_app().managersc.current = "gestion"
                popup.dismiss()

        ingresar.bind(on_press= ingresar_usr)
        salir.bind(on_press=popup.dismiss)
        popup.open()

class Quizz(Screen):
  
    salir = Button(text="Volver", background_color=hexed("#de3090"),background_normal="", color=hexed("#ffbb33"),
                   size_hint=[.2,None], size=["60dp","60dp"],
                   pos_hint={"right":1})

    def resize(self, widget, text):
        if len(text)>250:
            widget.font_size -= (len(text)-250)/3
        else:
            widget.font_size = "40dp"
        
    def __init__(self, **kwargs):
        super(Quizz, self).__init__(**kwargs)
        parent = BoxLayout(orientation="vertical", padding="5dp", spacing="10dp")
        self.preguntas = []
        self.titulo = Label(text="Pregunta no cargada",color=hexed("#000000"), bold=True,
                            size_hint=[0.9,.2] , font_size="50dp", pos_hint={"center_x":.5}, halign="center")
        self.titulo.bind(width=lambda *x: self.titulo.setter('text_size')(self.titulo, (self.titulo.width, None))) # texto cuadrado dentro del label
        self.titulo.bind(texture_size=lambda *x: self.titulo.setter('height')(self.titulo, self.titulo.texture_size[1]))
        self.salir.bind(on_release=CuestionarioApp.menu)
        self.salir.bind(on_release=self.limpiar)
        parent.add_widget(self.salir)
        self.caja_respuestas = BoxLayout(orientation="vertical", padding="5dp", spacing="10dp")#background_normal="", background_color=hexed("#6644ff"))
        self.tepts = []
        for i in range(3):
            self.label = Button(text="{}".format(i), color=hexed("#6644ff"), background_normal="", background_color=hexed("#ffbb33"),
                                size_hint=[.9,.8], font_size="40dp", halign="center", pos_hint={"center_x":.5}) #los enteros representan a los pixeles
            #self.label.bind(width=lambda *x: self.label.setter('text_size')(self.label, (self.label.width, None)))
            self.label.text_size = (adapt_text_size(self.label),None)
            self.label.bind(text=self.resize)
            self.label.bind(on_release=self.pintar)
            self.tepts.append(self.label)
            self.caja_respuestas.add_widget(self.label)  
        self.checkup = None
        self.obtain = None
        self.progreso = ProgressBar(size_hint=["0.7",".2"], pos_hint={"center_x":.5})
        enviar = Button(text="¿Estas seguro(a)?", background_normal="", background_color=hexed("#dceb00"), color=hexed("#6644ff"),
                        size_hint=[.5,.2], font_size="50dp",
                          pos_hint={"center_x":.5,"center_y":.5})
        enviar.bind(on_press=self.next_plus)
        enviar.bind(text=self.resize)
        parent.add_widget(self.titulo)
        parent.add_widget(self.caja_respuestas)
        parent.add_widget(self.progreso)
        parent.add_widget(enviar)
        self.puntaje = 0
        self.add_widget(Image(source="recursos/img/fondos/Fondo.png", fit_mode="fill"))
        self.add_widget(parent)
    
    def next_plus(self, *args):
        response = False
        for a in self.tepts:
            if a.color == hexed("#ffbb33"):
                self.obtain = a.text
                if self.checkup == self.obtain:
                    sonido = SoundLoader.load("recursos/sonidos/Success Fanfare Sound Effects.mp3")
                    center = BoxLayout(orientation="vertical", padding="10dp")
                    center.add_widget(AsyncImage(source="recursos/img/iconos/smile.png",
                                                               height="100px"))
                    center.add_widget(Label(text="¡Felicitaciones!"))
                    Popup(title="Correcto", content=center, 
                          size_hint=[None,None], size=["400dp","200dp"],
                          background_color=hexed("#a7f2b0")).open() #Popup exito
                    sonido.play()   
                    response = True                 
                else:
                    sonido = SoundLoader.load("recursos/sonidos/Fail Sound Effect.mp3")
                    center = BoxLayout(orientation="vertical", padding="10dp")
                    center.add_widget(AsyncImage(source="recursos/img/iconos/failure.png",
                                                               height="100px"))
                    center.add_widget(Label(text="Vuelve a concursar"))
                    Popup(title="Incorrecto", content=center , 
                          size_hint=[None,None], size=[400,200],
                          background_color=hexed("#fa9b9b")).open() #Popup fracaso
                    sonido.play()
                    response = True
                a.color = hexed("#6644ff")
                a.background_color = hexed("#ffbb33")
                
                
                break
        if response == True:
            try:
                self.titulo.text = self.preguntas[0]["pregunta"]
                for i in range(3):
                    self.tepts[i].text = self.preguntas[0]["respuestas"][i]
                self.checkup = self.preguntas[0]["respuesta_correcta"]
                self.preguntas.pop(0)
                self.progreso.value += 1
            except:
                #self.preguntas = []
                App.get_running_app().menu()
        elif response == False:
            pass

        else:
            Popup(title="Error", 
                content=Label(text="No hay respuesta seleccionada"),
                size_hint=[None,None], size=[400,200]).open()

    def next(self, *args):
        response = False
        for a in self.tepts:
            if a.color == hexed("#ffbb33"):
                self.checklist[self.titulo.text] = a.text
                if self.checklist[self.titulo.text] == self.checkup[self.titulo.text]:
                    sonido = SoundLoader.load("recursos/sonidos/Success Fanfare Sound Effects.mp3")
                    center = BoxLayout(orientation="vertical", padding="10dp")
                    center.add_widget(AsyncImage(source="recursos/img/iconos/smile.png",
                                                               height="100dp"))
                    center.add_widget(Label(text="¡Felicitaciones!"))
                    Popup(title="Correcto", content=center, 
                          size_hint=[None,None], size=["600dp","400dp"],
                          background_color=hexed("#a7f2b0")).open() #Popup exito
                    sonido.play()   
                    response = True                 
                else:
                    sonido = SoundLoader.load("recursos/sonidos/Fail Sound Effect.mp3")
                    center = BoxLayout(orientation="vertical", padding="10dp")
                    center.add_widget(AsyncImage(source="recursos/img/iconos/failure.png",
                                                               height="100dp"))
                    center.add_widget(Label(text="Vuelve a concursar"))
                    Popup(title="Incorrecto", content=center , 
                          size_hint=[None,None], size=[600,400],
                          background_color=hexed("#fa9b9b")).open() #Popup fracaso
                    sonido.play()
                    response = True
                a.color = hexed("#6644ff")
                a.background_color = hexed("#ffbb33")
                
                break
        if response == True:
            try:
                self.titulo.text = self.preguntas_label[0]
                for i in range(3):
                    self.tepts[i].text = self.preguntas[self.preguntas_label[0]][i]
                self.preguntas[self.preguntas_label[0]]
                self.preguntas_label.pop(0)
                self.progreso.value += 1
            except:
                self.reset(self)
        elif response == False:
            pass

        else:
            Popup(title="Error", 
                content=Label(text="No hay respuesta seleccionada"),
                size_hint=[None,None], size=[400,200]).open()
            
    def reset(self, *args):
        App.get_running_app().managersc.get_screen(name="menu").elegidor_tema.text = "Seleccione su tema"
        App.get_running_app().menu()

    def pintar(self, *args):
        b = [*args]
        if b[0].color == hexed("#6644ff"):
            for a in self.tepts:
                a.color = hexed("#6644ff")
                a.background_color = hexed("#ffbb33")
            b[0].color = hexed("#ffbb33")
            b[0].background_color = hexed("#6644ff")
        else:
            b[0].color = hexed("#6644ff")
            b[0].background_color = hexed("#ffbb33")

    def limpiar(self, *args):
        for a in self.tepts:
            a.color = hexed("#6644ff")
            a.background_color = hexed("#ffbb33")
    
class tamarindo(ScreenManager):
    def __init__(self, **kwargs):
        super(tamarindo, self).__init__(**kwargs)

class CuestionarioApp(App):
    
    def build(self):
        Window.fullscreen = "auto"
        Window.clearcolor = (0,199,177)
        self.icon="1-isologo-municipal-calipso-rgb.png"
        self.managersc = tamarindo(transition=FadeTransition(clearcolor=(0,199,177)))
        pantallas = [Menu(name="menu"),CRUD(name="gestion"),Quizz(name="quizz")]
        for pantalla in pantallas:
            self.managersc.add_widget(pantalla)
        return self.managersc
    
    def quizz(self):
        App.get_running_app().managersc.current = "quizz"

    def menu(self):
        App.get_running_app().managersc.current = "menu"

    def crud(self):
        App.get_running_app().managersc.current = "gestion"

    def salir(self):
        App.get_running_app().stop()

if __name__ == "__main__":
    CuestionarioApp().run()