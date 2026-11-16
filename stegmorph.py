"""
StegMorph: GA-driven adaptive LSB/PVD steganography for grayscale MRI images.
Implements Algorithms 1-3 of the paper (+ metrics: PSNR, SSIM, SSE, entropy, histogram).

Usage:
    python stegmorph.py embed   cover.png stego.png key.npy "secret message"
    python stegmorph.py extract stego.png key.npy
    python stegmorph.py demo    cover.png            # embed + extract + metrics + histograms

Requires: numpy, opencv-python, matplotlib (optional: scikit-image for SSIM)
"""
import sys
import numpy as np
import cv2

PVD_THRESHOLD = 128
DELIMITER = "1111111111111110"
REDUNDANCY = 3           # each bit is repeated 3x, majority vote on decode
POP_SIZE = 100
GENERATIONS = 50
MUTATION_PROB = 0.1
SEQ_FRACTION = 1 / 3     # sequence length ~ (H*W)/3 pixels


# ----------------------------------------------------------------------------
# 3.1 Preprocessing
# ----------------------------------------------------------------------------
def load_image(path, size=None):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(path)
    if size:
        img = cv2.resize(img, size)
    return np.clip(img, 0, 255).astype(np.uint8)


# ----------------------------------------------------------------------------
# 3.2 Genetic Algorithm for pixel-sequence (key) generation  -- Algorithm 1
# ----------------------------------------------------------------------------
def _fitness(pop, flat):
    """Sum of |I(p_k) - I(p_{k+1})| over consecutive pixels, for each candidate."""
    vals = flat[pop].astype(np.int32)
    return np.abs(vals[:, :-1] - vals[:, 1:]).sum(axis=1)


