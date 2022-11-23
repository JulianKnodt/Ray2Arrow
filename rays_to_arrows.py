import numpy as np
import argparse
import torch
import torch.nn.functional as F

def arguments():
  a = argparse.ArgumentParser()
  a.add_argument("--path", required=True, help="path to file of rays")
  a.add_argument("--scale", default=1, type=float, help="Scale of arrows")
  a.add_argument("--width", default=0.05, type=float, help="width of arrows")
  a.add_argument("--reso", default=6, type=int, help="Number of points on arrows")
  return a.parse_args()

def main():
  args = arguments()
  rays = torch.from_numpy(np.load(args.path)).float()
  if len(rays.shape) == 1: rays = rays[None]
  origin = rays[:, :3]
  dirs = args.scale * rays[:, 3:]

  tan = F.normalize(
    torch.cross(dirs, torch.randn_like(dirs), dim=-1),
    dim=-1
  )
  bit = F.normalize(torch.cross(tan, dirs, dim=-1), dim=-1)
  t = torch.linspace(0, 2 * torch.pi, args.reso+1)
  u = t.cos()[:-1]
  v = t.sin()[:-1]

  points = []
  for ui, vi in zip(u,v):
    plane_shift = (ui * tan + vi * bit) * args.width
    points.append([
      origin + plane_shift,
      origin + dirs + plane_shift,
    ])

  print("solid arrows")
  for i, [curr_o, curr_d] in enumerate(points):
    [next_o, next_d] = points[(i+1) % len(points)]
    for j in range(curr_o.shape[0]):
      v0 = curr_o[j]
      v1 = curr_d[j]
      v2 = next_o[j]
      v3 = next_d[j]

      print(f"""\
facet normal 0 0 1
    outer loop
        vertex {v0[0]} {v0[1]} {v0[2]}
        vertex {v1[0]} {v1[1]} {v1[2]}
        vertex {v2[0]} {v2[1]} {v2[2]}
    endloop
endfacet""")
      print(f"""\
facet normal 0 0 1
    outer loop
        vertex {v1[0]} {v1[1]} {v1[2]}
        vertex {v3[0]} {v3[1]} {v3[2]}
        vertex {v2[0]} {v2[1]} {v2[2]}
    endloop
endfacet""")

  print("endsolid arrows")
  return


if __name__ == "__main__": main()
