import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime, timedelta
import json
import ttkbootstrap as ttk

def replace_tabs_with_commas(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    content = content.replace('\t', ',')
    
    with open(file_path, 'w') as file:
        file.write(content)

def duplicate_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        content = file.read()
    
    with open(output_file_path, 'w') as file:
        file.write(content)
    return output_file_path

def get_date_from_day(start_date_str, day_name):
    start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
    days_of_week = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    
    if day_name not in days_of_week:
        raise ValueError("Invalid day name")
    
    start_day_index = start_date.weekday()
    target_day_index = days_of_week.index(day_name)
    
    delta_days = (target_day_index - start_day_index + 7) % 7
    target_date = start_date + timedelta(days=delta_days)
    
    return target_date.strftime('%m/%d/%Y')
        
def line_processing(start_date, active_file):
    with open(active_file, 'r') as file:
        lines = file.readlines()
    
    for i, line in enumerate(lines[1:], start=1):
        elements = line.split(',')
        lines[i] = elements
        elements.pop(0)
        
        converted_date = get_date_from_day(start_date, elements[0])
        elements[0] = converted_date
        lines[i] = ','.join(elements)
        
        elements[1] = f"{elements[3]} {elements[1]}"
        elements.pop(3)
        
        elements[-1] = f"Dosen: {elements[-1].replace('\n', '')}"
        
        start_time = elements[2].split('/')[0] if elements[2] else ''
        end_time = elements[2].split('/')[-1] if elements[2] else ''
        
        with open('timetable.json', 'r') as json_file:
            timetable = json.load(json_file)
        
        time_period = timetable["time period"].get(start_time, {})
        start_time_str = time_period.get("start", "")
        
        time_period = timetable["time period"].get(end_time, {})
        end_time_str = time_period.get("end", "")
        
        elements[2] = start_time_str
        elements.insert(3, end_time_str)

        if not start_time_str or not end_time_str:
            elements.append("True\n")
        else:
            elements.append("False\n")
        
        lines[i] = ','.join(elements)

        
        with open(active_file, 'w') as file:
            file.writelines(lines)
        
    lines[0] = "Start Date,Subject,Start Time,End Time,Description,All Day Event\n"
    
    with open(active_file, 'w') as file:
        file.writelines(lines)

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_file_path.delete(0, ttk.END)
        entry_file_path.insert(0, file_path)

def process_file():
    file_path = entry_file_path.get()
    start_date = entry_start_date.get()
    
    if not file_path or not start_date:
        messagebox.showerror("Error", "Please select a file and enter a start date.")
        return
    
    try:
        active_file = duplicate_file(file_path, "temp.astolfo")
        replace_tabs_with_commas(active_file)
        line_processing(start_date, active_file)
        messagebox.showinfo("Success", "File processed successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        entry_output_file_path.delete(0, ttk.END)
        entry_output_file_path.insert(0, file_path)

def toggle_input_method():
    if input_method.get() == "file":
        frame_file_input.grid()
        frame_manual_input.grid_remove()
    else:
        frame_file_input.grid_remove()
        frame_manual_input.grid()

def process_input():
    start_date = entry_start_date.get()
    output_file_path = entry_output_file_path.get()
    
    if not start_date or not output_file_path:
        messagebox.showerror("Error", "Please enter a start date and select an output file.")
        return
    
    try:
        if input_method.get() == "file":
            file_path = entry_file_path.get()
            if not file_path:
                messagebox.showerror("Error", "Please select a file.")
                return
            active_file = duplicate_file(file_path, output_file_path)
        else:
            data = text_manual_input.get("1.0", ttk.END).strip()
            if not data:
                messagebox.showerror("Error", "Please enter data.")
                return
            with open(output_file_path, 'w') as file:
                file.write(data)
            active_file = output_file_path
        
        replace_tabs_with_commas(active_file)
        line_processing(start_date, active_file)
        messagebox.showinfo("Success", "Data processed successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        
app = ttk.Window(themename="superhero")
app.title("UG College Schedule To Google Calendar Converter")
app.resizable(False, False)
app.iconbitmap('favicon.ico')

frame = ttk.Frame(app)
frame.pack(padx=10, pady=10)

input_method = ttk.StringVar(value="file")

top_frame = ttk.Frame(frame)
top_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

radio_file_input = ttk.Radiobutton(top_frame, text="File Input", variable=input_method, value="file", command=toggle_input_method)
radio_file_input.grid(row=0, column=0, padx=5, pady=5)

radio_manual_input = ttk.Radiobutton(top_frame, text="Manual Input", variable=input_method, value="manual", command=toggle_input_method)
radio_manual_input.grid(row=0, column=1, padx=5, pady=5)

label_start_date = ttk.Label(top_frame, text="Start Date (dd/mm/yyyy):")
label_start_date.grid(row=1, column=0, padx=5, pady=5)

entry_start_date = ttk.Entry(top_frame, width=20)
entry_start_date.grid(row=1, column=1, padx=5, pady=5)

frame_file_input = ttk.Frame(frame)
frame_file_input.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

label_file_path = ttk.Label(frame_file_input, text="Select File:")
label_file_path.grid(row=0, column=0, padx=5, pady=5)

entry_file_path = ttk.Entry(frame_file_input, width=50)
entry_file_path.grid(row=0, column=1, padx=5, pady=5)

button_browse = ttk.Button(frame_file_input, text="Browse", command=select_file)
button_browse.grid(row=0, column=2, padx=5, pady=5)

frame_manual_input = ttk.Frame(frame)
frame_manual_input.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
frame_manual_input.grid_remove()

label_manual_input = ttk.Label(frame_manual_input, text="Enter the raw data below:")
label_manual_input.grid(row=0, column=0, padx=5, pady=5, columnspan=3)

text_manual_input = ttk.Text(frame_manual_input, width=50, height=10)
text_manual_input.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

label_output_file_path = ttk.Label(frame, text="Output File:")
label_output_file_path.grid(row=3, column=0, padx=5, pady=5)

entry_output_file_path = ttk.Entry(frame, width=50)
entry_output_file_path.grid(row=3, column=1, padx=5, pady=5)

button_browse_output = ttk.Button(frame, text="Browse", command=select_output_file)
button_browse_output.grid(row=3, column=2, padx=5, pady=5)

button_process = ttk.Button(frame, text="Process", command=process_input)
button_process.grid(row=4, column=0, columnspan=3, pady=10)

app.mainloop()
