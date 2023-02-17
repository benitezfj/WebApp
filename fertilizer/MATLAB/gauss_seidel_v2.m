function x = gauss_seidel_v2(A, b, x) 
    %Gauss-Seidel method for nonnegative solutions
    %{
        https://es.mathworks.com/matlabcentral/fileexchange/63167-gauss-seidel-method-jacobi-method
    %}

    %Solution of the system Ax=b using Gauss Seidel Method
    
    n = size(x,1);
    normVal = Inf; 
    tol = 1e-5;
    itr = 0;
    num_itr = 9e3;
 
    while (num_itr > itr) && (normVal > tol)
        x_old = x;

        for i = 1:n

            sigma = 0;

            for j = 1 : i-1
                    sigma = sigma + A(i,j) * x(j);
            end

            for j = i + 1:n
                    sigma = sigma + A(i,j) * x_old(j);
            end

            x(i) = (1 / A(i,i))*(b(i) - sigma);
            
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