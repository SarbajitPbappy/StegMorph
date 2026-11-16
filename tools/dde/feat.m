% Feature extraction for V2.1 with the DDE Lab SRM / maxSRM MEX files (research licence, see tools/dde).
% env: FEAT_IN (.mat with imgs N x H x W uint8 and maps N x H x W double), FEAT_OUT (.bin float32, row-major N x 34671), FEAT_MODE (srm|max), FEAT_TMP (pgm path)
addpath(fullfile(getenv('FEAT_BIN')));
load('-mat', getenv('FEAT_IN')); mode = getenv('FEAT_MODE'); tmp = getenv('FEAT_TMP');
N = size(imgs, 1); out = zeros(N, 34671, 'single');
for i = 1:N
  I = uint8(squeeze(imgs(i, :, :)));
  if strcmp(mode, 'srm')
    imwrite(I, tmp); F = SRM({tmp});
  else
    F = maxSRM(I, double(squeeze(maps(i, :, :))));
  end
  fn = fieldnames(F); v = []; for k = 1:numel(fn), v = [v, F.(fn{k})(:)']; end
  out(i, :) = single(v);
end
fid = fopen(getenv('FEAT_OUT'), 'wb'); fwrite(fid, out', 'single'); fclose(fid);
