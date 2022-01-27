cd('~/github/ePSproc')  % Change to ePSproc root dir.

%% *** SETTINGS
%  Set up basic environment

% Name & path to ePS output file. In this version set full file name here, and working directory below.
% fileName='no2_demo_ePS.out'  % OK for MFPAD testing, but only single E point
fileName='n2_3sg_0.1-50.1eV_A2.inp.out'

% Set paths for Linux or Win boxes (optional!)
if isunix
    dirSlash='/';
else
    dirSlash='\';
end

filePath=[pwd dirSlash 'data' dirSlash 'photoionization'];                       % Root to working directory, here set as current dir/data/photoionization
fileBase=[filePath dirSlash fileName];   % Full path to ePS results file, here set as current working direcory

scriptPath=[pwd dirSlash 'matlab' dirSlash];  % Add path to ePSproc scrips to Matlab path list, here set as current dir/matlab
path(path,[scriptPath]);   

%% *** Read data
%  Variables:
%       rlAll contains matrix elements (from DumpIdy segments)
%       params contains various calculation parameters
%       getCro contains cross-section (from GetCro segments), if present

[rlAll, params, getCro]=ePSproc_read(fileBase);

params.fileBase=fileBase;
params.fileName=fileName;

% Matrix elements are stored in a structure
rlAll

% GetCro outputs (total cross-secions, LF betas)
getCro

% General calculation params
params

%% Plot GetCro results for each symm & total

col=2;  % Select column from getCro output (see params.GetCroHeader)

figure('color',[1 1 1],'name','GetCro outputs');

for n=1:length(getCro)
    plot(getCro(n).GetCro(:,1)-params.IP,getCro(n).GetCro(:,col));
    hold on;
end

title({['NO_2 ePS resutls, files ' strrep(fileName,'_','\_')]; 'X-sects from ePS(GetCro) results'});
xlabel('eKE/eV');
ylabel('X-sect/Mb');

legend([params.symmList 'Sum']);

%% *** Calculate MFPADs - single polarization geometry, all energies and symmetries
%  Calculate for specified Euler angles (polarization geometry) & energies

% Set resolution for calculated I(theta,phi) surfaces
res=100;

% ip components to use from ePS output (1=length gauge, 2=velocity gauge)
ipComponents=1;

% it components to use from ePS output (for degenerate cases), set an array here for as many components as required, e.g. it=1, it=[1 2] etc.
it=1;

% Set light polarization and axis rotations LF -> MF
p=0;                % p=0 for linearly pol. light, +/-1 for L/R circ. pol.
eAngs=[0 0 0];      % Eugler angles for rotation of LF->MF, set as [0 0 0] for z-pol, [0 pi/2 0] for x-pol, [pi/2 pi/2 0] for y-pol
polLabel='z';

% Run calculation - outputs are D, full set of MFPADs (summed over symmetries); Xsect, calculated X-sects; calcsAll, structure with results for all symmetries.
[Xsect, calcsAll, pWaves]=ePSproc_MFPAD(rlAll,p,eAngs,it,ipComponents,res);

% Add pol labels - currently expected in plotting routine, but not set in MFPAD routine
for n=1:size(calcsAll,2)
    for symmIn=1:size(calcsAll,1)
        calcsAll(symmInd,n).polLabel=polLabel;
    end
end
        

% Results are output as a structure, dims (symmetries, energies).
calcsAll

%plot -s 800,400

%% Plotting - MFPAD panel plots

% Set plot ranges
symmInd=1;     % Select symmetry (by index into calcsAll rows). Final symmetry state is set as sum over all symmetries
% eRange=1;      % Select energies (by index into calcsAll cols)
eRange=1:3:20;

% Additional options (optional)
sPlotSet=[2 4];             % Set [rows cols] for subplot panels. The final panel will be replaced with a diagram of the geometry
% titlePrefix='NO2 testing';  % Set a title prefix for the figure
titlePrefix='';

ePSproc_MFPAD_plot(calcsAll,eRange,symmInd,params,sPlotSet,titlePrefix);
% ePSproc_MFPAD_plot(calcsAll,eRange,symmInd,params,sPlotSet,'','n','off');
% ePSproc_MFPAD_plot(calcsAll,eRange,symmInd,params,[2 4],'','n','off');

% Calculate & plot for a different polarization state
eAngs = [0 pi/2 0];  % x-pol case
polLabel = 'x';

[Xsect, calcsAll, pWaves]=ePSproc_MFPAD(rlAll,p,eAngs,it,ipComponents,res);

% Add pol labels - currently expected in plotting routine, but not set in MFPAD routine
for n=1:size(calcsAll,2)
    for symmIn=1:size(calcsAll,1)
        calcsAll(symmInd,n).polLabel=polLabel;
    end
end

symmInd=3;
ePSproc_MFPAD_plot(calcsAll,eRange,symmInd,params,sPlotSet,titlePrefix);

% Calculate & plot for a different polarization state
eAngs = [0 pi/4 0];  % Diagonal pol case
polLabel = 'x';

[Xsect, calcsAll, pWaves]=ePSproc_MFPAD(rlAll,p,eAngs,it,ipComponents,res);

% Add pol labels - currently expected in plotting routine, but not set in MFPAD routine
for n=1:size(calcsAll,2)
    for symmIn=1:size(calcsAll,1)
        calcsAll(symmInd,n).polLabel=polLabel;
    end
end

% Plot all symmetries
for symmInd = 1:3
    ePSproc_MFPAD_plot(calcsAll,eRange,symmInd,params,sPlotSet,titlePrefix);
    
end

%% *** Calculate MFPADs - single polarization geometry, all energies and symmetries
%  Calculate for specified Euler angles (polarization geometry) & energies

% Set resolution for calculated I(theta,phi) surfaces
res=100;

% ip components to use from ePS output (1=length gauge, 2=velocity gauge)
ipComponents=1;

% it components to use from ePS output (for degenerate cases), set an array here for as many components as required, e.g. it=1, it=[1 2] etc.
it=1;

% Set light polarization and axis rotations LF -> MF
p=0;                % p=0 for linearly pol. light, +/-1 for L/R circ. pol.
eAngs=[0 0 0];      % Eugler angles for rotation of LF->MF, set as [0 0 0] for z-pol, [0 pi/2 0] for x-pol, [pi/2 pi/2 0] for y-pol
polLabel='z';

% Run calculation - outputs are D, full set of MFPADs (summed over symmetries); Xsect, calculated X-sects; calcsAll, structure with results for all symmetries.
calcsAll=ePSproc_MFPAD(rlAll,p,eAngs,it,ipComponents,res);

% Add pol labels - currently expected in plotting routine, but not set in MFPAD routine
% for n=1:size(calcsAll,2)
%     for symmIn=1:size(calcsAll,1)
%         calcsAll(symmInd,n).polLabel=polLabel;
%     end
% end
        

plot(calcsAll.')