def generate_pixel_sequence(img, pop_size=POP_SIZE, generations=GENERATIONS,
                            mutation_prob=MUTATION_PROB, seed=None):
    """Returns the key: an ordered array of unique flat pixel indices (even length)."""
    rng = np.random.default_rng(seed)
    flat = img.ravel()
    n_pix = flat.size
    seq_len = max(2, int(n_pix * SEQ_FRACTION))

    # Population: each candidate = list of random pixel coordinates (as flat indices)
    pop = rng.integers(0, n_pix, size=(pop_size, seq_len))

    for _ in range(generations):
        fit = _fitness(pop, flat)
        order = np.argsort(-fit)                    # descending fitness
        parents = pop[order[: pop_size // 2]]       # top 50%

        n_children = pop_size - len(parents)
        children = np.empty((n_children, seq_len), dtype=pop.dtype)
        for c in range(n_children):
            p1, p2 = parents[rng.integers(len(parents), size=2)]
            cut = rng.integers(1, seq_len)          # single-point crossover
            children[c, :cut] = p1[:cut]
            children[c, cut:] = p2[cut:]
            if rng.random() < mutation_prob:        # mutate one coordinate
                children[c, rng.integers(seq_len)] = rng.integers(n_pix)
        pop = np.vstack([parents, children])

    best = pop[np.argmax(_fitness(pop, flat))]

    # Repair: a pixel may appear twice in a random sequence; later writes would
    # overwrite earlier bits and corrupt decoding. Keep first occurrences only.
    _, first = np.unique(best, return_index=True)
    best = best[np.sort(first)]
    if len(best) % 2:
        best = best[:-1]
    return best.astype(np.int64)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def _use_pvd(v1, v2, threshold):
    """
    Decide PVD vs LSB from the pixel pair. The decision uses the values with the
    2 lowest bits cleared, which embedding never changes, so encoder and decoder
    always make the same decision (the paper's raw |I1-I2| can flip after
    embedding and desynchronise decoding).
    """
    return abs((int(v1) & 0xFC) - (int(v2) & 0xFC)) > threshold


def _text_to_bits(message):
    bits = format(len(message), "016b")
    bits += "".join(format(ord(c), "08b") for c in message)
    bits += DELIMITER
    return "".join(b * REDUNDANCY for b in bits)


def capacity_bits(img, key, threshold=PVD_THRESHOLD):
    flat = img.ravel()
    total = 0
    for i in range(0, len(key) - 1, 2):
        total += 4 if _use_pvd(flat[key[i]], flat[key[i + 1]], threshold) else 2
    return total


# ----------------------------------------------------------------------------
# 3.3 Message encoding  -- Algorithm 2
# ----------------------------------------------------------------------------
def embed(img, message, key, threshold=PVD_THRESHOLD):
    if any(ord(c) > 255 for c in message):
        raise ValueError("Message must be Latin-1/ASCII (8 bits per char).")
    if len(message) > 0xFFFF:
        raise ValueError("Message too long for the 16-bit length header.")

    bits = _text_to_bits(message)
    stego = img.copy().ravel()
    padded = bits + "0" * 4              # lets the final pair be filled
    idx = 0

    for i in range(0, len(key) - 1, 2):
        if idx >= len(bits):
            break
        a, b = key[i], key[i + 1]
        if _use_pvd(stego[a], stego[b], threshold):
            chunk = padded[idx: idx + 4]
            stego[a] = (int(stego[a]) & 0xFC) | int(chunk[0:2], 2)   # 2 LSBs
            stego[b] = (int(stego[b]) & 0xFC) | int(chunk[2:4], 2)
            idx += 4
        else:
            chunk = padded[idx: idx + 2]
            stego[a] = (int(stego[a]) & 0xFE) | int(chunk[0])        # 1 LSB each
            stego[b] = (int(stego[b]) & 0xFE) | int(chunk[1])
            idx += 2

    if idx < len(bits):
        raise ValueError(f"Message too large: needed {len(bits)} bits, "
                         f"capacity {capacity_bits(img, key, threshold)} bits.")
    return stego.reshape(img.shape)


# ----------------------------------------------------------------------------
# 3.4 Message decoding  -- Algorithm 3
# ----------------------------------------------------------------------------
def extract(stego, key, threshold=PVD_THRESHOLD):
    flat = stego.ravel()
    out = []
    for i in range(0, len(key) - 1, 2):
        a, b = flat[key[i]], flat[key[i + 1]]
        if _use_pvd(a, b, threshold):
            out.append(format(int(a) & 3, "02b") + format(int(b) & 3, "02b"))
        else:
            out.append(str(int(a) & 1) + str(int(b) & 1))
    stream = "".join(out)

    # Majority vote over each group of 3
    n = len(stream) // REDUNDANCY
    dedup = "".join(
        "1" if stream[k * 3: k * 3 + 3].count("1") >= 2 else "0" for k in range(n)
    )

    length = int(dedup[:16], 2)                       # header
    body = dedup[16: 16 + length * 8]
    if len(body) < length * 8:
        raise ValueError("Decoded data shorter than header length (wrong key/image?).")
    return "".join(chr(int(body[k: k + 8], 2)) for k in range(0, len(body), 8))


# ----------------------------------------------------------------------------
# 4.3 / 4.6 Metrics
# ----------------------------------------------------------------------------
def sse(a, b):
    return float(np.sum((a.astype(np.float64) - b.astype(np.float64)) ** 2))


def psnr(a, b):
    mse = np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2)
    return float("inf") if mse == 0 else 10 * np.log10(255.0 ** 2 / mse)


def ssim(a, b):
    try:
        from skimage.metrics import structural_similarity
        return float(structural_similarity(a, b, data_range=255))
    except ImportError:  # global (non-windowed) fallback
        x, y = a.astype(np.float64), b.astype(np.float64)
        c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
        mx, my = x.mean(), y.mean()
        vx, vy = x.var(), y.var()
        cov = ((x - mx) * (y - my)).mean()
        return float(((2 * mx * my + c1) * (2 * cov + c2)) /
                     ((mx ** 2 + my ** 2 + c1) * (vx + vy + c2)))


def entropy(img):
    p = np.bincount(img.ravel(), minlength=256) / img.size
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def plot_histograms(cover, stego, path="histograms.png"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.5), sharey=True)
    for a, im, t in zip(ax, (cover, stego), ("Original Image", "Stego Image")):
        a.hist(im.ravel(), bins=256, range=(0, 255), color="gray")
        a.set_title(f"Histogram of {t}")
        a.set_xlabel("Pixel Intensity")
    ax[0].set_ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close(fig)


def report(cover, stego):
    return {
        "PSNR (dB)": psnr(cover, stego),
        "SSIM": ssim(cover, stego),
        "SSE": sse(cover, stego),
        "Entropy (cover)": entropy(cover),
        "Entropy (stego)": entropy(stego),
    }


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return
    cmd = argv[1]

    if cmd == "embed":
        cover_p, stego_p, key_p, msg = argv[2], argv[3], argv[4], argv[5]
        cover = load_image(cover_p)
        key = generate_pixel_sequence(cover)
        stego = embed(cover, msg, key)
        cv2.imwrite(stego_p, stego)          # PNG (lossless) only!
        np.save(key_p, key)
        print(f"Saved {stego_p} and key {key_p}")
        for k, v in report(cover, stego).items():
            print(f"{k}: {v:.4f}")

    elif cmd == "extract":
        stego = load_image(argv[2])
        key = np.load(argv[3])
        print("Recovered message:", extract(stego, key))

    elif cmd == "demo":
        cover = load_image(argv[2])
        msg = "Patient ID: 12345 | Name: John Doe | Dx: Mild dementia"
        key = generate_pixel_sequence(cover)
        print(f"Key length: {len(key)} pixels | capacity: {capacity_bits(cover, key)} bits")
        stego = embed(cover, msg, key)
        recovered = extract(stego, key)
        print("Recovered OK:", recovered == msg, "|", recovered)
        for k, v in report(cover, stego).items():
            print(f"{k}: {v:.4f}")
        plot_histograms(cover, stego)
        cv2.imwrite("stego.png", stego)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv)
