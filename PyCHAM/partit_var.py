'''module to estimate the particle and wall partitioning coefficient'''
# the kimt_calc module is called at the start of the model loop time interval to update
# the mass transfer coefficient of gases to particles

import numpy as np
from part_prop import part_prop

def kimt_calc(y, mfp, num_sb, num_speci, accom_coeff, y_mw, surfT, R_gas, TEMP, NA, 
		y_dens, N_perbin, DStar_org, radius, Psat, therm_sp,
		H2Oi, act_coeff, wall_on, caller):
	
	# ------------------------------------------------------------------------------------
	# inputs:
	
	# y - concentration of components' molecules (molecules/cc (air))
	# mfp - mean free path of gas molecules (m) (num_speci, 1)
	# accom_coeff - accommodation coefficients of components in each size bin
	# DStar_org - gas molecule diffusion coefficient (m2/s) (num_speci, 1)
	# radius - particle radius (m)
	# Psat - liquid-phase saturation vapour pressures of components (molecules/cc (air))
	# surfT - surface tension (g/s2==mN/m==dyn/cm)
	# y_dens - density of components (kg/m3)
	# N_perbin - number of particles per size bin (excluding wall)
	# therm_sp - thermal speed of components (m/s) (num_speci, 1)
	# H2Oi - water index (integer)
	# act_coeff - activity coefficient of components (dimensionless)
	# wall_on - marker for whether wall present
	# caller - marker for the calling function
	# ------------------------------------------------------------------------------------
	
	if num_sb == 0: # fillers
		kimt = 0.
		kelv = 0.

		return(kimt, kelv)

	if num_sb>0 and (wall_on>0): # if wall present
		y_part = y[num_speci:-(num_speci)]
	if num_sb>0 and (wall_on==0): # if wall absent
		y_part = y[num_speci::]

	# density (g/cm3) and average molecular weight (g/mol) of particles (excluding wall)
	[tot_rho, ish, avMW] = part_prop(y_part, num_speci, (num_sb-wall_on), NA, y_mw, y_dens, 
					N_perbin)
	
	# Knudsen number (dimensionless)
	Kn = np.repeat(mfp, (num_sb-wall_on), 1)/np.repeat(radius, num_speci, 0)
	
	# update accommodation coefficients if necessary
	# note, using __import__ rather than import allows opening in run time, thereby using
	# updated module
	accom_coeff_calc = __import__('accom_coeff_calc')
	accom_coeff_now = accom_coeff_calc.accom_coeff_func(accom_coeff, radius)

	# Non-continuum regime correction 
	# calculate a correction factor according to the continuum versus non-continuum 
	# regimes
	# expression taken from Jacobson et al (2000), page 457, or Jacobson (2005), page 530 
	# (eq. 16.19).
	# They reference:
	# Fuchs and Sutugin 1971
	# Pruppacher and Klett 1997
	Inverse_Kn = np.power(Kn, -1.0E0)
	correct_1 = (1.33E0+0.71*Inverse_Kn)/(1.0+Inverse_Kn)
	correct_2 = (4.0E0*(1.0E0-accom_coeff_now))/(3.0E0*accom_coeff_now)
	correct_3 = 1.0E0+(correct_1+correct_2)*Kn
	correction = np.power(correct_3, -1.0E0)
	
	# kelvin factor for each size bin (excluding wall), eq. 16.33 Jacobson et al. (2005)
	# note that avMW has units g/mol, surfT (g/s2==mN/m==dyn/cm), R_gas is multiplied by 
	# 1e7 for units g cm2/s2.mol.K, 
	# TEMP is K, radius is multiplied by 1e2 to give cm and tot_rho is g/cm3
	kelv = np.zeros((num_sb-wall_on, 1))
	kelv[ish, 0] = np.exp((2.0E0*avMW[ish]*surfT)/(R_gas*1.0e7*TEMP*(
				radius[0, ish]*1.0e2)*tot_rho[ish]))

	
	# gas phase diffusion coefficient*Fuch-Sutugin correction (cm2/s)
	# eq. 5 Zaveri et al. (2008), scale by 1e4 to convert from m2/s to cm2/s
	kimt = (DStar_org*1e4)*correction
	# final partitioning coefficient (converting radius from m to cm)
	# eq. 16.2 of Jacobson (2005) and eq. 5 Zaveri et al. (2008)
	# components in rows and size bins in columns (/s)
	kimt = (4.0E0*np.pi*(radius*1.0e2)*N_perbin.reshape(1, -1))*kimt
	# transpose kimt ready for multiplication inside ode solver, so size bins
	# in rows and components in columns
	kimt = np.transpose(kimt)

	# zero partitioning to particles for any components with low partitioning rates
	# compared to their concentrations in the gas or particle
	#cp = y_part.reshape(num_sb-wall_on, num_speci)
	#cpsum = ((cp).sum(axis=1)).reshape(-1, 1).repeat(num_speci, 1)
	#cg = (y[0:num_speci].reshape(1, -1)).repeat(num_sb-wall_on, 0)
	#cpr = Psat*act_coeff*kelv.repeat(num_speci, 1)*cp
	#cpr[cpsum>0.] = cpr[cpsum>0.]/cpsum[cpsum>0.]
	#rates = np.zeros((num_sb-wall_on, num_speci))
	#rates[cpsum>0.] = cg[cpsum>0.]-cpr[cpsum>0.]
	#cdiff = (cg-cp)
	#cmax = np.ones((num_sb-wall_on, num_speci))*cg[:, :]
	#cmax[cdiff<0] = cp[cdiff<0]
	#eff_mar = np.ones((num_sb-wall_on, num_speci))==1
	#eff_mar[cmax>0.] = (np.abs(rates[cmax>0.])/cmax[cmax>0.])<1.e-4
	#kimt[eff_mar] = 0.
	# if vapour pressure very great then zero the transfer coefficient
	#cg = (y[0:num_speci].reshape(1, -1)).repeat(num_sb-wall_on, 0)
	#rat = np.ones((num_sb-wall_on, num_speci))<0
	#rat[cg>0] = (Psat[cg>0]*act_coeff[cg>0]/cg[cg>0])>1.e2
	#kimt[rat] = 0.
	
	# zero partitioning coefficient for size bins where no particles - enables significant
	# computation time acceleration and is physically realistic
	ish = N_perbin[:, 0]<=1.e-10
	kimt[ish, :] = 0.
	
	return(kimt, kelv)