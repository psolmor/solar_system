
#Same function as solar_system.py but this generates a gif with the movement.

import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def aceleracion(ax,ay,x,y,m):
    ax_act=np.zeros(10)
    ay_act=np.zeros(10)
    for i in range(0,10):
        for j in range(0,10):
            if i!=j:
               ax_act[i]+=-((x[i]-x[j])/((((x[i]-x[j])**2+(y[i]-y[j])**2)**0.5)**3))*m[j]
               ay_act[i]+=-((y[i]-y[j])/((((x[i]-x[j])**2+(y[i]-y[j])**2)**0.5)**3))*m[j]
    return ax_act,ay_act


def posicion(x,y,vx,vy,ax,ay,h):
     x1=x+h*vx+ax*(h*h)/2
     y1=y+h*vy+ay*(h*h)/2
     return x1,y1

def w(vx,vy,ax,ay,h):
    wx=vx+ax*h/2
    wy=vy+ay*h/2
    return wx,wy

def velocidad(wx,wy,ax,ay,h):
    vx=wx+ax*h/2
    vy=wy+ay*h/2
    return vx,vy

def energia(vx,vy,x,y,masa):
    energia=0
    for i in range(0,10):
        energia+=0.5*masa[i]*(vx[i]*vx[i]+vy[i]*vy[i])
        for j in range(0,10): 
            if i<j:
                distancia = np.sqrt((x[i]-x[j])**2 + (y[i]-y[j])**2)
                energia+= -0.5*( masa[i] * masa[j]) / (distancia)
    return energia 

# Normalizaciones
sol_masa=1.99e30
c=1.496e11
G=6.67e-11
tp=(c/(G*sol_masa))**0.5

# Condiciones iniciales
x=np.array([0/c,57.9e9/c,108.2e9/c,149.6e9/c,227.9e9/c,778.6e9/c,1433.5e9/c,2872.5e9/c,4495.1e9/c,5870e9/c])
y=np.zeros(10)
vx=np.zeros(10)
vy=np.array([0*tp,47.9e3*tp,35e3*tp,29.8e3*tp,24.1e3*tp,13.1e3*tp,9.7e3*tp,6.8e3*tp,5.4e3*tp,4.7e3*tp])
wx=np.zeros(10)
wy=np.zeros(10)
ax=np.zeros(10)
ay=np.zeros(10)
masa=np.array([sol_masa/sol_masa,0.33e24/sol_masa,4.87e24/sol_masa,5.97e24/sol_masa,0.642e24/sol_masa,1899e24/sol_masa,568e24/sol_masa,86.8e24/sol_masa,102e24/sol_masa,0.0125e24/sol_masa])

# Iteracciones
ax,ay=aceleracion(ax,ay,x,y,masa)

h=0.1
t=0
N=70

trayectorias_x = [[] for _ in range(10)]
trayectorias_y = [[] for _ in range(10)]

for i in range(N):
    for j in range(10):
        trayectorias_x[j].append(x[j])
        trayectorias_y[j].append(y[j])

    x,y=posicion(x,y,vx,vy,ax,ay,h)
    wx,wy=w(vx,vy,ax,ay,h)
    ax,ay=aceleracion(ax,ay,x,y,masa)
    vx,vy=velocidad(wx,wy,ax,ay,h)

# Crear una lista de índices para los planetas interiores
interiores = [0,1, 2, 3, 4]

# Función de animación
def animate(i):
    plt.clf()
    for j in interiores:
        plt.plot(trayectorias_x[j][:i], trayectorias_y[j][:i], label=f'Planeta {j}')
    plt.title('Trayectorias de los Planetas Interiores en el Sistema Solar')
    plt.xlabel('Posición en x ')
    plt.ylabel('Posición en y ')
    plt.legend()
    plt.grid(True)
    plt.xlim(-2.5, 2.5)  # Ajustar los límites del eje x
    plt.ylim(-2.5, 2.5)  # Ajustar los límites del eje y

fig = plt.figure(figsize=(10, 8))
ani = animation.FuncAnimation(fig, animate, frames=N, interval=200)
ani.save('trayectorias_planetas_interiores_lejos.gif', writer='pillow', fps=10)

plt.show()
