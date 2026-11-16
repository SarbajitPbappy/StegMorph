"""Yedroudj-Net-style detector for V2.2 (Yedroudj, Comby, Chaumont, ICASSP 2018 layer layout, our re-implementation): 30 fixed SRM-type high-pass kernels (5x5) with absolute value and truncation, five convolution blocks, three fully connected layers. Not the authors' code, no pre-training."""
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F
def srm30():
    k = []
    def emb(a, n=5):  # centre a small kernel in n x n
        o = np.zeros((n, n), np.float32); h, w = a.shape; r, c = (n - h) // 2, (n - w) // 2; o[r:r + h, c:c + w] = a; return o
    def rot(a): return [np.rot90(a, i) for i in range(4)]
    d1 = np.array([[0, 0, 0], [0, -1, 1], [0, 0, 0]], np.float32); dg1 = np.array([[0, 0, 0], [0, -1, 0], [0, 0, 1]], np.float32)
    for a in rot(d1) + rot(dg1): k.append(emb(a))                       # 8 first-order
    d2 = np.array([[0, 0, 0], [1, -2, 1], [0, 0, 0]], np.float32); dg2 = np.array([[1, 0, 0], [0, -2, 0], [0, 0, 1]], np.float32)
    for a in rot(d2)[:2] + rot(dg2)[:2]: k.append(emb(a))               # 4 second-order
    d3 = np.array([[0, 0, 0, 0], [0, -1, 3, -3, 1][:4], [0, 0, 0, 0], [0, 0, 0, 0]], np.float32)
    d3 = np.zeros((1, 4), np.float32); d3[0] = [-1, 3, -3, 1]; dg3 = np.diag([-1, 3, -3, 1]).astype(np.float32)
    for a in rot(d3) + rot(dg3): k.append(emb(a))                       # 8 third-order
    s3 = np.array([[-1, 2, -1], [2, -4, 2], [-1, 2, -1]], np.float32); k.append(emb(s3))                   # SQUARE 3x3
    e3 = np.array([[-1, 2, -1], [2, -4, 2], [0, 0, 0]], np.float32)
    for a in rot(e3): k.append(emb(a))                                  # 4 EDGE 3x3
    e5 = np.array([[-1, 2, -2, 2, -1], [2, -6, 8, -6, 2], [-2, 8, -12, 8, -2], [0] * 5, [0] * 5], np.float32)
    for a in rot(e5): k.append(emb(a))                                  # 4 EDGE 5x5
    s5 = np.array([[-1, 2, -2, 2, -1], [2, -6, 8, -6, 2], [-2, 8, -12, 8, -2], [2, -6, 8, -6, 2], [-1, 2, -2, 2, -1]], np.float32); k.append(emb(s5))  # SQUARE 5x5
    K = np.stack(k)[:30]; assert len(K) == 30, len(K); return K
class Yedroudj(nn.Module):
    def __init__(s):
        super().__init__(); s.register_buffer("K", torch.tensor(srm30() / 12.0)[:, None])
        s.c1 = nn.Conv2d(30, 30, 5, padding=2, bias=False); s.b1 = nn.BatchNorm2d(30); s.c2 = nn.Conv2d(30, 30, 5, padding=2, bias=False); s.b2 = nn.BatchNorm2d(30)
        s.c3 = nn.Conv2d(30, 32, 3, padding=1, bias=False); s.b3 = nn.BatchNorm2d(32); s.c4 = nn.Conv2d(32, 64, 3, padding=1, bias=False); s.b4 = nn.BatchNorm2d(64); s.c5 = nn.Conv2d(64, 128, 3, padding=1, bias=False); s.b5 = nn.BatchNorm2d(128)
        s.fc = nn.Sequential(nn.Linear(128, 256), nn.ReLU(), nn.Linear(256, 1024), nn.ReLU(), nn.Linear(1024, 2))
    def forward(s, x):
        x = F.conv2d(x, s.K, padding=2); x = x.abs().clamp(max=3.0)
        x = torch.clamp(s.b1(s.c1(x)), -1, 1); x = torch.clamp(s.b2(s.c2(x)), -1, 1); x = F.avg_pool2d(x, 5, 2, 2)
        x = F.avg_pool2d(F.relu(s.b3(s.c3(x))), 5, 2, 2); x = F.avg_pool2d(F.relu(s.b4(s.c4(x))), 5, 2, 2); x = F.relu(s.b5(s.c5(x)))
        return s.fc(x.mean((2, 3)))
