import payload_state


def update_data_display_pages():
    return [
        [
            ('Pressure', payload_state.pressure, 'Pa'),
            ('Temperature', payload_state.temperature, '°C'),
            ('Altitude', payload_state.altitude, 'm'),
        ]
    ]


def update_calibration_display_pages():
    return [
        [
            ('AC1', payload_state.calibration_data.AC1 if payload_state.calibration_data is not None else -1, ''),
            ('AC2', payload_state.calibration_data.AC2 if payload_state.calibration_data is not None else -1, ''),
            ('AC3', payload_state.calibration_data.AC3 if payload_state.calibration_data is not None else -1, ''),
            ('AC4', payload_state.calibration_data.AC4 if payload_state.calibration_data is not None else -1, ''),
            ('AC5', payload_state.calibration_data.AC5 if payload_state.calibration_data is not None else -1, ''),
            ('AC6', payload_state.calibration_data.AC6 if payload_state.calibration_data is not None else -1, '')
        ],
        [
            ('B1', payload_state.calibration_data.B1 if payload_state.calibration_data is not None else -1, ''),
            ('B2', payload_state.calibration_data.B2 if payload_state.calibration_data is not None else -1, ''),
            ('MB', payload_state.calibration_data.MB if payload_state.calibration_data is not None else -1, ''),
            ('MC', payload_state.calibration_data.MC if payload_state.calibration_data is not None else -1, ''),
            ('MD', payload_state.calibration_data.MD if payload_state.calibration_data is not None else -1, '')
        ]
    ]
