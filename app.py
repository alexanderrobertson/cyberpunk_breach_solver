import flask
import solver
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if flask.request.method == 'GET':
        return flask.render_template('main.html')

    if flask.request.method == 'POST':


        p = solver.Puzzle(grid_string=flask.request.form['grid'],
                          targets=flask.request.form['targets'],
                          buffer_size=int(flask.request.form['buffer']))

        print(p)

        data = p

        fig = p.plot_graph(display=False)

        as_png = io.BytesIO()
        FigureCanvas(fig).print_png(as_png)

        encoded = f"data:image/png;base64,{base64.b64encode(as_png.getvalue()).decode('utf8')}"

        return flask.render_template('main.html', data=data, image=encoded)


if __name__ == "__main__":
    app.run(port=5000,
            threaded=True,
            debug=True,
            host='0.0.0.0')
