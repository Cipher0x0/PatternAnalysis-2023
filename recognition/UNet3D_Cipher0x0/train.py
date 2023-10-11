from dataset import *
from modules import *


class DiceLoss(nn.Module):
    def __init__(self, weight=None, size_average=True):
        super(DiceLoss, self).__init__()

    '''calculate dsc per label'''
    def single_loss(self, inputs, targets, smooth=0.1):
        intersection = (inputs * targets).sum()
        dice = (2. * intersection + smooth) / (inputs.sum() + targets.sum() + smooth)
        return dice

    '''calculate dsc for each channel, add them up and get the mean'''
    def forward(self, inputs, targets, smooth=0.1):
        input0 = (inputs.argmax(1) == 0)  # prediction of label 0
        input1 = (inputs.argmax(1) == 1)  # prediction of label 1
        input2 = (inputs.argmax(1) == 2)  # prediction of label 2
        input3 = (inputs.argmax(1) == 3)  # prediction of label 3
        input4 = (inputs.argmax(1) == 4)  # prediction of label 4
        input5 = (inputs.argmax(1) == 5)  # prediction of label 5

        target0 = (targets == 0)  # target of label 0
        target1 = (targets == 1)  # target of label 1
        target2 = (targets == 2)  # target of label 2
        target3 = (targets == 3)  # target of label 3
        target4 = (targets == 4)  # target of label 4
        target5 = (targets == 5)  # target of label 5

        dice0 = self.single_loss(input0, target0)
        dice1 = self.single_loss(input1, target1)
        dice2 = self.single_loss(input2, target2)
        dice3 = self.single_loss(input3, target3)
        dice4 = self.single_loss(input4, target4)
        dice5 = self.single_loss(input5, target5)

        dice = (dice0 + dice1 + dice2 + dice3 + dice4 + dice5) / 6.0

        return 1 - dice


def main():
    # change path to current directory
    os.chdir(os.path.dirname(__file__))

    # check whether gpu is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(device, flush=True)
    torch.cuda.empty_cache()

    # build model and optimizer
    loss_fn = nn.CrossEntropyLoss().to(device)
    optimizer = torch.optim.Adam(model.parameters())

    epoch = 30

    # train loop
    for i in range(epoch):
        unet.train()
        for index, data in enumerate(trainloader, 0):
            image, mask = data
            image, mask = ag.crop_and_augment(image, mask)
            image = image.unsqueeze(0)
            image = image.float().to(device)
            mask = mask.long().to(device)
            optimizer.zero_grad()
            pred = unet(image)
            loss = loss_fn(pred, mask)
            loss.backward()
            optimizer.step()


if __name__ == "__main__":
    main()
