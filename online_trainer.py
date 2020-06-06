import time
import math


def theta_ss(x,y):
    if x>0:
        return abs(1*math.atan(2*y))#augmenter -10 10
    if x<=0:
        return abs(1*math.atan(-2*y))
    
def theta_s(x,y):
    
    if x>0:
        return 1*math.atan(2*y/(x**2+y**2))
    if x<=0:
        return 1*math.atan(-2*y/(x**2+y**2))
def theta_s2(x,y):
    return 2*math.atan(10*y)/(math.exp(x)+math.exp(-x))

def theta_s3(x, y, size):
    if x>0:
        return 1*math.atan(10*y/size)
    if x<=0:
        return 1*math.atan(-10*y/size)

def theta_s4(x, y):
    if x>0:
        return math.atan(10*y)*math.exp(-x*x)
    else:
        return math.atan(-10*y)*math.exp(-x*x)

def theta_s5(x, y):
    return math.atan(10*y)*math.exp(-18*x*x)

class OnlineTrainer:
    def __init__(self, robot, NN):
        """
        Args:
            robot (Robot): a robot instance following the pattern of
                VrepPioneerSimulation
            target (list): the target position [x,y,theta]
        """
        self.robot = robot
        self.network = NN
        self.log_file = {}
        self.running= True
        self.size = 4 #Size of the training area
        #self.alpha = [1/(2*self.size), 1/(2*self.size), 1/(2*math.pi)] #Normalization ratio, 2pi/3 is also possible
        #self.alpha = [1/(self.size), 1/(self.size), 1/(math.pi)] #Normalization ratio, 2pi/3 is also possible

        self.alpha = [1/(self.size/2), 1/(self.size/2), 1/(1*math.pi)] #Normalization ratio, 2pi/3 is also possible
        
        self.gain = [1, 2, 0.5] #Strategy gain for criterion calculation
        self.backprop_step = 0.25 #Step for back propagation
        self.random_ratio = 0.01 #Ratio for random updates

    def train(self, target):
        position = self.robot.get_position()
        
        #Relative positions for criterion and inputs calculation
        x_m = position[0]-target[0]
        y_m = position[1]-target[1]
        theta_m = position[2]-target[2]-theta_s(position[0]-target[0], position[1]-target[1])
        
        theta = position[2]

        #First network normalized inputs
        network_input = [0, 0, 0]
        network_input[0] = x_m*self.alpha[0]
        network_input[1] = y_m*self.alpha[1]
        network_input[2] = theta_m*self.alpha[2]

        #Calculation of the reference criterion
        J_ref = self.gain[0]*x_m**2 + self.gain[1]*y_m**2 + (1/10)*self.gain[2]*theta_m**2

        #Set up logging
        t0 = time.time()
        times = []
        Q1s = []
        positions = []
        theta_shifts = []
        criterions = []
        commands = []

        while self.running:
            debut = time.time()
            command = self.network.runNN(network_input) # propage erreur et calcul vitesses roues instant t
                      
            #alpha_x = 1/6
            #alpha_y = 1/6
            #alpha_teta = 1.0/(math.pi)
                        
            #crit_av= alpha_x*alpha_x*(position[0]-target[0])*(position[0]-target[0]) + alpha_y*alpha_y*(position[1]-target[1])*(position[1]-target[1]) + alpha_teta*alpha_teta*(position[2]-target[2]-theta_s(position[0], position[1]))*(position[2]-target[2]-theta_s(position[0], position[1]))  
            
                       
            self.robot.set_motor_velocity(command) # applique vitesses roues instant t,                     
            time.sleep(0.050) # attend delta t
            position = self.robot.get_position() #  obtient nvlle pos robot instant t+1       
            
            #Relative positions for criterion and inputs calculations
            x_m = position[0]-target[0]
            y_m = position[1]-target[1]
            theta_m = position[2]-target[2]-theta_s(position[0]-target[0], position[1]-target[1])
            #print(x_m, y_m, theta_m)

            
            
            #Normalization of network inputs
            network_input[0] = x_m*self.alpha[0]
            network_input[1] = y_m*self.alpha[1]
            network_input[2] = theta_m*self.alpha[2]

            #Calculation of the new criterion
            J = self.gain[0]*x_m**2 + self.gain[1]*y_m**2 + (1/10)*self.gain[2]*theta_m**2

            #Logs
            times.append(debut - t0)
            # Save the current state of the lesson
            positions.append(self.robot.get_position()) # This function takes 50 ms to compute
            commands.append(self.robot.get_motor_velocity())
            theta_shifts.append(theta_s(position[0]-target[0], position[1]-target[1]))
            criterions.append(J)

            if self.training:
                delta_t = (time.time()-debut)

                grad = [
                    -(self.gain[0]*x_m*delta_t*(self.robot.r/2)*math.cos(theta)
                    +self.gain[1]*y_m*delta_t*(self.robot.r/2)*math.sin(theta)
                    -self.gain[2]*theta_m*delta_t*(self.robot.r/(2*self.robot.R)))/delta_t,

                    -(self.gain[0]*x_m*delta_t*(self.robot.r/2)*math.cos(theta)
                    +self.gain[1]*y_m*delta_t*(self.robot.r/2)*math.sin(theta)
                    +self.gain[2]*theta_m*delta_t*(self.robot.r/(2*self.robot.R)))/delta_t
                ]

                #Conditional back propagation according to the evolution of the criterion
                if J <= 1.1*J_ref:

                    # The two args after grad are the gradient learning steps for t
                    # and t-1
                    self.network.backPropagate(grad, self.backprop_step, 0)
                else:
                    #The argument is the applied ratio for perturbation
                    #self.network.random_update(self.random_ratio)
                    self.network.backPropagate(grad, self.backprop_step, 0)

                #Stores the criterion for future comparison
                J_ref = J
            #theta = position[2]
        self.robot.set_motor_velocity([0,0]) # stop  apres arret  du prog d'app
        #position = self.robot.get_position() #  obtient nvlle pos robot instant t+1
                #Teta_t=position[2]
        
        #Logs
        duration = time.time()-t0
        print("heeeeeeeeeeeeeeeeeeeeeeere")
        self.log_file = {"size":self.size, "gain":self.gain, "backprop_step":self.backprop_step,
                         "random_ratio":self.random_ratio, "target":target, "duration":duration,
                         "times":times, "positions":positions, "theta_shifts":theta_shifts,
                         "criterions":criterions, "commands":commands}

                
        
        self.running = False
