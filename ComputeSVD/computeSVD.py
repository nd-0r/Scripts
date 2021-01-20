from sympy import Matrix

def computeSVD(A):
	if (not isinstance(A, Matrix)):
		raise InvalidArgumentException(f'can only compute the SVD of a matrix')
	ATA = A.transpose() * A
	AAT = A * A.transpose()
	ATA_eigenvectors = [v[2][0].normalized().evalf() for v in ATA.eigenvects()]
	print(ATA_eigenvectors)
	AAT_eigenvectors = [v[2][0].normalized().evalf() for v in AAT.eigenvects()]
	print(AAT_eigenvectors)
	eig_vals = [v for v in AAT.eigenvals().keys()]
	to_sigma = []
	count = 0
	for pos in range(0, A.rows * A.cols):
		if (pos % A.rows == count):
			to_sigma.append(eig_vals[count].evalf())
			count += 1
		else:
			to_sigma.append(0)
	SIGMA = Matrix(A.rows, A.cols, to_sigma)
	vt = Matrix([eigenvector for eigenvector in ATA_eigenvectors])
	v = vt.transpose()
	ut = Matrix([eigenvector for eigenvector in AAT_eigenvectors])
	u = ut.transpose()
	print("U:")
	print(u.__repr__())
	print("SIGMA:")
	print(SIGMA.__repr__())
	print("V:")
	print(v.__repr__())
