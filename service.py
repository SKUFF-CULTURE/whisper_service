import torch
print(torch.__version__)          # Должно быть 2.x.x
print(torch.version.cuda)         # Должно быть 11.8
print(torch.cuda.is_available())  # Должно быть True