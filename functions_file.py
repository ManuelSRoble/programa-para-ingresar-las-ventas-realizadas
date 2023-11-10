'''Archivo con funciones de tipo csv, txt y bd; y botones'''
#pagina 3 o bd
import mysql.connector
from mysql.connector import Error

import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox # para advertencias en imprimir graficos de barras

import pandas as pd # para csv
import csv

def volver(ventana,paginaPpal):
    borrarTodo(ventana)
    paginaPpal()

def borrarTodo(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()
        
def baseDeDatos(ventana,paginaPpal): # acepto la ventana como parametro
    # base de datos   
    # borrar elementos que habia en la pagina1
    borrarTodo(ventana)
    
    def conectarse_bd(usuario,contrasenia):
        # conectarse a la base de datos
        conexion = None
        try: 
            conexion= mysql.connector.connect(
                host="localhost",
                user=usuario,
                password=contrasenia,
                database= 'ventas'
            )
            if conexion: 
                print("conexion realizada correctamente")
                return conexion # retorno la conexion
            
        except Error as e:
            print("ha ocurrido un error:")
            print(e)
    
    
    def obtener_datos(conexion):# recibe el contenido de la tabla de la base de datos
        cursor= conexion.cursor()
        cursor.execute("SELECT * FROM tabladventas")
        #obtener todos los resultados
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    
    # funcion para agregar un producto que fue vendido            
    def agregar(conexion):
        def agregarProductoAlaBD(conexion):
            nombre = nombreProducto.get()
            precio = precioProducto.get()
            if nombre and precio and nombre.isalpha() and precio.isdigit():
                # conexion = conectarse_bd            
                cursor = conexion.cursor()   #creo un objeto cursor     
                query = "INSERT INTO tabladventas (nombre, precio) VALUES (%s, %s)"
                values = (nombre, precio)
                cursor.execute(query, values)
                conexion.commit()
                cursor.close()
                conexion.close()
                # mensaje para avisar que se agrego el dato en la bd con foreground verde
                mensaje.config(text="Producto agregado correctamente", fg="green")
            else:
                # mensaje de error
                mensaje.config(text="ingrese nombre y precio validos", fg="red")
        # flujo de la ventana de para agregar venta a la bd
        borrarTodo(ventana)
        #etiquetas y campos de entrada
        tagNombre = tk.Label(ventana, text="Nombre del producto:", bg='cyan')
        nombreProducto = tk.Entry(ventana)
        
        tagPrecio = tk.Label(ventana, text="Precio del producto:", bg='cyan')
        precioProducto = tk.Entry(ventana)
        
        
        tagNombre.place(x=10, y=20, width=200, height=15)      
        nombreProducto.place(x=10, y=45, width=200, height=20)   
        tagPrecio.place(x=10, y=70, width=200, height=15)   
        precioProducto.place(x=10, y=95, width=200, height=20)   
                
        #Boton para agregar el producto en la bd
        boton_agregar = tk.Button(ventana, text="Agregar producto", command=lambda: agregarProductoAlaBD(conexion))
        boton_agregar.place(x=10, y=135, width=200, height=25)   
        # etiqueta para mostrar mensajes
        mensaje = tk.Label(ventana, text='', fg="black",bg='cyan')
        mensaje.place(x=10, y=170, width=200, height=15)   
        # boton para volver a la pagina ppal
        botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
        botonVolver.place(x=10, y=200, width=200, height=25)   

    def modificar_entradasytags(conexion):
        borrarTodo(ventana)
        label_id= tk.Label(ventana, text="ID del producto a modificar:", bg='cyan')
        label_id.place(x=10, y=10, width=200, height=15)
        entry_id = tk.Entry(ventana)
        entry_id.place(x=10, y=28, width=200, height=20)
        
        label_nombre = tk.Label(ventana,text="Nuevo Pombre: ", bg='cyan')
        label_nombre.place(x=10, y=50, width=200, height=15)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.place(x=10, y=68, width=200, height=20)
        
        label_precio = tk.Label(ventana,text="Nuevo Precio: ", bg='cyan')
        label_precio.place(x=10, y=90, width=200, height=15)
        entry_precio = tk.Entry(ventana)
        entry_precio.place(x=10, y=108, width=200, height=20)
        
        boton_modificar = tk.Button(ventana, text="Modificar",command=lambda: modificar(conexion, entry_id, entry_nombre, entry_precio))
        boton_modificar.place(x=10, y=170, width=200, height=25)
        # boton para volver a la pagina ppal
        botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
        botonVolver.place(x=10, y=200, width=200, height=25)        
        
    def modificar(conexion, entry_id, entry_nombre, entry_precio):        
        id_value = entry_id.get()
        nombre_value = entry_nombre.get()
        precio_value = entry_precio.get()
        id_value=int(id_value)
        #variable sql
        sql = "UPDATE tabladventas SET nombre = %s, precio = %s WHERE id = %s"
        print(sql)
        values = (nombre_value, precio_value, id_value)
        #creo un cursor para ejecutar consultas sql
        cursor= conexion.cursor()
        #ejecutar la declaracion de actualizacion
        cursor.execute(sql, values)
        #confirmar los cambios en la base de datos
        conexion.commit()
        # imprimir mensaje de exito
        print("Datos actualizados correctamente")
        
        
    def desconectarse(conexion):
        #cerrar la conexion al servidor mysql
        if conexion:
            conexion.close()
            print('conexion cerrada correctamente')
            
    # funcion para mostrar en una tabla los datos de la bd
    def mostrar_tabla(datos):
        borrarTodo(ventana)
        
        tabla = ttk.Treeview(ventana)
        tabla['columns'] = ('N','Precio')
        
        tabla.column('#0', width=50, minwidth=50)
        tabla.column('N',width=100, minwidth=100)
        tabla.column('Precio', anchor=tk.W, width=100)
        
        tabla.heading('#0', text='ID')
        tabla.heading('N', text='Nombre')
        tabla.heading('Precio', text='Precio')
        
        for i, (id,nombre, precio) in enumerate(datos):
                tabla.insert(parent='', index='end', iid=i, text=id, values=(nombre,precio,))

        tabla.pack()
    
        # boton para volver a la pagina ppal
        botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
        botonVolver.pack()
        ventana.mainloop()        
        desconectarse(conexion)       
    
    
    def eliminarProducto(conexion):
        def eliminar():
            cursor= conexion.cursor()
            nombre_value= entry_nombre.get()
            sql = "DELETE FROM tabladventas WHERE nombre = %s"
            #le paso a la variable sql el nombre a eliminar con su info
            cursor.execute(sql, (nombre_value,)) #parentecis porque se string
            conexion.commit()
            cursor.close()
            print("exito")
        # borro witgets (botones de la pagina anterior)
        borrarTodo(ventana)
        #etiqueta y entrada
        label_nombre = tk.Label(ventana,text="Nombre: ", bg='cyan')
        label_nombre.place(x=10, y=20, width=200, height=20)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.place(x=10, y=50, width=200, height=25)
        # tomo el nombre que escribio en la entrada
        nombre_value= entry_nombre.get()
        # boton para confirmar el nombre a borrar
        botonDelete= tk.Button(ventana,text="Eliminar producto",command= eliminar)
        botonDelete.place(x=10, y=160, width=200, height=28)
        # boton para volver a la pagina ppal
        botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
        botonVolver.place(x=10, y=200, width=200, height=28)
        
    #flujo principal de trabajo con la bd
    usuario="root"
    contrasenia=""
    conexion=conectarse_bd(usuario,contrasenia)
    # botones
    botonMostrar = tk.Button(ventana, text="Mostrar",command= lambda: mostrar_tabla(obtener_datos(conexion)))
    botonMostrar.place(x=10, y=30,width=200,height=30)
    botonAgregar = tk.Button(ventana, text="Agregar producto",command= lambda: agregar(conexion))
    botonAgregar.place(x=10, y=70,width=200,height=30)
    botonModificar = tk.Button(ventana, text="Modificar", command=lambda: modificar_entradasytags(conexion))
    botonModificar.place(x=10, y=110,width=200,height=30)
    #boton que abre borra lo que hay en la ventana y pone una entrada para ingresar el nombre a eliminar
    botonEliminar = tk.Button(ventana, text="Eliminar producto de la base", command=lambda: eliminarProducto(conexion))
    botonEliminar.place(x=10, y=150,width=200,height=30)
    # boton para volver a la pagina ppal
    botonVolver = tk.Button(ventana,text="volver",command=lambda: volver(ventana,paginaPpal))
    botonVolver.place(x=10, y=190,width=200,height=30)

    
# txt
def archivoTXT(ventana,paginaPpal):
    borrarTodo(ventana)
    #Función para agregar datos en formato txt
    def agregar_txt(ventana): 
        def agrega(nombreProductot, precioProductot):            
            name = nombreProductot.get() #asigno el valor que esta en el entry nombreProductot a name
            price = precioProductot.get()     
            if price.isdigit(): 
                producto = name + ' ' + price + '\n'
                with open('ventas.txt', 'a') as archivo:
                    archivo.write(producto)
            else:
                print('Ingreso caracteres incorrectos')             

        def entradasybotones():
            borrarTodo(ventana)

            tagNombre = tk.Label(ventana, text="Nombre del producto:",bg="cyan")
            tagNombre.place(x=10, y=20,width=200,height=20)
            nombreProductot = tk.Entry(ventana)
            nombreProductot.place(x=10, y=45,width=200,height=20)

            tagPrecio = tk.Label(ventana, text="Precio del producto:",bg="cyan")
            tagPrecio.place(x=10, y=70,width=200,height=20)
            precioProductot = tk.Entry(ventana)
            precioProductot.place(x=10, y=95,width=200,height=20)

            botonAgregarP = tk.Button(ventana, text='Agregar', command=lambda: agrega(nombreProductot, precioProductot))
            botonAgregarP.place(x=10, y=135,width=200,height=25)

            
        #flujo para agregar, llamo al procedimiento
        entradasybotones()
        # boton para volver a la pagina ppal
        botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
        botonVolver.place(x=10, y=195,width=200,height=25)
                     
    # Función para mostrar los datos en formato txt
    def mostrar_txt(ventana):
        def leer_archivo():
            datos = [] #lista para almacenar los datos leido y separados por espacios para dividir la linea
            try: 
                with open("ventas.txt",'r') as archivo:
                    lineas = archivo.readlines()
                    #creo una lista de cada linea y la agrego a la lista 'datos'
                    for linea in lineas:
                        datos.append(linea.split()) # split separa por defecto por espacio
            except FileNotFoundError:
                print("El archivo no se encuentra o no se puede leer.")

            return datos
    
        def mostrar_tabla(datos):
            tabla = ttk.Treeview(ventana)
            tabla['columns'] = ('Precio')
            tabla.column('#0', width=100, minwidth=100)
            tabla.column('Precio', anchor=tk.W, width=100)
            tabla.heading('#0', text='Nombre')
            tabla.heading('Precio', text='Precio')

            for i, (nombre, precio) in enumerate(datos):
                tabla.insert(parent='', index='end', iid=i, text=nombre, values=(precio,))

            tabla.pack()
        #flujo de mostrar tabla
        borrarTodo(ventana)
        datos = leer_archivo()
        mostrar_tabla(datos) #envio los datos en una lista con listas (cada sublista tiene como elemento nombre y precio)
        # boton para volver a la pagina ppal
        botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
        botonVolver.pack()
            
    def modificar_txt(ventana):        
        def modificart(entry_nombret, entry_preciot, entry_nombren, entry_precion):
            nombre_value = entry_nombret.get()
            precio_value = entry_preciot.get()
            nombre_nuevo = entry_nombren.get()
            precio_nuevo = entry_precion.get()
            try:                
                # actualizar solo si los valores son numeros
                with open('ventas.txt', 'r') as archivo:
                    lineas = archivo.readlines()
                    
                lista=[]
                for linea in lineas:
                    datos = linea.split() #separar la linea en palabras
                    if len(datos) == 2:# Asumiendo que cada línea tiene dos elementos (nombre y precio)
                        nombre_archivo, precio_archivo = datos
                        if nombre_value == nombre_archivo and precio_archivo == precio_archivo:
                            nueva_linea = f"{nombre_nuevo} {precio_nuevo}\n"
                            lista.append(nueva_linea)
                        else:
                            lista.append(linea)
                with open('ventas.txt', 'w') as archivo:
                    archivo.writelines(lista)

                print("Datos actualizados correctamente")

            except ValueError:
                print('Ingresó un valor no numérico en el precio')
            
            except Exception as e:
                print(f'Error inesperado: {e}')
                        
                    
        def modificar_txt_entradasytags():
            borrarTodo(ventana)
            
            label_nombret = tk.Label(ventana, text="Nombre del producto a modificar: ", bg='cyan')
            label_nombret.place(x=10, y=10, width=200, height=15)
            entry_nombret = tk.Entry(ventana)
            entry_nombret.place(x=10, y=28, width=200, height=20)

            label_preciot = tk.Label(ventana, text="Precio del producto a modificar: ", bg='cyan')
            label_preciot.place(x=10, y=50, width=200, height=15)
            entry_preciot = tk.Entry(ventana)
            entry_preciot.place(x=10, y=68, width=200, height=20)
            
            # nombre y precio nuevo
            label_nombren = tk.Label(ventana, text="Nuevo nombre: ", bg='cyan')
            label_nombren.place(x=10, y=90, width=200, height=15)
            entry_nombren = tk.Entry(ventana,bg='#E3E3E3')
            entry_nombren.place(x=10, y=108, width=200, height=20)
            
            label_precion = tk.Label(ventana, text="Nuevo precio: ", bg='cyan')
            label_precion.place(x=10, y=130, width=200, height=15)
            entry_precion = tk.Entry(ventana, bg= '#E3E3E3')
            entry_precion.place(x=10, y=148, width=200, height=20)
            
            boton_modificart = tk.Button(ventana, text="Modificar", command=lambda: modificart(entry_nombret, entry_preciot, entry_nombren, entry_precion))
            boton_modificart.place(x=10, y=190, width=200, height=23)
            
            botonVolver = tk.Button(ventana, text="Volver atras", command=lambda: volver(ventana, paginaPpal))
            botonVolver.place(x=10, y=220, width=200, height=23)

        modificar_txt_entradasytags()
        
    def eliminar_txt(ventana):
        def eliminart(entry_nombre, entry_precio):
            nombre_value = entry_nombre.get()
            precio_value = entry_precio.get()
            lineaAeliminar = nombre_value + ' ' + precio_value + '\n'

            with open('ventas.txt', 'r') as archivo:
                lineas = archivo.readlines()

            with open('ventas.txt', 'w') as archivo:
                for linea in lineas:
                    if linea != lineaAeliminar:
                        archivo.write(linea)

        def eliminar_en_txt_entradasytags():
            borrarTodo(ventana)

            label_nombret = tk.Label(ventana, text="Nombre a eliminar: ",bg="cyan")
            label_nombret.place(x=10, y=20,width=200,height=20)
            entry_nombret = tk.Entry(ventana)
            entry_nombret.place(x=10, y=45,width=200,height=20)

            label_preciot = tk.Label(ventana, text="Precio del nombre a eliminar: ",bg="cyan")
            label_preciot.place(x=10, y=75,width=200,height=20)
            entry_preciot = tk.Entry(ventana)
            entry_preciot.place(x=10, y=100,width=200,height=20)

            boton_eliminart = tk.Button(ventana, text="Eliminar", command=lambda: eliminart(entry_nombret, entry_preciot))
            boton_eliminart.place(x=10, y=140,width=200,height=25)

            botonVolver = tk.Button(ventana, text="Volver atras", command=lambda: volver(ventana, paginaPpal))
            botonVolver.place(x=10, y=195,width=200,height=25)
            
        # llamo a la funcion para que agregue los witgets para eliminar un producto
        eliminar_en_txt_entradasytags()

    
    
    #flujo del pagina txt
    # botones
    botonMostrar = tk.Button(ventana, text="Mostrar",command= lambda: mostrar_txt(ventana))
    botonMostrar.place(x=10, y=30,width=200,height=30)
    botonAgregar = tk.Button(ventana, text="Agregar producto",command= lambda: agregar_txt(ventana))
    botonAgregar.place(x=10, y=70,width=200,height=30)
    botonModificar = tk.Button(ventana, text="Modificar", command=lambda: modificar_txt(ventana))
    botonModificar.place(x=10, y=110,width=200,height=30)
    #boton que abre borra lo que hay en la ventana y pone una entrada para ingresar el nombre a eliminar
    botonEliminar = tk.Button(ventana, text="Eliminar producto", command=lambda: eliminar_txt(ventana))
    botonEliminar.place(x=10, y=150,width=200,height=30)
    #volver
    botonVolver = tk.Button(ventana,text="volver",command=lambda: volver(ventana,paginaPpal))
    botonVolver.place(x=10, y=190,width=200,height=30)


'''=========================================================================================='''
'''========================================== CSV ==========================================='''
'''=========================================================================================='''
# Archivo CSV
def archivoCSV(ventana,paginaPpal):
    borrarTodo(ventana)
    '''
    def crear_cargar_csv():
            try:
                datos = pd.read_csv('ventas.csv')
            except FileNotFoundError:
                datos = pd.DataFrame(columns=['Nombre del producto', 'Precio'])
                datos.to_csv('ventas.csv', index=False)
            return datos
    
    def guardar_datos_csv(df):
        df.to_csv('ventas.csv', index=False)
    '''
    
    def mostrar_csv(ventana):
        def leer_archivo():
            try:
                # Lista para almacenar los datos
                datos = []
                # Leer el archivo CSV y almacenar los datos en una lista
                with open('ventas.csv', newline='') as csvfile:
                    archivo_csv = csv.reader(csvfile)
                    for fila in archivo_csv:
                        datos.append(fila)            
                return(datos)
            except Error as e:
                print('error: ',e)
        
        # Mostrar los datos leídos del archivo    
        def mostrar_tabla(datos):
            tabla = ttk.Treeview(ventana)
            tabla['columns'] = ('Precio')
            tabla.column('#0', width=100, minwidth=100)
            tabla.column('Precio', anchor=tk.W, width=100)
            tabla.heading('#0', text='Nombre')
            tabla.heading('Precio', text='Precio')

            for i, (nombre, precio) in enumerate(datos):
                tabla.insert(parent='', index='end', iid=i, text=nombre, values=(precio,))
            tabla.pack()
            
        # flujo de mostrar tabla
        borrarTodo(ventana)
        datos = leer_archivo()
        mostrar_tabla(datos) #envio los datos en una lista con listas (cada sublista tiene como elemento nombre y precio)
        botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
        botonVolver.pack()    

    def agregar_producto_csv(ventana):
        def leer_archivo():
            try:
                datos = []
                with open('ventas.csv', newline='') as csvfile:
                    archivo_csv = csv.reader(csvfile)
                    for fila in archivo_csv:
                        datos.append(fila)
                return datos
            except Exception as e:
                print('Error: ', e)

        def guardar_datos_csv(datos):
            try:
                with open('ventas.csv', 'w', newline='') as csvfile:
                    archivo_csv = csv.writer(csvfile)
                    archivo_csv.writerows(datos)
            except Exception as e:
                print('Error al guardar datos: ', e)

        def agrega_csv(nombreProducto, precioProducto, mensaje_agregar):
            nombre = nombreProducto.get()
            precio = precioProducto.get()
            if nombre and precio:
                if nombre.isalpha() and precio.isdigit():
                    try:
                        datos = leer_archivo()
                        nueva_fila = [nombre, precio]
                        datos.append(nueva_fila)
                        guardar_datos_csv(datos)
                        mensaje_agregar.config(text="Se agregó el producto correctamente")
                    except Exception as e:
                        mensaje_agregar.config(text=f"Error al agregar el producto: {str(e)}")
                else:
                    mensaje_agregar.config(text="Ingrese valores válidos")# para nombre y precio
            else:
                mensaje_agregar.config(text="Por favor, complete todos los campos")

        def entradas_botones():
            borrarTodo(ventana)

            etiquetaNombre = tk.Label(ventana, text="Nombre del producto:", bg='cyan')
            etiquetaNombre.place(x=10, y=20,width=200,height=20)
            nombreProducto = tk.Entry(ventana)
            nombreProducto.place(x=10, y=45,width=200,height=20)

            etiquetaPrecio = tk.Label(ventana, text="Precio del producto:", bg='cyan')
            etiquetaPrecio.place(x=10, y=70,width=200,height=20)
            precioProducto = tk.Entry(ventana)
            precioProducto.place(x=10, y=95,width=200,height=20)
            
            mensaje_agregar = tk.Label(ventana, text="", fg="green", bg='cyan')
            mensaje_agregar.place(x=10, y=125,width=200,height=20)

            botonAgregarProducto = tk.Button(ventana, text='Agregar', command=lambda: agrega_csv(nombreProducto, precioProducto, mensaje_agregar))
            botonAgregarProducto.place(x=10, y=150,width=200,height=25)
            
        
        # Flujo para agregar producto
        entradas_botones()
        botonVolver = tk.Button(ventana, text="Volver atras", command=lambda: volver(ventana, paginaPpal))
        botonVolver.place(x=10, y=195,width=200,height=25)

    def modificar_producto_csv(ventana):
        def modificar_csv(nombreProducto,precioProducto,nombreNuevo,precioNuevo,mensaje_modificar):
            nombre_viejo = nombreProducto.get()
            precio_viejo = precioProducto.get()
            nombre_nuevo = nombreNuevo.get()
            precio_nuevo = precioNuevo.get()
        
            if nombre_viejo and precio_viejo and nombre_nuevo and precio_nuevo:
                if nombre_viejo.isalpha() and precio_viejo.isdigit() and precio_nuevo.isdigit():
                    try:
                        with open('ventas.csv', mode='r', newline='') as infile:
                            reader = csv.reader(infile)
                            data = list(reader)

                        producto_modificado = False

                        for row in data:
                            if row[0] == nombre_viejo and row[1] == precio_viejo:
                                row[0] = nombre_nuevo
                                row[1] = precio_nuevo
                                producto_modificado = True

                        if producto_modificado:
                            with open('ventas.csv', mode='w', newline='') as outfile:
                                writer = csv.writer(outfile)
                                writer.writerows(data)
                            mensaje_modificar.config(text="Modificación realizada")
                        else:
                            mensaje_modificar.config(text="El producto no existe") # en el archivo CSV
                    except:
                        mensaje_modificar.config(text="Error al modificar") # al modificar producto
                else:
                    mensaje_modificar.config(text="Ingrese valores válidos") # para nombre y precio
            else:
                mensaje_modificar.config(text="Complete todos los campos")
            
        def entradas_botones_modificar_csv():
            borrarTodo(ventana)
            
            etiquetaNombrem = tk.Label(ventana, text="Nombre del producto a modificar: ", bg='cyan')
            etiquetaNombrem.place(x=10, y=10, width=200, height=15)
            nombreProducto = tk.Entry(ventana)
            nombreProducto.place(x=10, y=28, width=200, height=20)

            etiquetaPreciom = tk.Label(ventana, text="Precio del producto a modificar: ", bg='cyan')
            etiquetaPreciom.place(x=10, y=50, width=200, height=15)
            precioProducto = tk.Entry(ventana)
            precioProducto.place(x=10, y=68, width=200, height=20)
            
            # nombre y precio nuevo
            etiquetaNombren = tk.Label(ventana, text="Nuevo nombre: ", bg='cyan')
            etiquetaNombren.place(x=10, y=90, width=200, height=15)
            nombreNuevo = tk.Entry(ventana, bg= '#E3E3E3')
            nombreNuevo.place(x=10, y=108, width=200, height=20)
            
            etiquetaPrecion = tk.Label(ventana, text="Nuevo precio: ", bg='cyan')
            etiquetaPrecion.place(x=10, y=130, width=200, height=15)
            precioNuevo = tk.Entry(ventana, bg= '#E3E3E3')
            precioNuevo.place(x=10, y=148, width=200, height=20)
            
            mensaje_modificar = tk.Label(ventana, text="", fg="green", bg='cyan')
            mensaje_modificar.place(x=10, y=168, width=200, height=15)
            
            boton_modificarcsv = tk.Button(ventana, text="Modificar", command=lambda: modificar_csv(nombreProducto,precioProducto,nombreNuevo,precioNuevo,mensaje_modificar))
            boton_modificarcsv.place(x=10, y=190, width=200, height=25)
            
            botonVolver = tk.Button(ventana, text="Volver", command=lambda: volver(ventana, paginaPpal))
            botonVolver.place(x=10, y=220, width=200, height=25)
        #flujo
        entradas_botones_modificar_csv()
    
    def eliminar_producto_csv(ventana):
        def eliminar_csv(nombreProducto,precioProducto,mensaje_eliminar):
            nombre = nombreProducto.get()
            precio = precioProducto.get()
            
            if nombre and nombre.isalpha() and precio and precio.isdigit():
                try:
                    with open('ventas.csv', mode='r', newline='') as infile:
                        reader = csv.reader(infile)
                        data = list(reader)

                    columnas = []
                    producto_eliminado = False

                    for row in data:
                        if row[0] == nombre and row[1] == precio:
                            producto_eliminado = True
                        else:
                            columnas.append(row)

                    if producto_eliminado:
                        with open('ventas.csv', mode='w', newline='') as outfile:
                            writer = csv.writer(outfile)
                            writer.writerows(columnas)
                        mensaje_eliminar.config(text="Se eliminó el producto") # correctamente
                    else:
                        mensaje_eliminar.config(text="El producto no existe") # en el archivo CSV
                except:
                    mensaje_eliminar.config(text="Error al eliminar producto")
            else:
                mensaje_eliminar.config(text="Ingrese nombre y precio válidos")
                                
        def entradas_botones_eliminar_csv():
            borrarTodo(ventana)

            etiquetaNombree = tk.Label(ventana, text="Nombre a eliminar: ",bg="cyan")
            etiquetaNombree.place(x=10, y=20,width=200,height=20)
            nombreProducto = tk.Entry(ventana)
            nombreProducto.place(x=10, y=50,width=200,height=20)

            etiquetaPrecioe = tk.Label(ventana, text="Precio del nombre a eliminar: ",bg="cyan")
            etiquetaPrecioe.place(x=10, y=80,width=200,height=20)
            precioProducto = tk.Entry(ventana)
            precioProducto.place(x=10, y=110,width=200,height=20)
            
            mensaje_eliminar = tk.Label(ventana, text="", fg="green", bg='cyan')
            mensaje_eliminar.place(x=10, y=170)

            boton_eliminarcsv = tk.Button(ventana, text="Eliminar", command=lambda: eliminar_csv(nombreProducto,precioProducto,mensaje_eliminar))
            boton_eliminarcsv.place(x=10, y=140,width=200,height=25)

            botonVolver = tk.Button(ventana, text="Volver", command=lambda: volver(ventana, paginaPpal))
            botonVolver.place(x=10, y=200,width=200,height=25)

        entradas_botones_eliminar_csv()
    
    
    #flujo del pagina CSV
    # Botones del menú de CSV
    botonMostrar = tk.Button(ventana, text="Mostrar Archivo CSV",command= lambda: mostrar_csv(ventana))
    botonMostrar.place(x=10, y=30,width=200,height=30)
    botonAgregar = tk.Button(ventana, text="Agregar Producto",command= lambda: agregar_producto_csv(ventana))
    botonAgregar.place(x=10, y=70,width=200,height=30)
    botonModificar = tk.Button(ventana, text="Modificar", command=lambda: modificar_producto_csv(ventana))
    botonModificar.place(x=10, y=110,width=200,height=30)
    botonEliminar = tk.Button(ventana, text="Eliminar Producto", command=lambda: eliminar_producto_csv(ventana))
    botonEliminar.place(x=10, y=150,width=200,height=30)

    # Botón para volver a la página principal
    botonVolver = tk.Button(ventana, text="Volver", command=lambda: volver(ventana, paginaPpal))
    botonVolver.place(x=10, y=190, width=200, height=30)            
    



# importacion de funciones para imprimir graficos de barra

import matplotlib.pyplot as plt
from collections import Counter

#imprimir grafico de barras con matplotlib    
def imprimirGrafica(): #ventana
    #sql
    def obtener_datos_vendidos():
        try:
            # Conectarse a la base de datos
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ventas"
            )

            if conexion.is_connected():
                cursor = conexion.cursor()

                # Consulta SQL para obtener la cantidad de ventas por producto
                query = "SELECT nombre, COUNT(*) AS cantidad FROM tabladventas GROUP BY nombre"
                cursor.execute(query)

                resultados = cursor.fetchall()

                return resultados

        except Error as e:
            print("Error al conectar a la base de datos:", e)
            return []

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def crear_grafico_de_barras():
        datos = obtener_datos_vendidos()

        if not datos:
            print("No se encontraron datos para crear el gráfico.")
            return #para salir?

        nombres_productos, cantidad_ventas = zip(*datos)

        plt.bar(nombres_productos, cantidad_ventas)
        plt.xlabel("Productos")
        plt.ylabel("Cantidad de Ventas")
        plt.title("Cantidad de Ventas por Producto")

        # Guardar el gráfico en un archivo de imagen en formato JPG        
        # plt.savefig("image.jpg")
        # muestro el grafico de barras con la cantidad de ventas por producto
        plt.show()
        
    # Llamar a la función para crear el gráfico
    crear_grafico_de_barras()


