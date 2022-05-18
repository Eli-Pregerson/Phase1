from sympy import *

# def readCFG(cfg, recurlist):
#     """Takes in a dot file, and extracts a list of two entry lists, each of which
#     represents an edge in the control flow graph. This list, as well as the recurlist
#     are passed into calculateSystem."""
#     f = open(cfg, "r")
#     edgelist = []
#     for x in f:
#         start = ""
#         end = ""
#         startDone = False
#         for char in x:
#             if char.isdigit():
#                 if startDone:
#                     end += char
#                 else:
#                     start += char
#             else:
#                 startDone = True
#         if end != "": #ignore lines that don't give edges
#             edgelist += [[int(start), int(end)]]
#     f.close()
#     return calculateSystem(edgelist, recurlist)
def recurapc(edgelist, recurlist):
    """Calculates the apc of a recursive function"""
    gamma = expand(calculateSystem(edgelist, recurlist))
    print("Gamma Function: " + str(gamma))
    discrim = calculateDiscrim(gamma)
    print("Discriminant: " + str(discrim))
    if len(real_roots(discrim)) == 0:
        print("case1")
    else:
        print("case2")
        rStar = min(map(lambda x: x if x > 0 else oo,real_roots(discrim)))
        apc = (1/rStar)**symbols("n")
    return apc




def calculateSystem(edgelist, recurlist):
    """Takes in a list of all edges in a graph, and a list of where recursive calls are
    located, and creates a system of equations in the form of a dictionary"""
    edgedict = {}
    for edge in edgelist: #reformatting our list of edges into a dictionary where keys are edge starts, and values are lists of edge ends
        startnode = str(edge[0])
        if startnode in edgedict:
            endnodes = edgedict[startnode] + [edge[1]]
        else:
            endnodes = [edge[1]]
        edgedict[startnode] = endnodes
    system = []
    x = symbols('x')
    accGF = 1/(1-x)
    # firstnode = symbols("V"+str(edgelist[0][0])) #chr(edgelist[0][0] + 65)
    # recurexpr = firstnode*x
    firstnode = symbols("T")
    recurexpr = firstnode
    symbs = []
    for startnode in edgedict.keys():
        endnodes = edgedict[startnode]
        expr = Integer(0)
        sym = symbols("V" + str(startnode)) #chr(int(startnode) + 65)
        symbs += [sym]
        for node in endnodes:
            if str(node) in edgedict.keys(): #makes sure the end node is not terminal
                var = symbols("V" + str(node)) #str(chr(node+ 65))
                expr = expr + var*x
            else:
                expr = expr + x
            expr = (recurexpr**recurlist[int(startnode)]) * expr #recursion
        system += [expr - sym]
    gamma = eliminate(system, symbs, symbols("V0")*x - firstnode)
    return gamma
    # solutions = nonlinsolve(system, symbs)
    # possibleGenFunc = []
    # for i in solutions.args:
    #     func = i[0]
    #     sumfunc = accGF*func
    #     partialSeries = series(sumfunc, x, 0, 40)
    #     if "-" not in str(partialSeries):
    #         possibleGenFunc += [sumfunc]
    # if len(possibleGenFunc) == 1:
    #     return possibleGenFunc[0]
    # else:
    #     print("Oh dear, not sure which generating function is right")
    #     return possibleGenFunc[0]


def calculateDiscrim(polynomial):
    """Takes in a polynomial and calculates its discriminant"""
    terms = polynomial.args
    domTerm = polynomial.args[0]
    for term in terms:
        if termPow(term, "T") > termPow(domTerm, "T"):
            domTerm = term
    maxpow = termPow(domTerm, "T")
    maxcoeff = 1
    for arg in domTerm.args:
        if not "T" in str(arg):
            maxcoeff *= arg
    print(maxcoeff)
    power = int(maxpow*(maxpow-1)/2)
    disc = ((-1)^power)/(maxcoeff)*resultant(polynomial, diff(polynomial, symbols("T")), symbols("T"))
    return disc

def resultant(p, q, symb):
    """Calculates the resultant of two polynomials"""
    Ppow = 0
    Qpow = 0
    Pcoeffs = {}
    Qcoeffs = {}
    for term in p.args:
        pow = termPow(term, symb)
        Pcoeffs[pow] += term/(symb**pow)
        if  pow > Ppow:
            Ppow = pow
    for term in q.args:
        pow = termPow(term, symb)
        Qcoeffs[pow] += term/(symb**pow)
        if  pow > Qpow:
            Qpow = pow
    MatrixArray = []
    for i in range(Ppow + Qpow):
        MatrixArray += [[0]*(Ppow + Qpow)]
    for i in range(Ppow + 1):
        for j in range(Qpow):
            MatrixArray[j][i + j] = Pcoeffs[i]
    for i in range(Qpow + 1):
        for j in range(Ppow):
            MatrixArray[j + Qpow][i +j] = Qcoeffs[i]
    m = Matrix(MatrixArray)
    m = m.T
    return m.det()

def termPow(term, symb):
    """for a expression, find the power a symbol is raised to"""
    #print(str(term) + str(type(term)))
    if not str(symb) in str(term):
        return 0
    if not str(symb)+"**" in str(term):
        return 1
    if type(term) == Mul:
        args = term.args
        for arg in args:
            if str(symb) in str(arg):
                return termPow(arg, symb)
    if type(term) == Pow:
        return int(str(term).split("**")[1])
    else:
        print("PANIC PANIC termPow")
        print(type(term))
        return 0



def eliminate(system, symbs, gamma):
    """Takes in a system of equations and gets the gamma function"""
    done = True
    for symb in symbs:
        if str(symb) in str(gamma):
            done = False
    if done:
        return gamma
    for i in range(len(symbs)):
        sub = system[i] + symbs[i]
        if str(symbs[i]) in str(gamma):
            gamma = expand(gamma.subs(symbs[i], sub))
    return eliminate(system, symbs, gamma)

# recurlist = [0,0,0,0,1,1,0,0]
# edgelist = [[0,1],[1,2],[2,3],[3,7],[2,4],[4,5],[5,6],[6,7]]
recurlist = [0,0,0,0,1,0]
edgelist = [[0,1],[1,2],[2,3],[2,4],[3,5],[4,5]]
# recurlist = [0,0,0,0,0,1,0]
# edgelist = [[0,1],[1,2],[2,3],[3,4],[3,5],[4,6],[5,6]]
#print(calculateSystem(edgelist, recurlist))

print("Recursive APC: " + str(recurapc(edgelist, recurlist)))
