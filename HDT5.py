import simpy
import random
import math
random.seed(20289)

interval = 1
env = simpy.Environment()  # crear ambiente de simulacion
CPU = simpy.Resource(env, capacity=2)  # el cargador de bateria soporta 2 carros
RAM = simpy.Container(env, init=100, capacity=100)
count = []

def proc(env, name, cpu, creacion, pros):

    yield env.timeout(creacion)
    print('%s new at %d' % (name, env.now))
    timeI = env.now
    termori = True
    memoria = random.randint(1,10)
    instrucciones = random.randint(1, 10)
    while termori == True:
        RAM.get(memoria)
        
     

        if instrucciones > 0:
            print('%s ready at %s' % (name, env.now))

            with cpu.request() as req:  # pedimos conectarnos al cargador de bateria
                yield req

  
                print('%s running at %s' % (name, env.now))
                instrucciones = instrucciones - pros
                yield env.timeout(1)
                print('%s leaving the CPU at %s' % (name, env.now))

                estado = random.randint(1,2)
                if instrucciones <= 0:
                    print('%s terminated at %s' % (name, env.now))
                    RAM.put(memoria)
                    termori = False
                    timeF = env.now
                    Tiempo = timeF - timeI
                    
                    count.append(Tiempo)

                if estado == 2 and instrucciones>0:
                    print('%s waiting at %s' % (name, env.now))
                # se hizo release automatico del cargador bcs
        
   
   
for i in range(400):
    env.process(proc(env, 'Proceso %d' % i, CPU, i + int(random.expovariate(1.0 / interval)), 3))

# correr la simulacion
env.run()
print("numero total", len(count))
media = sum(count) / len(count)
listaDesv = []
for j in count:
    desv = count[i] - media
    desv = desv * desv
    listaDesv.append(desv)
    
desviacion = sum(listaDesv) / len(count)
desviacion = math.sqrt(desviacion)
    
print("La media de tiempo es: ", media)
print("La desviacion de tiempo es: ", desviacion)
    