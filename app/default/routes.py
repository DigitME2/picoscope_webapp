from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from app.analysis import analysis
from app.analysis.graphing import get_line_graph
from app.default import bp


@bp.route('/')
def default():
    return redirect(url_for('login.login'))


@bp.route('/index')
@login_required
def index():
    """ The default page """
    if current_user.is_authenticated:
        user = {'username': current_user.username, 'id': current_user.id}
    else:
        user = {'username': "nobody"}
    return render_template('default/index.html', title='Index', user=user)


@bp.route('/test')
def test():
    import time
    from picoscope import ps2000

    import numpy as np

    ps = ps2000.PS2000()

    waveform_desired_duration = 50E-3
    obs_duration = 3 * waveform_desired_duration
    sampling_interval = obs_duration / 4096

    (actualSamplingInterval, nSamples, maxSamples) = ps.setSamplingInterval(sampling_interval, obs_duration)
    channelRange = ps.setChannel('A', 'DC', 2.0, 0.0, enabled=True, BWLimited=False)
    #ps.setSimpleTrigger('A', 1.0, 'Falling', timeout_ms=100, enabled=True)

    #ps.setSigGenBuiltInSimple(offsetVoltage=0, pkToPk=1.2, waveType="Sine", frequency=50E3)

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

    #dataA= [1,2,3]
    #dataTimeAxis = [4,5,6]

    print(dataA)
    print(dataTimeAxis)

    return render_template('default/test.html',
                           values=dataA,
                           labels=dataTimeAxis)

