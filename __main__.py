import os
import sys
from datetime import datetime, timedelta
from math import floor
from symtable import Function

import serial
from asciimatics.screen import Screen

import payload_state
from ack_status import AckStatus
from display_pages import update_calibration_display_pages, update_data_display_pages
from log_message import LogMessage
from packets.calibration_data_bmp_180_packet import CalibrationDataBMP180Packet
from packets.calibration_data_bmp_280_packet import CalibrationDataBMP280Packet
from packets.collection_data_packet import CollectionDataPacket
from packets.loop_time_packet import LoopTimePacket
from packets.packet_types import PacketTypes, packet_lens
from packets.set_sea_level_press_packet import SetSeaLevelPressPacket
from packets.set_time_packet import SetTimePacket
from packets.string_packet import StringPacket

tty: serial.Serial | None = None

right_headers = ['Project Elijah: Payload Serial Communication', 'NASA Student Launch 2024-2025',
                 'Cedarville University']
selected_opt = 0

data_display_pages = update_data_display_pages()
calibration_display_pages = update_calibration_display_pages()
current_display_pages = data_display_pages
alt_page_selected = 0
selected_display_page = 0
is_calibration_page_selected = False

current_prompt = ''
current_input = ''
is_input_mode = False
post_enter: Function | None = None


def print_sys_log(message: str):
    payload_state.log_messages.add_message(LogMessage(message, is_system=True))


full_device_path: str | None = None


def try_connect():
    global tty, full_device_path, data_display_pages, calibration_display_pages
    try:
        if sys.platform == 'win32':
            tty = serial.Serial(port="COM4", baudrate=9600)
        else:
            devices = [device for device in os.listdir('/dev') if 'tty.usbmodem' in device]

            if len(devices) == 0:
                return

            full_device_path = f'/dev/{devices[0]}'

            tty = serial.Serial(full_device_path)
        tty.open()
        payload_state.reset_state()
        data_display_pages = update_data_display_pages()
        calibration_display_pages = update_calibration_display_pages()
    except serial.SerialException:
        return


def update_payload_clock():
    if tty is None:
        return
    tty.write(SetTimePacket().serialize())
    payload_state.time_set_ack_status = AckStatus.WAITING


def send_signal_packet(packet_type: int):
    if tty is None:
        return

    packet = bytearray()
    packet.append(packet_type.to_bytes(byteorder='little')[0])
    tty.write(packet)


def say_hello():
    if tty is None:
        return
    print_sys_log('Hello, payload \u263a')
    send_signal_packet(PacketTypes.HELLO)


def scan_bus(bus: int):
    packet_type = PacketTypes.I2C_SCAN_0 if bus == 0 else PacketTypes.I2C_SCAN_1
    send_signal_packet(packet_type)

def scan_bus_0():
    scan_bus(0)


def scan_bus_1():
    scan_bus(1)


def ds_1307_reg_dump():
    send_signal_packet(PacketTypes.DS_1307_REG_DUMP)

def ds_1307_erase():
    send_signal_packet(PacketTypes.DS_1307_ERASE)


def request_calibration_data():
    if tty is None:
        return
    packet = bytearray()
    packet.append(PacketTypes.REQ_CALIBRATION_DATA.to_bytes(byteorder='little')[0])
    tty.write(packet)


def send_sea_level_press():
    if tty is None:
        return

    global is_input_mode, post_enter
    is_input_mode = False
    post_enter = None
    try:
        send_value = float(current_input)
    except ValueError:
        print_sys_log(f"Invalid value for pressure: {current_input}")
        return

    payload_state.update_sea_level_press_ack_status = AckStatus.WAITING
    tty.write(SetSeaLevelPressPacket(send_value).serialize())


def update_sea_level_press():
    global is_input_mode, current_input, post_enter, current_prompt
    is_input_mode = True
    current_input = ""
    post_enter = send_sea_level_press
    current_prompt = "Sea level pressure (Pa):"


