import json
import pandas as pd


class Modificacion_BDD():
#si una variable es colocada fuera del init, puede estar sin "self"
#si está dentro del init, si o si debe tener "self." unido
    #archivo = 
    with open("recursos/data/preguntas.json", "rb") as file:
        obj:list = json.load(file)
        
    def __init__(self) -> None:
        self.temas = []
        for x in self.obj:
            self.temas.append(x["tema"])

    def traducir_excel(self, ruta:str="recursos/data/preguntas_mini.xlsx"):
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
                    print(a["tema"])
                    if pregunta in a["preguntas"]:
                        print("pregunta ya incluida")
                        break
                    else:
                        print("incluyendo pregunta")
                        a["preguntas"].append(pregunta)
                        break
                else:
                    pass#print("tema no coincidente")

        print(self.obj)
        with open("recursos/data/preguntas.json", "w") as file:
            json.dump(self.obj, file)
        #print(segmento)  

    def preguntasDelTema(self, tema):
        """
        Función para recuperar las preguntas asignadas a un tema del .JSON
        """
        #listado = {}
        #listado_respondido = {}
        listado_esp = []
        for a in self.obj:
            if a["tema"] == tema:
                #for b in a["preguntas"]:
                    #listado[b["pregunta"]] = b["respuestas"]
                    #listado_respondido[b["pregunta"]] = b["respuesta_correcta"]
                listado_esp = a["preguntas"]
        #return listado, listado_respondido
        return listado_esp

    def agregar_tema(self, tema): #probado
        data = {"tema":tema, "preguntas":[]}
        self.obj.append(data)
        with open("preguntas.json", "w") as file:
            json.dump(self.obj, file)
        print(self.obj)

    def editar_tema(self, tema, tema_new): #probado
        for alpha in self.obj:
            if alpha["tema"] == tema:
                alpha["tema"] = tema_new
        with open("preguntas.json", "w") as file:
            json.dump(self.obj, file)
        print(self.obj)

    def borrar_tema(self, tema): #probado
        for alpha in self.obj:
            if alpha["tema"] == tema:
                self.obj.remove(alpha)
                break
        with open("preguntas.json", "w") as file:
                            json.dump(self.obj, file)
        print(self.obj)

    def agregar_pregunta(self, tema:str, pregunta:dict): #probado
        for alpha in self.obj:
            if alpha["tema"] == tema:
                alpha["preguntas"].append(pregunta)
                with open("preguntas.json", "w") as file:
                    json.dump(self.obj, file)
                print(self.obj)
                break
    
    def editar_pregunta(self, tema:str, pregunta:str, pregunta_new:dict):
        for alpha in self.obj: #revisa cada elemento de la base de datos
            print("buscando tema")
            if alpha["tema"] == tema: #comprueba si el tema coincide
                print("tema coincidente")
                for a in alpha["preguntas"]: #revisa cada pregunta del tema
                    print("buscando pregunta")
                    if a["pregunta"] == pregunta: #verifica que la pregunta coincida con la que queremos modificar
                        print("pregunta encontrada")
                        for beta in pregunta_new.keys():
                            a[beta] = pregunta_new[beta]
                            print(a)
                    break
            break
        with open("preguntas.json", "w") as file:
                    json.dump(self.obj, file)

    def borrar_pregunta(self, tema:str, pregunta:str): #probado
        for alpha in self.obj:
            if alpha["tema"] == tema:
                for beta in alpha["preguntas"]:
                    if beta["pregunta"] == pregunta:
                        alpha["preguntas"].remove(beta)
                        with open("preguntas.json", "w") as file:
                            json.dump(self.obj, file)
                break

if __name__ == "__main__":
    Modificacion_BDD().traducir_excel()