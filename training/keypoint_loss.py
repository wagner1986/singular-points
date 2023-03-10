import torch
from kornia.losses import ssim_loss


class kp_loss:
  def __init__(self) -> None:
     self.basic = torch.nn.MSELoss()

  def __call__(self, im1,im2):
     _std = im1.std()+0.01
     return self.basic(im1,im2)/_std

class triplet_loss:
  def __init__(self) -> None:
     def my_ssim(input1, input2):
        return ssim_loss(input1, input2, 5)

     # self.basic = torch.nn.MSELoss()
     self.basic = my_ssim
  def __call__(self, img_anchor,img_pos,img_neg):
      #https://medium.com/analytics-vidhya/triplet-loss-b9da35be21b8
     _margin = 1 # to mse 2 or 1 to ssim
     loss_pos= self.basic(img_anchor,img_pos)
     loss_neg = self.basic(img_anchor, img_neg)
     full_loss = loss_pos-loss_neg+_margin
     # print('loss_pos ', loss_pos, 'loss_neg ', loss_neg, 'full_loss ',full_loss)
     return full_loss

if __name__ == '__main__':
    input1 = torch.rand(1, 4, 5, 5)
    input2 = torch.rand(1, 4, 5, 5)
    def my_loss(i1,i2):
       return ssim_loss(i1, i2, 5)

    loss = my_loss(input1, input2)
    print(loss)