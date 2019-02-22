from itertools import combinations as comb
from math import inf

class Vertex:
	def __init__(self, l):
		self.__n = []
		self.l = l

	def n(self):
		return list(self.__n)

	def add_n(self, l):
		self.__n.append(l)

	def __repr__(self):
		return "<%s>" % str(self.l)

class Graph:
	def __init__(self):
		self.__v = []
		self.__e = []

	def v(self):
		return list(self.__v)

	def vl(self):
		return [v.l for v in self.__v]

	def size(self):
		return len(self.__v)

	def e(self):
		return list(self.__e)

	def tuple(self):
		return (self.v(), self.e())

	def get_v(self, l):
		for v in self.v():
			if v.l == l:
				return v
		return Vertex("error")

	def create_v(self, l):
		self.__v.append(Vertex(l))

	def add_v(self, v):
		self.__v.append(v)

	def create_e(self, a, b):
		if self.query_e((a, b)):
			return
		self.__e.append((a, b))
		for v in self.__v:
			if v.l == a:
				v.add_n(b)
			if v.l == b:
				v.add_n(a)

	def create_e_l(self, a, b):
		self.create_e(self.get_v(a), self.get_v(b))

	def query_e(self, e):
		return e in self.e() or ((e[1], e[0]) in self.e() and len(e) == 2)

	def query_e_l(self, e):
		return self.query_e((self.get_v(e[0]), self.get_v(e[1]))) and len(e) == 2

	def __repr__(self):
		return str(self.tuple())

# Creates a path graph with n vertices
def path(n):
	g = Graph()
	for i in range(1,n+1):
		g.create_v(i)
	for i in range(1,n):
		g.create_e_l(i, i+1)
	return g

# Creates a cycle graph with n vertices
def cycle(n):
	g = path(n)
	g.create_e_l(1,n)
	return g

# Creates a wheel graph with n vertices
def wheel(n):
	g = cycle(n-1)
	g.create_v(n)
	for i in range(1,n):
		g.create_e_l(i, n)
	return g

# Creates a complete graph with n vertices
def complete(n):
	g = Graph()
	for i in range(n):
		g.create_v(i+1)
	for p in comb(g.v(), 2):
		g.create_e(*p)
	return g

# Generates the double vertex of an arbitrary graph
def double_vertex(g):
	dv = Graph()
	for i in range(1,g.size()):
		for j in range(i+1,g.size()+1):
			dv.create_v((i,j))

	for a in dv.vl():
		for b in dv.vl():
			if a == b:
				continue
			for i in range(4):
				if a[i//2] == b[i%2] and g.query_e_l((int(a[1-i//2]),int(b[1-i%2]))):
					dv.create_e_l(a, b)
					break

	return dv

# Creates a dict that contains all of the distances for every pair of vertices
def floyd_warshall(g, dup=True):
        l = g.size()
        dist = {p: inf for p in comb(g.v(), 2)}
        d = lambda a, b: dist.get((a, b), dist.get((b, a)))

        if dup:
                for v in g.v():
                        dist[(v, v)] = 0

        for e in g.e():
                dist[e] = 1

        for x in g.v():
                for a in g.v():
                        for b in g.v():
                                if (a == b or b == x or x == a) and not dup:
                                        continue

                                if d(a, b) > d(a, x) + d(x, b):
                                        if (a, b) in dist:
                                                dist[(a, b)] = d(a, x) + d(x, b)
                                        else:
                                                dist[(b, a)] = d(a, x) + d(x, b)

        return dist

def wiener(g):
	return int(round(sum(floyd_warshall(g, False).values())))

# Calculates the Wiener index of a path graph containing n vertices
def wiener_u2pn(x):
	return int(round(x**5/15 - x**4/6 + x**2/6 - x/15))

# Calculates the Wiener index of a complete graph containing n vertices
def wiener_u2kn(x):
	return int(round(x**4/4 - x**3 + 5*x**2/4  - x/2))

# Calculates the Wiener index of a wheel graph containing n vertices
def wiener_u2wn(x):
	return int(round(x**4/2 - 7*x**3/2 + 21*x**2/2 - 33*x/2 + 9))

# Calculates the Wiener index of a cycle graph containing n vertices
def wiener_u2cn(x):
	a = 19*x**5/384 - x**4/8
	if x&1 == 1:
		return int(round(a + x**3/192 + x**2/8 - 7*x/128))
	return int(round(a + 5*x**3/96))
