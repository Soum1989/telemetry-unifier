from datetime import datetime


def convert_from_format1(data):
    try:
        parts = data.get("location", "").split("/")
        country = parts[0] if len(parts) > 0 else ""
        state = parts[1] if len(parts) > 1 else ""
        plant = parts[2] if len(parts) > 2 else ""
        block = parts[3] if len(parts) > 3 else ""

        start_ts = data.get("startTime")
        end_ts = data.get("endTime")
        duration = (end_ts - start_ts) / 60000 if start_ts and end_ts else None

        return {
            "device_id": data.get("deviceID", ""),
            "device_type": data.get("deviceType", ""),
            "timestamp": data.get("timestamp"),
            "start_time": start_ts,
            "end_time": end_ts,
            "duration_minutes": round(duration, 2) if duration else None,
            "status": data.get("operationStatus", ""),
            "temperature": data.get("temp", ""),
            "vibration": data.get("vibration", ""),
            "country": country,
            "state": state,
            "plant": plant,
            "block": block
        }
    except Exception as e:
        raise Exception(f"Error in convert_from_format1: {e}")


def convert_from_format2(data):
    try:
        def parse_ts(ts_str):
            return int(datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ").timestamp() * 1000)

        start_ts = parse_ts(data["startTime"])
        end_ts = parse_ts(data["endTime"])
        duration = (end_ts - start_ts) / 60000

        return {
            "device_id": data["device"]["id"],
            "device_type": data["device"]["type"],
            "timestamp": parse_ts(data["timestamp"]),
            "start_time": start_ts,
            "end_time": end_ts,
            "duration_minutes": round(duration, 2),
            "status": data["data"].get("status", ""),
            "temperature": data["data"].get("temperature", ""),
            "vibration": data["data"].get("vibration", ""),
            "country": data.get("country", ""),
            "state": data.get("state", ""),
            "plant": data.get("plant", ""),
            "block": data.get("block", "")
        }
    except Exception as e:
        raise Exception(f"Error in convert_from_format2: {e}")
