*DigitRecognizer* - мы распознаем ваши цифры!
-------------

Наше приложение сможет распознавать рукописные цифры с помощью CNN *(Convolutional Neural Network)*. Предварительное обучение происходит на базе данных MNIST, точность распознания тестовых данных около **98%** после десяти циклов.

Для корректной работы программы необходимо иметь установленные библиотеки tensorflow 2.0.0 (!), cv2, h5py и PyQT5. 

Ход действий:
1. Скачать из репозитория файлы mnist_trainedCNN.py, test.py, window.py, web.jpg. 
2. Запустить файл window.py. 
3. Нарисовать в белом окошке цифру с помощью мышки или тачпада.
4. Нажать кнопку “Обработать изображение”.
5. При выведении ошибки “Нейросеть не обучена!” закрыть диалоговое окно с ошибкой и нажать кнопку “Обучить сеть”. После получения диалогового окна “Сеть обучена!” закрыть его и снова нажать кнопку “Обработать изображение”. Обучение сети может занимать до десяти минут.


![Коротко о нашей нейросетке](https://github.com/ksyu-zait/project_2020/blob/master/24NgYdXNMho.jpg)
