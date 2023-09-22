from datetime import datetime
from tabulate import tabulate
from os import path
import csv
import logger as log
import ui_text as ui

db_file = 'database.csv'
notebook = []
last_id = 0
headers = ['ID', 'Date', 'Title', 'Text']


def read_file():
    global notebook, db_file, last_id, headers
    while True:
        if path.exists(db_file):
            with open(db_file, mode='r', encoding='utf-8', newline='') as file:
                reader = csv.reader(file, delimiter=';')
                notebook = [line for line in reader]
            last_id = int(notebook[-1][0])
            return notebook
        else:
            log.logging.error('Incorrect file')
            ui.show_error_file_message()
            ask_user = input('Would you like to create new database (y/n): ')
            if ask_user.lower() == 'y':
                with open(db_file, mode='w', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(headers)
                log.logging.info('New datafile was created')
                id_num = last_id + 1
                print('Please, create a new note.')
                note_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                note_title = input('Enter title: ')
                note_text = input('Enter text: ')
                new_note = [str(id_num), note_date, note_title, note_text]
                log.logging.info(f'Created new note with id {id_num}')
                add_data(new_note)
                print('Note successfully saved.')
                input(ui.waiting_msg)
                break
            elif ask_user.lower() == 'n':
                ui.show_exit_message()
                log.logging.info('Finish program')
                exit()
            else:
                log.logging.error('Incorrect selection')
                ui.show_error_input_msg()


def write_file(new_db):
    with open(db_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for line in new_db:
            writer.writerow(line)
    log.logging.info('New datafile was created')


def add_data(new_data):
    with open(db_file, mode='a', encoding='utf-8', newline='\n') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(new_data)
    log.logging.info('New data was added')


def create_note():
    read_file()
    id_num = last_id + 1
    note_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    note_title = input('Enter title: ')
    note_text = input('Enter text: ')
    new_note = [str(id_num), note_date, note_title, note_text]
    log.logging.info(f'Created new note with id {id_num}')
    add_data(new_note)
    print('Note successfully saved.')
    input(ui.waiting_msg)


def find_note(num_id):
    read_file()
    index_id = 0
    for i in range(1, len(notebook)):
        if notebook[i][0] == num_id: index_id = i
    return index_id


def show_all():
    read_file()
    result = [[line[i] for i in range(3)] for line in notebook]
    print(tabulate(result, headers='firstrow', tablefmt='pipe', stralign='center'))
    input(ui.waiting_msg)


def search_by_id():
    read_file()
    search = input('Enter ID of note for searching: ')
    if search == '':
        ui.show_error_input_msg()
    else:
        result = searching(id_note=search)
        if len(result) == 0:
            print('Nothing was found.')
        else:
            print(tabulate(result, headers=headers, maxcolwidths=[None, None, None, 100]))
    input(ui.waiting_msg)


def search_by_date():
    read_file()
    search = input('Enter a date of creating or modifying for searching\n'
                   '(in format YYYY-MM-DD, where YYYY - year, MM - month, DD - day, e.g. 2020-01-01): ')
    search_result = searching(date_note=search)
    if len(search_result) == 0:
        print('Nothing was found.')
    else:
        result = [[line[i] for i in range(3)] for line in search_result]
        print(tabulate(result, headers=['ID', 'Date', 'Title']))
    input(ui.waiting_msg)


def searching(id_note='', date_note=''):
    result = []
    for row in notebook:
        if id_note != '' and row[0] != id_note: continue
        if date_note != '' and row[1].find(date_note): continue
        result.append(row)
    return result


def change_note():
    id_num = input('Enter ID of editing note: ')
    ch_id_ind = find_note(id_num)
    if ch_id_ind == 0:
        print('Note not found.')
    else:
        print('Note found.')
        print(*notebook[ch_id_ind], sep='\t')
        ask_user = input("Confirm your selection (y/n): ")
        if ask_user.lower() == 'y':
            note_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            note_title = input('Enter title: ')
            note_text = input('Enter text: ')
            notebook[ch_id_ind] = [str(id_num), note_date, note_title, note_text]
            log.logging.info(f'Changed note with id {id_num}')
            write_file(notebook)
            log.logging.info('Database was changed')
            print(f'Note with ID {id_num} was changed successfully!')
            input(ui.waiting_msg)
        elif ask_user.lower() == 'n':
            print(f'Note with ID {id_num} was not changed!')
            input(ui.waiting_msg)
        else:
            log.logging.error('Incorrect selection')
            ui.show_error_input_msg()


def del_note():
    id_num = input('Enter ID of deleting note: ')
    del_id_index = find_note(id_num)
    if del_id_index == 0:
        print('Note not found.')
    else:
        print('Note found.')
        print(*notebook[del_id_index], sep='\t')
        ask_user = input("Confirm deletion (y/n): ")
        if ask_user.lower() == 'y':
            note_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            notebook[del_id_index] = [str(id_num), '', f'<Deleted {note_date}>', '']
            log.logging.info(f'Deleted note with id {del_id_index}')
            write_file(notebook)
            print(f'Note with ID {id_num} was deleted successfully!')
            log.logging.info('Database was changed')
            input(ui.waiting_msg)
        elif ask_user.lower() == 'n':
            print(f'Note with ID {id_num} was not deleted!')
            input(ui.waiting_msg)
        else:
            log.logging.error('Incorrect selection')
            ui.show_error_input_msg()