def handle_serial_input():
    global tty, data_display_pages, calibration_display_pages, is_input_mode
    try:
        packet_type = bytes(tty.read(1))[0]
        if packet_type not in packet_lens:
            print_sys_log(f'Unknown packet_type 0x{packet_type.to_bytes().hex()}')
            return

        packet_len = packet_lens[packet_type]
        data = bytearray()
        if packet_len > 0:
            data = bytearray(tty.read(packet_len))
        elif packet_len == -1:
            len_data = bytearray(tty.read(2))
            packet_len = len_data[0] << 8 | len_data[1]
            data = bytearray(tty.read(packet_len))

        match packet_type:
            case PacketTypes.TIME_SET_SUCCESS:
                payload_state.time_set_ack_status = AckStatus.SUCCESS
                payload_state.clear_time_set_ack_status_at = datetime.now() + timedelta(seconds=5)
            case PacketTypes.TIME_SET_FAIL:
                payload_state.time_set_ack_status = AckStatus.FAILED
                payload_state.clear_time_set_ack_status_at = datetime.now() + timedelta(seconds=5)
            case PacketTypes.COLLECTION_DATA:
                collection_data_packet = CollectionDataPacket(data)
                collection_data_packet.update_payload_state()
                data_display_pages = update_data_display_pages()
            case PacketTypes.STRING:
                payload_state.log_messages.add_message(str(StringPacket(data)))
            case PacketTypes.CALIBRATION_DATA_BMP_180:
                calib_packet = CalibrationDataBMP180Packet(data)
                calib_packet.update_payload_state()
                payload_state.calibration_data_ack_status = AckStatus.SUCCESS
                payload_state.clear_calibration_data_ack_status_at = datetime.now() + timedelta(seconds=5)
                calibration_display_pages = update_calibration_display_pages()
            case PacketTypes.CALIBRATION_DATA_BMP_280:
                calib_packet = CalibrationDataBMP280Packet(data)
                calib_packet.update_payload_state()
                payload_state.calibration_data_ack_status = AckStatus.SUCCESS
                payload_state.clear_calibration_data_ack_status_at = datetime.now() + timedelta(seconds=5)
                calibration_display_pages = update_calibration_display_pages()
            case PacketTypes.LOOP_TIME:
                loop_packet = LoopTimePacket(data)
                loop_packet.update_payload_state()
            case PacketTypes.SEA_LEVEL_PRESS_ACK_SUCCESS:
                payload_state.update_sea_level_press_ack_status = AckStatus.SUCCESS
                payload_state.clear_update_sea_level_press_ack_status_at = datetime.now() + timedelta(seconds=5)
            case PacketTypes.SEA_LEVEL_PRESS_ACK_FAIL:
                payload_state.update_sea_level_press_ack_status = AckStatus.FAILED
                payload_state.clear_update_sea_level_press_ack_status_at = datetime.now() + timedelta(seconds=5)
            case _:
                if packet_len == 0:
                    print_sys_log(f'Received unimplemented signal packet 0x{packet_type.to_bytes(1, byteorder='little').hex()}')
                else:
                    print_sys_log(f'Data for unimplemented packet 0x{packet_type.to_bytes(1, byteorder='little').hex()}: 0x{data.hex()}')
    except serial.SerialException:
        is_input_mode = False
        tty = None


def check_ack_flag_clears():
    if payload_state.clear_calibration_data_ack_status_at is not None and datetime.now() > payload_state.clear_calibration_data_ack_status_at:
        payload_state.clear_calibration_data_ack_status_at = None
        payload_state.calibration_data_ack_status = AckStatus.NOT_WAITING
    if payload_state.clear_time_set_ack_status_at is not None and datetime.now() > payload_state.clear_time_set_ack_status_at:
        payload_state.clear_time_set_ack_status_at = None
        payload_state.time_set_ack_status = AckStatus.NOT_WAITING
    if payload_state.clear_update_sea_level_press_ack_status_at is not None and datetime.now() > payload_state.clear_update_sea_level_press_ack_status_at:
        payload_state.clear_update_sea_level_press_ack_status_at = None
        payload_state.update_sea_level_press_ack_status = AckStatus.NOT_WAITING


def print_right_header(screen: Screen) -> None:
    for i in range(len(right_headers)):
        bg = Screen.COLOUR_BLACK
        if i == 1 and tty is None:
            bg = Screen.COLOUR_RED

        header = right_headers[i]
        screen.print_at(header, screen.width - len(header), i, bg=bg)


def print_bar(screen: Screen, y: int) -> None:
    screen.print_at('\u2015' * screen.width, 0, y)


