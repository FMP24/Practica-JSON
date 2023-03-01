import json
import random
with open('./dnd.json') as fichero:
    datos=json.load(fichero)

#1. Listar información: 
#Lista de todas las clases disponibles con sus subclases
def subclassList():
    cont=0
    for clase in datos:
        cont=cont+1
        print(cont, end='. ')
        print(clase['name'])
        subclases=clase['subclasses']
        for info in subclases:
            print('subclase:',info['name'],'\n')
        
#2. Contar información:
#Muestra cuantas proeficiencias de habilidad tiene cada clase para elegir.
def proeficiencyList():
    cont=0
    for clase in datos:
        cont=cont+1
        print(cont, end='. ')
        print(clase['name'])
        listaproefs=clase['proficiency_choices']
        for info in listaproefs:
            print('Choose',info['choose'],end=': \n')
            de=list(info['from'].values())
            opciones=de[1]
            for opcion in opciones:
                indiceproef=list(opcion.values())
                datosproef=list(indiceproef[1].values())
                habilidad=datosproef[1]
                print (habilidad[6:])
            break #los instrumentos musicales estan en el mismo bloque que las habilidades por algun motivo.

#3. Buscar o filtrar información
#Buscar todas las clases que tengan proeficiencia con armaduras pesadas, y si empiezan con escudo o no. (haría falta entrar en proeficiencias de armaduras y filtrar por subcadena "heavy")
def acList():
    cont=0
    for clase in datos:
        cont=cont+1
        print(cont, end='. ')
        print(clase['name'])
        listaproefs=clase['proficiencies']
        exflag=False
        for proef in listaproefs:
            elem=list(proef.values())
            if 'heavy' in elem[0] or 'all' in elem[0]:
                exflag=True  
                print ('-Heavy armor', end='. ')

            if 'shields' in elem[0]:
                exflag=True
                print ('-Shields', end='.\n')

        if exflag==False:
            print('None found')
        print()

#4. Buscar información relacionada
# Muestra las clases, Así como la lista de proeficiencias de habilidad y equipamiento disponibles a elegir.
def startingList():
    cont=0
    for clase in datos:
        cont=cont+1
        print(cont, end='. ')
        print(clase['name'])
        listaproefs=clase['proficiency_choices']
        for info in listaproefs:
            print('\t Proficiencies (',info['choose'],')',end=': ')
            de=list(info['from'].values())
            opciones=de[1]
            for opcion in opciones:
                indiceproef=list(opcion.values())
                datosproef=list(indiceproef[1].values())
                habilidad=datosproef[1]
                print (habilidad[6:], end='.')
            break #las proeficiencias con instrumentos estan en el mismo bloque que las habilidades, pero junto al equipamiento en el bloque de las elecciones. (mira la segunda clase p. ej.)
        print()
        stequip=clase['starting_equipment']
        print ('\t Starts with:', end=' ')
        for elem in stequip:
            print (elem['equipment']['name'], end=', ')
        chcstequip=clase['starting_equipment_options']
        print('And...')
        for elem2 in chcstequip:
            print ('\t\t -',elem2['desc'])

#5. Ejercicio libre
#Crea una funcion interactiva para seleccionar clase, elegir proeficiencias de habilidad, y equipamiento inicial.
#La comento por que puede ser confusa
#Está en ingles para que se vea coherente con el JSON

def classListReturn(): #Funcion de utilidad para tener todas las clases en una lista.
    l=[]
    for clase in datos:
        l.append(clase['name'])
    return l

