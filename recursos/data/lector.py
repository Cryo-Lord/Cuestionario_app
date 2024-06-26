import json
import pandas as pd


class Modificacion_BDD():
#si una variable es colocada fuera del init, puede estar sin "self"
#si está dentro del init, si o si debe tener "self." unido
    obj = None
    def reload(self):
        self.temas = []
        with open("recursos/data/preguntas.json", "rb") as file:
            self.obj = json.load(file)
        for x in self.obj:
            self.temas.append(x["tema"])
        
    def __init__(self) -> None:
        self.reload()        

    def traducir_excel(self, ruta:str="recursos/data/preguntas_mini.xlsx"): #probado
        """
        Función especifica para leer un excel, transformarlo en .JSON y ahorrar trabajo [EXPERIMENTAL]
        """
        dataframe = pd.read_excel(ruta)
        datalist = dataframe.values.tolist()
        theme_list = []
        for b in self.obj:
            if b["tema"] not in theme_list:
                theme_list.append(b["tema"])
        for list in datalist:
            if list[0] not in theme_list:
                 theme_list.append(list[0])
                 self.obj.append({"tema":list[0],"preguntas":[]})
            for a in self.obj:
                pregunta={"pregunta":list[1],"respuesta_correcta":list[-1],"respuestas":[list[2],list[3],list[4]]}
                if list[0] == a["tema"]:
                    if pregunta in a["preguntas"]:
                        print("pregunta ya incluida")
                        break
                    else:
                        print("incluyendo pregunta")
                        a["preguntas"].append(pregunta)
                        break
                else:
                    pass

        print(self.obj)
        with open("recursos/data/preguntas.json", "w") as file:
            json.dump(self.obj, file) 

    def preguntasDelTema(self, tema): #probado
        """
        Función para recuperar las preguntas asignadas a un tema del .JSON
        """
        listado_esp = []
        for a in self.obj:
            if a["tema"] == tema:
                listado_esp = a["preguntas"]
        return listado_esp

    def agregar_tema(self, tema): #probado
        data = {"tema":tema, "preguntas":[]}
        self.obj.append(data)
        with open("recursos/data/preguntas.json", "w") as file:
            json.dump(self.obj, file)
        self.reload()

    def editar_tema(self, tema, tema_new): #probado
        for alpha in self.obj:
            if alpha["tema"] == tema:
                alpha["tema"] = tema_new
        with open("recursos/data/preguntas.json", "w") as file:
            json.dump(self.obj, file)
        self.reload()

    def borrar_tema(self, tema): #probado
        for alpha in self.obj:
            if alpha["tema"] == tema:
                self.obj.remove(alpha)
                break
        with open("recursos/data/preguntas.json", "w") as file:
                            json.dump(self.obj, file)
        self.reload()

    def agregar_pregunta(self, tema:str, pregunta:dict): #probado
        for alpha in self.obj:
            if alpha["tema"] == tema:
                alpha["preguntas"].append(pregunta)
                print(alpha)
                with open("recursos/data/preguntas.json", "w") as file:
                    json.dump(self.obj, file)
                break
        self.reload()
    
    def editar_pregunta(self, tema:str, pregunta:str, pregunta_new:dict):
        for alpha in self.obj: #revisa cada elemento de la base de datos
            if alpha["tema"] == tema: #comprueba si el tema coincide
                for a in alpha["preguntas"]: #revisa cada pregunta del tema
                    if a["pregunta"] == pregunta: #verifica que la pregunta coincida con la que queremos modificar
                        print("pregunta encontrada")
                        for beta in pregunta_new.keys():
                            a[beta] = pregunta_new[beta]
                            print(a)
                        break
                break
        with open("recursos/data/preguntas.json", "w") as file:
            json.dump(self.obj, file)

    def borrar_pregunta(self, tema:str, pregunta:str): #probado
        for alpha in self.obj:
            if alpha["tema"] == tema:
                for beta in alpha["preguntas"]:
                    if beta["pregunta"] == pregunta:
                        alpha["preguntas"].remove(beta)
                        break                      
                break
        with open("recursos/data/preguntas.json", "w") as file:
            json.dump(self.obj, file)
if __name__ == "__main__":
    Modificacion_BDD().borrar_pregunta("Prueba","Pregunta_4")