def print_data(screen: Screen) -> None:
    output_len = 0
    data_page = current_display_pages[selected_display_page]
    for i in range(len(data_page)):
        label, value, unit = data_page[i]
        value_str = str(value)
        if type(value) is float:
            value_str = f'{value:.2f}'

        output_label = f'{label}: '
        screen.print_at(output_label, output_len, 4, colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_BLACK,
                        attr=screen.A_NORMAL)
        output_len += len(output_label)

        output_value = f'{value_str} {unit}' if unit != '' else value_str
        screen.print_at(output_value, output_len, 4, colour=45, bg=Screen.COLOUR_BLACK,
                        attr=screen.A_BOLD)
        output_len += len(output_value)

        if i == len(data_page) - 1:
            break

        output_sep = ' | '
        screen.print_at(output_sep, output_len, 4, colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_BLACK,
                        attr=screen.A_NORMAL)
        output_len += len(output_sep)

    calibration_data_message: str
    if is_calibration_page_selected:
        calibration_data_message = 'Press C to see payload data'
    else:
        calibration_data_message = 'Press C to see calibration data'
    calibration_data_message += '.' if len(current_display_pages) == 1 else ', or \u2190/\u2192 to switch pages.'

    if tty is not None:
        screen.print_at(calibration_data_message, screen.width - len(calibration_data_message), 4,
                        colour=243)
    print_bar(screen, 5)


user_has_quit = False

menu_options = [
    ('Say hello', say_hello),
    ('Update payload clock', update_payload_clock),
    ('Request calibration data', request_calibration_data),
    ('Scan I2C bus 0', scan_bus_0),
    ('Scan I2C bus 1', scan_bus_1),
    ('Update sea level pressure', update_sea_level_press),
    ('DS 1307 register dump', ds_1307_reg_dump),
    ('DS 1307 erase', ds_1307_erase),
    ('Clear message history', payload_state.clear_messages),
]
menu_options.sort(key=lambda opt: opt[0])


