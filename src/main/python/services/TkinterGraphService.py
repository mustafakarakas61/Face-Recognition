import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from src.resources.Environments import pathFaceOutputs, pathEyeOutputs


def printGraph(modelName: str):
    root = tk.Tk()
    root.geometry("800x600")

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

    fig = plt.Figure(figsize=(6, 6), dpi=100)
    ax1 = fig.add_subplot(211)
    ax1.plot(epochs, acc, label='Train Set', linewidth=2)
    ax1.plot(epochs, val_acc, label='Validation Set', linestyle='--')
    ax1.set_ylabel('Accuracy - Doğruluk')
    ax1.legend()

    ax2 = fig.add_subplot(212)
    ax2.plot(epochs, loss, label='Train Set', linewidth=2)
    ax2.plot(epochs, val_loss, label='Validation Set', linestyle='--')
    ax2.set_xlabel('Epoch - Tur')
    ax2.set_ylabel('Loss - Kayıp')
    ax2.legend()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    fig.suptitle(modelName, fontsize=12, fontweight='bold')

    root.mainloop()
