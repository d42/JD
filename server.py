from flask import Flask, Response, render_template, url_for, request
from jakdojade.orm import JakDojade
import json

app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


@app.route('/route/<line>')
def get_route(line):
    # TODO :3

    return Response(stops_json)


@app.route('/schedule/next/<line>/<stop>/<direction>')
@app.route('/schedule/next')
@app.route('/schedule/next/<line>/<stop>', defaults={'direction': None})
def get_next_departure():

    # TODO :3

    return Response(json.dumps({
        'line': line.name,
        'stop': stop.name,
        'minutes': entry.minutes,
        'hours': entry.hours,
        'heading': route.geo_direction_name
    }))


@app.route('/map/route/<line>')
def map_route(line):
    return render_template('plot_map.jade', line=line)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
