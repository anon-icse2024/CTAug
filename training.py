import torch
import torchvision
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch.utils.data import DataLoader,Dataset
import matplotlib.pyplot as plt
import torchvision.utils
import numpy as np
import random
import siamese

net = SiameseNetwork().cuda() 
criterion = ContrastiveLoss() 
optimizer = optim.Adam(net.parameters(), lr = 0.0005) 

new = True
saved_model = './saved_model/siamese.pt'
if os.path.isfile(saved_model):
    input_var = None
    while input_var not in ['yes', 'no']:
        input_var = raw_input("Do you want to load saved model [yes/no]?")
    if input_var == 'yes':
        new = False


#training
if new == True:
	iteration_number = 0
	for epoch in range(0, train_number_epochs):
		for i, data in enumerate(train_dataloader, 0):
			code0, code1 , label = data
			code0, code1 , label = code0.cuda(), code1.cuda(), label.cuda() 
			optimizer.zero_grad()
			output1,output2 = net(code0, code1)
			loss_contrastive = criterion(output1, output2, label)
			loss_contrastive.backward()
			optimizer.step()
			if i % 10 == 0 :
				iteration_number +=10
				counter.append(iteration_number)
				loss_history.append(loss_contrastive.item())
				torch.save(net.state_dict(), "./saved_model/siamese.pt")
		print("Epoch number: {} , Current loss: {:.4f}\n".format(epoch,loss_contrastive.item()))
else:
	net.load_state_dict(torch.load("./saved_model/siamese.pt"))
	net.eval()
   
