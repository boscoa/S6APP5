import sys
import random

sys.setrecursionlimit(1000000)

def pgcd(x, y):
	while y != 0:
		(x, y) = (y, x%y)
	return x

def xgcd(e, phi_n):
	x0, x1, y0, y1 = 1, 0, 0, 1
	while phi_n != 0:
		q, e, phi_n = e // phi_n, phi_n, e % phi_n
		x0, x1 = x1, x0 - q * x1
		y0, y1 = y1, y0 - q * y1

	return e, x0, y0

def puissance_mod(a, w, n):
	if w == 0:
		return 1
	r = puissance_mod(a, w // 2, n)
	r = (r * r) % n

	if w % 2:
		r = (r * a) % n
	
	return r

def polynome(x):
	return x**2 + 1
	
def pollard_rho(n):
	x = 1; y = 1; z = 1; m = 100000
	while True:
		x = polynome(x) % n
		y = polynome(polynome(y) % n) % n
		z = (z * abs(x - y)) % n
		m = m - 1
		
		if m == 0:
			p = pgcd(n, z)
			if p != 1:
				return p
			
			z = 1; m = 100000
	
def pollard_pm1(n):
	m = 2
	max = 100000

	for i in range(1, max):
		m = puissance_mod(m, i, n)
		a = pgcd(n, m-1)
		if a != 1:
			return a

def euclide(e, phi_n):
	g, x, _ = xgcd(e, phi_n)
	if g == 1:
		return x % phi_n

def miller_rabin(n):
    if n == 2:
        return True
    
    if n < 3 or n % 2 == 0:
        return False

    w = n - 1
    k = 0
    while w % 2 == 0:
        w /= 2
        k += 1
    
    tries = 0
    while tries < 64:
        a = random.randint(2, n - 3)
        temp = puissance_mod(a, w, n)
        if temp != 1:
            r = 0
            while temp != n - 1:
                if r == k - 1:
                    return False
                else:
                    temp = puissance_mod(temp, 2, n)
                    r += 1
        tries += 1
    
    return True