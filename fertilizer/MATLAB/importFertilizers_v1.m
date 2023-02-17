function matrix = importFertilizers_v1(n)
    %Import N-P-K values from commercial fertilizers in Excel workbook
    switch n
        case 1
            %Fertiberia - Spain
            matrix(1,:) = xlsread('FertilizersFertiberia_v1.xlsx','B:B');
            matrix(2,:) = xlsread('FertilizersFertiberia_v1.xlsx','F:F');
            matrix(3,:) = xlsread('FertilizersFertiberia_v1.xlsx','J:J');
        case 2
            %Bunge - Paraguay
            matrix(1,:) = xlsread('BungeParaguay_v1.xlsx','C:C');
            matrix(2,:) = xlsread('BungeParaguay_v1.xlsx','D:D');
            matrix(3,:) = xlsread('BungeParaguay_v1.xlsx','E:E');
    end
end