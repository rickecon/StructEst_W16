'''
------------------------------------------------------------------------
This is Bobae's PS2 for MACS 40000: Structural Estimation
------------------------------------------------------------------------
'''
# import pacakges
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import scipy as sp
import scipy.stats as sts
import scipy.special as spc
import scipy.optimize as opt
import matplotlib.pyplot as plt

# import module
import module as mod

# read data
data = pd.Series(np.loadtxt('clms.txt'))
# print(data[data <= 800])
# print(data)

'''
------------------------------------------------------------------------------
1.(a) Calculate and report the mean, median, maximum, minimum,
and standard deviation of monthly health expenditures for these data.
Plot two histograms of the data in which the y-axis gives the percent
of observations in the particular bin of health expenditures and the x-axis
gives the value of monthly health expenditures.
------------------------------------------------------------------------------
'''
print('The answers for the 1.(a) are as follows: ')
if False:
    mean = np.mean(data)
    median = np.median(data)
    maximum = np.max(data)
    minimum = np.min(data)
    std = np.std(data)
    print('The mean of the monthly health expenditures data is: ', mean[0])
    print('The median of the monthly health expenditures data is: ', median)
    print('The maximum of the monthly health expenditures data is: ', maximum[0])
    print('The minimum of the monthly health expenditures data is: ', minimum[0])
    print('The standard deviation of the monthly health expenditures data is: ', std[0])

if False:
    num_bins1 = 1000
    weights1 = (1 / data.shape[0]) * np.ones_like(data)
    n, bin_cuts, patches = plt.hist(data, num_bins1, weights = weights1)
    plt.title('Histogram of Fictitious Health Claims', fontsize = 15)
    plt.xlabel(r'Health claim amounts (USD)')
    plt.ylabel(r'Percent of observations in bin')
    plt.show()
    plt.close()

if False:
    data_cut = data[data <= 800]
    num_bins2 = 100
    weights2 = (1 / data_cut.shape[0]) * np.ones_like(data_cut) * (len(data_cut) / len(data))
    n, bin_cuts, patches = plt.hist(data_cut, num_bins2, weights = weights2)
    plt.title('Histogram of Fictitious Health Claims (=< 800)', fontsize = 15)
    plt.xlabel(r'Health claim amounts (USD)')
    plt.ylabel(r'Percent of observations in bin')
    plt.show()
    plt.close()

    print('Histogram Bins sum to: ', n.sum())

'''
------------------------------------------------------------------------------
1.(b) Using MLE, fit the gamma distribution to the individual observation
data. Report your estimated values for parameters, as well as
the value of the maximized log likelihood function. Plot the second
histogram from part (a) overlayed with a line representing the implied
histogram from your estimated gamma distribution.
------------------------------------------------------------------------------
'''
print('The answers for the 1.(b) (fitting the gamma distribution) are as follows: ')
# log likelihood value for the gamma distribution
def log_lik_ga(xvals, alpha, beta):
    '''
    --------------------------------------------------------------------
    Compute the log likelihood function for data xvals given gamma
    distribution parameters alpha and beta.
    --------------------------------------------------------------------
    INPUTS:
    xvals  = (N,) vector, values of the gamma distributed random variable
    alpha, beta = scalar > 0, parameters for the gamma distribution

    OTHER FUNCTIONS AND FILES CALLED BY THIS FUNCTION:
        mod.ga_pdf()

    OBJECTS CREATED WITHIN FUNCTION:
    pdf_vals    = (N,) vector, normal PDF values for mu and sigma
                  corresponding to xvals data
    ln_pdf_vals = (N,) vector, natural logarithm of normal PDF values
                  for mu and sigma corresponding to xvals data
    log_lik_val = scalar, value of the log likelihood function

    FILES CREATED BY THIS FUNCTION: None

    RETURNS: log_lik_val
    --------------------------------------------------------------------
    '''
    pdf_vals = mod.ga_pdf(xvals, alpha, beta)
    ln_pdf_vals = np.log(pdf_vals)
    log_lik_val = ln_pdf_vals.sum()

    return log_lik_val

