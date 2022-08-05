meterType = 1; % for the PR670
%CMCheckInit(5, 'ACM1'); % default linux port, Windows would be COM1, COM2...
PR670init('/dev/ttyACM1'); % initialize photometer to remote mode

portNumber = 'ACM1';
% measure from 380nm to 785nm in 4nm in 81 steps -- default can be changed
wavelengthSampling = [380 5 81];

try
    
    fprintf('\n(calibration)$ turn on the photometer...\n');
    fprintf('(calibration)$ hit any key to continue...\n');
    WaitSecs(0.1);
    while(KbCheck==0)
	end;
    fprintf('initializing photometer...\n');

	% ---------- Open Photometer ------
	retval = PR670init(meterType);
    
    fprintf('taking measurements...\n');
	
		WaitSecs(0.1);
        % get xyz measurement
        %[xyz, q] = MeasXYZ(meterType); 
        % need to convert XYZ to LUV?
        %luv = xyz;
        %qual = q;
 		%fprintf('RGB = [%i,%i,%i]; luminance = %g\n',rgb(1),rgb(2),rgb(3),xyz(2));
        
        % measure SPD data        
        [spd, q] = MeasSpd(wavelengthSampling, meterType);
        spdData(kk,:) = [rgb(whichC) spd'];        
        
		if KbCheck
			break;
		end;
	end;
	
	PR670close;
	
