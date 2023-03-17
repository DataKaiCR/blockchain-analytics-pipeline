from datetime import datetime

def generate_path():
    year = datetime.utcnow().strftime('%Y')
    month = datetime.utcnow().strftime('%m')
    day = datetime.utcnow().strftime('%d')
    hour = datetime.utcnow().strftime('%H')
    timestamp = str(datetime.utcnow().timestamp())
    return f'{year}/{month}/{day}/{hour}/{timestamp}'