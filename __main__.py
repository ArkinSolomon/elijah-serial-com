from datetime import datetime, timedelta
from math import floor
from pyexpat.errors import messages

import serial
from asciimatics.screen import Screen

import payload_state
from ack_status import AckStatus
from log_message import LogMessage
from packets.calibration_data_packet import CalibrationDataPacket
from packets.collection_data_packet import CollectionDataPacket
from packets.packet_types import PacketTypes
from packets.set_time_packet import SetTimePacket
from packets.string_packet import StringPacket

packet_lens = {
    PacketTypes.TIME_SET: 8,
    PacketTypes.TIME_SET_SUCCESS: 0,
    PacketTypes.TIME_SET_FAIL: 0,
    PacketTypes.COLLECTION_DATA: 28,
    PacketTypes.STRING: -1,
    PacketTypes.REQ_CALIBRATION_DATA: 0,
    PacketTypes.CALIBRATION_DATA: 23
}

tty: serial.Serial | None = None

right_headers = ['Project Elijah Payload Serial Communication', 'NASA Student Launch 2024', 'Cedarville University']

def print_sys_log(message: str):
    payload_state.log_messages.add_message(LogMessage(message, is_system=True))

def try_connect():
    global tty
    try:
        tty = serial.Serial('/dev/tty.usbmodem1301')
        tty.open()
        payload_state.reset_state()
    except serial.SerialException as e:
        return


def update_payload_clock():
    if tty is None:
        return
    tty.write(SetTimePacket().serialize())
    payload_state.time_set_ack_status = AckStatus.WAITING

def request_calibration_data():
    if tty is None:
        return
    packet = bytearray()
    packet.append(PacketTypes.REQ_CALIBRATION_DATA.to_bytes(byteorder='little')[0])
    tty.write(packet)


def handle_serial_input():
    global tty
    try:
        packet_type = bytes(tty.read(1))[0]
        if packet_type not in packet_lens:
            # print(f'Unknown packet_type {packet_type.to_bytes()}')
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
            case PacketTypes.STRING:
                payload_state.log_messages.add_message(str(StringPacket(data)))
            case PacketTypes.CALIBRATION_DATA:
                calib_packet = CalibrationDataPacket(data)
                calib_packet.update_payload_state()
                payload_state.calibration_data_ack_status = AckStatus.SUCCESS
                payload_state.clear_calibration_data_ack_status_at = datetime.now() + timedelta(seconds=5)
                print_sys_log(f'Calibration Data: {calib_packet.calibration_data}')
            case _:
                print_sys_log(f'Data for unimplemented {packet_type}: 0x{data.hex()}')
    except serial.SerialException:
        tty = None


def check_ack_flag_clears():
    if payload_state.clear_calibration_data_ack_status_at is not None and datetime.now() > payload_state.clear_calibration_data_ack_status_at:
        payload_state.clear_calibration_data_ack_status_at = None
        payload_state.calibration_data_ack_status = AckStatus.NOT_WAITING
    if payload_state.clear_time_set_ack_status_at is not None and datetime.now() > payload_state.clear_time_set_ack_status_at:
        payload_state.clear_time_set_ack_status_at = None
        payload_state.time_set_ack_status = AckStatus.NOT_WAITING


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
    data: (str, any, str) = [
        ('Pressure', payload_state.pressure, 'Pa'),
        ('Temperature', payload_state.temperature, '°C'),
        ('Altitude', payload_state.altitude, 'm'),
    ]

    output_len = 0
    for i in range(len(data)):
        label, value, unit = data[i]
        value_str = str(value)
        if type(value) is float:
            value_str = f'{value:.2f}'

        output_label = f'{label}: '
        screen.print_at(output_label, output_len, 4, colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_BLACK, attr=screen.A_NORMAL)
        output_len += len(output_label)

        output_value = f'{value_str} {unit}'
        screen.print_at(output_value, output_len, 4, colour=Screen.COLOUR_CYAN, bg=Screen.COLOUR_BLACK, attr=screen.A_BOLD)
        output_len += len(output_value)

        if i == len(data) - 1:
            break

        output_sep = ' | '
        screen.print_at(output_sep, output_len, 4, colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_BLACK,
                        attr=screen.A_NORMAL)
        output_len += len(output_sep)
    print_bar(screen, 5)


request_calibration_data()
user_has_quit = False


def main(screen: Screen):
    global user_has_quit, tty

    selected_opt = 0
    options = [
        ('Update payload clock', update_payload_clock),
        ('Request calibration data', request_calibration_data),
        ('Clear message history', payload_state.clear_messages),
    ]

    while True:
        if tty is None:
            try_connect()

        if screen.has_resized():
            return

        check_ack_flag_clears()
        screen.clear_buffer(Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)

        print_bar(screen, 3)
        print_data(screen)

        avail_space = screen.height - 8

        print_messages = payload_state.log_messages.messages
        if len(payload_state.log_messages.messages) > avail_space:
            print_messages = print_messages[-avail_space:]

        for i in range(len(print_messages)):
            screen.print_at(print_messages[i], 0, 6 + i, bg=Screen.COLOUR_MAGENTA if print_messages[i].is_system else Screen.COLOUR_BLACK)

        screen.print_at('System time: ', 0, 0)
        screen.print_at(datetime.now().strftime(
            "%A, %B %d, %Y %I:%M:%S %p"),
            14, 0, colour=Screen.COLOUR_WHITE)

        screen.print_at('Payload time: ', 0, 1)
        payload_time_str = payload_state.time.strftime(
            f"{payload_state.sys_day_of_week_str()}, %B %d, %Y %I:%M:%S %p") if payload_state.time is not None else '[Not Set]'

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

        help_text = 'Use \u2191/\u2193 to switch options and \u21B5 to select. Press Q to quit.'
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            user_has_quit = True
            return

        if tty is None:
            disconnected_text = 'PAYLOAD DISCONNECTED'
            padding_len = floor((screen.width - len(disconnected_text)) / 2)
            disconnected_text = ' ' * padding_len + disconnected_text
            disconnected_text += ' ' * (screen.width - len(disconnected_text))
            screen.print_at(disconnected_text, 0, 1, colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_RED,
                            attr=Screen.A_BOLD)
            screen.print_at(disconnected_text, 0, screen.height - 1, colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_RED,
                            attr=Screen.A_BOLD)
            help_text = 'Payload disconnected, please reconnect to continue, or press Q to quit.'
        else:
            screen.print_at(options[selected_opt][0], 0,
                            screen.height - 1, colour=Screen.COLOUR_MAGENTA)

            if ev == -204:
                selected_opt -= 1
                if selected_opt == -1:
                    selected_opt = len(options) - 1
            elif ev == -206:
                selected_opt += 1
                if selected_opt == len(options):
                    selected_opt = 0
            elif ev == 10:
                options[selected_opt][1]()

        screen.print_at(help_text, 0,
                        screen.height - 2, colour=Screen.COLOUR_GREEN)

        if screen.width > 105 and screen.height > 12:
            print_right_header(screen)

        screen.refresh()
        try:
            if (tty is not None) and tty.in_waiting:
                handle_serial_input()
        except OSError:
            tty = None


while True:
    Screen.wrapper(main)
    if user_has_quit:
        break
