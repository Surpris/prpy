# -*- coding: utf-8 -*-

"""
Constraints to density map
"""

import numpy as np

RHO_CONSTS = ['real', 'positive', 'absolute', 'complex']

def projection_er(rho, C_s, rho_const, *args, **kwargs):
    """ Error reduction algorithm.
    < Input parameters >
        rho: density map
        C_s: constraint region where the deisity is expected to be non-zero.
        rho_const: type of constraint
            "real"     : real and positive
            "positive" : complex with positive real part and positive imaginary part
            "absolute" : absolute value
            "complex"  : complex
    < Output >
        Constrained density map
    """
    if rho_const=='real': # real positivity
        return np.real(rho)*(np.real(rho) >= 0)*C_s
    elif rho_const=='positive': # complex positivity
        return (np.real(rho)*(np.real(rho) >= 0)+1j*np.imag(rho)*(np.imag(rho) >= 0))*C_s
    elif rho_const=='absolute': # absolute
        return np.abs(rho)*C_s
    else: # complex
        return rho*C_s

def projection_hio(rho, C_s, rho_const, rho_before, beta, *args, **kwargs):
    """
    Hybrid input-output algorithm.
    < Input parameters >
        rho: density map
        C_s: constraint region where the deisity is expected to be non-zero.
        rho_const: type of constraint
            "real"     : real and positive
            "positive" : complex with positive real part and positive imaginary part
            "absolute" : absolute value
            "complex"  : complex
        rho_before: density map at the previous step
        beta: coefficient of HIO
    < Output >
        Constrained density map
    """
    if rho_const == 'real': # real positivity
        C_s_0 = (np.real(rho) >= 0)*C_s
        return np.real(rho)*C_s_0 + (np.real(rho_before) - beta*np.real(rho))*(1-C_s_0)
    elif rho_const == 'positive': # complex positivity
        C_s_0 = (np.real(rho) >= 0)*(np.imag(rho) >= 0)*C_s
        return rho*C_s_0 + (rho_before - beta*rho)*(1-C_s_0)
    elif rho_const == 'absolute':
        return np.abs(rho)*C_s + (np.abs(rho_before) - beta*np.abs(rho))*(1-C_s)
    else: # complex
        return rho*C_s + (rho_before - beta*rho)*(1-C_s)

def projection_hpr(rho, C_s, rho_const, rho_before, beta, *args, **kwargs):
    """ Hybrid projection-reflection algorithm.
    < Input parameters >
        rho: density map
        C_s: constraint region where the deisity is expected to be non-zero.
        rho_const: type of constraint
            "real"     : real and positive
            "positive" : complex with positive real part and positive imaginary part
            "absolute" : absolute value
            "complex"  : complex
        rho_before: density map at the previous step
        beta: coefficient of HPR
    < Output >
        Constrained density map
    """
    if rho_const == 'real': # real positivity
        C_s_0 = (np.real(rho) >= 0)*(np.real(rho)>= 1./(1+beta)*np.real(rho_before))*C_s
        return np.real(rho)*C_s_0 + (np.real(rho_before) - beta*np.real(rho))*(1-C_s_0)
    elif rho_const=='positive': # complex positivity
        C_s_0 = (np.real(rho) >= 0)*(np.imag(rho) >= 0)*C_s
        C_s_0 *= (np.real(rho)>= 1./(1+beta)*np.real(rho_before))*(np.imag(rho)>= 1./(1+beta)*np.imag(rho_before))
        return rho*C_s_0 + (rho_before - beta*rho)*(1-C_s_0)
    elif rho_const == 'absolute':
        C_s_0 = (np.abs(rho) >= 0) * (np.abs(rho)>= 1./(1+beta) * np.abs(rho_before)) * C_s
        return np.abs(rho)*C_s_0 + (np.abs(rho_before) - beta*np.abs(rho))*(1-C_s_0)
    else: # complex
        return rho*C_s + (rho_before - beta*rho)*(1-C_s)
