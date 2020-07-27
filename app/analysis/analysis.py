from app.default.models import ReadingSet


def get_reading_set(id):
    rs = ReadingSet.query.get(1)
    values = []
    times = []
    for reading in rs.readings:
        values.append(reading.value)
        times.append(reading.time_delta)

    return {"values": values,
            "times": times}