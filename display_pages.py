import payload_state


def update_data_display_pages():
    return [
        [
            ('Pressure', payload_state.pressure, 'Pa'),
            ('Temperature', payload_state.temperature, '°C'),
            ('Altitude', payload_state.altitude, 'm'),
        ]
    ]


# def update_calibration_display_pages():
#     return [
#         [
#             ('AC1', payload_state.calibration_data.AC1 if payload_state.calibration_data is not None else -1, ''),
#             ('AC2', payload_state.calibration_data.AC2 if payload_state.calibration_data is not None else -1, ''),
#             ('AC3', payload_state.calibration_data.AC3 if payload_state.calibration_data is not None else -1, ''),
#             ('AC4', payload_state.calibration_data.AC4 if payload_state.calibration_data is not None else -1, ''),
#             ('AC5', payload_state.calibration_data.AC5 if payload_state.calibration_data is not None else -1, ''),
#             ('AC6', payload_state.calibration_data.AC6 if payload_state.calibration_data is not None else -1, '')
#         ],
#         [
#             ('B1', payload_state.calibration_data.B1 if payload_state.calibration_data is not None else -1, ''),
#             ('B2', payload_state.calibration_data.B2 if payload_state.calibration_data is not None else -1, ''),
#             ('MB', payload_state.calibration_data.MB if payload_state.calibration_data is not None else -1, ''),
#             ('MC', payload_state.calibration_data.MC if payload_state.calibration_data is not None else -1, ''),
#             ('MD', payload_state.calibration_data.MD if payload_state.calibration_data is not None else -1, '')
#         ]
#     ]

def update_calibration_display_pages():
    return [
        [
            ('T1',
             payload_state.calibration_data_bmp_280.dig_T1 if payload_state.calibration_data_bmp_280 is not None else -1,
             ''),
            ('T2',
             payload_state.calibration_data_bmp_280.dig_T2 if payload_state.calibration_data_bmp_280 is not None else -1,
             ''),
            ('T3',
             payload_state.calibration_data_bmp_280.dig_T3 if payload_state.calibration_data_bmp_280 is not None else -1,
             ''),
            ('P1',
             payload_state.calibration_data_bmp_280.dig_P1 if payload_state.calibration_data_bmp_280 is not None else -1,
             ''),
            ('P2',
             payload_state.calibration_data_bmp_280.dig_P2 if payload_state.calibration_data_bmp_280 is not None else -1,
             ''),
            ('P3',
             payload_state.calibration_data_bmp_280.dig_P3 if payload_state.calibration_data_bmp_280 is not None else -1,
             ''),
            ('P4',
             payload_state.calibration_data_bmp_280.dig_P4 if payload_state.calibration_data_bmp_280 is not None else -1,
             ''),
            ('P5',
             payload_state.calibration_data_bmp_280.dig_P5 if payload_state.calibration_data_bmp_280 is not None else -1,
             ''),
            ('P6',
             payload_state.calibration_data_bmp_280.dig_P6 if payload_state.calibration_data_bmp_280 is not None else -1,
             ''),
            ('P7',
             payload_state.calibration_data_bmp_280.dig_P7 if payload_state.calibration_data_bmp_280 is not None else -1,
             ''),
            ('P8',
             payload_state.calibration_data_bmp_280.dig_P8 if payload_state.calibration_data_bmp_280 is not None else -1,
             ''),
            ('P9',
             payload_state.calibration_data_bmp_280.dig_P9 if payload_state.calibration_data_bmp_280 is not None else -1,
             ''),
            ('Sea Level Pressure',
             payload_state.calibration_data_bmp_280.sea_level_pressure if payload_state.calibration_data_bmp_280 is not None else -1,
             'Pa'),
        ]
    ]
