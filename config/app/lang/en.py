# korean language file
LANGUAGE_MAP = {
    # config-group
    'system': 'System',
    'notification': 'Notification',
    # config-name
    'resolution': 'resolution',
    'language': 'language',
    'refresh-interval': 'refresh interval',
    'run-on-boot': 'run on boot',
    'size': 'size',
    'animation': 'animation',
    'fade-out-time': 'fade out time',
    'auto-open': 'auto open on notify',
    # config-value
    'English': 'English',
    'Korean': 'Korean',
    'ON': 'ON',
    'OFF': 'OFF',
    'small': 'small',
    'medium': 'medium',
    'large': 'large',
    'FADE': 'fade',
    'BOUND': 'bound',
    'SMOOTH': 'smooth',
}


def resolve(key):
    return LANGUAGE_MAP.get(key)
