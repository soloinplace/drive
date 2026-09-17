import json

from detector import detect_logs


with open("backend/security_test.json") as file:
    log = json.load(file)

alerts = detect_logs(log)

for alert in alerts:
    print(alert)