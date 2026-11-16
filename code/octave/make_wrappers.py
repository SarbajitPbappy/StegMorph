"""Builds matrix-input wrappers of the official-code simulators (HILL: Shenzhen University 2014; S-UNIWARD: DDE Lab, Binghamton 2013), as distributed in the Aletheia toolkit.
Only I/O is changed: image matrix instead of file path, a caller-set random seed instead of the clock, and the cost map returned. The cost and embedding-simulator code is untouched."""
import re, sys
SRC = "github/aletheia_src/aletheia-master/aletheia-cache/octave/"
h = open(SRC + "HILL.m").read()
h = h.replace("function stego = HILL(cover_path, payload)", "function [stego, cost] = HILL_mat(x, payload, seed)\nrand('state', seed);").replace("x = imread(cover_path);", "x = double(x);")
h = h.replace("rand('state', sum(100*clock));", "% seeded by caller")
assert "HILL_mat" in h and "sum(100*clock)" not in h
open("code/octave/HILL_mat.m", "w").write(h)
s = open(SRC + "S_UNIWARD.m").read()
s = s.replace("function stego = S_UNIWARD(coverPath, payload)", "function [stego, rho] = SUNI_mat(coverPath, payload, seed)\nrand('state', seed);").replace("cover = double(imread(coverPath));", "cover = double(coverPath);")
s = s.replace("rand('state', sum(100*clock));", "% seeded by caller")
assert "SUNI_mat" in s and "rand('state', sum(100*clock))" not in s and "double(imread" not in s
open("code/octave/SUNI_mat.m", "w").write(s)
open("code/octave/batch_embed.m", "w").write('''function batch_embed(method, infile, outfile, rhofile, N, H, W, payload, seed0)
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
''')
