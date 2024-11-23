import torch
import torch.nn as nn
from torch.ao.nn.quantized import Dropout
from torch.optim import Adam
import sqlite3
from torch.utils.data import Dataset, DataLoader, random_split
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

input_neurons = 103  # 8000
hiden_layers_num = 3
dropout = 0.1
lr = 0.001
proportion = 0.995
n_epochs = 40
save_every = 1
PATH = r"C:\Users\student.CLUMBA.013\PycharmProjects\pythonProject\MAP_V1.8.pt"  # f"/home/ceslav/PycharmProjects/BFT_test/model/Translator11:06:58"
mode = "use"  # learn or use


class Perceptron(nn.Module):
    def __init__(self, input_neurons, hiden_layers_num):
        super().__init__()
        num_hiden_neuron = int(input_neurons * 1.5)
        self.linear_stack = nn.Sequential()

        self.linear_stack.add_module("input_layer", nn.Linear(input_neurons, num_hiden_neuron))
        self.linear_stack.add_module("input_act", nn.Sigmoid())
        for i in range(hiden_layers_num):
            name = "layer_" + str(i)
            self.linear_stack.add_module(name, nn.Linear(num_hiden_neuron, num_hiden_neuron))
            name = "act_" + str(i)
            self.linear_stack.add_module(name, nn.ReLU())
            name = "dropout_" + str(i)
            self.linear_stack.add_module(name, Dropout(0.12))
        self.linear_stack.add_module("output_layer", nn.Linear(num_hiden_neuron, 2))
        self.linear_stack.add_module("output_act", nn.Softmax())
        # self.linear_stack.add_module("output_ReLU", nn.ReLU())
        # print(self.linear_stack)

    def forward(self, x):
        x = self.linear_stack(x)
        # for i, layer in enumerate(self.linear_stack):
        #     x = layer(x)
        return x


class DB_connect:
    def __init__(self):
        self.ru_dict = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "\'",
                        11: "\"", 12: ",", 13: ".", 14: "!", 15: "?", 16: " ", 17: "/", 18: "|", 19: "{", 20: "}",
                        21: "[", 22: "]", 23: "@", 24: "#", 25: "№", 26: "$", 27: ";", 28: "^", 29: ":", 30: "&",
                        31: "_", 32: "-", 33: "~", 34: "", 35: ">", 36: "<", 37: "+", 38: "*", 39: "=", 40: "\n",
                        41: "А", 42: "а", 43: "Б", 44: "б", 45: "В", 46: "в", 47: "Г", 48: "г", 49: "Д", 50: "д",
                        51: "Е", 52: "е", 53: "Ё", 54: "ё", 55: "Ж", 56: "ж", 57: "З", 58: "з", 59: "И", 60: "и",
                        61: "Й", 62: "й", 63: "К", 64: "к", 65: "Л", 66: "л", 67: "М", 68: "м", 69: "Н", 70: "н",
                        71: "О", 72: "о", 73: "П", 74: "п", 75: "Р", 76: "р", 77: "С", 78: "с", 79: "Т", 80: "т",
                        81: "У", 82: "у", 83: "Ф", 84: "ф", 85: "Х", 86: "х", 87: "Ц", 88: "ц", 89: "Ч", 90: "ч",
                        91: "Ш", 92: "ш", 93: "Щ", 94: "щ", 95: "Ь", 96: "ь", 97: "Ы", 98: "ы", 99: "Ъ", 100: "ъ",
                        101: "Э", 102: "э", 103: "Ю", 104: "ю", 105: "Я", 106: "я"}
        self.con = sqlite3.connect("datasets.db")
        self.ids = self.con.execute("SELECT id FROM matches").fetchall()

    def __getitem__(self, item_id):

        row_id = self.ids[item_id][0]
        data = self.con.execute(f"SELECT * FROM matches WHERE id={row_id}").fetchone()
        sample = torch.tensor(self.text_to_tensor(data[1], input_neurons), dtype=torch.float32)
        target = torch.tensor(self.text_to_tensor(data[0], int(input_neurons * 1.1)), dtype=torch.float32)
        return sample, target

    def text_to_tensor(self, text, tensor_len):
        tensor = []
        for i in text:
            for j in self.ru_dict:
                if self.ru_dict[j] == i:
                    tensor.append(j)

        while len(tensor) < tensor_len:
            tensor.append(34)

        # print(len(tensor))
        return tensor

    def __len__(self):
        return len(self.ids)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(device)
