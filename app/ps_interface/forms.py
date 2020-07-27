from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, InputRequired

# This list didn't work if the first values were numbers, so keep them as strings. No idea why.
time_prefix_choices = [("seconds", "s"),
                       ("milliseconds", "ms"),
                       ("microseconds", "µs"),
                       ("nanoseconds", "ns"),
                       ("picoseconds", "ps")]


class TestForm(FlaskForm):
    test_duration = FloatField('Test Duration', validators=[InputRequired()])
    test_duration_prefix = SelectField(choices=time_prefix_choices)
    sampling_interval = FloatField('Sampling Interval', validators=[InputRequired()])
    sampling_interval_prefix = SelectField(choices=time_prefix_choices)
    channel = SelectField('Channel', choices=[('A', 'A'), ('B', 'B')])
    coupling = SelectField('Coupling', choices=[('AC', 'AC'), ('DC', 'DC')])
    v_range = FloatField('V Range')
    v_offset = FloatField('V Offset')

    run = SubmitField('Run')
