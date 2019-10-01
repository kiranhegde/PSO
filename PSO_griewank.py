import random
import math


# Particle
class Particle:
    def __init__(self,dim,bounds,v0):
        self.velocity = []                  # particle velocity
        self.position = []                  # particle position
        self.p_best = []                    # best individual position
        self.cost = -1                      # particle cost
        self.c_best = -1                    # best individual cost

        for i in range(0, dim):
            self.velocity.append(random.uniform(-v0, v0))
            self.position.append(random.uniform(bounds[i][0], bounds[i][1]))

    def cost_evaluate(self,costFunc):
        self.cost = costFunc(self.position)
        if self.cost < self.c_best or self.c_best == -1:
            self.p_best = self.position
            self.c_best = self.cost

    def update_velocity(self,p_best_global,w,c1,c2):
        for i in range(0,dim):
            r1 = random.random()
            r2 = random.random()

            vel_cognitive = c1 * r1 * (self.p_best[i] - self.position[i])
            vel_social = c2 * r2 * (p_best_global[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + vel_cognitive + vel_social

    def update_position(self,bounds):
        for i in range(0, dim):
            self.position[i] += self.velocity[i]

            # reflecting walls strategy
            if self.position[i] < bounds[i][0] or self.position[i] > bounds[i][1]:
                self.velocity[i] = -self.velocity[i]


# Main
def PSO(costFunc,dim,bounds,N,iterations,v0,w,c1,c2):
    p_best_global = []              # best global position
    c_best_global = -1              # best global cost
    swarm = []                      # particle swarm

    for i in range(0, N):
        swarm.append(Particle(dim,bounds,v0))

    for i in range(0, iterations):

        for j in range(0, N):
            swarm[j].cost_evaluate(costFunc)
            if swarm[j].cost < c_best_global or c_best_global == -1:
                p_best_global = list(swarm[j].position)
                c_best_global = float(swarm[j].cost)

        for j in range(0, N):
            swarm[j].update_velocity(p_best_global,w,c1,c2)
            swarm[j].update_position(bounds)

    return [p_best_global, c_best_global]


# Griewank Function
def costFunc(x):
    function = 1
    s = 1

    for i in range(len(x)):
        function += x[i] ** 2 / 4000
        s *= math.cos(x[i] / (i + 1) ** 0.5)

    function -= s
    return function


# Test
dim = 2                                 # dimension
bounds = [[-10, 10], [-10, 10]]         # boundary conditions
N = 100                                 # number of particles
iterations = 250                        # number of iterations
v0 = 10                                 # initial speed parameter
w = 0.78                                # inertia constant
c1 = 1.6                                # cognative constant
c2 = 1.6                                # social constant

result = [[], -1]
for i in range(8):
    ans = PSO(costFunc,dim,bounds,N,iterations,v0,w,c1,c2)
    if ans[1] < result[1] or result[1] == -1:
        result = ans
print('Position:', result[0])
print('Result:', result[1])