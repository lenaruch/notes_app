import ui_text as ui
import logger as log
import actions as db


def operations():
    while True:
        ui.show_menu()
        user_command = input(ui.select_msg)
        if user_command == '0':
            log.logging.info('Stop program')
            ui.show_exit_message()
            exit()
        elif user_command == '1':
            log.logging.info('Show all notes')
            db.show_all()
        elif user_command == '2':
            log.logging.info('Selected by ID')
            db.search_by_id()
        elif user_command == '3':
            log.logging.info('Selected by date')
            db.search_by_date()
        elif user_command == '4':
            log.logging.info('Enter new note')
            db.create_note()
        elif user_command == '5':
            db.change_note()
        elif user_command == '6':
            db.del_note()
        elif user_command not in ['0', '1', '2', '3', '4', '5', '6']:
            log.logging.error('Incorrect selection')
            ui.show_error_input_msg()
            continue
        else:
            break