# criterion function for the gamma distribution
def crit_ga(params, *args):
    '''
    --------------------------------------------------------------------
    This function computes the negative of the log likelihood function
    given parameters and data. This is the minimization problem version
    of the maximum likelihood optimization problem
    --------------------------------------------------------------------
    INPUTS:
    params = (2,) vector, ([alpha, beta])
    args   = length 1 tuple, (xvals)

    OTHER FUNCTIONS AND FILES CALLED BY THIS FUNCTION:
        log_lik_income()

    OBJECTS CREATED WITHIN FUNCTION:
    log_lik_val = scalar, value of the log likelihood function
    neg_log_lik_val = scalar, negative of log_lik_val

    FILES CREATED BY THIS FUNCTION: None

    RETURNS: neg_log_lik_val
    --------------------------------------------------------------------
    '''
    alpha, beta = params
    xvals = args
    log_lik_val = log_lik_ga(xvals, alpha, beta)
    neg_log_lik_val = -log_lik_val

    return neg_log_lik_val

ga_beta_0 = data.var() / data.mean()
ga_alpha_0 = data.mean() / ga_beta_0
ga_params_0 = np.array([ga_alpha_0, ga_beta_0])
ga_mle_args = (data)
ga_results = opt.minimize(crit_ga, ga_params_0, args=(ga_mle_args), bounds = ((0, None), (0, None)))
ga_alpha_MLE, ga_beta_MLE = ga_results.x

if False:
    print('GA alpha_MLE = ', ga_alpha_MLE, 'GA beta_MLE = ', ga_beta_MLE)
    print('the value of the likelihood function = ', -1 * ga_results.fun)
    print('VCV = ', ga_results.hess_inv.todense())

dist_pts = np.linspace(0, 800, 800)
data_cut = data[data <= 800]
num_bins = 800
weights = (1 / data_cut.shape[0]) * np.ones_like(data_cut) * (len(data_cut) / len(data))

if False:
    n, bin_cuts, patches = plt.hist(data_cut, num_bins, weights = weights)
    plt.plot(dist_pts, mod.ga_pdf(dist_pts, ga_alpha_MLE, ga_beta_MLE),
        linewidth=2, color='r', label='GA MLE')
    plt.title('Histogram of Fictitious Health Claims (=< 800)', fontsize = 15)
    plt.xlabel(r'Health claim amounts (USD)')
    plt.ylabel(r'Percent of observations in bin')
    plt.show()
    plt.close()


'''
------------------------------------------------------------------------------
1.(c) Using MLE, fit the generalized gamma distribution to the individual
observation data. Use your estimates for alpha and beta from part(b),
as well as m = 1, as your initial guess. Report your estimated
values for parameters, as well as the value of the maximized log likelihood
function. Plot the second histogram from part (a) overlayed with a
line representing the implied histogram from your estimated generalized
gamma distribution.
------------------------------------------------------------------------------
'''
print('The answers for the 1.(c) (fitting the generalized gamma distribution) are as follows: ')
# log likelihood value for the generalized gamma distribution
def log_lik_gg(xvals, alpha, beta, mm):
    '''
    --------------------------------------------------------------------
    Compute the log likelihood function for data xvals given generalized gamma
    distribution parameters alpha and beta.
    --------------------------------------------------------------------
    INPUTS:
    xvals  = (N,) vector, values of the gamma distributed random variable
    alpha, beta, mm  = scalar > 0, parameters for the generalized gamma distribution

    OTHER FUNCTIONS AND FILES CALLED BY THIS FUNCTION:
        mod.ga_pdf()

    OBJECTS CREATED WITHIN FUNCTION:
    pdf_vals    = (N,) vector, normal PDF values for mu and sigma
                  corresponding to xvals data
    ln_pdf_vals = (N,) vector, natural logarithm of normal PDF values
                  for mu and sigma corresponding to xvals data
    log_lik_val = scalar, value of the log likelihood function

    FILES CREATED BY THIS FUNCTION: None

    RETURNS: log_lik_val
    --------------------------------------------------------------------
    '''
    pdf_vals = mod.gg_pdf(xvals, alpha, beta, mm)
    ln_pdf_vals = np.log(pdf_vals)
    log_lik_val = ln_pdf_vals.sum()

    return log_lik_val

# criterion function for the generalized gamma distribution
def crit_gg(params, *args):
    '''
    --------------------------------------------------------------------
    This function computes the negative of the log likelihood function
    given parameters and data. This is the minimization problem version
    of the maximum likelihood optimization problem
    --------------------------------------------------------------------
    INPUTS:
    params = (3,) vector of parameters, ([alpha, beta, mm])
    args   = length 1 tuple, (xvals)

    OTHER FUNCTIONS AND FILES CALLED BY THIS FUNCTION:
        log_lik_gg()

    OBJECTS CREATED WITHIN FUNCTION:
    log_lik_val = scalar, value of the log likelihood function
    neg_log_lik_val = scalar, negative of log_lik_val

    FILES CREATED BY THIS FUNCTION: None

    RETURNS: neg_log_lik_val
    --------------------------------------------------------------------
    '''
    alpha, beta, mm = params
    xvals = args
    log_lik_val = log_lik_gg(xvals, alpha, beta, mm)
    neg_log_lik_val = -log_lik_val

    return neg_log_lik_val

