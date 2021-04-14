import numpy as np

def plot_results(filename):
        import matplotlib.pyplot as plt
        file = open(filename)  # loading and formatting data
        data = np.loadtxt(file, delimiter=",")
        file.close()
        loss = data[:, 0]
        acc = data[:, 1]

        plt.subplot(1, 2, 1)  # plotting data
        plt.gca().set_title("Loss")
        plt.plot(loss)
        plt.subplot(1, 2, 2)
        plt.gca().set_title("Accuracy")
        plt.plot(acc, color="green")
        plt.show()

plot_results("data.txt")