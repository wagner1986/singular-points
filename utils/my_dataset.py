import os

import torch
import torchvision
import torchvision.transforms as transforms
import random
import glob

from PIL import Image
from matplotlib import pyplot as plt

from config import args
from torchvision.transforms import InterpolationMode


class MyFlowersDataset(torch.utils.data.Dataset):

    def __init__(self, train=True) -> None:
        super().__init__()
        split = 'train' if train else 'test'
        print(split)
        transform = transforms.Compose([
            transforms.Resize((args.img_size, args.img_size), interpolation=InterpolationMode.NEAREST),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        self.data = torchvision.datasets.Flowers102(root='./data', split=split,
                                                    download=True, transform=transform)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        index = random.randrange(0,self.__len__())
        index = index if index != idx else 0
        image, label = self.data[idx]
        image2, label2 = self.data[index]
        return image, image2


class FibersDataset(torch.utils.data.Dataset):
    """Fibers dataset. to train neural net"""

    def __init__(self, transform=None,train=True, path='./data/fibers/'):
        self.transform = transform
        self.data = glob.glob('{}*.jpg'.format(path))
        limit_train = int(len(self.data)*0.6)
        self.image_list = []
        if train:
            self.data = self.data[:limit_train]
        else:
            self.data = self.data[limit_train:]
        print(self.data)

        # for filename in self.data:  # assuming gif
        #     im = Image.open(filename)
        #     self.image_list.append(im)
        # self.image_list = transform(self.image_list)
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        filename = self.data[idx]
        img = Image.open(filename)
        img_t = self.transform(img)
        return img_t,' rrr '


if __name__ == '__main__':
    transform = transforms.Compose([
        transforms.Resize((450,450), interpolation=InterpolationMode.NEAREST),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        # transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225])
    ])
    fibers_set = FibersDataset(transform=transform,train=True,path='../data/fibers/')
    trainloader = torch.utils.data.DataLoader(fibers_set, batch_size=args.batch_size,
                                            shuffle=True)
    for imgs,labels in trainloader:
        plt.imshow(imgs[0].permute(1, 2, 0))
        plt.show()
        print(imgs.shape,labels)