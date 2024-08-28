%%%%
% Adjust loudness difference between noise and stimulus

%% Get Loudness of stimuli

directory = 'D:\MeineDaten\Dokumente\04_AUDICTIVE\WP_Acou_B\acou-1\aVSR_Code\Input_Data\AudioFiles';
fileList = dir('*.wav');
which -all audioread
for ida=1:length(fileList)

    stimulus = ita_read(fileList(ida).name);
    stimulus.channelUnits(:) = {'Pa'};
    tmp = ita_loudness(stimulus);
    loudness_vals(ida) = tmp.value;
    db_vals(ida) = 20*log10(stimulus.rms/(20*10^-6));

end


%% Loudness Adjustment
db_mean = mean(db_vals(5:end))
db_diff = 3;

%PinkNoise
stimulus = ita_read(fileList(2).name);
stimulus.channelUnits(:) = {'Pa'};
stimulus.timeData = stimulus.timeData * 10^((db_mean - db_diff - 20*log10(stimulus.rms/(20*10^-6)))/20) 
ita_write_wav(stimulus, strcat('PinkNoise_44100_10_', num2str(round(db_mean-db_diff)), '.wav'))

%PinkNoise
stimulus = ita_read(fileList(3).name);
stimulus.channelUnits(:) = {'Pa'};
stimulus.timeData = stimulus.timeData * 10^((db_mean - db_diff - 20*log10(stimulus.rms/(20*10^-6)))/20) 
ita_write_wav(stimulus, strcat('SpeechShapedNoise_44100_10_', num2str(round(db_mean-db_diff)), '.wav'))

%PinkNoise
stimulus = ita_read(fileList(4).name);
stimulus.channelUnits(:) = {'Pa'};
stimulus.timeData = stimulus.timeData * 10^((db_mean - db_diff - 20*log10(stimulus.rms/(20*10^-6)))/20) 
ita_write_wav(stimulus, strcat('WhiteNoise_44100_10_', num2str(round(db_mean-db_diff)), '.wav'))
