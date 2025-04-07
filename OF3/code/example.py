import math as m
# ---------------- # 

def normalshockrelations(M,gamma,cp,R):
    '''
    Return : m1,m2,rhoratio,pratio,Tratio,p0ratio
    '''

    m1 = M

    #Mach Relation M2
    m2 = m.sqrt( (1+0.5*(gamma-1)*M**2)/(gamma*M**2 - 0.5*(gamma-1)))

    #Density Relation 
    rhoratio = ((gamma+1)*M**2)/(2+(gamma-1)*M**2)

    #Pressure Relation
    pratio = 1 + ((2*gamma)*(gamma+1)**-1)*(M**2 -1)

    #Temperature Relation
    Tratio = (1-gamma+2*gamma*M**2)*(2+(gamma-1)*M**2)/( ((gamma+1)**2)*M**2 )

    #Entropy Change
    dels = cp*m.log(Tratio) - R*m.log(pratio)

    #stagnation pressure ratio
    p0ratio = m.exp(-(dels)/R)

    # #P01/P1
    # p01p1ratio = (1+ 0.5*(gamma-1)*M**2)**(gamma/gamma-1)

    # #P01/P2
    # p02p2ratio = (1+ 0.5*(gamma-1)*m2**2)**(gamma/gamma-1)  

    return m1,m2,rhoratio,pratio,Tratio,p0ratio


def isentropic_pressure(p,M,gamma):
    return p*(1 + 0.5*(gamma-1)*M**2)**(gamma/(gamma-1))


M1 = 3
p1 = 1 # Pa (N/m^2)
gamma = 1.4
R = 287.05 # J/(kgK)
cp = gamma*R/(gamma-1)

result = normalshockrelations(M1,gamma,cp,R)

p01 = isentropic_pressure(p1,M1,gamma)

print(f"p_01 = {p01} Pa")

M2 = result[1]
p2 = result[3]*p1

# p02 = p01*result[5]

p02 = p2*(1 + 0.5*(gamma-1)*M2**2)**(gamma/(gamma-1))

print(f"M2 = {M2}")

print(f"p2 = {p2} Pa")

print(f"p_02 = {p02} Pa")




