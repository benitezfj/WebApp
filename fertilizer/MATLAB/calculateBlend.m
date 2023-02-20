function [result, diff] = calculateBlend_v4(my_n, my_p, my_k, my_db)  

    %Calculates optimal blend of fertilizers

    %{
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
        - 1 fertilizer: [Q1 N1 P1 K1]
        - 2 fertilizers: [Q1 N1 P1 K1; Q2 N2 P2 K2]
        - 3 fertilizers: [Q1 N1 P1 K1; Q2 N2 P2 K2; Q3 N3 P3 K3]
    
    The output format of the second matrix is:
        [Nd Pd Kd]
    
    Where Qn is the quantity of the fertilizer Nn, Pn and Kn are the N-P- K 
    values of the fertilizers, and Nd, Pd and Kd are the N-P-K differences
    between the desired blend and the obtained blend.

    %}

    %% Obtain fertilizer types and desired quantity
    
    %Import fertilizers
    %Case my_db = 1 -> Import fertilizers from Fertiberia
    %Case my_db = 2 -> Import fertilizers form Bunge
    A = importFertilizers_v1(my_db);
    
    n = size(A, 2); % n = number of fertilizers
    range = 1:n; %Range from 1 to number of fertilizers
    k = size(A, 1); %Number of nutrients in fertilizer
    
    %Quantity for each of the nutrients (kg/ha)
    b = [my_n; my_p; my_k];

    %% Use Jacobi and Gauss-Seidel methods to find the best blend
    
    A = A .*(0.01); %We need to divide by 100 because NPK values come as a percentage.
    
    C = nchoosek(range, k); %Matrix with all the possible combinations of the fertilizers
    s = size(C);
    
    x_J = zeros(k, s(1)); %Solution found by Jacobi method for each of the possible combinations
    x_GS = zeros(k, s(1)); %Solution found by Gauss-Seidel method for each of the possible combinations
    
    diff_vec_J = zeros(s(1), k); %Difference between the desired solution and the one found using Jacobi method
    diff_vec_GS = zeros(s(1), k); %Difference between the desired solution and the one found using Gauss-Seidel method

    diff_sum_J = zeros(s(1), 1); %Average difference between the desired solution and the one found using Jacobi method
    diff_sum_GS = zeros(s(1),1); %Average difference between the desired solution and the one found using Gauss-Seidel method
    
    A2 = zeros(k); %Matrix that contains the data about the fertilizers in a combination
    
    %Iterate and use Jacobi and Gauss-Seidel to find the best solution
    for i = 1:s(1)
        for j = 1:k
            A2(:,j) = A(:,C(i,j));
        end
        
        x = zeros(k, 1);
        x_J(:,i) = jacobi_v2(A2, b, x); %kg per hectare for each of the fertilizers
        diff_J = abs(b - (A2 * x_J(:,i))); %Difference between the needed quantity and the final one

        x_GS(:,i) = gauss_seidel_v2(A2, b, x); %kg per hectare for each of the fertilizer
        diff_GS = abs(b - (A2 * x_GS(:,i))); %Difference between the needed quantity and the final one

        %Obatain the difference and mean difference between all the 
        %nutrients in each combination in the different methods
        diff_vec_J(i,:) = diff_J';
        diff_vec_GS(i,:) = diff_GS';
        
        diff_sum_J(i) = sum(diff_J) / k;
        diff_sum_GS(i) = sum(diff_GS) / k;


    end
    
    %Find the combination that has the smallest difference with the desired
    %solution for each of the methods and then find the best overall
    %solution
    [~, i_J] = min(diff_sum_J);
    [~, i_GS] = min(diff_sum_GS);
    [~, i] = min([diff_sum_J(i_J), diff_sum_GS(i_GS)]);
    
    
    %% Print the best solution

    result = [];
    k = 1;
    switch i
        %Case 1 - Jacobi method found the best solution
        %Case 2 - Gauss-Seidel method found the best solution
        
        case 1 
            
            F = C(i_J(1), :); %Fertilizers used to obtain the best blend
            
            for j = 1:length(x_J(:,i_J(1)))
                if x_J(j,i_J(1)) ~= 0
                    q = x_J(j, i_J(1)); %Quantity of fertilizer
                    m = A(:, F(j))*100; %N-P-K from fertilizer
                    result(:, k) = vertcat(q, m);
                    k = k + 1;
                end
            end

            result = result.'; %Transpose result matrix

            %Difference between the desired blend and the one obtained
            diff = diff_vec_GS(i_GS(1), :);
           

        case 2
            
            F = C(i_GS(1), :); %Fertilizers used to obtain the best blend

            for j = 1:length(x_GS(:, i_GS(1)))
                if x_GS(j, i_GS(1)) ~= 0
                    q = x_GS(j, i_GS(1)); %Quantity of fertilizer
                    m = A(:, F(j))*100; %N-P-K from fertilizer
                    result(:, k) = vertcat(q, m);
                    k = k + 1;
                end
                
            end
            
            result = result.'; %Transpose result matrix

            %Difference between the desired blend and the one obtained
            diff = diff_vec_GS(i_GS(1), :);

    end
end