gg_beta_0 = ga_beta_MLE
gg_alpha_0 = ga_alpha_MLE
gg_mm_0 = 1
gg_params_0 = np.array([gg_alpha_0, gg_beta_0, gg_mm_0])
gg_mle_args = (data)
gg_results = opt.minimize(crit_gg, gg_params_0, args=(gg_mle_args),
            bounds = ((0, None), (0, None), (0, None)))
gg_alpha_MLE, gg_beta_MLE, gg_mm_MLE = gg_results.x

if False:
    print('GG alpha_MLE = ', gg_alpha_MLE, 'GG beta_MLE = ', gg_beta_MLE,
        'GG mm_MLE = ', gg_mm_MLE)
    print('the value of the likelihood function = ', -1 * gg_results.fun)
    print('VCV = ', gg_results.hess_inv.todense())

if False:
    n, bin_cuts, patches = plt.hist(data_cut, num_bins, weights = weights)
    plt.plot(dist_pts, mod.gg_pdf(dist_pts, gg_alpha_MLE, gg_beta_MLE, gg_mm_MLE),
        linewidth=2, color='r', label='GA MLE')
    plt.title('Histogram of Fictitious Health Claims (=< 800)', fontsize = 15)
    plt.xlabel(r'Health claim amounts (USD)')
    plt.ylabel(r'Percent of observations in bin')
    plt.show()
    plt.close()


'''
------------------------------------------------------------------------------
1.(d) Using MLE, fit the generalized beta 2 distribution to the individual
observation data. Use your estimates for alpha, beta and m from part (c),
as well as q = 10,000, as your initial guess. Report your estimated values
for parameters, as well as the value of the maximized log likelihood function.
Plot the second histogram from part(a) overlayed with a line representing
the implied histogram from your estimated generalized beta 2 distribution.
------------------------------------------------------------------------------
'''
# log likelihood value for the generalized beta 2 distribution
print('The answers for the 1.(d) (fitting the generalized beta 2 distribution) are as follows: ')
def log_lik_gb2(xvals, aa, bb, pp, qq):
    '''
    --------------------------------------------------------------------
    Compute the log likelihood function for data xvals given gamma
    distribution parameters alpha and beta.
    --------------------------------------------------------------------
    INPUTS:
    xvals  = (N,) vector, values of the generalized beta 2 distributed random variable
    aa, bb, pp, qq = scalar > 0, parameters for the generalized beta 2 distribuion

    OTHER FUNCTIONS AND FILES CALLED BY THIS FUNCTION:
        mod.gb2_pdf()

    OBJECTS CREATED WITHIN FUNCTION:
    pdf_vals    = (N,) vector, normal PDF values for mu and sigma
                  corresponding to xvals data
    ln_pdf_vals = (N,) vector, natural logarithm of normal PDF values
                  for mu and sigma corresponding to xvals data
    log_lik_val = scalar, value of the log likelihood function

    FILES CREATED BY THIS FUNCTION: None

    RETURNS: log_lik_val
    --------------------------------------------------------------------
    '''
    pdf_vals = mod.gb2_pdf(xvals, aa, bb, pp, qq)
    ln_pdf_vals = np.log(pdf_vals)
    log_lik_val = ln_pdf_vals.sum()

    return log_lik_val

# criterion function for the generalized beta 2 distribution
def crit_gb2(params, *args):
    '''
    --------------------------------------------------------------------
    This function computes the negative of the log likelihood function
    given parameters and data. This is the minimization problem version
    of the maximum likelihood optimization problem
    --------------------------------------------------------------------
    INPUTS:
    params = (4,) vector of parameters, ([aa, bb, pp, qq])
    args   = length 2 tuple, (xvals, cutoff)

    OTHER FUNCTIONS AND FILES CALLED BY THIS FUNCTION:
        log_lik_gb2()

    OBJECTS CREATED WITHIN FUNCTION:
    log_lik_val = scalar, value of the log likelihood function
    neg_log_lik_val = scalar, negative of log_lik_val

    FILES CREATED BY THIS FUNCTION: None

    RETURNS: neg_log_lik_val
    --------------------------------------------------------------------
    '''
    aa, bb, pp, qq = params
    xvals = args
    log_lik_val = log_lik_gb2(xvals, aa, bb, pp, qq)
    neg_log_lik_val = -log_lik_val

    return neg_log_lik_val

