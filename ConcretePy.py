class Shape:
    def __init__(self,width,depth):
        self.width = width
        self.depth = depth

class Force:
    def __init__(self,moment):
        self.moment = moment
 
class ReinforcementData:
    def __init__(self ,cover_top ,cover_bot):
        self.cover_top = cover_top
        self.cover_bot = cover_bot

class Material:
    def __init__(self,fc,fy):
        self.f_c = fc
        self.f_y = fy
        self.epsilon_c_max = 0.003
        self.epsilon_s_min = 0.005
        self.E_s =  2.04 * 10 **6   # kgf/cm2
        self.beta1 = self.beta1()
        self.epsilon_s = None

    def beta1(self):
        if self.f_c <= 280:
            return 0.85
        else:
            return max(0.85 - 0.05 * ((self.f_c - 280)/70),0.65)

    def sigma_s(self):
        if self.epsilon_s > 0:
            return +min(abs(self.epsilon_s * self.E_s), self.f_y)
        else:
            return -min(abs(self.epsilon_s * self.E_s), self.f_y)

class InputData:
    def __init__(self, Shape, Force, Material,ReinforcementData):
        self.shape = Shape
        self.force = Force
        self.material = Material
        self.rebar= ReinforcementData

   
def rectangleRCdesign(input):
    # 土木 401-100
    output_dict  = {}

    phi = 0.9
    Es = input.material.E_s
    epsilon_c_max = input.material.epsilon_c_max
    epsilon_s_min = input.material.epsilon_c_max
    fc = input.material.f_c
    fyr = input.material.f_y
    beta1 = input.material.beta1

    B = input.shape.width
    H = input.shape.depth

    db = input.rebar.cover_bot
    dt = input.rebar.cover_top 

    Mu = input.force.moment

    d = H - db
    c_max = epsilon_c_max/(epsilon_c_max + epsilon_s_min)* d
    a_max = beta1*c_max
    a = d - (d**2-2 * abs(Mu)/(0.85*fc*phi*B))**0.5

    if type(a) is complex or a > a_max:
        # 雙筋
        Cc = 0.85*fc * B * a_max
        Muc = Cc * (d-a_max/2) * phi
        Mus = Mu - Muc
        fs = min(Es * epsilon_c_max * (c_max - dt)/c_max, fyr)
        #  total compression reinforcement is Asc
        As_c = Mus / (fs - 0.85*fc)/(d-dt)/phi
        As_t1 = Muc /fyr/(d-a_max/2)/phi
        As_t2 = Mus /fyr/(d-dt)/phi
        #  total tensile reinforcement is Ast = As1 + As2
        As_t = As_t1 + As_t2
        output_dict['type']="雙筋"
    else:
        # 單筋
        As_t = Mu / (phi * fyr * (d-a/2))
        As_c = 0
        output_dict['type']="單筋"

    ps_min = As_t / B / d
    As_min = min(max(0.8*fc**0.5/fyr, 14/fyr) * B * d, 4/3*As_t)
    As_max = 0.04 * B*d

    output_dict['As_t']=As_t
    output_dict['As_c']=As_c
    output_dict['ps_min']=ps_min
    output_dict['As_min']=As_min
    output_dict['As_max']=As_max

    return output_dict

