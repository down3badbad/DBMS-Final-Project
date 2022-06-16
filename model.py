import torch
import sys
import numpy as np
import os
import glob
import yaml
import matplotlib.pyplot as plt
import torch
import torchvision
from torchvision import models
from torchvision import transforms
from PIL import Image
from utils import float_to_hex, padhexa

def forward(model, batch_img):
    x = model.conv1(batch_img)
    x = model.bn1(x)
    x = model.relu(x)
    x = model.maxpool(x)
    x = model.layer1(x)
    x = model.layer2(x)
    x = model.layer3(x)
    x = model.layer4(x)
    x = model.avgpool(x)
    return x

def run_simclr(search_img):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print("Using device:", device)
    
    model = torchvision.models.resnet18(pretrained=False, num_classes=10).to(device)
    checkpoint = torch.load('C:/Database_lec/Final/SimCLR/checkpoint_0100.pth.tar', map_location=device)
    state_dict = checkpoint['state_dict']

    for k in list(state_dict.keys()):
        if k.startswith('backbone.'):
            if k.startswith('backbone') and not k.startswith('backbone.fc'):
                # remove prefix
                state_dict[k[len("backbone."):]] = state_dict[k]
        del state_dict[k]

    log = model.load_state_dict(state_dict, strict=False)
    assert log.missing_keys == ['fc.weight', 'fc.bias']

    preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )])
    
    img = preprocess(search_img)
    batch_img = torch.unsqueeze(img, 0)
    out = forward(model, batch_img)[0].squeeze()
    out_np = out.detach().numpy()

    return out_np