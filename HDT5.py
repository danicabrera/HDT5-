import simpy
import random
random.seed(20289)
interval = 10
env = simpy.Environment()  # crear ambiente de simulacion
CPU = simpy.Resource(env, capacity=1)  # el cargador de bateria soporta 2 carros
RAM = simpy.Container(env, init=100, capacity=100)

def proc(env, name, bcs, driving_time, pros):
    # Simulate driving to the BCS
    yield env.timeout(driving_time)
    print('%s new at %d' % (name, env.now))
    termori = True
    memoria = random.randint(1,10)
    instrucciones = random.randint(1, 10)
    while RAM.level >= memoria and termori == True:
        RAM.get(memoria)

        # Request one of its charging spots

        if instrucciones > 0:
            print('%s ready at %s' % (name, env.now))

            with bcs.request() as req:  # pedimos conectarnos al cargador de bateria
                yield req

                # Charge the battery
                print('%s running at %s' % (name, env.now))
                instrucciones = instrucciones - pros
                print(instrucciones)
                yield env.timeout(pros)
                print('%s leaving the CPU at %s' % (name, env.now))

                estado = random.randint(1,2)
                if instrucciones <= 0:
                    print('%s terminated at %s' % (name, env.now))
                    RAM.put(memoria)
                    termori = False

                if estado == 2 and instrucciones>0:
                    print('%s waiting at %s' % (name, env.now))
                # se hizo release automatico del cargador bcs


for i in range(20):
    env.process(proc(env, 'Proceso %d' % i, CPU, i + int(random.expovariate(1.0 / interval)), 3))

# correr la simulacion
env.run()