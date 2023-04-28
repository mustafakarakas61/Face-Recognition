import matplotlib.pyplot as plt
import warnings

from src.resources.Environments import pathFaceOutputs, pathEyeOutputs

warnings.filterwarnings("ignore",
                        message="Support for FigureCanvases without a required_interactive_framework attribute was deprecated in Matplotlib 3.6")


def printGraph(modelName: str):
    epochs = []
    loss = []
    acc = []
    val_loss = []
    val_acc = []
    modelName = modelName.replace(".h5", "")
    if modelName.__contains__("face"):
        pathOutput = pathFaceOutputs + modelName + ".txt"
    else:
        pathOutput = pathEyeOutputs + modelName + ".txt"

    with open(pathOutput, 'r') as file:
        next(file)  # İlk satırı atla (başlıklar)
        lines = file.readlines()[:-2]  # Son 2 satırı atla
        for line in lines:
            epoch, loss_val, acc_val, val_loss_val, val_acc_val = line.strip().split('\t')
            epochs.append(int(epoch))
            loss.append(float(loss_val))
            acc.append(float(acc_val))
            val_loss.append(float(val_loss_val))
            val_acc.append(float(val_acc_val))

    fig, ax = plt.subplots(2)
    ax[0].plot(epochs, acc, label='Train Set', linewidth=2)
    ax[0].plot(epochs, val_acc, label='Validation Set', linestyle='--')
    ax[0].set_ylabel('Accuracy - Doğruluk')
    ax[0].legend()

    ax[1].plot(epochs, loss, label='Train Set', linewidth=2)
    ax[1].plot(epochs, val_loss, label='Validation Set', linestyle='--')
    ax[1].set_xlabel('Epoch - Tur')
    ax[1].set_ylabel('Loss - Kayıp')
    ax[1].legend()

    plt.suptitle(modelName, fontsize=12, fontweight='bold')
    plt.show()
