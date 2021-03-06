'''generate the module to solve ODEs'''
# writes a module based on the supplied chemical scheme and user inputs,
# since the solved ODEs can represent gas-phase photochemistry,
# gas-particle partitioning and gas-wall partitioning, note use %f when
# writing floats from inputs

import datetime

# function to generate the ordinary differential equation (ODE)
# solver file
def ode_gen(con_infl_indx, int_tol, rowvals, wall_on, num_comp, 
		num_asb, con_C_indx, testf):

	# inputs: ------------------------------------------------
	# con_infl_indx - indices of components with constant influx
	# int_tol - integration tolerances
	# rowvals - indices of rows for Jacobian
	# wall_on - marker for whether to consider wall 
	# 	partitioning
	# num_comp - number of components
	# num_asb - number of actual size bins (excluding wall)
	# con_C_indx - index of components with constant gas-phase 
	#	concentration
	# testf - marker for whether in test mode or not
	# -------------------------------------------------------
	
	# create new  file to store solver module
	f = open('PyCHAM/ode_solv.py', mode='w')
	f.write('\'\'\'solution of ODEs, generated by eqn_pars.py\'\'\'\n')
	f.write('# module to solve ordinary differential equations (ODEs)\n')
	f.write('# File Created at %s\n' %(datetime.datetime.now()))	
	f.write('\n')
	f.write('import numpy as np\n')
	f.write('import scipy.sparse as SP\n')
	f.write('from assimulo.problem import Explicit_Problem\n')
	f.write('from assimulo.solvers import CVode\n')
	f.write('from assimulo.solvers import CVode\n')
	f.write('from numba import jit, f8\n')
	f.write('\n')	
	f.write('# define function\n')
	f.write('def ode_solv(y, integ_step, rindx, pindx, rstoi, pstoi, \n')
	f.write('	nreac, nprod, rrc, jac_stoi, njac, jac_den_indx, \n')
	f.write('	jac_indx, Cinfl_now, y_arr, y_rind, uni_y_rind, \n')
	f.write('	y_pind, uni_y_pind, reac_col, prod_col, \n')
	f.write('	rstoi_flat, pstoi_flat, rr_arr, rr_arr_p,\n') 
	f.write('	rowvals, colptrs, num_comp, num_sb,\n')
	f.write('	wall_on, Psat, Cw, act_coeff, kw, jac_wall_indx,\n') 
	f.write('	seedi, core_diss, kelv_fac, kimt, num_asb,\n')
	f.write('	jac_part_indx,\n')
	f.write('	rindx_aq, pindx_aq, rstoi_aq, pstoi_aq,\n')
	f.write('	nreac_aq, nprod_aq, jac_stoi_aq, njac_aq, jac_den_indx_aq, jac_indx_aq,\n')
	f.write('	y_arr_aq, y_rind_aq, uni_y_rind_aq, y_pind_aq, uni_y_pind_aq,\n')
	f.write('	reac_col_aq, prod_col_aq, rstoi_flat_aq,\n')
	f.write('	pstoi_flat_aq, rr_arr_aq, rr_arr_p_aq, eqn_num):\n')
	f.write('\n')
	f.write('	# inputs: -------------------------------------\n')
	f.write('	# y - initial concentrations (moleucles/cm3)\n')
	f.write('	# integ_step - the maximum integration time step (s)\n')
	f.write('	# rindx - index of reactants per equation\n')
	f.write('	# pindx - index of products per equation\n')
	f.write('	# rstoi - stoichiometry of reactants\n')
	f.write('	# pstoi - stoichiometry of products\n')
	f.write('	# nreac - number of reactants per equation\n')
	f.write('	# nprod - number of products per equation\n')
	f.write('	# rrc - reaction rate coefficient\n')
	f.write('	# jac_stoi - stoichiometries relevant to Jacobian\n')
	f.write('	# njac - number of Jacobian elements affected per equation\n')
	f.write('	# jac_den_indx - index of component denominators for Jacobian\n')
	f.write('	# jac_indx - index of Jacobian to place elements per equation (rows)\n')
	f.write('	# Cinfl_now - influx of components with constant influx \n')
	f.write('	#		(molecules/cc/s)\n')
	f.write('	# y_arr - index for matrix used to arrange concentrations, \n')
	f.write('	#	enabling calculation of reaction rate coefficients \n')
	f.write('	# y_rind - index of y relating to reactants for reaction rate \n')
	f.write('	# 	coefficient equation\n')
	f.write('	# uni_y_rind - unique index of reactants \n')
	f.write('	# y_pind - index of y relating to products\n')
	f.write('	# uni_y_pind - unique index of products \n')
	f.write('	# reac_col - column indices for sparse matrix of reaction losses\n')
	f.write('	# prod_col - column indices for sparse matrix of production gains\n')
	f.write('	# rstoi_flat - 1D array of reactant stoichiometries per equation\n')
	f.write('	# pstoi_flat - 1D array of product stoichiometries per equation\n')
	f.write('	# rr_arr - index for reaction rates to allow reactant loss\n')
	f.write('	# 	calculation\n')
	f.write('	# rr_arr_p - index for reaction rates to allow reactant loss\n')
	f.write('	# 	calculation\n')
	f.write('	# rowvals - row indices of Jacobian elements\n')
	f.write('	# colptrs - indices of  rowvals corresponding to each column of the\n') 
	f.write('	# 	Jacobian\n')
	f.write('	# num_comp - number of components\n')
	f.write('	# num_sb - number of size bins\n')
	f.write('	# wall_on - flag saying whether to include wall partitioning\n')
	f.write('	# Psat - pure component saturation vapour pressures (molecules/cc)\n')
	f.write('	# Cw - effective absorbing mass concentration of wall (molecules/cc) \n')
	f.write('	# act_coeff - activity coefficient of components\n')
	f.write('	# kw - mass transfer coefficient to wall (/s)\n')
	f.write('	# jac_wall_indx - index of inputs to Jacobian by wall partitioning\n')
	f.write('	# seedi - index of seed material\n')
	f.write('	# core_diss - dissociation constant of seed material\n')
	f.write('	# kelv_fac - kelvin factor for particles\n')
	f.write('	# kimt - mass transfer coefficient for gas-particle partitioning (s)\n')
	f.write('	# num_asb - number of actual size bins (excluding wall)\n')
	f.write('	# jac_part_indx - index for sparse Jacobian for particle influence \n')
	f.write('	# eqn_num - number of gas- and aqueous-phase reactions \n')
	f.write('	# ---------------------------------------------\n')
	f.write('\n')
	
	# the module if needed for testing
	if (testf > 0):
		f.write('	# gas-particle partitioning-----------------\n')
		f.write('	# transform particle phase concentrations into\n')
		f.write('	# size bins in rows, components in columns\n')
		f.write('	ymat = (y[num_comp:num_comp*(num_asb+1)]).reshape(num_asb, num_comp)\n')
		f.write('	# total particle-phase concentration per size bin (molecules/cc (air))\n')
		f.write('	csum = ((ymat.sum(axis=1)-ymat[:, seedi])+((ymat[:, seedi]*core_diss))).reshape(-1, 1)\n')
		f.write('	# size bins with contents \n')
		f.write('	isb = (csum[:, 0]>0.)\n')
		f.write('	\n')
		f.write('	# container for gas-phase concentrations at particle surface\n')
		f.write('	Csit = np.zeros((num_asb, num_comp))\n')
		f.write('	# mole fraction of components at particle surface\n')
		f.write('	Csit[isb, :] = (ymat[isb, :]/csum[isb, :])\n')
		f.write('	\n')
		f.write('	return(Csit)\n')
		f.close() # close file
		return()


	# testing with 16 size bins and the MCM alpha-pinene chemical scheme
	# showed that using the vectorised Python code gave just 1 %
	# increase in wall clock time compared to using numba, and won't
	# give the gradual slow down in computation that arises with numba
	# when many integration time steps are set, furthermore it means that 
	# for fast integration systems, time isn't wasted on compilation, 
	# therefore we use the
	# vectorised form by default and the numba version is commented out 
	# below
	f.write('	def dydt(t, y): # define the ODE(s)\n')
	f.write('\n')
	f.write('		# empty array to hold rate of change per component\n')
	f.write('		dd = np.zeros((len(y)))\n')
	f.write('		\n')
	f.write('		# gas-phase reactions -------------------------\n')
	f.write('		# empty array to hold relevant concentrations for\n')
	f.write('		# reaction rate coefficient calculation\n')
	f.write('		rrc_y = np.ones((rindx.shape[0]*rindx.shape[1]))\n')
	f.write('		rrc_y[y_arr] = y[y_rind]\n')
	f.write('		rrc_y = rrc_y.reshape(rindx.shape[0], rindx.shape[1], order = \'C\')\n')
	f.write('		# reaction rate (molecules/cc/s) \n')
	f.write('		rr = rrc[0:rindx.shape[0]]*((rrc_y**rstoi).prod(axis=1))\n')
	f.write('		# loss of reactants\n')
	f.write('		data = rr[rr_arr]*rstoi_flat # prepare loss values\n')
	f.write('		# convert to sparse matrix\n')
	f.write('		loss = SP.csc_matrix((data, y_rind, reac_col))\n')
	f.write('		# register loss of reactants\n')
	f.write('		dd[uni_y_rind] -= np.array((loss.sum(axis = 1))[uni_y_rind])[:, 0]\n')
	f.write('		# gain of products\n')
	f.write('		data = rr[rr_arr_p]*pstoi_flat # prepare loss values\n')
	f.write('		# convert to sparse matrix\n')
	f.write('		loss = SP.csc_matrix((data, y_pind, prod_col))\n')
	f.write('		# register gain of products\n')
	f.write('		dd[uni_y_pind] += np.array((loss.sum(axis = 1))[uni_y_pind])[:, 0]\n')
	f.write('		\n')
	f.write('		# particle-phase reactions -------------------------\n')
	f.write('		if (eqn_num[1] > 0):\n')
	f.write('			# empty array to hold relevant concentrations for\n')
	f.write('			# reaction rate coefficient calculation\n')
	f.write('			# tile aqueous-phase reaction rate coefficients\n')
	f.write('			rr_aq = np.tile(rrc[rindx.shape[0]::], num_asb)\n')
	f.write('			# prepare aqueous-phase concentrations\n')
	f.write('			rrc_y = np.ones((rindx_aq.shape[0]*rindx_aq.shape[1]))\n')
	f.write('			rrc_y[y_arr_aq] = y[y_rind_aq]\n')
	f.write('			rrc_y = rrc_y.reshape(rindx_aq.shape[0], rindx_aq.shape[1], order = \'C\')\n')
	f.write('			# reaction rate (molecules/cc/s) \n')
	f.write('			rr = rr_aq*((rrc_y**rstoi_aq).prod(axis=1))\n')
	f.write('			# loss of reactants\n')
	f.write('			data = rr[rr_arr_aq]*rstoi_flat_aq # prepare loss values\n')
	f.write('			# convert to sparse matrix\n')
	f.write('			loss = SP.csc_matrix((data[0, :], y_rind_aq, reac_col_aq))\n')
	f.write('			# register loss of reactants\n')
	f.write('			dd[uni_y_rind_aq] -= np.array((loss.sum(axis = 1))[uni_y_rind_aq])[:, 0]\n')
	f.write('			# gain of products\n')
	f.write('			data = rr[rr_arr_p_aq]*pstoi_flat_aq # prepare loss values\n')
	f.write('			# convert to sparse matrix\n')
	f.write('			loss = SP.csc_matrix((data[0, :], y_pind_aq, prod_col_aq))\n')
	f.write('			# register gain of products\n')
	f.write('			dd[uni_y_pind_aq] += np.array((loss.sum(axis = 1))[uni_y_pind_aq])[:, 0]\n')
	f.write('		\n')

	if (len(con_infl_indx)>0): # if any components have a continuous gas-phase influx
		f.write('		dd[[')	
		for Ci in range(len(con_infl_indx)):
			if Ci<len(con_infl_indx)-1:
				f.write('%d, ' %int(con_infl_indx[Ci]))
			else:
				f.write('%d]] += Cinfl_now[:, 0]\n' %int(con_infl_indx[Ci]))
		f.write('		\n')
	# if any components have a constant gas-phase concentration
	if (len(con_C_indx)>0):
		f.write('		dd[[')
		for Ci in range(len(con_C_indx)):
			if Ci<len(con_C_indx)-1:
				f.write('%d, ' %int(con_C_indx[Ci]))
			else:
				f.write('%d]] = 0. \n' %int(con_C_indx[Ci]))
		f.write('		\n')
	if (num_asb)>0: # include gas-particle partitioning in ode solver
		f.write('		# gas-particle partitioning-----------------\n')
		f.write('		# transform particle phase concentrations into\n')
		f.write('		# size bins in rows, components in columns\n')
		f.write('		ymat = (y[num_comp:num_comp*(num_asb+1)]).reshape(num_asb, num_comp)\n')		
		f.write('		# total particle-phase concentration per size bin (molecules/cc (air))\n')
		f.write('		csum = ((ymat.sum(axis=1)-ymat[:, seedi].sum(axis=1))+((ymat[:, seedi]*core_diss).sum(axis=1)).reshape(-1)).reshape(-1, 1)\n')
		f.write('		# size bins with contents \n')
		f.write('		isb = (csum[:, 0]>0.)\n')
		f.write('		\n')
		f.write('		# container for gas-phase concentrations at particle surface\n')
		f.write('		Csit = np.zeros((num_asb, num_comp))\n')
		f.write('		# mole fraction of components at particle surface\n')
		f.write('		Csit[isb, :] = (ymat[isb, :]/csum[isb, :])\n')	
		f.write('		# gas-phase concentration of components at\n')
		f.write('		# particle surface (molecules/cc (air))\n')
		f.write('		Csit[isb, :] = Csit[isb, :]*Psat[isb, :]*kelv_fac[isb]*act_coeff[isb, :]\n')	
		f.write('		# partitioning rate (molecules/cc/s)\n')
		f.write('		dd_all = kimt*(y[0:num_comp].reshape(1, -1)-Csit)\n')
		f.write('		# gas-phase change\n')
		f.write('		dd[0:num_comp] -= dd_all.sum(axis=0)\n')
		f.write('		# particle change\n')
		f.write('		dd[num_comp:num_comp*(num_asb+1)] += (dd_all.flatten())\n')
		f.write('		\n')

	if wall_on>0: # include gas-wall partitioning in ode solver
		f.write('		# gas-wall partitioning ----------------\n')
		f.write('		# concentration on wall (molecules/cc (air))\n')
		f.write('		Csit = y[num_comp*num_sb:num_comp*(num_sb+1)]\n')
		f.write('		# saturation vapour pressure on wall (molecules/cc (air))\n')
		f.write('		# note, just using the top rows of Psat and act_coeff\n')
		f.write('		# as do not need the repetitions over size bins\n')
		f.write('		if (Cw>0.):\n')
		f.write('			Csit = Psat[0, :]*(Csit/Cw)*act_coeff[0, :]\n')
		f.write('			# rate of transfer (molecules/cc/s)\n')
		f.write('			dd_all = kw*(y[0:num_comp]-Csit)\n')
		f.write('			dd[0:num_comp] -= dd_all # gas-phase change\n')
		f.write('			dd[num_comp*num_sb:num_comp*(num_sb+1)] += dd_all # wall change\n')
		f.write('		\n')
	#	f.write('	# numba compiler to convert to machine code\n')
	#	f.write('	@jit(f8[:](f8, f8[:]), nopython=True, cache=False)\n')
	#	f.write('	# ode solver -------------------------------------\n')
	#	f.write('	def dydt(t, y): # define the ODE(s)\n')
	#	f.write('		\n')
	#	f.write('		# empty array to hold rate of change per component\n')
	#	f.write('		dd = np.zeros((len(y)))\n')
	#	f.write('		# gas-phase rate of change -----------------------\n')
	#	f.write('		for i in range(nreac.shape[0]): # equation loop\n')
	#	f.write('			# gas-phase rate of change (molecules/cc (air).s)\n')
	#	f.write('			if (y[rindx[i, 0:nreac[i]]]==0.0).sum()>0:\n')	
	#	f.write('				continue # if any reactants not present skip this reaction\n')			
	#	f.write('			else:\n')
	#	f.write('				gprate = ((y[rindx[i, 0:nreac[i]]]**rstoi[i, 0:nreac[i]]).prod())*rrc[i]\n')
	#	f.write('				# loss of reactants\n')
	#	f.write('				dd[rindx[i, 0:nreac[i]]] -= gprate*rstoi[i, 0:nreac[i]]\n')
	#	f.write('				# gain of products\n')
	#	f.write('				dd[pindx[i, 0:nprod[i]]] += gprate*pstoi[i, 0:nprod[i]]\n')
	#	f.write('		\n')
	#	# only write next section if particles present
	#	if (num_asb>0):
	#		f.write('		# if size bins present estimate gas-particle partitioning\n')
	#		f.write('		for ibin in range(num_asb): # size bin loop\n')
	#		f.write('			# particle-phase concentrations in this size bin (moclecules/cc)\n')
	#		f.write('			Csit = y[num_comp*(ibin+1):num_comp*(ibin+2)]\n')
	#		f.write('			# prepare for # sum of molecular concentrations per bin (molecules/cc (air))\n')
	#		f.write('			conc_sum = np.zeros((1))\n')
	#		f.write('			conc_sum[0] = ((Csit.sum()-Csit[seedi])+Csit[seedi]*core_diss)\n')
	#		f.write('			# only need to continue if particles present\n')
	#		f.write('			if (conc_sum[0]>1.e-20):\n')
	#		f.write('				# particle surface gas-phase concentration (molecules/cc (air))\n')
	#		f.write('				Csit = (Csit/conc_sum)*Psat[0, :]*kelv_fac[ibin]*act_coeff[0, :]\n')
	#		f.write('				# partitioning rate (molecules/cc.s)\n')
	#		f.write('				dydt_all = kimt[ibin, :]*(y[0:num_comp]-Csit)\n')
	#		f.write('				dd[0:num_comp] -= dydt_all # gas-phase change\n')
	#		f.write('				# particle-phase change\n')
	#		f.write('				dd[num_comp*(ibin+1):num_comp*(ibin+2)] += dydt_all\n')
	#		f.write('		\n')
	#	# only write next section if gas-wall partitioning active
	#	if (wall_on==1):
	#		f.write('		if (Cw>0.): # only consider if wall present\n')
	#		f.write('			# if wall consideration turned on, estimate gas-wall partitioning\n')
	#		f.write('			# concentration at wall (molecules/cc (air))\n')
	#		f.write('			Csit = y[num_comp*num_sb:num_comp*(num_sb+1)]\n')
	#		f.write('			Csit = (Psat[0, :]*(Csit/Cw)*act_coeff[0, :]) # with Raoult term\n')
	#		f.write('			dydt_all = (kw)*(y[0:num_comp]-Csit)\n')
	#		f.write('			dd[0:num_comp] -= dydt_all # gas-phase change\n')
	#		f.write('			# wall concentration change \n')
	#		f.write('			dd[num_comp*num_sb:num_comp*(num_sb+1)] += dydt_all\n')
	#		f.write('			\n')
	f.write('		return (dd)\n')
	f.write('\n')
	# testing with 16 size bins and the MCM alpha-pinene chemical scheme
	# showed that defining the Jacobian gave a 10 % reduction in wall
	# clock time, therefore this set by default
	f.write('	def jac(t,y): # define the Jacobian\n')
	f.write('		# elements of sparse Jacobian matrix\n')
	f.write('		data = np.zeros((%s))\n' %len(rowvals))
	f.write('		\n')
	f.write('		for i in range(rindx.shape[0]): # gas-phase reaction loop\n')
	f.write('			# reaction rate (molecules/cc/s)\n')
	f.write('			rr = rrc[i]*(y[rindx[i, 0:nreac[i]]].prod())\n')
	f.write('			# prepare Jacobian inputs\n')
	f.write('			jac_coeff = np.zeros((njac[i, 0]))\n')
	f.write('			# only fill Jacobian if reaction rate sufficient\n')
	f.write('			if (rr != 0.):\n')
	f.write('				jac_coeff = (rr*(jac_stoi[i, 0:njac[i, 0]])/\n')
	f.write('				(y[jac_den_indx[i, 0:njac[i, 0]]]))\n')
	f.write('			data[jac_indx[i, 0:njac[i, 0]]] += jac_coeff\n')
	f.write('		\n')
	f.write('		n_aqr = nreac_aq.shape[0] # number of aqueous-phase reactions \n')
	f.write('		aqi = 0 # aqueous-phase reaction counter\n')
	f.write('		for i in range(rindx.shape[0], rrc.shape[0]): # aqueous-phase reaction loop\n')
	f.write('			# reaction rate (molecules/cc/s)\n')
	f.write('			rr = rrc[i]*(y[rindx_aq[aqi::n_aqr, 0:nreac_aq[aqi]]].prod(axis=1))\n')
	f.write('			# spread along affected components\n')
	f.write('			rr = rr.reshape(-1, 1)\n')
	f.write('			rr = (np.tile(rr, int(njac_aq[aqi, 0]/(num_sb-wall_on)))).flatten(order=\'C\')\n')
	f.write('			# prepare Jacobian inputs\n')
	f.write('			jac_coeff = np.zeros((njac_aq[aqi, 0]))\n')
	f.write('			nzi = (rr != 0)\n')
	f.write('			jac_coeff[nzi] = (rr[nzi]*((jac_stoi_aq[aqi, 0:njac_aq[aqi, 0]])[nzi])/\n')
	f.write('				((y[jac_den_indx_aq[aqi, 0:njac_aq[aqi, 0]]])[nzi]))\n')
	f.write('			# stack size bins\n')
	f.write('			jac_coeff = jac_coeff.reshape(int(num_sb-wall_on), int(njac_aq[aqi, 0]/(num_sb-wall_on)), order=\'C\')\n')
	f.write('			data[jac_indx_aq[aqi::n_aqr, 0:(int(njac_aq[aqi, 0]/(num_sb-wall_on)))]] += jac_coeff\n')
	f.write('			aqi += 1\n')
	f.write('		\n')
	if (num_asb > 0): # include gas-particle partitioning in ode solver Jacobian
		f.write('		# gas-particle partitioning\n')
		f.write('		part_eff = np.zeros((%s))\n' %((num_comp)*(num_asb+1)+((num_comp)*(num_asb*2))))
		f.write('		part_eff[0:%s:%s] = -kimt.sum(axis=0) # effect of gas on gas\n' %(num_comp*(num_asb+1), (num_asb+1)))
		f.write('		\n')
		f.write('		# transform particle phase concentrations into\n')
		f.write('		# size bins in rows, components in columns\n')
		f.write('		ymat = (y[num_comp:num_comp*(num_asb+1)]).reshape(num_asb, num_comp)\n')
		f.write('		# total particle-phase concentration per size bin (molecules/cc (air))\n')
		f.write('		csum = ymat.sum(axis=1)-ymat[:, seedi].sum(axis=1)+(ymat[:, seedi]*core_diss).sum(axis=1)\n')
		f.write('		\n')
		f.write('		# effect of particle on gas\n')
		f.write('		for isb in range(int(num_asb)): # size bin loop\n')
		f.write('			if csum[isb]>0: # if particles present\n')
		f.write('				# effect of gas on particle\n')
		f.write('				part_eff[1+isb:num_comp*(num_asb+1):num_asb+1] = +kimt[isb, :]\n')
		f.write('				# start and finish index\n')
		f.write('				sti = int((num_asb+1)*num_comp+isb*(num_comp*2))\n')
		f.write('				fii = int(sti+(num_comp*2.))\n')
		f.write('				# diagonal index\n')
		f.write('				diag_indxg = sti+np.arange(0, num_comp*2, 2).astype(\'int\')\n')
		f.write('				diag_indxp = sti+np.arange(1, num_comp*2, 2).astype(\'int\')\n')
		f.write('				# prepare for diagonal (component effect on itself)\n')
		f.write('				diag = kimt[isb, :]*Psat[0, :]*act_coeff[0, :]*kelv_fac[isb, 0]*(csum[isb]-ymat[isb, :])/(csum[isb]**2.)\n')
		f.write('				# implement to part_eff\n')
		f.write('				part_eff[diag_indxg] = +diag\n')
		f.write('				part_eff[diag_indxp] = -diag\n')
		f.write('		\n')
		f.write('		data[jac_part_indx] += part_eff\n')
		f.write('		\n')

	if wall_on>0: # include gas-wall partitioning in ode solver Jacobian
		f.write('		if (Cw>0.):\n')
		f.write('			wall_eff = np.zeros((%s))\n' %(num_comp*4))
		f.write('			wall_eff[0:%s:2] = -kw # effect of gas on gas \n' %(num_comp*2))
		f.write('			wall_eff[1:%s:2] = +kw # effect of gas on wall \n' %(num_comp*2))
		f.write('			# effect of wall on gas\n')
		f.write('			wall_eff[%s:%s:2] = +kw*(Psat[0,:]*act_coeff[0, :]/Cw) \n' %(num_comp*2, num_comp*4))
		f.write('			# effect of wall on wall\n')
		f.write('			wall_eff[%s+1:%s:2] = -kw*(Psat[0,:]*act_coeff[0, :]/Cw) \n' %(num_comp*2, num_comp*4))
		f.write('			data[jac_wall_indx] += wall_eff\n')
		f.write('		\n')
	f.write('		# create Jacobian\n')
	f.write('		j = SP.csc_matrix((data, rowvals, colptrs))\n')
	f.write('		return(j)\n')
	f.write('\n')
	f.write('	mod = Explicit_Problem(dydt, y) # instantiate solver\n')
	f.write('	mod.jac = jac # set the Jacobian\n')
	f.write('	mod_sim = CVode(mod) # define a solver instance\n')
	f.write('	# there is a general trend of an inverse relationship\n')
	f.write('	# between tolerances and computation time\n')
	f.write('	mod_sim.atol = %s\n'%int_tol[0])
	f.write('	mod_sim.rtol = %s\n'%int_tol[1])
	f.write('	# integration approach (backward differentiation formula)\n')
	f.write('	mod_sim.discr = \'BDF\'\n')
	f.write('	# call solver\n')
	f.write('	res_t, res = mod_sim.simulate(integ_step)\n')
	f.write('	# return concentrations following integration\n')
	f.write('	return(res, res_t)\n')
	f.close() # close file

