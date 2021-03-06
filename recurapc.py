from sympy import *
import signal
# from eliminate import eliminate


def recurapc(edgelist, recurlist):
    """Calculates the apc of a recursive function"""
    gamma = gammaFunction(edgelist, recurlist)
    print("Gamma Function: " + str(gamma))
    discrim = calculateDiscrim(gamma)
    print("Discriminant: " + str(discrim))
    try:
        numroots = len(real_roots(discrim))
    except:
        numroots = 0
    if numroots == 0:
        print("case1")
        T = symbols("T")
        x = symbols("x")
        gens = solve(gamma,T)
        possibleGenFunc = []
        for gen in gens:
            partialSeries = series(gen, x, 0, 40)
            if "-" not in str(partialSeries):
                possibleGenFunc += [gen]
        if len(possibleGenFunc) == 1:
            genFunc = possibleGenFunc[0]/(1-x)
            print("Generating Function: " + str(genFunc))
        else:
            print("PANIC PANIC Oh dear, not sure which generating function is right")
        denominator = 1
        for factor in genFunc.args:
            if type(factor) == Pow and factor.args[1] < 0:
                denominator *= 1/factor
        denominator = expand(denominator)
        print(denominator)
        maxPow = 0
        for term in denominator.args:
            power = termPow(term, symbols("x"))
            if power > maxPow:
                maxPow = power
        rootsDict = roots(denominator)
        numRoots = sum(rootsDict.values())
        if numRoots < maxPow:
            newRootsDict = {}
            approxroots = nroots(denominator)
            for root in approxroots:
                found = False
                for dictRoot in newRootsDict.keys():
                    if abs(root-dictRoot)<10**(-12):
                        newRootsDict[dictRoot] += 1
                        break
                if not found:
                    newRootsDict[root] = 1
            rootsDict = newRootsDict
            numRoots = sum(rootsDict.values())
        if numRoots < maxPow:
            raise Exception("Can't find all the roots :(")
        nonZeroIndex = 0
        while True:
            zseries = series(genFunc, x, 0, nonZeroIndex)
            if not type(zseries) == Order:
                break
            nonZeroIndex += 1
        coeffs = [0]*(numRoots + nonZeroIndex)
        Tseries = series(genFunc, x, 0, numRoots + nonZeroIndex)
        exprs = []
        symbs = set()
        for term in Tseries.args:
            if not type(term) == Order:
                c = str(term).split("*")[0]
                if c == "x":
                    c = "1"
                coeffs[termPow(term, x)] = int(c)
        for val in range(nonZeroIndex, nonZeroIndex + numRoots):
            expr = -coeffs[val]

            for rootindex, root in enumerate(rootsDict.keys()):
                for mj in range(rootsDict[root]):
                    expr += symbols(f'c\-{rootindex}\-{mj}')*(val**mj)*((1/root)**val)
                    symbs.add(symbols(f'c\-{rootindex}\-{mj}'))
            exprs += [expr]


        def handler(signum, frame):
            raise Exception("end of time")

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(200)

        try:
            solutions = solve(exprs)
        except:
            solutions = nsolve(exprs, list(symbs), [0]*numRoots, dict=True)[0]
        signal.alarm(0)
        patheq = 0
        for rootindex, root in enumerate(rootsDict.keys()):
            for mj in range(rootsDict[root]):
                n = symbols("n")
                patheq += symbols(f'c\-{rootindex}\-{mj}')*(n**mj)*(abs(1/root)**n)
        if not type(patheq) == int:
            patheq = patheq.subs(solutions)
        apc = patheq
    else:
        print("case2")
        rStar = min(map(lambda x: x if x > 0 else oo,real_roots(discrim)))
        apc = (1/rStar)**symbols("n")
    return apc


def gammaFunction(edgelist, recurlist):
    """Takes in a list of all edges in a graph, and a list of where recursive calls are
    located, and calculates a gamma function in terms of x and the start node"""
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
    eq1 = symbols("V0")*x - firstnode
    symbs = [firstnode]+symbs
    gamma = expand(eliminate([eq1]+system, symbs))
    return gamma


def calculateDiscrim(polynomial):
    """Takes in a polynomial and calculates its discriminant"""
    terms = polynomial.args
    domPow = max([termPow(term, "T") for term in terms])
    maxcoeff = 0
    for term in terms:
        if termPow(term, "T") == domPow:
            newprod = 1
            for arg in term.args:
                if not "T" in str(arg):
                    newprod *= arg
            maxcoeff += newprod
    power = int(domPow*(domPow-1)/2)
    disc = ((-1)**power)/(maxcoeff)*resultant(polynomial, diff(polynomial, symbols("T")), symbols("T"))
    return disc

def resultant(p, q, symb):
    """Calculates the resultant of two polynomials"""
    Ppow = 0
    Qpow = 0
    Pcoeffs = {}
    Qcoeffs = {}
    for term in p.args:
        pow = termPow(term, symb)
        if pow in Pcoeffs.keys():
            Pcoeffs[pow] += term/(symb**pow)
        else:
            Pcoeffs[pow] = term/(symb**pow)
        if  pow > Ppow:
            Ppow = pow
    for term in q.args:
        pow = termPow(term, symb)
        if pow in Qcoeffs.keys():
            Qcoeffs[pow] += term/(symb**pow)
        else:
            Qcoeffs[pow] = term/(symb**pow)
        if  pow > Qpow:
            Qpow = pow
    MatrixArray = []
    for i in range(Ppow + Qpow):
        MatrixArray += [[0]*(Ppow + Qpow)]
    for i in range(Ppow + 1):
        for j in range(Qpow):
            if i in Pcoeffs.keys():
                MatrixArray[j][i + j] = Pcoeffs[i]
    for i in range(Qpow + 1):
        for j in range(Ppow):
            if i in Qcoeffs.keys():
                MatrixArray[j + Qpow][i +j] = Qcoeffs[i]
    m = Matrix(MatrixArray)
    m = m.T
    return m.det()

