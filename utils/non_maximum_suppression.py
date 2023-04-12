
import numpy as np
import torch
import torch.nn as nn
from matplotlib import pyplot as plt
from scipy.ndimage import maximum_filter

#TODO refatorar
class NMSHead(nn.Module):
    def __init__(self, nms_size=5, nms_min_val=1e-5):
        super(NMSHead, self).__init__()
        self.nms_size = nms_size
        self.min_val = nms_min_val

    def _get_max_coords(self, input_map):
        """ _get_max_coords uses NMS of window size (self.nms_size) and
        threshold (self.min_val) to extract the coordinates of the local
        maximums in the input_map.
        :param input_map: (H, W) tensor of the map
        :return tensor: (2, N) tensor of the local maximum coordinates
        """
        assert input_map.ndim == 2, 'invalid input shape'
        device = input_map.device
        input_map = input_map.cpu().numpy()
        max_map = maximum_filter(input_map, size=self.nms_size, mode='constant')
        max_coords = np.stack(
            ((max_map > self.min_val) & (max_map == input_map)).nonzero()
        )
        plt.imshow(((max_map > 1e-5) & (max_map == input_map)))
        plt.show()

        return torch.tensor(max_coords).flip(0).to(device)  # flip axes

    def get_max_coords(self, input_maps):
        return [self._get_max_coords(input_map[0]) for input_map in input_maps]

    def forward(self, input_map):
        bs = len(input_map)

        # non-maximum suppression
        bev_coords = self.get_max_coords(input_map)
        n_coords = [coord.shape[1] for coord in bev_coords]
        bev_pixels = torch.zeros(bs, 3, max(n_coords)).to(input_map.device)
        bev_pixels[:, 2] = 1

        for i, bev_coord in enumerate(bev_coords):
            bev_pixels[i, :2, :bev_coord.shape[1]] = bev_coord

        # convert to world scale
        bev_size = input_map.shape[2:]
        return bev_pixels

#TODO refatorar
def bound_box(points, size=14):
    boxs = []
    for point in points:
        [x, y] = point[:2]
        x, y = int(x), int(y)
        box = [(x - size, y - size), (x + size, y + size)]
        boxs.append(box)
    return boxs

#TODO refatorar
def create_circular_mask(h, w, center=None, radius=None):
    if center is None:  # use the middle of the image
        center = (int(w / 2), int(h / 2))
    if radius is None:  # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w - center[0], h - center[1])
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)
    mask = dist_from_center <= radius
    return mask

#TODO refatorar
def apply_circular_mask_box(img, box):
    pt1, pt2 = box
    crop_img = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
    h, w = crop_img.shape
    mask = torch.tensor(create_circular_mask(h, w))

    masked_img = crop_img.clone()
    masked_img[~mask] = 0
    return masked_img

#TODO refatorar
def get_features(img_batch, coords):
    for i, img in enumerate(img_batch):
        points = torch.stack((coords[i, 0, :], coords[i, 1, :]), axis=-1)
        boxs = bound_box(points, size=30)

        for i, box in enumerate(boxs):
            print(i)
            masked_img = apply_circular_mask_box(img.clone(), box)
            plt.imshow(masked_img.detach())
            plt.show()


#TODO Sample usando NMS

# size =30
# feat_temp = torch.cat([_k,_k])
# feat_temp = remove_borders(feat_temp,size)
# plt.imshow(feat_temp[0][0].detach())
# plt.show()
#
# nms =NMSHead(nms_size=size)
# coords = nms.forward(feat_temp.clone().detach())

# ori_batch = torch.cat([ori_arg_max,ori_arg_max])
#
# get_features(ori_batch[:1,:,:],coords[:1,:,:])