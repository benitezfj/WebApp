function result = spinachFertilizer(rend)
    %% Description of the function
    %{
        This function returns a vector with the necessary micro and macro
        nutrients for spinach for some specific expected productivity.

        The function gets as input the expected productivity in t/ha

        The function returns a vector with 11 different nutrients.
        1 - N kg/ha
        2 - P2O5 kg/ha
        3 - K2O kg/ha
        4 - Ca kg/ha
        5 - Mg kg/ha
        6 - S kg/ha
        7 - Cu kg/ha
        8 - Mn kg/ha
        9 - Fe kg/ha
        10 - Zn kg/ha
        11 - B kg/ha
    
        The conversion functions p_p2o5.m and k_k2o.m are needed for the
        execution of the program.

        Reference:
            sanzar agro / 4 funcion de fertilizacion / función fertilización espinacas / spinach fertiliser function.xlsx
    %}
    
    %% Compute the bases coefficients
    tha_baseHumeda = 22.6; %t/ha wetted base
    tha_baseSeca = 1.74; %t/ha dry base
    relBases = tha_baseSeca / tha_baseHumeda; %Ratio of the bases
    coef = rend * relBases;
    
    %% Obtain the nutrients needed
    result = zeros(1, 11); %Initialize the vector with zeros 1 x 11
    result(1) = 37 + 0.00004 * coef; %N
    result(2) = 3.1 + 0.048 * coef; %P
    result(2) = p_p2o5(result(2)); %Convert from P to P2O5
    result(3) = 91.3 - 6.34 * coef; %K
    result(3) = k_k2o(result(3)); %Convert from K to K2O
    result(4) = 13.34 - 0.889 * coef; %Ca
    result(5) = 11.88 + 0.77 * coef; %Mg
    result(6) = 3.03 - 0.082 * coef; %S
    result(7) = (29.8 - 5.99 * coef) / 1000; %Cu
    result(8) = (269.2 - 34.82 * coef) / 1000; %Mn
    result(9) = (715.1 - 99.12 * coef) / 1000; %Fe
    result(10) = (103.34 - 4.98 * coef) / 1000; %Zn
    result(11) = (77.5 - 5.13 * coef) / 1000; %B
    
    result = result * coef; %Multiply the result by the coefficient
end