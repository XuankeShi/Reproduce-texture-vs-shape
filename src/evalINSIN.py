

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler

from torchvision import datasets, models, transforms
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import copy
from tqdm import tqdm


# Data augmentation and normalization for training
# Just normalization for validation
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

# data_dirs = [r'../input/imagenet16', r'../input/stylizedimagenet16']
data_dir = r'../input/imagenet16'
# data_dir = r'../input/stylizedimagenet16'

image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                          data_transforms[x])
                  for x in ['train', 'val']}
dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=32,
                                             shuffle=True, num_workers=4)
              for x in ['train', 'val']}
dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}

class_names = image_datasets['train'].classes

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def top5(outputs, labels):
    # print(outputs.shape)
    # print(labels.shape)
    _, idx = outputs.topk(5, 1)
    return (idx == labels.unsqueeze(1)).sum().sum()

def eval_model(model, criterion):

    model.eval()
    phase = 'val'
    with torch.no_grad():
        running_top5acc = 0.0
        running_corrects = 0

        # Iterate over data.
        for inputs, labels in tqdm(dataloaders[phase]):
            inputs = inputs.to(device)
            labels = labels.to(device)

            # forward
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            top5acc = criterion(outputs, labels)
            # print(top5acc)
            # return

            # statistics
            running_top5acc += top5acc.item()
            running_corrects += torch.sum(preds == labels.data)

            # print(running_top5acc)

        epoch_loss = running_top5acc / dataset_sizes[phase]
        epoch_acc = running_corrects.double() / dataset_sizes[phase]

        print('{} Loss: {:.4f} Acc: {:.4f}'.format(
            phase, epoch_loss, epoch_acc))


if __name__ == '__main__':
    model = models.resnet50(pretrained=False)
    #     for param in model.parameters():
    #         param.requires_grad = False
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 16)
    model.load_state_dict(torch.load('../input/resnet50-IN.pth'))
    model = model.to(device)

    # criterion = nn.CrossEntropyLoss()
    criterion = top5


    res = eval_model(model, criterion)
    # Observe that all parameters are being optimized
    # optimizer = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9, weight_decay=1e-4)

    # Decay LR by a factor of 0.1 every 7 epochs
    # exp_lr_scheduler = lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

    # model = train_model(model, criterion, optimizer, num_epochs=25)
    # torch.save(model.state_dict(), f'resnet50-IN.pth')