def characterCreation():
    listaclases=classListReturn()
    n=int(input('''Select your class.
    1. Barbarian
    2. Bard
    3. Cleric
    4. Druid
    5. Fighter
    6. Monk
    7. Paladin
    8. Ranger
    9. Rogue
    10. Sorcerer
    11. Warlock
    12. Wizard
(1-12) => '''))
    print(listaclases[n-1],'Selected.')
    nombre=input('Name your character\n => ')
    for clase in datos: #Recorrer todas la clases
        if clase['name'] == listaclases[n-1]: #Utilizar clase seleccionada solo
            listaproefs=clase['proficiency_choices']
            nchoices=clase['proficiency_choices'][0]['choose'] #nchoices: Numero de elecciones. esta dentro del mismo bloque con los metadatos, lo tengo que recoger fuera antes de recorrer todos los metadatos de todas las clases.
            for info in listaproefs:
                #Listado de proeficiencias (es literalmente la segunda funcion pero guardandolas en una variable.)
                print('Choose',info['choose'],'from:',end=' | ')
                de=list(info['from'].values())
                opciones=de[1]
                habilPermit=[]
                for opcion in opciones:
                    indiceproef=list(opcion.values())
                    datosproef=list(indiceproef[1].values())
                    habilidad=datosproef[1]
                    habilPermit.append(habilidad[7:].capitalize())
                    print(habilidad[7:], end=' | ')
                print()
                #Selección de proeficiencias + confirmación
                confirm=False
                while confirm==False:
                    habilSelec=[]
                    cont=1
                    for i in range(0,nchoices): #nchoices
                        flag=True
                        while flag==True:
                            print('(Skill',cont,end=') ')
                            habilNSel=input('=> ')
                            if habilNSel.capitalize() in habilPermit: #aquí se comprueba si la habilidad está dentro de las posibles
                                habilSelec.append(habilNSel.capitalize())
                                flag=False
                            else:
                                flag=True
                                print('Habilidad no encontrada')
                        cont=cont+1
                    print ('You\'ve selected:', end=' ')
                    for i in habilSelec:
                        print (end='"')
                        print (i,end='" ')
                    print ()
                    print ('Confirm?')
                    yn=input ('("Yes" to confirm) => ')
                    yn=yn.upper()
                    if yn =='Y' or yn == 'YE' or yn== 'YES':
                        confirm=True
                    else:
                        habilSelec=[]
                break
            #Lista de objetos iniciales.
            inventory=[]
            stequip=clase['starting_equipment']
            print ('Starting items:', end=' ') #todas las clases empiezan con algunos objetos, y despues tienen que elegir entre 2 o 3 mas.
            for elem in stequip:
                print (elem['equipment']['name'], end=', ')
                inventory.append(elem['equipment']['name'])
            chcstequip=clase['starting_equipment_options']
            print('And...')
            #Seleccion de objetos.
            for elem2 in chcstequip:
                confirm=False
                while confirm==False:
                    print ('\t -',elem2['desc'])
                    opciones=elem2['from']['options']
                    abc=input ('(a/b/c) => ')
                    abc=abc.lower()
                #Seguro que esto se puede hacer de forma mas eficiente
                    while abc != 'a' and abc != 'b' and abc != 'c':
                        abc=input ('(a/b/c) => ')
                    if abc == 'a':
                            abc=0
                    elif abc == 'b':
                            abc=1
                    elif abc == 'c':
                            abc=2
                    print ('Are you sure?')
                    yn=input ('("Yes" to confirm) => ')
                    yn=yn.upper()
                    if yn =='Y' or yn == 'YE' or yn== 'YES':
                        confirm=True
                        if opciones[abc]['option_type'] == 'choice':
                            inventory.append(opciones[abc]['choice']['desc'])
                        else:
                            inventory.append(opciones[abc]['of']['name'])
            #La cantidad de oro depende de mas cosas, pero para el proposito, con una formula general nos vale.
            gold=random.randint(4, 32)+20
            #Los atributos representan bonificadores o decrementos en las tiradas de dados. estos valores conforman lo que se llama "Standard Array" 
            attributes=[8,10,12,13,14,15]
            random.shuffle(attributes)
            print 
            #Aqui hago la ficha con toda la información por pantalla (se podría hacer tambien un return con toda la información en diccionarios)
            print ('\n\n\n')
            print (end='"')
            print (nombre, end='", ')
            print ('The level 1', clase['name'])
            print ('\n')

            print ('STR DEX CON INT WIS CHA')
            for i in attributes:
                if i ==8:
                    print(i, end='   ')
                else:
                    print (i, end='  ')
            print ('\n')

            print ('Skills:', end=' ')
            for i in habilSelec:
                print(end='"')
                print(i, end='", ')
            print ('\n')

            print ('Inventory:', end= ' ')
            for i in inventory:
                print(end='"')
                print(i, end='", ') 
            print ('And', gold, 'Gold Coins...')

#debugging:
#subclassList()
#proeficiencyList()
#acList()
#startingList()
#characterCreation()
