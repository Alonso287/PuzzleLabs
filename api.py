from flask import Flask, jsonify, request

import draw
from mitm import Mitm

app = Flask(__name__)


@app.route("/puzzle", methods=["GET"])
def get_puzzle():
    # Tamaño del puzle desde parámetros GET
    w = int(request.args.get("w", 6))
    h = int(request.args.get("h", 6))

    # Inicializar mitm
    mitm = Mitm(lr_price=2, t_price=1)
    mitm.prepare(min(20, max(h, 6)))

    # Generar puzle
    grid = gen_puzzle(w, h, mitm)
    color_grid, _ = draw.color_tubes(grid, no_colors=True)

    # Convertir a formato de consola
    salida = ""
    for y in range(color_grid.h):
        for x in range(color_grid.w):
            if grid[x, y] in "v^<>":
                salida += color_grid[x, y]
            else:
                salida += "."
        salida += "\n"

    return jsonify({"width": w, "height": h, "puzzle": salida})


def gen_puzzle(w, h, mitm):
    from gen import make

    return make(w, h, mitm)


if __name__ == "__main__":
    app.run(debug=True)
