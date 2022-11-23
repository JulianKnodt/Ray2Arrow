# ray2arrow

Basic usage:
```
python rays_to_arrows.py --path <npy file>
```
Where `<npy file>` contains one tensor of shape (\*, 6), where the first 3 elements are the
origin, and the last 3 are the ray direction.
