import matlab.engine

def fertilizerCalculator(n, p, k, db):
    '''
        This function calls the function calculateBlend from Matlab.
        
        We want an over-determined or well-determined system, so the number of 
        fertilizers we are going to use for the belnd is going to be less than or 
        equal to the total number of nutrients in the ferilizers.

        The function receives the following input values:
            1. my_n: desired quantity of N in kg/ha
            2. my_p: desired quantity of P2O5 in kg/ha
            3. my_k: desired quantity of K2O in kg/ha
            4. my_db: commercial fertilizer database code
                    1 -> Fertiberia (Spain)
                    2 -> Bunge (Paraguay)

        The function returns two matrices. The first one specifies the best 
        fertilization blend for obtaining the desired nutrient values. The 
        second one indicates the difference between the output blend and the 
        ideal fertilization blend. The output can combine from 0 to 3 different 
        fertilizers. Thus, the output of the first matrix can be in any of the 
        following formats:
            - 0 fertilizers: []
            - 1 fertilizer: [[Q1, N1, P1, K1]]
            - 2 fertilizers: [[Q1, N1, P1, K1], [Q2, N2, P2, K2]]
            - 3 fertilizers: [[Q1, N1, P1, K1], [Q2, N2, P2, K2], [Q3, N3, P3, K3]]
        
        The output format of the second matrix is:
            [[Nd, Pd, Kd]]
        
        Where Qn is the quantity of the fertilizer Nn, Pn and Kn are the N-P- K 
        values of the fertilizers, and Nd, Pd and Kd are the N-P-K differences
        between the desired blend and the obtained blend.
    '''

    print('Start matlab engine API')
    #Start matlab engine API
    eng = matlab.engine.start_matlab()

    #Call calculateBlend_v3 Matlab function
    fert, diff = eng.calculateBlend(n, p, k, db, nargout=2)
    print('End matlab engine API')
    return fert, diff

#fertilizerCalculator_v2(n=20.0, p=15.0, k=30.0, db=2)