'''
Función de conversión K a K2O
20/01/2023
'''
#Dada la cantidad de K, devuelve la cantidad equivalente de K2O (en las mismas unidades)
def k_k2o (k):
    return k * 1.2046


'''
Función de conversión P a P2O5
24/01/2023
'''
#Dada la cantidad de P, devuelve la cantidad equivalente de P2O5 (en las misma unidades)
def p_p2o5 (p):
    return p * 2.2914


'''
Función de conversión K2O a K
20/01/2023
'''
#Dada la cantidad de K2O, devuelve la cantidad equivalente de K (en las mismas unidades)
def k2o_k (k2o):
    return round((1/1.2046) * k2o, 4) #1/0.8302

'''
Función de conversión P2O5 a P
20/01/2023
'''
#Dada la cantidad de P2O5, devuelve la cantidad equivalente de P (en las mismas unidades)
def p2o5_p (p2o5):
    return round((1/2.2914) * p2o5, 4) #1/0.4364

# from k_k2o import k_k2o
# from p_p2o5 import p_p2o5
# First one, the spinachFertilizer results are arguments of fertilizerCalculator
def spinachFertilizer(rend): 
    '''
        This function returns a vector with the necessary micro and macro
        nutrients for spinach for some specific expected productivity.

        The function gets as input the expected productivity in t/ha

        The function returns a vector with 11 different nutrients.
        0 - N kg/ha
        1 - P2O5 kg/ha
        2 - K2O kg/ha
        3 - Ca kg/ha
        4 - Mg kg/ha
        5 - S kg/ha
        6 - Cu kg/ha
        7 - Mn kg/ha
        8 - Fe kg/ha
        9 - Zn kg/ha
        10 - B kg/ha
    
        The conversion functions p_p2o5.py and k_k2o.py are needed for the
        execution of the program.
    '''
    
    #Compute tha bases coefficients
    tha_baseHumeda = 22.6 #t/ha wetted base
    tha_baseSeca = 1.74 #t/ha dry base
    relBases = tha_baseSeca / tha_baseHumeda #Ratio of the bases
    coef = rend * relBases
    
    #Obtain the nutrients needed
    result = []
    result.append(37 + 0.00004 * coef) #N
    result.append(3.1 + 0.048 * coef) #P
    result[1] = p_p2o5(result[1]) #Convert from P to P2O5
    result.append(91.3 - 6.34 * coef) #K
    result[2] = k_k2o(result[2]) #Convert from K to K2O
    result.append(13.34 - 0.889 * coef) #Ca
    result.append(11.88 + 0.77 * coef) #Mg
    result.append(3.03 - 0.082 * coef) #S
    result.append((29.8 - 5.99 * coef) / 1000) #Cu
    result.append((269.2 - 34.82 * coef) / 1000) #Mn
    result.append((715.1 - 99.12 * coef) / 1000) #Fe
    result.append((103.34 - 4.98 * coef) / 1000) #Zn
    result.append((77.5 - 5.13 * coef) / 1000) #B
    
    #Multiply the result by the coefficient
    for i in range(0, len(result)):
        result[i] = result[i] * coef
    
    # Return only Nitrogen, P2O5, K2O
    # return result[0], result[2], result[4] 
    return result

# spinachFertilizer(production_expected)[0:3]