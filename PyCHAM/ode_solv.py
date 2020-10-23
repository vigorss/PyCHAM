'''solution of ODEs, generated by eqn_pars.py'''
# module to solve ordinary differential equations (ODEs)
# File Created at 2020-10-23 17:33:53.199748

import numpy as np
import scipy.sparse as SP
from assimulo.problem import Explicit_Problem
from assimulo.solvers import CVode
from assimulo.solvers import CVode
from numba import jit, f8

# define function
def ode_solv(y, integ_step, rindx, pindx, rstoi, pstoi, 
	nreac, nprod, rrc, jac_stoi, njac, jac_den_indx, 
	jac_indx, Cinfl_now, y_arr, y_rind, uni_y_rind, 
	y_pind, uni_y_pind, reac_col, prod_col, 
	rstoi_flat, pstoi_flat, rr_arr, rr_arr_p,
	rowvals, colptrs, num_comp, num_sb,
	wall_on, Psat, Cw, act_coeff, kw, jac_wall_indx,
	corei, core_diss, kelv_fac, kimt, num_asb,
	jac_part_indx,
	rindx_aq, pindx_aq, rstoi_aq, pstoi_aq,
	nreac_aq, nprod_aq, jac_stoi_aq, njac_aq, jac_den_indx_aq, jac_indx_aq,
	y_arr_aq, y_rind_aq, uni_y_rind_aq, y_pind_aq, uni_y_pind_aq,
	reac_col_aq, prod_col_aq, rstoi_flat_aq,
	pstoi_flat_aq, rr_arr_aq, rr_arr_p_aq, eqn_num):

	# inputs: -------------------------------------
	# y - initial concentrations (moleucles/cm3)
	# integ_step - the maximum integration time step (s)
	# rindx - index of reactants per equation
	# pindx - index of products per equation
	# rstoi - stoichiometry of reactants
	# pstoi - stoichiometry of products
	# nreac - number of reactants per equation
	# nprod - number of products per equation
	# rrc - reaction rate coefficient
	# jac_stoi - stoichiometries relevant to Jacobian
	# njac - number of Jacobian elements affected per equation
	# jac_den_indx - index of component denominators for Jacobian
	# jac_indx - index of Jacobian to place elements per equation (rows)
	# Cinfl_now - influx of components with constant influx 
	#		(molecules/cc/s)
	# y_arr - index for matrix used to arrange concentrations, 
	#	enabling calculation of reaction rate coefficients 
	# y_rind - index of y relating to reactants for reaction rate 
	# 	coefficient equation
	# uni_y_rind - unique index of reactants 
	# y_pind - index of y relating to products
	# uni_y_pind - unique index of products 
	# reac_col - column indices for sparse matrix of reaction losses
	# prod_col - column indices for sparse matrix of production gains
	# rstoi_flat - 1D array of reactant stoichiometries per equation
	# pstoi_flat - 1D array of product stoichiometries per equation
	# rr_arr - index for reaction rates to allow reactant loss
	# 	calculation
	# rr_arr_p - index for reaction rates to allow reactant loss
	# 	calculation
	# rowvals - row indices of Jacobian elements
	# colptrs - indices of  rowvals corresponding to each column of the
	# 	Jacobian
	# num_comp - number of components
	# num_sb - number of size bins
	# wall_on - flag saying whether to include wall partitioning
	# Psat - pure component saturation vapour pressures (molecules/cc)
	# Cw - effective absorbing mass concentration of wall (molecules/cc) 
	# act_coeff - activity coefficient of components
	# kw - mass transfer coefficient to wall (/s)
	# jac_wall_indx - index of inputs to Jacobian by wall partitioning
	# corei - index of seed material
	# core_diss - dissociation constant of seed material
	# kelv_fac - kelvin factor for particles
	# kimt - mass transfer coefficient for gas-particle partitioning (s)
	# num_asb - number of actual size bins (excluding wall)
	# jac_part_indx - index for sparse Jacobian for particle influence 
	# eqn_num - number of gas- and aqueous-phase reactions 
	# ---------------------------------------------

	def dydt(t, y): # define the ODE(s)

		# empty array to hold rate of change per component
		dd = np.zeros((len(y)))
		
		# gas-phase reactions -------------------------
		# empty array to hold relevant concentrations for
		# reaction rate coefficient calculation
		rrc_y = np.ones((rindx.shape[0]*rindx.shape[1]))
		rrc_y[y_arr] = y[y_rind]
		rrc_y = rrc_y.reshape(rindx.shape[0], rindx.shape[1], order = 'C')
		# reaction rate (molecules/cc/s) 
		rr = rrc[0:rindx.shape[0]]*((rrc_y**rstoi).prod(axis=1))
		# loss of reactants
		data = rr[rr_arr]*rstoi_flat # prepare loss values
		# convert to sparse matrix
		loss = SP.csc_matrix((data, y_rind, reac_col))
		# register loss of reactants
		dd[uni_y_rind] -= np.array((loss.sum(axis = 1))[uni_y_rind])[:, 0]
		# gain of products
		data = rr[rr_arr_p]*pstoi_flat # prepare loss values
		# convert to sparse matrix
		loss = SP.csc_matrix((data, y_pind, prod_col))
		# register gain of products
		dd[uni_y_pind] += np.array((loss.sum(axis = 1))[uni_y_pind])[:, 0]
		
		# particle-phase reactions -------------------------
		if (eqn_num[1] > 0):
			# empty array to hold relevant concentrations for
			# reaction rate coefficient calculation
			# tile aqueous-phase reaction rate coefficients
			rr_aq = np.tile(rrc[rindx.shape[0]::], num_asb)
			# prepare aqueous-phase concentrations
			rrc_y = np.ones((rindx_aq.shape[0]*rindx_aq.shape[1]))
			rrc_y[y_arr_aq] = y[y_rind_aq]
			rrc_y = rrc_y.reshape(rindx_aq.shape[0], rindx_aq.shape[1], order = 'C')
			# reaction rate (molecules/cc/s) 
			rr = rr_aq*((rrc_y**rstoi_aq).prod(axis=1))
			# loss of reactants
			data = rr[rr_arr_aq]*rstoi_flat_aq # prepare loss values
			# convert to sparse matrix
			loss = SP.csc_matrix((data[0, :], y_rind_aq, reac_col_aq))
			# register loss of reactants
			dd[uni_y_rind_aq] -= np.array((loss.sum(axis = 1))[uni_y_rind_aq])[:, 0]
			# gain of products
			data = rr[rr_arr_p_aq]*pstoi_flat_aq # prepare loss values
			# convert to sparse matrix
			loss = SP.csc_matrix((data[0, :], y_pind_aq, prod_col_aq))
			# register gain of products
			dd[uni_y_pind_aq] += np.array((loss.sum(axis = 1))[uni_y_pind_aq])[:, 0]
		
		# gas-particle partitioning-----------------
		# transform particle phase concentrations into
		# size bins in rows, components in columns
		ymat = (y[num_comp:num_comp*(num_asb+1)]).reshape(num_asb, num_comp)
		# total particle-phase concentration per size bin (molecules/cc (air))
		csum = ((ymat.sum(axis=1)-ymat[:, corei].sum(axis=1))+((ymat[:, corei]*core_diss).sum(axis=1)).reshape(-1)).reshape(-1, 1)
		# size bins with contents 
		isb = (csum[:, 0]>0.)
		
		# container for gas-phase concentrations at particle surface
		Csit = np.zeros((num_asb, num_comp))
		# mole fraction of components at particle surface
		Csit[isb, :] = (ymat[isb, :]/csum[isb, :])
		# gas-phase concentration of components at
		# particle surface (molecules/cc (air))
		Csit[isb, :] = Csit[isb, :]*Psat[isb, :]*kelv_fac[isb]*act_coeff[isb, :]
		# partitioning rate (molecules/cc/s)
		dd_all = kimt*(y[0:num_comp].reshape(1, -1)-Csit)
		# gas-phase change
		dd[0:num_comp] -= dd_all.sum(axis=0)
		# particle change
		dd[num_comp:num_comp*(num_asb+1)] += (dd_all.flatten())
		
		# gas-wall partitioning ----------------
		# concentration on wall (molecules/cc (air))
		Csit = y[num_comp*num_sb:num_comp*(num_sb+1)]
		# saturation vapour pressure on wall (molecules/cc (air))
		# note, just using the top rows of Psat and act_coeff
		# as do not need the repetitions over size bins
		if (Cw>0.):
			Csit = Psat[0, :]*(Csit/Cw)*act_coeff[0, :]
			# rate of transfer (molecules/cc/s)
			dd_all = kw*(y[0:num_comp]-Csit)
			dd[0:num_comp] -= dd_all # gas-phase change
			dd[num_comp*num_sb:num_comp*(num_sb+1)] += dd_all # wall change
		
		return (dd)

	def jac(t,y): # define the Jacobian
		# elements of sparse Jacobian matrix
		data = np.zeros((9188))
		
		for i in range(rindx.shape[0]): # gas-phase reaction loop
			# reaction rate (molecules/cc/s)
			rr = rrc[i]*(y[rindx[i, 0:nreac[i]]].prod())
			# prepare Jacobian inputs
			jac_coeff = np.zeros((njac[i, 0]))
			# only fill Jacobian if reaction rate sufficient
			if (rr != 0.):
				jac_coeff = (rr*(jac_stoi[i, 0:njac[i, 0]])/
				(y[jac_den_indx[i, 0:njac[i, 0]]]))
			data[jac_indx[i, 0:njac[i, 0]]] += jac_coeff
		
		n_aqr = nreac_aq.shape[0] # number of aqueous-phase reactions 
		aqi = 0 # aqueous-phase reaction counter
		for i in range(rindx.shape[0], rrc.shape[0]): # aqueous-phase reaction loop
			# reaction rate (molecules/cc/s)
			rr = rrc[i]*(y[rindx_aq[aqi::n_aqr, 0:nreac_aq[aqi]]].prod(axis=1))
			# spread along affected components
			rr = rr.reshape(-1, 1)
			rr = (np.tile(rr, int(njac_aq[aqi, 0]/(num_sb-wall_on)))).flatten(order='C')
			# prepare Jacobian inputs
			jac_coeff = np.zeros((njac_aq[aqi, 0]))
			nzi = (rr != 0)
			jac_coeff[nzi] = (rr[nzi]*((jac_stoi_aq[aqi, 0:njac_aq[aqi, 0]])[nzi])/
				((y[jac_den_indx_aq[aqi, 0:njac_aq[aqi, 0]]])[nzi]))
			# stack size bins
			jac_coeff = jac_coeff.reshape(int(num_sb-wall_on), int(njac_aq[aqi, 0]/(num_sb-wall_on)), order='C')
			data[jac_indx_aq[aqi::n_aqr, 0:(int(njac_aq[aqi, 0]/(num_sb-wall_on)))]] += jac_coeff
			#print(jac_coeff)
			#import ipdb; ipdb.set_trace()
			aqi += 1
		
		# gas-particle partitioning
		part_eff = np.zeros((2448))
		part_eff[0:1224:2] = -kimt.sum(axis=0) # effect of gas on gas
		
		# transform particle phase concentrations into
		# size bins in rows, components in columns
		ymat = (y[num_comp:num_comp*(num_asb+1)]).reshape(num_asb, num_comp)
		# total particle-phase concentration per size bin (molecules/cc (air))
		csum = ymat.sum(axis=1)-ymat[:, corei].sum(axis=1)+(ymat[:, corei]*core_diss).sum(axis=1)
		
		# effect of particle on gas
		for isb in range(int(num_asb)): # size bin loop
			if csum[isb]>0: # if particles present
				# effect of gas on particle
				part_eff[1+isb:num_comp*(num_asb+1):num_asb+1] = +kimt[isb, :]
				# start and finish index
				sti = int((num_asb+1)*num_comp+isb*(num_comp*2))
				fii = int(sti+(num_comp*2.))
				# diagonal index
				diag_indxg = sti+np.arange(0, num_comp*2, 2).astype('int')
				diag_indxp = sti+np.arange(1, num_comp*2, 2).astype('int')
				# prepare for diagonal (component effect on itself)
				diag = kimt[isb, :]*Psat[0, :]*act_coeff[0, :]*kelv_fac[isb, 0]*(csum[isb]-ymat[isb, :])/(csum[isb]**2.)
				# implement to part_eff
				part_eff[diag_indxg] = +diag
				part_eff[diag_indxp] = -diag
		
		data[jac_part_indx] += part_eff
		
		if (Cw>0.):
			wall_eff = np.zeros((2448))
			wall_eff[0:1224:2] = -kw # effect of gas on gas 
			wall_eff[1:1224:2] = +kw # effect of gas on wall 
			# effect of wall on gas
			wall_eff[1224:2448:2] = +kw*(Psat[0,:]*act_coeff[0, :]/Cw) 
			# effect of wall on wall
			wall_eff[1224+1:2448:2] = -kw*(Psat[0,:]*act_coeff[0, :]/Cw) 
			data[jac_wall_indx] += wall_eff
		
		# create Jacobian
		j = SP.csc_matrix((data, rowvals, colptrs))
		return(j)

	mod = Explicit_Problem(dydt, y) # instantiate solver
	mod.jac = jac # set the Jacobian
	mod_sim = CVode(mod) # define a solver instance
	# there is a general trend of an inverse relationship
	# between tolerances and computation time
	mod_sim.atol = 0.001
	mod_sim.rtol = 0.0001
	# integration approach (backward differentiation formula)
	mod_sim.discr = 'BDF'
	# call solver
	res_t, res = mod_sim.simulate(integ_step)
	# return concentrations following integration
	return(res, res_t)
