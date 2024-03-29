from flask import Flask, render_template
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput,CustomJS, DatePicker
from bokeh.io import curdoc
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool
import bokeh.plotting as bpl
from bokeh.palettes import d3
import bokeh
import bokeh.models as bmo
from main import *
from datetime import date

from flask import Flask, render_template
import os
import requests

app = Flask(__name__)
today = str(date.today())

@app.route('/model/<index>/<keyword>/<startTime>/<endTime>') #, methods=['GET'])
def index(index,keyword,startTime,endTime):
    if keyword == 'empty':
        keyword = ""
    result = main(index,keyword,startTime,endTime)[0]
    data = main(index,keyword,startTime,endTime)[1]

    palette = d3['Category20'][20][:15]
    grey = palette[-1]
    palette = palette[:-1]

    result['title'] = data

    result['color'] = [
        palette[label % len(palette)]
        for label in result.labels.values
    ]

    result.loc[result.labels == -1, 'color'] = grey
    result = result[result.labels != -1]

    source = bpl.ColumnDataSource(data=result)
    hover = HoverTool(tooltips=[('title', '@title'), ('topic', '@labels')])

    # title for the graph

    p = bpl.figure(title="Topic Modelling", plot_width=1800, plot_height=1100)

    # label on x-axis
    p.xaxis.axis_label = 'X'

    # label on y-axis
    p.yaxis.axis_label = 'Y'

    # plot each datapoint as a circle
    # with custom attributes.
    p.circle(x='x',
             y='y',
             color='color',
             # fill_alpha=0.3,
             size=3,
             source=source)

    p.add_tools(hover)
    script, div = components(p)

    return render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    ).encode(encoding='UTF-8')


@app.route('/model/<index>/<keyword>/<startTime>/<endTime>/topics')
def topics(index,keyword,startTime,endTime):
    if keyword == 'empty':
        keyword = ""
    result = main(index,keyword,startTime,endTime)[0]
    data = main(index,keyword,startTime,endTime)[1]

    topic_df = topicDataFrame(data, result)

    return topic_df.to_html(header="true", table_id="table")


if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.

    app.run(host='127.0.0.1', port=8080, debug=True)
