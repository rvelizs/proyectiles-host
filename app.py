from flask import Flask, request, render_template, jsonify
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.optimize import fsolve
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    # Obtener los parámetros del formulario
    b = float(request.form['b'])
    v0 = float(request.form['v0'])
    u = float(request.form['u'])
    alfa = float(request.form['alfa'])
    h0 = float(request.form['h0'])
    angulo = float(request.form['angulo'])

    # Convertir alfa y angulo a radianes
    alfa = np.radians(alfa)
    angulo = np.radians(angulo)

    # Funciones f_x y f_y
    def f_x(t, angulo):
        return u * np.cos(alfa) * t + (v0 * np.cos(angulo) - u * np.cos(alfa)) * (1 - np.exp(-b * t)) / b

    def f_y(t, angulo):
        return h0 + (9.8 / b + v0 * np.sin(angulo) - u * np.sin(alfa)) * (1 - np.exp(-b * t)) / b - (9.8 / b - u * np.sin(alfa)) * t

    # Graficar
    fig, ax = plt.subplots()

    T0 = 2 * v0 * np.sin(angulo) / 9.8  # Tiempo de vuelo sin rozamiento
    t_vuelo = fsolve(lambda t: f_y(t, angulo), T0)[0]  # Tiempo de vuelo
    tt = np.linspace(0, t_vuelo, 100)
    x1 = f_x(tt, angulo)
    y1 = f_y(tt, angulo)

    ax.set_xlim(-30, 350)  # Límite fijo para el eje x
    ax.set_ylim(0, 100)  # Límite fijo para el eje y
    ax.grid(True)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title('Tiro parabólico con rozamiento y viento')

    line, = ax.plot([], [], '-', lw=2)

    def animate(i):
        line.set_data(x1[:i+1], y1[:i+1])
        return line,

    ani = animation.FuncAnimation(fig, animate, frames=len(tt), interval=50)

    # Guardar la animación como gif
    gif_path = os.path.join('static', 'result.gif')
    ani.save(gif_path, writer='imagemagick', fps=20)
    plt.close()

    return jsonify(result_image=gif_path)

if __name__ == '__main__':
    app.run(debug=True)
