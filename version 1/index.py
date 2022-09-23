from tkinter import ttk
from tkinter import *
from ttkthemes import ThemedStyle

import sqlite3

class Product:
    # Connection
    db_name = 'database.db'

    def __init__(self, window):

        # Declaration of Variables
        self.cont1 = 0

        # Initialization
        self.wind = window
        self.wind.title('Base de datos de CV')

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 20, column = 0, sticky = W)

        # Table
        self.tree = ttk.Treeview(height = 10, columns = ('#1','#2','#3', '#4', '#5'))
        self.tree.grid(row = 3, column = 0, columnspan = 3)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Dirección', anchor = CENTER)
        self.tree.heading('#2', text = 'Estudios', anchor = CENTER)
        self.tree.heading('#3', text = 'Experiencia', anchor = CENTER)
        self.tree.heading('#4', text = 'Carnet de conducir', anchor = CENTER)
        self.tree.heading('#5', text = 'Edad', anchor = CENTER, command = self.sort_by_age)

        # Buttons
        ttk.Button(text = 'Agregar Persona', command = self.add_product).grid(row = 1, column = 0, sticky = W + E)
        ttk.Button(text = 'Editar Persona', command = self.edit_product).grid(row = 1, column = 1, sticky = W + E)
        ttk.Button(text = 'Eliminar Persona', command = self.delete_product).grid(row = 1, column = 2, sticky = W + E)

        # Filling the Rows
        self.get_products()

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get Products from Database
    def get_products(self):

        # Cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Getting data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)

        # Filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = (row[2], row[3], row[4], row[5], row[6]))

    # User Input Validation
    def validation(self):
        return len(self.name.get("0.0", END)) != 0

    # Lets you move from widget to widget using TAB
    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return("break")

    def sort_by_age(self):
        self.cont1 = self.cont1 + 1
        if (self.cont1 == 1):
            print("Ascendente")
        if (self.cont1 == 2):
            self.cont1 = 0
            print("Descendente")

    def add_product(self):

        # Creating a Toplevel Window
        self.edit_wind = Toplevel()
        self.edit_wind.geometry("405x570")
        self.edit_wind.title = 'Agregar Persona'

        # Create a Frame Container
        frame = LabelFrame(self.edit_wind, text = 'Agregar nueva persona', font = ("Bold", 10))
        frame.grid(row = 0, column = 0, columnspan = 5, pady = 20, padx = 40)

        # Name Input
        Label(frame, text = 'Nombre y apellido: ').grid(row = 1, column = 3)
        self.name = Text(frame, width = 20, height = 2, font = ("Bold", 10))
        self.name.focus()
        self.name.grid(row = 1, column = 4, pady = 15, padx = 25)
        self.name.bind("<Tab>", self.focus_next_widget)

        # Address Related Input
        Label(frame, text = 'Dirección: ').grid(row = 2, column = 3)
        self.address = Text(frame, width = 20, height = 2, font = ("Bold", 10))
        self.address.focus()
        self.address.grid(row = 2, column = 4, pady = 15, padx = 25)
        self.address.bind("<Tab>", self.focus_next_widget)

        # Schooling Related Input
        Label(frame, text = 'Estudios completados: ').grid(row = 3, column = 3)
        self.school = Text(frame, width = 20, height = 2, font = ("Bold", 10))
        self.school.focus()
        self.school.grid(row = 3, column = 4, pady = 15, padx = 25)
        self.school.bind("<Tab>", self.focus_next_widget)

        # Experience Related Input
        Label(frame, text = 'Experiencia laboral: ').grid(row = 4, column = 3)
        self.exp = Text(frame, width = 20, height = 2, font = ("Bold", 10))
        self.exp.focus()
        self.exp.grid(row = 4, column = 4, pady = 15, padx = 25)
        self.exp.bind("<Tab>", self.focus_next_widget)

        # Driving License Related Input
        Label(frame, text = 'Carnet de conducir: ').grid(row = 5, column = 3)
        self.drive = Text(frame, width = 20, height = 2, font = ("Bold", 10))
        self.drive.focus()
        self.drive.grid(row = 5, column = 4, pady = 15, padx = 25)
        self.drive.bind("<Tab>", self.focus_next_widget)

        # Age Related Input
        Label(frame, text = 'Edad (en numero): ').grid(row = 6, column = 3)
        self.age = Text(frame, width = 20, height = 2, font = ("Bold", 10))
        self.age.focus()
        self.age.grid(row = 6, column = 4, pady = 15, padx = 25)
        self.age.bind("<Tab>", self.focus_next_widget)

        # Button Add New Person
        ttk.Button(frame, text = 'Agregar Empleado', command = self.add_product_backend).grid(row = 8, columnspan = 8, column = 4, pady = 15, padx = 25)

    def add_product_backend(self):

        if self.validation():
            query = 'INSERT INTO product(name, direccion, estudios, experiencia, carnet, edad) VALUES (?, ?, ?, ?, ?, ?)'
            parameters =  (self.name.get("0.0", END), self.address.get("0.0", END), self.school.get("0.0", END), self.exp.get("0.0", END), self.drive.get("0.0", END), self.age.get("0.0", END))
            self.run_query(query, parameters)
            self.message['text'] = 'Persona {} agregada satisfactoriamente'.format(self.name.get("0.0", END))
            self.name.delete("0.0", END)
            self.address.delete("0.0", END)
            self.school.delete("0.0", END)
            self.exp.delete("0.0", END)
            self.drive.delete("0.0", END)
            self.age.delete("0.0", END)

            self.edit_wind.destroy()
            self.edit_wind.update()

        else:
            self.message['text'] = 'Mínimamente Nombre y Apellido requeridos'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Seleccione una persona'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Persona ({}) eliminada satisfactoriamente'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Seleccione una persona'
            return
        name = self.tree.item(self.tree.selection())['text']
        address = self.tree.item(self.tree.selection())['values'][0]
        school = self.tree.item(self.tree.selection())['values'][1]
        exp = self.tree.item(self.tree.selection())['values'][2]
        drive = self.tree.item(self.tree.selection())['values'][3]
        age = self.tree.item(self.tree.selection())['values'][4]

        # Creating a Toplevel Window
        self.edit_wind = Toplevel()
        self.edit_wind.geometry("370x470")
        self.edit_wind.title = 'Editar Persona'

        # Create a Frame Container
        frame = LabelFrame(self.edit_wind, text = 'Editar persona', font = ("Bold", 10))
        frame.grid(row = 0, column = 0, columnspan = 5, pady = 20, padx = 40)

        # Name
        Label(frame, text = 'Nombre:').grid(row = 0, column = 1)
        new_name = Entry(frame, textvariable = StringVar(self.edit_wind, value = name))
        new_name.grid(row = 0, column = 2, pady = 15, padx = 25)

        # Direccion
        Label(frame, text = 'Dirección:').grid(row = 1, column = 1)
        new_address = Entry(frame, textvariable = StringVar(self.edit_wind, value = address))
        new_address.grid(row = 1, column = 2, pady = 15, padx = 25)

        # Estudios
        Label(frame, text = 'Estudios:').grid(row = 2, column = 1)
        new_school = Entry(frame, textvariable = StringVar(self.edit_wind, value = school))
        new_school.grid(row = 2, column = 2, pady = 15, padx = 25)

        # Experiencia
        Label(frame, text = 'Experiencia:').grid(row = 3, column = 1)
        new_exp = Entry(frame, textvariable = StringVar(self.edit_wind, value = exp))
        new_exp.grid(row = 3, column = 2, pady = 15, padx = 25)

        # Carnet de conducir
        Label(frame, text = 'Carnet de conducir:').grid(row = 4, column = 1)
        new_drive = Entry(frame, textvariable = StringVar(self.edit_wind, value = drive))
        new_drive.grid(row = 4, column = 2, pady = 15, padx = 25)

        # Edad
        Label(frame, text = 'Edad:').grid(row = 5, column = 1)
        new_age = Entry(frame, textvariable = StringVar(self.edit_wind, value = age))
        new_age.grid(row = 5, column = 2, pady = 15, padx = 25)

        ttk.Button(frame, text = 'Actualizar', command = lambda: self.edit_records(new_name.get(), name, new_address.get(), address, new_school.get(), school, new_exp.get(), exp, new_drive.get(), drive, new_age.get(), age)).grid(row = 8, column = 2, sticky = W, pady = 15, padx = 25)

    def edit_records(self, new_name, name, new_address, address, new_school, school, new_exp, exp, new_drive, drive, new_age, age):

        print("Variable name")
        print(name)
        print("Variable new_name")
        print(new_name)

        query = 'UPDATE product SET name = ?, direccion = ?, estudios = ?, experiencia = ?, carnet = ?, edad = ? WHERE name = ? AND direccion = ? AND estudios = ? AND experiencia = ? AND carnet = ? AND edad = ?'
        parameters = (new_name, new_address, new_school, new_exp, new_drive, new_age, name, address, school, exp, drive, age)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Persona ({}) actualizada satisfactoriamente'.format(name)
        self.get_products()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    style = ThemedStyle(window)
    style.set_theme("adapta")
    window.mainloop()
