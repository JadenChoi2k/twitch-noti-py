CONFIG_FILE_NAME = 'app.ini'
APP_CONFIG_CONSTANTS = {
    'system': {'resolution': ['480 X 320', '760 X 480', '1024 X 576', '1280 X 720', '1600 X 900', '1920 X 1080'],
               'language': ['English', 'Korean'],
               'refresh-interval': ['1', '3', '5', '10', '20', '30', '60'],
               'run-on-boot': ['ON', 'OFF']},
    'notification': {'size': ['small', 'medium', 'large'],
                     'animation': ['OFF', 'ENERGETIC', 'BOUND', 'SMOOTH'],
                     'move-out-time': ['1', '5', '10', '30', '60', '180', 'OFF'],
                     'auto-open': ['ON', 'OFF']}
}
VALUE_PARSER = {
    'system': {'resolution': lambda x: tuple(map(int, x.split('X'))),
               'language': lambda x: x,
               'refresh-interval': int,
               'run-on-boot': lambda x: x == 'ON'},
    'notification': {'size': lambda x: x,
                     'animation': lambda x: x,
                     'move-out-time': lambda x: int(x) if x != 'OFF' else -1,
                     'auto-open': lambda x: x == 'ON'}
}
APP_DEFAULT_SETTINGS = {
    'system': {'resolution': 2,
               'language': 1,
               'refresh-interval': 2,
               'run-on-boot': 1},
    'notification': {'size': 1,
                     'animation': 1,
                     'move-out-time': 6,
                     'auto-open': 1}
}
