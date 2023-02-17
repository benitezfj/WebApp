import matlab.engine

def fertilizerCalculator(n, p, k, db):
    '''
        This function calls the function calculateBlend_v3 from Matlab.
        
        The function receives the following input values:
            1. n - > Desired quantity of N in kg/ha (double type)
            2. p -> Desired quantity of P2O5 in kg/ha (double type)
            3. k -> Desired quantity of K2O in kg/ha (double type)
            4. db -> Commercial fertilizer database code
                1 -> Fertiberia (Spain)
                2 -> Bunge (Paraguay)

        The function returns a string containing specifying the best
        fertilization blend for obtaining the desired nutrient values. The 
        output has the following format:

            x kg/ha of N- P- K-

        The output can combine from 0 to 3 different fertilizers.

        The program also prints on screen the resulted blend, the difference
        between the output blend and the ideal fertilization blend, and the
        elapsed time:

            x kg/ha of N1- P1- K1-
            y kg/ha of N2- P2- K2-
            z kg/ha of N3- P3- K3-
            Difference from desired blend: (N4) - (P4) - (K4) -
            Elapsed time is s seconds.
    '''

    #Start matlab engine API
    print('Start matlab engine API')
    eng = matlab.engine.start_matlab()

    #Call calculateBlend_v3 Matlab function
    eng.calculateBlend_v3(n, p, k, db, nargout=0)
    
# fertilizerCalculator(n=20.0, p=15.0, k=30.0, db=1)