dataset = DB_connect()
model = Perceptron(input_neurons, hiden_layers_num).to(device)
torch.save(model.state_dict(), r"C:\Users\student.CLUMBA.013\PycharmProjects\pythonProject\MAP_V1.8.pt")
model.share_memory()
train_data, val_data = random_split(dataset, [0.5, 0.5])

train_loader = DataLoader(train_data, batch_size=1, shuffle=True, num_workers=1)
val_loader = DataLoader(val_data, batch_size=1, shuffle=False, num_workers=1)
# dataset.close_connection()


def use_neuro(command1, command2, date, model):

    tensor_com1 = dataset.text_to_tensor(command1, 50)
    tensor_com2 = dataset.text_to_tensor(command2, 50)
    date = str(date)
    year, month, day = date.split("-")

    for i in tensor_com2:
        tensor_com1.append(i)
    tensor_com1.append(int(day))
    tensor_com1.append(int(month))
    tensor_com1.append(int(int(year) % 100))
    sample = torch.tensor(tensor_com1, dtype=torch.float32)
    results = torch.Tensor.tolist(model(sample))
    winner = command1
    if results[1] > results[0]:
        winner = command2

    return round(results[0], 2) * 100, round(results[1], 2) * 100, winner

loss = nn.MSELoss(reduction="sum")
opt = Adam(params=model.parameters(), lr=lr)


if mode == "use" and PATH:
    model.load_state_dict(torch.load(PATH, weights_only=True))
    model.eval()
    # print(use_neuro(input("Введите название первой комманды: "), input("Введите название второй комманды: "),
    #                         input("Введите дату проведения матча(дд.мм.гггг): "), model))
elif mode == "learn":
    path = r"C:\Users\student.CLUMBA.001\PycharmProjects\pythonProject\MAP_V1.8.pt"
    torch.save(model.state_dict(), path)
    # for i in range(int(n_epochs / num_processes)):
    #     train()
    for epochs in range(n_epochs):
        model.train()

        train_loop = tqdm(train_loader, leave=True)
        running_train_loss = []
        mean_train_loss = 100
        count = 0
        for x, targets in train_loop:
            try:
                opt.zero_grad()
                # print("a")
                x = x.reshape([-1, input_neurons]).to(device)
                targets = targets.reshape([-1, int(input_neurons * 1.1)]).to(torch.float32).to(device)
                pred = model(x).to(torch.float32)
                # print(pred.shape)
                # print(targets.shape)
                pred = pred.reshape([-1, int(input_neurons * 1.1)]).to(torch.float32)
                targets = targets.reshape([-1, int(input_neurons * 1.1)]).to(torch.float32)
                train_loss = loss(
                    pred,
                    targets
                )  #  / pred.shape([0])

                train_loss.backward()
                opt.step()

                running_train_loss.append(train_loss.item())
                mean_train_loss = sum(running_train_loss) / len(running_train_loss)
                train_loop.set_description(f"Epoch [{epochs + 1} / {n_epochs}], train_loss={mean_train_loss:.4f}")
                # num += 1
                # if num % 100000:
                #     print(num)
            except Exception as e:
                print(e)
                count += 1

        model.eval()
        running_train_loss = []
        mean_train_loss = 100
        count = 0
        with torch.no_grad():
            for x, targets in val_loader:
                try:
                    x = x.reshape([-1, input_neurons]).to(device)

                    targets = targets.reshape([-1, int(input_neurons * 1.1)]).to(torch.float32).to(device)
                    pred = model(x).to(torch.float32)
                    # print(pred.shape)
                    # print(targets.shape)
                    train_loss = loss(
                        pred,
                        targets
                    )
                    running_train_loss.append(train_loss.item())
                    mean_train_loss = sum(running_train_loss) / len(running_train_loss)
                    train_loop.set_description(f"Epoch [{epochs + 1} / {n_epochs}], train_loss={mean_train_loss:.4f}")

                except Exception as e:
                    print(e)
                    count += 1

        try:

            if epochs % save_every == 1:
                path = r"C:\Users\student\CLUMBA.001\PycharmProjects\model\MAP_V1.8.pt"
                torch.save(model.state_dict(), path)
        except Exception as e:
            print(e)

# [0.48510250449180603, 0.5148975849151611]
# 00.000.00000000