def main(screen: Screen):
    global user_has_quit, tty, selected_opt, alt_page_selected, selected_display_page
    global current_display_pages, is_calibration_page_selected
    global is_input_mode, current_input

    while True:
        if tty is None:
            try_connect()

        if screen.has_resized():
            return

        check_ack_flag_clears()
        screen.clear_buffer(Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)

        if is_calibration_page_selected:
            current_display_pages = calibration_display_pages
        else:
            current_display_pages = data_display_pages
        print_bar(screen, 3)
        print_data(screen)

        avail_space = screen.height - 8

        print_messages = payload_state.log_messages.generate_screen_text(screen.width, avail_space)
        if len(payload_state.log_messages.messages) > avail_space:
            print_messages = print_messages[-avail_space:]

        for i in range(len(print_messages)):
            message, color = print_messages[i]
            screen.print_at(message, 0, 6 + i,
                            colour=color)

        screen.print_at('System time: ', 0, 0)
        screen.print_at(datetime.now().strftime(
            '%A, %B %d, %Y %I:%M:%S %p'),
            14, 0, colour=Screen.COLOUR_WHITE)

        screen.print_at('Payload time: ', 0, 1)
        payload_time_str = payload_state.time.strftime(
            f'{payload_state.sys_day_of_week_str()}, %B %d, %Y %I:%M:%S %p') if payload_state.time is not None else '[Not Set]'

        payload_time_is_valid = payload_state.time is not None and abs(
            (datetime.now() - payload_state.time).total_seconds()) < 3

        screen.print_at(payload_time_str,
                        14, 1, colour=Screen.COLOUR_WHITE if payload_time_is_valid else Screen.COLOUR_YELLOW,
                        bg=Screen.COLOUR_BLACK if payload_time_is_valid else Screen.COLOUR_RED)

        if payload_state.time_set_ack_status != AckStatus.NOT_WAITING:
            print_pos = len(payload_time_str) + 15
            print_color = Screen.COLOUR_YELLOW
            print_text = 'Waiting for acknowledgment...'
            if payload_state.time_set_ack_status == AckStatus.SUCCESS:
                print_text = 'Time set!'
                print_color = Screen.COLOUR_GREEN
            elif payload_state.time_set_ack_status == AckStatus.FAILED:
                print_text = 'Unable to set time :('
                print_color = Screen.COLOUR_RED
            screen.print_at(print_text, print_pos, 1, colour=print_color)

        loop_time_label = 'Loop time: '
        screen.print_at(loop_time_label, 0, 2)

        loop_time_str = '{:.3} ms'.format(payload_state.last_loop_time / 100)
        screen.print_at(loop_time_str, len(loop_time_label), 2, colour=45)

        misc_ack_status_x = len(loop_time_str) + len(loop_time_label) + 1
        if payload_state.update_sea_level_press_ack_status != AckStatus.NOT_WAITING:
            print_color = Screen.COLOUR_YELLOW
            status_text = 'Waiting for sea level pressure change acknowledgment...'
            if payload_state.update_sea_level_press_ack_status == AckStatus.SUCCESS:
                status_text = 'Sea level pressure changed!'
                print_color = Screen.COLOUR_GREEN
            elif payload_state.update_sea_level_press_ack_status == AckStatus.FAILED:
                status_text = 'Unable to set sea level pressure :('
                print_color = Screen.COLOUR_RED
            screen.print_at(status_text, misc_ack_status_x, 2, colour=print_color)
            misc_ack_status_x += len(status_text) + 1


        help_text = 'Use \u2191/\u2193 to switch options and \u21B5 to select. Press Q to quit.'
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            user_has_quit = True
            return

        if tty is None:
            disconnected_text = f'PAYLOAD DISCONNECTED (device: {full_device_path if full_device_path is not None else "unknown"})'
            padding_len = floor((screen.width - len(disconnected_text)) / 2)
            disconnected_text = ' ' * padding_len + disconnected_text
            disconnected_text += ' ' * (screen.width - len(disconnected_text))
            screen.print_at(disconnected_text, 0, 1, colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_RED,
                            attr=Screen.A_BOLD)
            screen.print_at(disconnected_text, 0, screen.height - 1, colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_RED,
                            attr=Screen.A_BOLD)
            help_text = 'Payload disconnected, please reconnect to continue, or press Q to quit.'
        elif not is_input_mode:
            screen.print_at(menu_options[selected_opt][0], 0,
                            screen.height - 1, colour=Screen.COLOUR_MAGENTA)
            if ev == -203:
                selected_display_page -= 1
                if selected_display_page < 0:
                    selected_display_page = len(current_display_pages) - 1
            elif ev == -205:
                selected_display_page += 1
                if selected_display_page == len(current_display_pages):
                    selected_display_page = 0
            elif ev == -204:
                selected_opt -= 1
                if selected_opt == -1:
                    selected_opt = len(menu_options) - 1
            elif ev == -206:
                selected_opt += 1
                if selected_opt == len(menu_options):
                    selected_opt = 0
            elif ev == 10:
                menu_options[selected_opt][1]()
            elif ev in (ord('C'), ord('c')):
                current_page = selected_display_page
                selected_display_page = alt_page_selected
                alt_page_selected = current_page
                is_calibration_page_selected = not is_calibration_page_selected
        else:
            help_text = "Press ESC to cancel."
            if ev == -1:
                is_input_mode = False
            elif ev == 10:
                is_input_mode = False
                if post_enter is not None:
                    post_enter()
            elif ev == -300:
                if len(current_input) > 0:
                    current_input = current_input[:-1]
            elif ev is not None:
                current_input += chr(ev)

            screen.print_at(current_prompt, 0,
                            screen.height - 1, colour=Screen.COLOUR_MAGENTA)
            screen.print_at(current_input, len(current_prompt) + 1, screen.height - 1, colour=45)

        if tty is not None:
            additional_info_text = f'Device: {full_device_path}'
            screen.print_at(additional_info_text, screen.width - len(additional_info_text), screen.height - 1,
                            colour=243)

        screen.print_at(help_text, 0,
                        screen.height - 2, colour=Screen.COLOUR_GREEN)

        if screen.width > 105 and screen.height > 12:
            print_right_header(screen)

        screen.refresh()
        try:
            if (tty is not None) and tty.in_waiting:
                handle_serial_input()
        except OSError:
            is_input_mode = False
            tty = None


while True:
    Screen.wrapper(main)
    if user_has_quit:
        break
