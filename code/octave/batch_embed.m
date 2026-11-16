function batch_embed(method, infile, outfile, rhofile, N, H, W, payload, seed0)
pkg load image;
fid = fopen(infile, 'r'); X = fread(fid, N*H*W, 'uint8=>uint8'); fclose(fid); X = reshape(X, [W, H, N]);
fo = fopen(outfile, 'w'); fr = 0; if ~strcmp(rhofile, 'none'), fr = fopen(rhofile, 'w'); end
for n = 1:N
  im = double(X(:,:,n)');
  if strcmp(method, 'hill'), [s, c] = HILL_mat(im, payload, seed0 + n); else [s, c] = SUNI_mat(im, payload, seed0 + n); end
  s = uint8(s); fwrite(fo, s', 'uint8'); if fr, fwrite(fr, single(c'), 'single'); end
end
fclose(fo); if fr, fclose(fr); end
end
