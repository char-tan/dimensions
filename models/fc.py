import torch
import torch.nn as nn
import torch.nn.functional as F



class FC_MNIST(nn.Module):

    def __init__(self, input_dim=28*28, width=50, depth=3, num_classes=10, use_bias=True):
        super(FC_MNIST, self).__init__()
        self.input_dim = input_dim
        self.width = width
        self.depth = depth
        self.num_classes = num_classes

        layers = self.get_layers(use_bias)

        self.fc = nn.Sequential(
            nn.Linear(self.input_dim, self.width, bias=use_bias),
            nn.ReLU(inplace=True),
            *layers,
            nn.Linear(self.width, self.num_classes, bias=use_bias),
        )

    def get_layers(self, use_bias):
        layers = []
        for i in range(self.depth - 2):
            layers.append(nn.Linear(self.width, self.width, bias=use_bias))
            layers.append(nn.ReLU(inplace=True))
        return layers

    def forward(self, x):
        x = x.view(x.size(0), self.input_dim)
        x = self.fc(x)
        return x


class BHP_FCNN(nn.Module):

    def __init__(self, depth: int = 5, width: int = 50, input_dim: int = 13, use_bias=True):
        super(BHP_FCNN, self).__init__()
        self.input_dim = input_dim
        self.width = width
        self.depth = depth

        layers = self.get_layers(use_bias)

        self.fc = nn.Sequential(
            nn.Linear(self.input_dim, self.width, bias=use_bias),
            nn.ReLU(inplace=True),
            *layers,
            nn.Linear(self.width, 1, bias=use_bias),
        )

    def get_layers(self, use_bias):
        layers = []
        for _ in range(self.depth - 2):
            layers.append(nn.Linear(self.width, self.width, bias=use_bias))
            layers.append(nn.ReLU())
        return layers

    def forward(self, x):
        x = x.view(x.size(0), self.input_dim)
        x = self.fc(x)
        return x


def fc_bhp(**kwargs):
    return BHP_FCNN(**kwargs)


def fc_mnist(**kwargs):
    return FC_MNIST(**kwargs)


class FC_CIFAR(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(3072, 1024)
        self.linear2 = nn.Linear(1024, 512)
        self.linear3 = nn.Linear(512, 64)
        self.linear4 = nn.Linear(64, 64)
        self.linear5 = nn.Linear(64, 10)

    def forward(self, xb):
        # Flatten images into vectors
        out = xb.view(xb.size(0), -1)
        out = self.linear1(out)
        out = F.relu(out)
        out = self.linear2(out)
        out = F.relu(out)
        out = self.linear3(out)
        out = F.relu(out)
        out = self.linear4(out)
        out = F.relu(out)
        out = self.linear5(out)
        return out


def fc_cifar(**kwargs):
    return FC_CIFAR(**kwargs)
