import time
from datetime import datetime
from picoscope import ps2000

from app import db
from app.default.models import Reading, ReadingSet

import matplotlib.pyplot as plt
import numpy as np


def run_picoscope(sampling_interval, duration, channel, coupling, v_range, v_offset):
    """ Run the picoscope and save the results to database. Returns the readingSet db object"""

    ps = ps2000.PS2000()

    (actualSamplingInterval, nSamples, maxSamples) = \
        ps.setSamplingInterval(sampleInterval=sampling_interval, duration=duration)
    ps.setChannel(channel, coupling, v_range, v_offset, enabled=True, BWLimited=False)
    ps.setSimpleTrigger('A', 1.0, 'Falling', timeout_ms=100, enabled=True)

    ps.setSigGenBuiltInSimple(offsetVoltage=0, pkToPk=1.2, waveType="Sine",
                              frequency=50E3)

    # Create a new readings set to hold the results
    rs = ReadingSet(start=datetime.now(),
                    block_duration=duration,
                    requested_sampling_interval=sampling_interval,
                    actual_sampling_interval=actualSamplingInterval,
                    samples_number=nSamples,
                    maximum_samples=maxSamples,
                    coupling=coupling,
                    v_range=v_range,
                    v_offset=v_offset)
    db.session.add(rs)
    db.session.commit()

    ps.runBlock()
    ps.waitReady()
    print("Waiting for awg to settle.")
    time.sleep(2.0)
    ps.runBlock()
    ps.waitReady()
    print("Done waiting for trigger")
    dataA = ps.getDataV('A', nSamples, returnOverflow=False)

    dataTimeAxis = np.arange(nSamples) * actualSamplingInterval
    ps.stop()
    ps.close()
    print("Connection closed.")


    for i in range(0, len(dataA)):
        reading = Reading(set_id=rs.id, value=dataA[i], time_delta=dataTimeAxis[i])
        db.session.add(reading)
    db.session.commit()

    return rs