def termPow(term, symb):
    """for a expression, find the power a symbol is raised to"""
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

def eliminate(system, symbs):
    """Takes in a system of equations and gets the gamma function"""
    if len(system) == 1:
        return system[0]
    sub = system[-1] + symbs[-1]
    if symbs[-1] in sub.free_symbols:
        for eq in system:
            if symbs[-1] in eq.free_symbols:
                sol = solve(eq, symbs[-1], dict=True)
                if len(sol) == 1:
                    sub = expand(sub.subs(symbs[-1], sol[0][symbs[-1]]))
    if symbs[-1] in sub.free_symbols:
        print("PANIC PANIC not sure how to substitute")
        return 98287340987134
    for count, eq in enumerate(system):
        if symbs[-1] in eq.free_symbols:
            system[count] = expand(eq.subs(symbs[-1], sub))
    return eliminate(system[:-1], symbs[:-1])

recurlist = [0,0,0,0,1,1,0,0]
edgelist = [[0,1],[1,2],[2,3],[2,4],[3,7],[4,5],[5,6],[6,7]]
print("This comes from the 2022 paper and apc should be O(1.12^n)")
print("APC: " + str(recurapc(edgelist, recurlist)))


recurlist = [0,0,0,0,1,0]
edgelist = [[0,1],[1,2],[2,3],[2,4],[3,5],[4,5]]
print("This comes from the 2022 paper and apc should be O(n/5)")
print("APC: " + str(recurapc(edgelist, recurlist)))


recurlist = [0,0,0,0,0]
edgelist = [[0,1],[1,2],[2,3],[3,1],[1,4]]
print("This comes from the 2015 paper and apc should be O(n/3)")
print("APC: " + str(recurapc(edgelist, recurlist)))


#bin2dec = {{0, 1, 0, f}, {1, 2, 0, f}, {1, 3, 0, f}, {2, 6, 0, t}, {3,
     # 4, 0, f}, {3, 5, 0, f}, {4, 6, 1, t}, {5, 6, 1, t}};
recurlist = [0,0,0,0,1,1,0]
edgelist = [[0,1],[1,2],[1,3],[2,6],[3, 4], [3,5], [4,6], [5,6]]
print("This comes from the 2022 paper and apc should be O(1.15^n)")
print("APC: " + str(recurapc(edgelist, recurlist)))


#crossSum = {{0, 1, 0, f}, {0, 2, 0, f}, {1, 3, 0, t}, {2, 3, 1, t}};
recurlist = [0,0,1,0]
edgelist = [[0,1],[0,2],[1,3],[2,3]]
print("This comes from the 2022 paper and apc should be O(n/3)")
print("APC: " + str(recurapc(edgelist, recurlist)))




#power = {{0, 1, 0, f}, {0, 2, 0, f}, {1, 5, 0, t}, {2, 3, 0, f}, {2,
#    4, 0, f}, {3, 5, 0, t}, {4, 5, 1, t}};
recurlist = [0,0,0,0,1,0]
edgelist = [[0,1],[0,2],[1,5],[2,3],[2,4],[3,5],[4,5]]
print("This comes from the 2022 paper and apc should be O(n/2)")
print("APC: " + str(recurapc(edgelist, recurlist)))







recurlist = [0,0,0,0,0,0,0]
edgelist = [[0,1],[0,2],[1,2],[2,3],[2,4],[3,4],[4,5],[4,6],[5,6]]
print("This comes from the 2015 paper and apc should be 2^3 = 8")
print("APC: " + str(recurapc(edgelist, recurlist)))



recurlist = [0,0,0,0,0,0,0]
edgelist = [[0,1],[0,6],[1,2],[1,5],[2,3],[2,4],[3,4],[4,5],[5,6]]
print("This comes from the 2015 paper and apc should be 3+1 = 4")
print("APC: " + str(recurapc(edgelist, recurlist)))


recurlist = [0,0,0,0,0]
edgelist = [[0,0],[0,1],[1,1],[1,2],[2,2],[2,3],[3,3],[3,4],[4,4]]
print("This comes from the 2015 paper and apc should be n^4")
print("APC: " + str(recurapc(edgelist, recurlist)))


recurlist = [0,0,0,0,0]
edgelist = [[0,0],[0,1],[1,1],[1,2],[2,2],[2,3],[3,3],[3,4]]
print("This comes from the 2015 paper and apc should be n^3")
print("APC: " + str(recurapc(edgelist, recurlist)))


recurlist = [0,0,0,0,0,0,0,0,0]
edgelist = [[0,1],[1,2],[2,8],[1,3],[3,4],[3,5],[5,8],[4,6],[4,7],[6,8],[7,8]]
print("This comes from the 2015 paper and apc should be 4")
print("APC: " + str(recurapc(edgelist, recurlist)))


recurlist = [0,0,0,0,0,0,0,0,0]
edgelist = [[0,1],[1,2],[2,3],[3,2],[2,4],[4,5],[5,6],[6,5],[5,7],[7,8]]
print("This comes from the 2015 paper and apc should be n^2")
print("APC: " + str(recurapc(edgelist, recurlist)))

recurlist = [0,0,0,0,0,0,0,0,0,0,0]
edgelist = [[0,1],[1,2],[2,3],[2,4],[4,6],[4,5],[6,8],[6,9],[5,7],[8,10],[9,7],[7,2],[3,10]]
print("This comes from the 2015 paper and apc should be 1.17^n")
print("APC: " + str(recurapc(edgelist, recurlist)))
