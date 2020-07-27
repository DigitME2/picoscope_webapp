from flask import render_template, abort

from app.ps_interface import bp
from app.ps_interface.ps_interface import run_picoscope
from app.ps_interface.forms import TestForm
from app.analysis.graphing import get_line_graph


@bp.route('/run_test', methods=["GET", "POST"])
def run_test():
    form = TestForm()
    if form.validate_on_submit():
        sampling_interval = parse_time_form(form.sampling_interval.data, form.sampling_interval_prefix.data)
        duration = parse_time_form(form.test_duration.data, form.test_duration_prefix.data)

        try:
            rs = run_picoscope(sampling_interval=sampling_interval,
                               duration=duration,
                               channel=form.channel.data,
                               coupling=form.coupling.data,
                               v_range=form.v_range.data,
                               v_offset=form.v_offset.data)
        except:
            return render_template('default/run_test.html', form=form, graph="Error getting readings")
        values = []
        times = []
        for reading in rs.readings:
            values.append(reading.value)
            times.append(reading.time_delta)
        graph = get_line_graph(x=times, y=values)
        return render_template('default/run_test.html', form=form, graph=graph)

    return render_template('default/run_test.html', form=form)


def parse_time_form(value, form_prefix):
    """Return the actual numerical value from two values, one number and one time prefix from a dropdown box and
    e.g. value=1, prefix=millisecond, return 0.001 """
    value = float(value)
    if form_prefix == "seconds":
        return value
    elif form_prefix == "milliseconds":
        return value / 1E3
    elif form_prefix == "microseconds":
        return value / 1E6
    elif form_prefix == "nanoseconds":
        return value / 1E9
    elif form_prefix == "picoseconds":
        return value / 1E12
    else:
        abort(400, "incorrect time prefix")

