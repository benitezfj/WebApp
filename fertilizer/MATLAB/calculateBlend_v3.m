function calculateBlend_v3(my_n, my_p, my_k, my_db)  

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

    The function returns a string specifying the best fertilization blend 
    for obtaining the desired nutrient values. The output has the following 
    format:

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

    %}
    
    tic; %Start measuring execution time

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

    switch i
        %Case 1 - Jacobi method found the best solution
        %Case 2 - Gauss-Seidel method found the best solution
        
        case 1 
            
            F = C(i_J(1), :); %Fertilizers used to obtain the best blend
            
            for j = 1:length(x_J(:,i_J(1)))
                if x_J(j,i_J(1)) ~= 0
                    fprintf('\n%f kg/ha of ', x_J(j,i_J(1)));
                    fprintf(' %d-', A(:, F(j))*100);
                end
            end
            
            fprintf('\nDifference from desired blend: ');
            fprintf('(%f) - ', diff_vec_J(i_J(1), :));

        case 2
            
            F = C(i_GS(1), :); %Fertilizers used to obtain the best blend

            for j = 1:length(x_GS(:, i_GS(1)))
                if x_GS(j, i_GS(1)) ~= 0
                    fprintf('\n%f kg/ha of', x_GS(j, i_GS(1)));
                    fprintf(' %d-', A(:, F(j))*100);
                end
                
            end

            %frpintf('\nDifference from desired blend: ');
            fprintf('(%f) - ', diff_vec_GS(i_GS(1), :));

    end
    
    fprintf('\n');
    toc; %End measuring execution time
end