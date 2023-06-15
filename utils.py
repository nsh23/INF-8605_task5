import os
import torch
from torchinfo import summary
import config
import json
from sklearn import metrics
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def test_net(model, device='cpu', size=(3,256,256), n_batch=32):
    model = model.to(device)
    model.eval()
    x = torch.randn(n_batch, *size, device=device)
    with torch.no_grad():
        output = model(x)
    print()
    print(f'Input shape: {x.shape}')
    print(f'Output shape: {output.shape}')
    summary(model, input_size=(n_batch,*(size)), device=device)

def save_run_config(fname):
    consts = {}
    for k in dir(config):
        if k.isupper() and not k.startswith('_'):
            consts[k] = str(getattr(config, k))
    with open(f'{fname}.conf', 'w') as f:
        f.write(json.dumps(obj=consts, indent=4))

def construct_cm(targets, preds, labels, save_dir=config.MODEL_FOLDER):
    cm = metrics.confusion_matrix(targets, preds)
    cm_df = pd.DataFrame(cm, labels, labels)
    plt.figure(figsize = (9,6))
    sns.heatmap(cm_df, annot=True, fmt="d", cmap='BuGn')
    plt.xlabel("Predicted")
    plt.ylabel("Ground truth")
    plt.title(f"{config.MODEL_NAME} confusion matrix")
    plt.savefig(os.path.join(save_dir, f'{config.CONFIG_ID}_confusion_matrix.png'))
