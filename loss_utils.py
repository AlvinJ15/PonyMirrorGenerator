import numpy as np
import torch.nn.functional as F
import torch
def dice_loss(pred, target, smooth = 1e-5):

    intersection = (pred * target).sum(dim=(1,2))
    union= pred.sum(dim=(1,2)) + target.sum(dim=(1,2)) 
    
    dice= 2.0 * (intersection + smooth) / (union+ smooth)    
    loss = 1.0 - dice
    
    return loss.sum(), dice.sum()


def loss_func(pred, target):
    #bce = F.binary_cross_entropy_with_logits(pred, target,  reduction='sum')
    pred= torch.sigmoid(pred)
    ##bce = F.mse_loss(pred, target,  reduction='sum')
    
    ##dlv, _ = dice_loss_custom(pred, target)
    
    ##loss = bce  + dlv
    loss, _ = dice_loss_custom(pred>=4e-3, target)
    return loss

def dice_loss_custom(pred, target, alpha=4e-3, smoth = 1e-5):
    dice = torch.abs(target-pred) <= alpha
    loss = torch.abs(target-pred) > alpha
    total = np.prod(dice.shape[1:])

    if False:
        print("TOTAL ",total)
        print("DICE:",dice.shape)
        print("LOSSSHAPE:",loss.shape)
        print("DICESUM:", dice.sum(dim=(1,2,3)))
        print("LOSSSUM:",loss.sum(dim=(1,2,3)))
        print("-"*10)
    dice = dice.sum(dim=(1,2))/float(total)
    loss = loss.sum(dim=(1,2))/float(total)
    #print("DICEFINAL:", dice.sum())
    #print("LOSSFINAL:", loss.sum()) 

    return loss.sum(), dice.sum()

def loss_batch(loss_func, output, target, opt=None):   
    loss = loss_func(output, target)
    
    pred= torch.sigmoid(output)
    
    _, metric_b=dice_loss_custom(pred, target)
    
    if opt is not None:
        opt.zero_grad()
        loss.backward()
        opt.step()

    return loss.item(), metric_b.item()