function x = jacobi_v2 (A, b, x)
    %Jacobi method for nonnegative solutions
    %{
        https://es.mathworks.com/matlabcentral/fileexchange/63167-gauss-seidel-method-jacobi-method
    %}

    % Solution of the system Ax=b using Jacobi Method
    
    n=size(x,1);
    normVal=Inf; %Initial value of the norm
    % Tolerence for method
    %tol=0.9; 
    tol=1e-5; 
    itr=0;
    num_itr = 9e3;
    %Iterate while the tolerance constraint is not satisfied
    
    while (normVal > tol) && (num_itr > itr)
        x_old = x;
        
        for i = 1:n
            sigma = 0;
            for j = 1:n
                if j ~= i
                    sigma = sigma + A(i,j) * x(j);
                end
            end
            x(i) = (1 / A(i,i)) * (b(i) - sigma);
            
            %The solution needs to be nonnegative
            if x(i) < 0
                x(i) = 0;
            end
        end
        itr = itr + 1;
        
        %If the system converges, stop iterating
        if sum(x_old - x) == 0
            normVal = 0;
        else
            normVal = norm(b - (A*x), 2);
        end

    end
end