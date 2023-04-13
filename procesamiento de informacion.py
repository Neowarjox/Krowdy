import json
import csv
import unicodedata

def remover_diacriticos(texto):
    # Normalizar la cadena de texto
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    # Retirar los caracteres diacríticos
    texto_sin_diacriticos = ''.join(c for c in texto_normalizado if not unicodedata.combining(c))
    # Convertir el texto a minúsculas
    texto_en_minusculas = texto_sin_diacriticos.lower()
    return texto_en_minusculas

def retirar_palabras(nombre_universidad, palabras_a_retirar):
    # Separar el nombre de la universidad en palabras
    palabras = nombre_universidad.split()

    # Filtrar las palabras que no queremos incluir
    palabras_filtradas = [palabra for palabra in palabras if palabra not in palabras_a_retirar]

    # Unir las palabras restantes en una nueva frase
    nuevo_nombre_universidad = ' '.join(palabras_filtradas)

    return nuevo_nombre_universidad

#lectura de json
with open('Universidades.json') as f:
    data = json.load(f)

nombres =[]
siglas =[]
sinonimos =[ [], [], [] ]
palabras_a_retirar = ["universidad", "escuela", "de", "del", "la", "s.a.c.", "s.r.l", "s.a."]

for item in data:
    nombre = item["Nombre "]
    sigla = item["Siglas "]

    nombre_sin_diacritico = remover_diacriticos(nombre)
    nuevo_nombre_universidad = retirar_palabras(nombre_sin_diacritico , palabras_a_retirar )

    nombres.append(nombre) 

    sinonimos[0].append(sigla.lower())
    sinonimos[1].append(nuevo_nombre_universidad)
    sinonimos[2].append(nuevo_nombre_universidad + " (" + sigla.lower() +")" )

sinonimo_universidades = []

for i in range(len(nombres)):
    dato = {}
    dato["nombre_universidad"] = nombres[i]
    dato["sinonimos"] = [sinonimos[0][i] , sinonimos[1][i], sinonimos[2][i]]
    sinonimo_universidades.append(dato)

#guardando el json sinonimo_universidades 
with open("sinonimo_universidades.json", "w") as archivo_json:
    json.dump(sinonimo_universidades, archivo_json)

#iniciando con las cabeceras
universidades_homologadas = [['candidateId', 'value', 'universidad homologada']]

# Abre el archivo CSV en modo lectura
with open('instituciones_educativas.csv', 'r') as archivo_csv:
    
    lector_csv = csv.reader(archivo_csv)
    next(lector_csv)

    for fila in lector_csv:
       
        value_sin_diacritico = remover_diacriticos(fila[1])
        value_por_verificar = retirar_palabras(value_sin_diacritico , palabras_a_retirar )

        #para prevenir errores con el split e indice -1
        if len(value_por_verificar) == 0:
          value_por_verificar = 'ERROR'

         
        palabras_value = value_por_verificar.split()
        
        palabra_value_por_verificar = palabras_value[-1]
     
        
        if ( value_por_verificar in sinonimos[0]) :
          posicion = sinonimos[0].index(value_por_verificar)
          fila.append(nombres[posicion])
        elif (value_por_verificar in sinonimos[1]) :
          posicion = sinonimos[1].index(value_por_verificar)
          fila.append(nombres[posicion])
        elif ( palabra_value_por_verificar in sinonimos[0] ):
          posicion = sinonimos[0].index(palabras_value[-1])
          fila.append(nombres[posicion])
        else: 
          fila.append("")
      
        universidades_homologadas.append(fila)
    
with open('universidades_homologadas.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(universidades_homologadas)