#txt  
# Gráfica archivo TXT
def imprimirGraficaTXT():
    try:
        with open('ventas.txt', 'r') as archivo:
            lineas = archivo.readlines()
        
        productos_vendidos = [] # Lista que almacena productos con mismo nombre y precio
        cantidad = [] # Lista que almacena la cantidad de veces que se encuentra el mismo producto en el archivo TXT
        
        for linea in lineas:
            datos = linea.split()
            if len(datos) == 2:
                nombre, precio = datos
                producto_unico = f"{nombre} (${precio})"
                
                if producto_unico in productos_vendidos:
                    indice = productos_vendidos.index(producto_unico)
                    cantidad[indice] += 1 # Suma 1 si la combinacion o  producto_unico ya está en la lista
                else:
                    productos_vendidos.append(producto_unico)
                    cantidad.append(1)
                
        # Creo el gráfico de barras
        plt.figure(figsize=(8, 6))
        plt.bar(productos_vendidos, cantidad)
        plt.xlabel('Productos')
        plt.ylabel('Cantidad de Ventas')
        plt.title('Cantidad de Ventas por Producto (archivo TXT)')
        plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para mayor legibilidad
        plt.tight_layout()

        plt.show()

    except FileNotFoundError:
        messagebox.showinfo("El archivo TXT no existe")


#Imprimir grafica de csv 
def imprimirGraficaCSV():
    # Cargo los datos desde el archivo CSV
    def obtenerDatosCSV():
        try:
            with open('ventas.csv', mode='r', newline='') as infile:
                lector = csv.reader(infile)
                # Lee los datos existentes
                datos = list(lector)
                return datos
        except FileNotFoundError:
            messagebox.showinfo("El archivo CSV no existe")
            return None
        
    #flujo de ejecucion de la funcion
    datos = obtenerDatosCSV()
    if datos:
        # Obtener la cuenta de cada producto
        conteo_productos = Counter([dato[0] for dato in datos])

        # Obtener los nombres de los productos y sus conteos
        nombres = list(conteo_productos.keys())
        cantidades = list(conteo_productos.values())

        # Crear gráfico de barras
        plt.figure(figsize=(8, 6))
        plt.bar(nombres, cantidades)
        plt.xlabel('Nombre del Producto')
        plt.ylabel('Cantidad de Veces')
        plt.title('Gráfico de Barras de Frecuencia por Producto (archivo CSV)')
        plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para mayor legibilidad
        plt.tight_layout()  # Ajustar el diseño del gráfico
        # Mostrar el gráfico en una ventana emergente
        plt.show()
