import argparse

import torch

parser = argparse.ArgumentParser()
parser.add_argument("--num_channels", required=False, default=3, type=int)
parser.add_argument("--pyramid_levels", required=False, default=3, type=int)# min 2
parser.add_argument("--scale_pyramid", required=False, default=1.3, type=int)# min 2
parser.add_argument("--dim_first", required=False, default=2, type=int)
parser.add_argument("--dim_second", required=False, default=2, type=int)
parser.add_argument("--dim_third", required=False, default=2, type=int)
parser.add_argument("--group_size", required=False, default=36, type=int)
parser.add_argument("--epochs", required=False, default=25, type=int)
parser.add_argument("--img_size", required=False, default=200, type=int)
parser.add_argument("--batch_size", required=False, default=6, type=int)
parser.add_argument('--path_data', required=False, default='./data', type=str)
parser.add_argument('--path_model', required=False, default='model.pt', type=str)
parser.add_argument('--outlier_rejection', required=False, default=False, type=bool)
args = parser.parse_args([])

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)
torch.manual_seed(0)