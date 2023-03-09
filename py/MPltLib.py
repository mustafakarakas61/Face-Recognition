import os
import glob
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore",
                        message="Support for FigureCanvases without a required_interactive_framework attribute was deprecated in Matplotlib 3.6")

# PATHS
path = "C:/Project/Proje-2/face_recognition/models/txts/"

fileList = glob.glob(os.path.join(path, '*.txt'))

print("Model Çıktıları:")
for filePath in fileList:
    fileName = os.path.basename(filePath)
    print(fileName.replace(".txt", ""))

# SETS
txt = input("Lütfen bir modelin çıktısının ismini giriniz: ")

epochs = []
loss = []
acc = []
val_loss = []
val_acc = []

with open(path + txt + ".txt", 'r') as file:
    next(file)  # İlk satırı atla
    for line in file:
        epoch, loss_val, acc_val, val_loss_val, val_acc_val = line.strip().split('\t')
        epochs.append(int(epoch))
        loss.append(float(loss_val))
        acc.append(float(acc_val))
        val_loss.append(float(val_loss_val))
        val_acc.append(float(val_acc_val))

fig, ax = plt.subplots(2)
ax[0].plot(epochs, loss, label='Train Set')
ax[0].plot(epochs, val_loss, label='Validation Set')
# ax[0].set_xlabel('Epoch - Tur')
ax[0].set_ylabel('Loss - Kayıp')
ax[0].legend()
ax[1].plot(epochs, acc, label='Train Set')
ax[1].plot(epochs, val_acc, label='Validation Set')
ax[1].set_xlabel('Epoch - Tur')
ax[1].set_ylabel('Accuracy - Doğruluk')
ax[1].legend()
plt.show()
