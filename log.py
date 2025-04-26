import datetime
def print_as_log(message: str):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}", end=" ")
