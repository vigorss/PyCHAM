'''module for calculating reaction rate coefficients (automatically generated)'''
# module to hold expressions for calculating rate coefficients # 
# created at 2020-10-14 17:26:31.944734

import numpy
import photolysisRates

def evaluate_rates(RO2, H2O, TEMP, lightm, time, lat, lon, act_flux_path, DayOfYear, M, N2, O2, photo_par_file, Jlen, tf):

	# inputs: ------------------------------------------------------------------
	# RO2 - names of components included in peroxy radical list
	# M - third body concentration (molecules/cc (air))
	# N2 - nitrogen concentration (molecules/cc (air))
	# O2 - oxygen concentration (molecules/cc (air))
	# H2O, TEMP: given by the user
	# lightm: given by the user and is 0 for lights off and 1 for on
	# reaction rate coefficients and their names parsed in eqn_parser.py 
	# Jlen - number of photolysis reactions
	# tf - sunlight transmission factor
	# ------------------------------------------------------------------------

	# calculate generic reaction rate coefficients given by chemical scheme
	KRO2NO=2.7e-12*numpy.exp(360/TEMP) 
	KRO2HO2=2.91e-13*numpy.exp(1300/TEMP) 
	KAPHO2=5.2e-13*numpy.exp(980/TEMP) 
	KAPNO=7.5e-12*numpy.exp(290/TEMP) 
	KRO2NO3=2.3e-12 
	KNO3AL=1.4e-12*numpy.exp(-1860/TEMP) 
	KDEC=1.00e+06 
	KROPRIM=2.50e-14*numpy.exp(-300/TEMP) 
	KROSEC=2.50e-14*numpy.exp(-300/TEMP) 
	KCH3O2=1.03e-13*numpy.exp(365/TEMP) 
	K298CH3O2=3.5e-13 
	K14ISOM1=3.00e7*numpy.exp(-5300/TEMP) 
	KD0=1.10e-05*M*numpy.exp(-10100/TEMP) 
	KDI=1.90e17*numpy.exp(-14100/TEMP) 
	KRD=KD0/KDI 
	FCD=0.30 
	NCD=0.75-1.27*(numpy.log10(FCD)) 
	FD=10**(numpy.log10(FCD)/(1+(numpy.log10(KRD)/NCD)**2)) 
	KBPAN=(KD0*KDI)*FD/(KD0+KDI) 
	KC0=3.28e-28*M*(TEMP/300)**-6.87 
	KCI=1.125e-11*(TEMP/300)**-1.105 
	KRC=KC0/KCI 
	FCC=0.30 
	NC=0.75-1.27*(numpy.log10(FCC)) 
	FC=10**(numpy.log10(FCC)/(1+(numpy.log10(KRC)/NC)**2)) 
	KFPAN=(KC0*KCI)*FC/(KC0+KCI) 
	K10=1.0e-31*M*(TEMP/300)**-1.6 
	K1I=5.0e-11*(TEMP/300)**-0.3 
	KR1=K10/K1I 
	FC1=0.85 
	NC1=0.75-1.27*(numpy.log10(FC1)) 
	F1=10**(numpy.log10(FC1)/(1+(numpy.log10(KR1)/NC1)**2)) 
	KMT01=(K10*K1I)*F1/(K10+K1I) 
	K20=1.3e-31*M*(TEMP/300)**-1.5 
	K2I=2.3e-11*(TEMP/300)**0.24 
	KR2=K20/K2I 
	FC2=0.6 
	NC2=0.75-1.27*(numpy.log10(FC2)) 
	F2=10**(numpy.log10(FC2)/(1+(numpy.log10(KR2)/NC2)**2)) 
	KMT02=(K20*K2I)*F2/(K20+K2I) 
	K30=3.6e-30*M*(TEMP/300)**-4.1 
	K3I=1.9e-12*(TEMP/300)**0.2 
	KR3=K30/K3I 
	FC3=0.35 
	NC3=0.75-1.27*(numpy.log10(FC3)) 
	F3=10**(numpy.log10(FC3)/(1+(numpy.log10(KR3)/NC3)**2)) 
	KMT03=(K30*K3I)*F3/(K30+K3I) 
	K40=1.3e-3*M*(TEMP/300)**-3.5*numpy.exp(-11000/TEMP) 
	K4I=9.7e+14*(TEMP/300)**0.1*numpy.exp(-11080/TEMP) 
	KR4=K40/K4I 
	FC4=0.35 
	NC4=0.75-1.27*(numpy.log10(FC4)) 
	F4=10**(numpy.log10(FC4)/(1+(numpy.log10(KR4)/NC4)**2)) 
	KMT04=(K40*K4I)*F4/(K40+K4I) 
	KMT05=1.44e-13*(1+(M/4.2e+19)) 
	KMT06=1+(1.40e-21*numpy.exp(2200/TEMP)*H2O) 
	K70=7.4e-31*M*(TEMP/300)**-2.4 
	K7I=3.3e-11*(TEMP/300)**-0.3 
	KR7=K70/K7I 
	FC7=0.81 
	NC7=0.75-1.27*(numpy.log10(FC7)) 
	F7=10**(numpy.log10(FC7)/(1+(numpy.log10(KR7)/NC7)**2)) 
	KMT07=(K70*K7I)*F7/(K70+K7I) 
	K80=3.2e-30*M*(TEMP/300)**-4.5 
	K8I=3.0e-11 
	KR8=K80/K8I 
	FC8=0.41 
	NC8=0.75-1.27*(numpy.log10(FC8)) 
	F8=10**(numpy.log10(FC8)/(1+(numpy.log10(KR8)/NC8)**2)) 
	KMT08=(K80*K8I)*F8/(K80+K8I) 
	K90=1.4e-31*M*(TEMP/300)**-3.1 
	K9I=4.0e-12 
	KR9=K90/K9I 
	FC9=0.4 
	NC9=0.75-1.27*(numpy.log10(FC9)) 
	F9=10**(numpy.log10(FC9)/(1+(numpy.log10(KR9)/NC9)**2)) 
	KMT09=(K90*K9I)*F9/(K90+K9I) 
	K100=4.10e-05*M*numpy.exp(-10650/TEMP) 
	K10I=6.0e+15*numpy.exp(-11170/TEMP) 
	KR10=K100/K10I 
	FC10=0.4 
	NC10=0.75-1.27*(numpy.log10(FC10)) 
	F10=10**(numpy.log10(FC10)/(1+(numpy.log10(KR10)/NC10)**2)) 
	KMT10=(K100*K10I)*F10/(K100+K10I) 
	K1=2.40e-14*numpy.exp(460/TEMP) 
	K3=6.50e-34*numpy.exp(1335/TEMP) 
	K4=2.70e-17*numpy.exp(2199/TEMP) 
	K2=(K3*M)/(1+(K3*M/K4)) 
	KMT11=K1+K2 
	K120=2.5e-31*M*(TEMP/300)**-2.6 
	K12I=2.0e-12 
	KR12=K120/K12I 
	FC12=0.53 
	NC12=0.75-1.27*(numpy.log10(FC12)) 
	F12=10**(numpy.log10(FC12)/(1.0+(numpy.log10(KR12)/NC12)**2)) 
	KMT12=(K120*K12I*F12)/(K120+K12I) 
	K130=2.5e-30*M*(TEMP/300)**-5.5 
	K13I=1.8e-11 
	KR13=K130/K13I 
	FC13=0.36 
	NC13=0.75-1.27*(numpy.log10(FC13)) 
	F13=10**(numpy.log10(FC13)/(1+(numpy.log10(KR13)/NC13)**2)) 
	KMT13=(K130*K13I)*F13/(K130+K13I) 
	K140=9.0e-5*numpy.exp(-9690/TEMP)*M 
	K14I=1.1e+16*numpy.exp(-10560/TEMP) 
	KR14=K140/K14I 
	FC14=0.36 
	NC14=0.75-1.27*(numpy.log10(FC14)) 
	F14=10**(numpy.log10(FC14)/(1+(numpy.log10(KR14)/NC14)**2)) 
	KMT14=(K140*K14I)*F14/(K140+K14I) 
	K150=8.6e-29*M*(TEMP/300)**-3.1 
	K15I=9.0e-12*(TEMP/300)**-0.85 
	KR15=K150/K15I 
	FC15=0.48 
	NC15=0.75-1.27*(numpy.log10(FC15)) 
	F15=10**(numpy.log10(FC15)/(1+(numpy.log10(KR15)/NC15)**2)) 
	KMT15=(K150*K15I)*F15/(K150+K15I) 
	K160=8e-27*M*(TEMP/300)**-3.5 
	K16I=3.0e-11*(TEMP/300)**-1 
	KR16=K160/K16I 
	FC16=0.5 
	NC16=0.75-1.27*(numpy.log10(FC16)) 
	F16=10**(numpy.log10(FC16)/(1+(numpy.log10(KR16)/NC16)**2)) 
	KMT16=(K160*K16I)*F16/(K160+K16I) 
	K170=5.0e-30*M*(TEMP/300)**-1.5 
	K17I=1.0e-12 
	KR17=K170/K17I 
	FC17=0.17*numpy.exp(-51/TEMP)+numpy.exp(-TEMP/204) 
	NC17=0.75-1.27*(numpy.log10(FC17)) 
	F17=10**(numpy.log10(FC17)/(1.0+(numpy.log10(KR17)/NC17)**2)) 
	KMT17=(K170*K17I*F17)/(K170+K17I) 
	KMT18=9.5e-39*O2*numpy.exp(5270/TEMP)/(1+7.5e-29*O2*numpy.exp(5610/TEMP)) 
	KPPN0=1.7e-03*numpy.exp(-11280/TEMP)*M 
	KPPNI=8.3e+16*numpy.exp(-13940/TEMP) 
	KRPPN=KPPN0/KPPNI 
	FCPPN=0.36 
	NCPPN=0.75-1.27*(numpy.log10(FCPPN)) 
	FPPN=10**(numpy.log10(FCPPN)/(1+(numpy.log10(KRPPN)/NCPPN)**2)) 
	KBPPN=(KPPN0*KPPNI)*FCPPN/(KPPN0+KPPNI) 

	# estimate and append photolysis rates
	J = photolysisRates.PhotolysisCalculation(time, lat, lon, TEMP, act_flux_path, DayOfYear, photo_par_file, Jlen, tf)

	if lightm == 0:
		J = [0]*len(J)
	rate_values = numpy.zeros((84))
	
	# reac_coef has been formatted so that python can recognize it
	# gas-phase reactions
	rate_values[0] = 5.6e-34*N2*(TEMP/300)**-2.6*O2
	rate_values[1] = 6.0e-34*O2*(TEMP/300)**-2.6*O2
	rate_values[2] = 8.0e-12*numpy.exp(-2060/TEMP)
	rate_values[3] = KMT01
	rate_values[4] = 5.5e-12*numpy.exp(188/TEMP)
	rate_values[5] = KMT02
	rate_values[6] = 3.2e-11*numpy.exp(67/TEMP)*O2
	rate_values[7] = 2.0e-11*numpy.exp(130/TEMP)*N2
	rate_values[8] = 1.4e-12*numpy.exp(-1310/TEMP)
	rate_values[9] = 1.4e-13*numpy.exp(-2470/TEMP)
	rate_values[10] = 3.3e-39*numpy.exp(530/TEMP)*O2
	rate_values[11] = 1.8e-11*numpy.exp(110/TEMP)
	rate_values[12] = 4.50e-14*numpy.exp(-1260/TEMP)
	rate_values[13] = KMT03
	rate_values[14] = 2.14e-10*H2O
	rate_values[15] = 1.70e-12*numpy.exp(-940/TEMP)
	rate_values[16] = 7.7e-12*numpy.exp(-2100/TEMP)
	rate_values[17] = KMT05
	rate_values[18] = 2.9e-12*numpy.exp(-160/TEMP)
	rate_values[19] = 2.03e-16*(TEMP/300)**4.57*numpy.exp(693/TEMP)
	rate_values[20] = 4.8e-11*numpy.exp(250/TEMP)
	rate_values[21] = 2.20e-13*KMT06*numpy.exp(600/TEMP)
	rate_values[22] = 1.90e-33*M*KMT06*numpy.exp(980/TEMP)
	rate_values[23] = KMT07
	rate_values[24] = KMT08
	rate_values[25] = 2.0e-11
	rate_values[26] = 3.45e-12*numpy.exp(270/TEMP)
	rate_values[27] = KMT09
	rate_values[28] = 3.2e-13*numpy.exp(690/TEMP)*1.0
	rate_values[29] = 4.0e-12
	rate_values[30] = 2.5e-12*numpy.exp(260/TEMP)
	rate_values[31] = KMT11
	rate_values[32] = 4.0e-32*numpy.exp(-1000/TEMP)*M
	rate_values[33] = KMT12
	rate_values[34] = 1.3e-12*numpy.exp(-330/TEMP)*O2
	rate_values[35] = 6.00e-06
	rate_values[36] = 4.00e-04
	rate_values[37] = 1.20e-15*H2O
	rate_values[38] = J[1]
	rate_values[39] = J[2]
	rate_values[40] = J[3]
	rate_values[41] = J[4]
	rate_values[42] = J[5]
	rate_values[43] = J[6]
	rate_values[44] = J[7]
	rate_values[45] = J[8]
	rate_values[46] = KMT04
	rate_values[47] = KMT10
	rate_values[48] = 1.22e-11*0.90
	rate_values[49] = 1.22e-11*0.10
	rate_values[50] = 2.80e-15*numpy.exp(-770/TEMP)*0.640
	rate_values[51] = 2.80e-15*numpy.exp(-770/TEMP)*0.100
	rate_values[52] = 2.80e-15*numpy.exp(-770/TEMP)*0.270
	rate_values[53] = 4.28e-11*numpy.exp(401/TEMP)*0.408
	rate_values[54] = 4.28e-11*numpy.exp(401/TEMP)*0.222
	rate_values[55] = 4.28e-11*numpy.exp(401/TEMP)*0.370
	rate_values[56] = KRO2HO2*0.914
	rate_values[57] = KRO2NO
	rate_values[58] = KRO2NO3
	rate_values[59] = 9.20e-14*RO2*0.3
	rate_values[60] = 9.20e-14*RO2*0.7
	rate_values[61] = KDEC*0.5
	rate_values[62] = KDEC*0.5
	rate_values[63] = KDEC*0.5
	rate_values[64] = KDEC*0.5
	rate_values[65] = KRO2HO2*0.914
	rate_values[66] = KRO2NO*0.228
	rate_values[67] = KRO2NO*0.772
	rate_values[68] = KRO2NO3
	rate_values[69] = 9.20e-14*RO2*0.7
	rate_values[70] = 9.20e-14*RO2*0.3
	rate_values[71] = KRO2HO2*0.914
	rate_values[72] = KRO2NO*0.228
	rate_values[73] = KRO2NO*0.772
	rate_values[74] = KRO2NO3
	rate_values[75] = 8.80e-13*RO2*0.2
	rate_values[76] = 8.80e-13*RO2*0.2
	rate_values[77] = 8.80e-13*RO2*0.6
	rate_values[78] = KRO2HO2*0.914
	rate_values[79] = KRO2NO*0.228
	rate_values[80] = KRO2NO*0.772
	rate_values[81] = KRO2NO3
	rate_values[82] = 9.20e-14*RO2*0.7
	rate_values[83] = 9.20e-14*RO2*0.3
	
	# aqueous-phase reactions
	
	return(rate_values)
