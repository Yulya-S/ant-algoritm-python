import matplotlib.pyplot as plt

fig = plt.figure(figsize=(20,2))

x = []
y = []
y2 = []
y3 = []
with open("result.txt", "r") as file:
    for i in file:
        data = i.split(" ")
        x.append(int(data[0]))
        y.append(int(data[1]))
        y2.append(float(data[2]))
        y3.append(float(data[3]))
        
plt.subplot(1, 3, 1)
plt.title('Суммарная длина пути муравья')
plt.xlabel("Номер муравья")
plt.ylabel("Длина пути")
plt.plot(x, y)

plt.subplot(1, 3, 2)
plt.title('Суммы феромонов')
plt.xlabel("Номер муравья")
plt.ylabel("Сумма феромонов")
plt.plot(x, y2)

plt.subplot(1, 3, 3)
plt.title('Произведение вероятностей')
plt.xlabel("Номер муравья")
plt.ylabel("Вероятности")
plt.plot(x, y3)

plt.subplots_adjust(wspace = 0.3)
plt.show()
