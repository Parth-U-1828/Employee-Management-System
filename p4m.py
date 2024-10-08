import sqlite3
import tkinter as tk
from tkinter import messagebox
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests


class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("1000x700+10+10")

        self.conn = sqlite3.connect('employees.db')
        self.create_table()

        self.create_widgets()

        self.weather_label = tk.Label(self.root, font=('Times New Roman', 20, 'bold'))
        self.weather_label.pack()

        self.api_key = 'f6b8bfc28add381904066bf0a01c1c94'
  # Replace 'YOUR_API_KEY' with your actual API key
        self.update_weather()

    def validate_employee_id(self, employee_id):
        # Employee ID should be a positive integer
        try:
            employee_id = int(employee_id)
            return employee_id > 0
        except ValueError:
            return False

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS employees
                     (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, position TEXT, salary REAL, phone TEXT)''')
        self.conn.commit()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Employee Management System", font=('Copperplate Gothic Bold', 30,'bold'))
        self.label.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Add Employee", command=self.add_employee, font=('Times New Roman', 25 ,'bold'))
        self.add_button.pack(pady=20)

        self.view_button = tk.Button(self.root, text="View Employees", command=self.view_employees,font=('Times New Roman', 25 ,'bold'))
        self.view_button.pack(pady=20)

        self.delete_button = tk.Button(self.root, text="Delete Employee", command=self.delete_employee,font=('Times New Roman', 25 ,'bold'))
        self.delete_button.pack(pady=20)

        self.update_button = tk.Button(self.root, text="Update Employee", command=self.update_employee,font=('Times New Roman',25, 'bold'))
        self.update_button.pack(pady=20)

        self.chart_button = tk.Button(self.root, text="Generate Salary Chart", command=self.generate_salary_chart,font=('Times New Roman',25 ,'bold'))
        self.chart_button.pack(pady=20)

    def validate_name(self, name):
        # Name should contain only alphabets and spaces
        return re.match("^[a-zA-Z ]+$", name) and len(name.strip()) > 0
    def validate_age(self, age):
        # Age should be a positive integer
        try:
            age = int(age)
            return age > 0
        except ValueError:
            return False

    def validate_position(self, position):
        # Position should not be empty
        return len(position.strip()) > 0

    def validate_salary(self, salary):
        # Salary should be a positive number
        try:
            salary = float(salary)
            return salary > 0
        except ValueError:
            return False

    def validate_phone(self, phone):
        # Phone should contain only digits and be 10 characters long
        return re.match("^[0-9]{10}$", phone)

    def add_employee(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Add Employee")
        self.add_window.geometry("1000x700+10+10")

       
        tk.Label(self.add_window, text="Name:",font=('Times New Roman', 25 ,'bold')).grid(row=0, column=2,padx=10,pady=10)
        tk.Label(self.add_window, text="Age:",font=('Times New Roman', 25 ,'bold')).grid(row=1, column=2,padx=10,pady=10)
        tk.Label(self.add_window, text="Position:",font=('Times New Roman', 25 ,'bold')).grid(row=2, column=2,padx=10,pady=10)
        tk.Label(self.add_window, text="Salary:",font=('Times New Roman', 25 ,'bold')).grid(row=3, column=2,padx=10,pady=10)
        tk.Label(self.add_window, text="Phone:", font=('Times New Roman', 25 ,'bold')).grid(row=4, column=2,padx=10,pady=10)

        self.name_entry = tk.Entry(self.add_window,font=('Times New Roman',25 ,'bold'))
        self.age_entry = tk.Entry(self.add_window,font=('Times New Roman', 25 ,'bold'))
        self.position_entry = tk.Entry(self.add_window,font=('Times New Roman', 25 ,'bold'))
        self.salary_entry = tk.Entry(self.add_window,font=('Times New Roman', 25 ,'bold'))
        self.phone_entry = tk.Entry(self.add_window,font=('Times New Roman', 25 ,'bold'))

        self.name_entry.grid(row=0, column=3)
        self.age_entry.grid(row=1, column=3)
        self.position_entry.grid(row=2, column=3)
        self.salary_entry.grid(row=3, column=3)
        self.phone_entry.grid(row=4, column=3)

        tk.Button(self.add_window, text="Save", command=self.save_employee,font=('Times New Roman', 25 ,'bold')).grid(row=5,columnspan=2,padx=10,pady=40)

    def save_employee(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        position = self.position_entry.get()
        salary = self.salary_entry.get()
        phone = self.phone_entry.get()

        if not self.validate_name(name):
            messagebox.showerror("Error", "Name should contain only alphabets and spaces.")
            return
        if not self.validate_age(age):
            messagebox.showerror("Error", "Invalid age.")
            return

        if not self.validate_position(position):
            messagebox.showerror("Error", "Invalid position.")
            return

        if not self.validate_salary(salary):
            messagebox.showerror("Error", "Invalid salary.")
            return


        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number format. It should contain 10 digits.")
            return

        c = self.conn.cursor()
        c.execute("INSERT INTO employees (name, age, position, salary, phone) VALUES (?, ?, ?, ?, ?)",
                  (name, age, position, salary, phone))
        self.conn.commit()
        

        self.add_window.destroy()
        messagebox.showinfo("Success", "Employee added successfully.")

    def view_employees(self):
        self.view_window = tk.Toplevel(self.root)
        self.view_window.title("View Employees")
        self.view_window.geometry("1000x700+10+10")

        c = self.conn.cursor()
        c.execute("SELECT * FROM employees")
        rows = c.fetchall()

        for i, row in enumerate(rows):
            for j, item in enumerate(row):
                tk.Label(self.view_window, text=item,font=('Times New Roman', 25 ,'bold')).grid(row=i, column=j, padx = 10, pady = 10)

    def delete_employee(self):
        self.delete_window = tk.Toplevel(self.root)
        self.delete_window.title("Delete Employee")
        self.delete_window.geometry("1000x700+10+10")

        tk.Label(self.delete_window, text="Enter ID to delete:",font=('Times New Roman',15,'bold')).grid(row=1, column=2,padx=20,pady=20)
        self.id_entry = tk.Entry(self.delete_window,font=('Times New Roman', 25 ,'bold'))
        self.id_entry.grid(row=1 ,column=3)
        tk.Button(self.delete_window, text="Delete", command=self.perform_delete,font=('Times New Roman', 25 ,'bold')).grid(row=2,columnspan=2)

    def perform_delete(self):
        employee_id = self.id_entry.get()
        if not self.validate_employee_id(employee_id):
            messagebox.showerror("Error", "Invalid employee ID.")
            return

        c = self.conn.cursor()
        c.execute("DELETE FROM employees WHERE id=?", (employee_id,))
        self.conn.commit()

        self.delete_window.destroy()
        messagebox.showinfo("Success", "Employee deleted successfully.")

    def update_employee(self):
        self.update_window = tk.Toplevel(self.root)
        self.update_window.title("Update Employee")
        self.update_window.geometry("1000x700+10+10")


        tk.Label(self.update_window, text="Enter ID to update:",font=('Times New Roman', 25 ,'bold')).grid(row=0, column=0,padx=20,pady=20)
        self.id_entry = tk.Entry(self.update_window,font=('Times New Roman', 25 ,'bold'))
        self.id_entry.grid(row=0, column=1)
        tk.Button(self.update_window, text="Update", command=self.update_employee_form,font=('Times New Roman', 25 ,'bold')).grid(row=1, columnspan=2)

    def update_employee_form(self):
        employee_id = self.id_entry.get()

        if not self.validate_employee_id(employee_id):
            messagebox.showerror("Error", "Invalid employee ID.")
            return


        self.employee_id = employee_id  # Store employee_id as an instance attribute

        c = self.conn.cursor()
        c.execute("SELECT * FROM employees WHERE id=?", (employee_id,))
        employee = c.fetchone()

        if not employee:
            messagebox.showerror("Error", "Employee ID not found.")
            return

        self.update_window.destroy()
        self.update_window = tk.Toplevel(self.root)
        self.update_window.title("Update Employee")

        tk.Label(self.update_window, text="Name:",font=('Times New Roman',25 ,'bold')).grid(row=0, column=0)
        tk.Label(self.update_window, text="Age:",font=('Times New Roman', 25 ,'bold')).grid(row=1, column=0)
        tk.Label(self.update_window, text="Position:",font=('Times New Roman', 25 ,'bold')).grid(row=2, column=0)
        tk.Label(self.update_window, text="Salary:",font=('Times New Roman', 25 ,'bold')).grid(row=3, column=0)
        tk.Label(self.update_window, text="Phone:",font=('Times New Roman', 25 ,'bold')).grid(row=4, column=0)

        self.name_entry = tk.Entry(self.update_window,font=('Times New Roman', 25 ,'bold'))
        self.age_entry = tk.Entry(self.update_window,font=('Times New Roman', 25 ,'bold'))
        self.position_entry = tk.Entry(self.update_window,font=('Times New Roman', 25 ,'bold'))
        self.salary_entry = tk.Entry(self.update_window,font=('Times New Roman', 25 ,'bold'))
        self.phone_entry = tk.Entry(self.update_window,font=('Times New Roman', 25 ,'bold'))

        self.name_entry.grid(row=0, column=1)
        self.age_entry.grid(row=1, column=1)
        self.position_entry.grid(row=2, column=1)
        self.salary_entry.grid(row=3, column=1)
        self.phone_entry.grid(row=4, column=1)

        self.name_entry.insert(0, employee[1])
        self.age_entry.insert(0, employee[2])
        self.position_entry.insert(0, employee[3])
        self.salary_entry.insert(0, employee[4])
        self.phone_entry.insert(0, employee[5])

        tk.Button(self.update_window, text="Save", command=self.save_updated_employee,font=('Times New Roman', 25 ,'bold')).grid(row=5, columnspan=2)

    def save_updated_employee(self):
        employee_id = self.employee_id
        name = self.name_entry.get()
        age = self.age_entry.get()
        position = self.position_entry.get()
        salary = self.salary_entry.get()
        phone = self.phone_entry.get()

        if not self.validate_name(name):
            messagebox.showerror("Error", "Name should contain only alphabets and spaces.")
            return

        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number format. It should contain 10 digits.")
            return

        c = self.conn.cursor()
        c.execute("UPDATE employees SET name=?, age=?, position=?, salary=?, phone=? WHERE id=?",
                  (name, age, position, salary, phone, employee_id))
        self.conn.commit()

        self.update_window.destroy()
        messagebox.showinfo("Success", "Employee details updated successfully.")

    def generate_salary_chart(self):
        self.chart_window = tk.Toplevel(self.root)
        self.chart_window.title("Salary Chart")
        self.chart_window.geometry("1000x600+10+10")


        c = self.conn.cursor()
        c.execute("SELECT position, AVG(salary) FROM employees GROUP BY position")
        rows = c.fetchall()
        positions = [row[0] for row in rows]
        avg_salaries = [row[1] for row in rows]

        fig, ax = plt.subplots()
        ax.bar(positions, avg_salaries)
        ax.set_xlabel('Position')
        ax.set_ylabel('Average Salary')
        ax.set_title('Average Salary by Position')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

   

        # Add temperature and location display
        self.weather_label = tk.Label(self.root, font=('Times New Roman', 20,'bold'))
        self.weather_label.pack()

        self.update_weather()

    def update_weather(self):
        api_key = 'f6b8bfc28add381904066bf0a01c1c94'  # Replace 'YOUR_API_KEY' with your actual API key
        city = 'Mumbai'  # You can change the city as per your preference

        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            response = requests.get(url)
            data = response.json()

            temperature = data['main']['temp']
            location = data['name']
            weather_description = data['weather'][0]['description']

            weather_info = f'{location}: {temperature}°C, {weather_description}'
            self.weather_label.config(text=weather_info)
        except Exception as e:
            print("Error fetching weather:", e)

        # Update weather every 10 minutes (600000 milliseconds)
        self.root.after(600000, self.update_weather)

    


root = tk.Tk()
app = EmployeeManagementApp(root)
root.mainloop()