gb2_qq_0 = 10000
gb2_aa_0 = gg_mm_MLE
gb2_bb_0 = gb2_qq_0**(1/gg_mm_MLE)*gg_beta_MLE
gb2_pp_0 = gg_alpha_MLE/gg_mm_MLE
gb2_params_0 = np.array([gb2_aa_0, gb2_bb_0, gb2_pp_0, gb2_qq_0])
gb2_mle_args = (data)
gb2_results = opt.minimize(crit_gb2, gb2_params_0, args=(gb2_mle_args),
            bounds = ((0, None), (0, None), (0, None), (0, None)))
gb2_aa_MLE, gb2_bb_MLE, gb2_pp_MLE, gb2_qq_MLE = gb2_results.x

if False:
    print('aa_MLE = ', gb2_aa_MLE, ' bb_MLE = ', gb2_bb_MLE,
            'pp_MLE = ', gb2_pp_MLE, 'qq_MLE = ', gb2_qq_MLE)
    print('the value of the likelihood function = ', -1 * gb2_results.fun)
    print('VCV = ', gb2_results.hess_inv.todense())

if False:
    n, bin_cuts, patches = plt.hist(data_cut, num_bins, weights = weights)
    plt.plot(dist_pts, mod.gb2_pdf(dist_pts, gb2_aa_MLE, gb2_bb_MLE, gb2_pp_MLE, gb2_qq_MLE),
        linewidth=2, color='r', label='GB2 MLE')
    plt.title('Histogram of Fictitious Health Claims (=< 800)', fontsize = 15)
    plt.xlabel(r'Health claim amounts (USD)')
    plt.ylabel(r'Percent of observations in bin')
    plt.show()
    plt.close()


'''
------------------------------------------------------------------------------
1.(e) Perform a likelihood ratio test for each of the estimated in parts
(b) and (c), respectively, against the GB2 specication in part (d).
Report the chi-square(4) values from the likelihood ratio test for
the estimated GA and the estimate GG.
------------------------------------------------------------------------------
'''
print('The answers for the 1.(e) (performing likelihood ratio test) are as follows: ')
log_lik_gb2_mle = log_lik_gb2(data, gb2_aa_MLE, gb2_bb_MLE, gb2_pp_MLE, gb2_qq_MLE)
log_lik_gg_mle = log_lik_gg(data, gg_alpha_MLE, gg_beta_MLE, gg_mm_MLE)
log_lik_ga_mle = log_lik_ga(data, ga_alpha_MLE, ga_beta_MLE)

LR_val_ga_gb2 = 2 * (log_lik_ga_mle - log_lik_gb2_mle)
LR_val_gg_gb2 = 2 * (log_lik_gg_mle - log_lik_gb2_mle)

ga_pval_h0 = 1.0 - sts.chi2.cdf(LR_val_ga_gb2, 4)
gg_pval_h0 = 1.0 - sts.chi2.cdf(LR_val_gg_gb2, 4)

if False:
    print('chi squared of H0: ga = gb2 with 4 df p-value = ', ga_pval_h0)
    print('chi squared of H0: gg = gb2 with 4 df p-value = ', gg_pval_h0)


'''
------------------------------------------------------------------------------
1.(f) Using the estimated GB2 distribution from part (d), how likely
am I to have a monthly health care claim of more than $1,000? How does
this amount change if I use the estimated GA distribution from part (b)?
------------------------------------------------------------------------------
'''
print('The answers for the 1.(f) are as follows: ')
gb2_1000 = 1 - sp.integrate.quad(lambda x: mod.gb2_pdf(x, gb2_aa_MLE, gb2_bb_MLE, gb2_pp_MLE, gb2_qq_MLE), 0, 1000)[0]
ga_1000 = 1 - sp.integrate.quad(lambda x: mod.ga_pdf(x, ga_alpha_MLE, ga_beta_MLE), 0, 1000)[0]

if True:
    print('Likelihood of having a monthly healthcare claim of more than $1000',
        'according to the Generalized Beta 2 Distribution: ', gb2_1000)
    print('Likelihood of having a monthly healthcare claim of more than $1000',
        'according to the Gamma Distribution: ', ga_1000)
