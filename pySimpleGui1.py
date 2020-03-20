import PySimpleGUI as sg

form = sg.FlexForm('PPP Simple data entry form')
# begin with a blank form
layout = [[sg.Text('Please enter your First Name, Last Name, E-Mail')],   
		[sg.Text('First Name', size=(15, 1)), sg.InputText('X')],
		[sg.Text('Last Name', size=(15, 1)), sg.InputText('Y')],
		[sg.Text('E-mail Address', size=(15, 1)), sg.InputText('Z')],
		[sg.Submit(), sg.Cancel()]]

window=sg.Window('Earth Residents Contact Data', layout)

button, values = window.Read()

window.Close() # added to fix downstream problem

print(button, values[0], values[1], values[2])

quit()