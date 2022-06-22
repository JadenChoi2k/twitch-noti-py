# korean language file
LANGUAGE_MAP = {
    # config-group
    'system': '시스템',
    'notification': '알림',
    # config-name
    'resolution': '해상도',
    'language': '언어',
    'refresh-interval': '새로고침 빈도',
    'run-on-boot': '부팅 시 자동실행',
    'size': '알림 크기',
    'animation': '알림 애니메이션',
    'move-out-time': '알림 자동 꺼짐',
    'auto-open': '알림 도착 시 방송 켜기',
    # config-value
    'English': '영어',
    'Korean': '한국어',
    'ON': '켜기',
    'OFF': '끄기',
    'small': '작게',
    'medium': '적당하게',
    'large': '크게',
    'FADE': '페이드',
    'BOUND': '튀어오름',
    'SMOOTH': '부드럽게',
}


def resolve(key):
    return LANGUAGE_MAP[key] if LANGUAGE_MAP.get(key) else key
