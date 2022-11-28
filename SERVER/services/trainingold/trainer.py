import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import model_from_json
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam


def train():
    path = "./services/tmp/"
    for expression in os.listdir(path+"train/"):
        print(str(len(os.listdir(path+"train/" + expression))) + " " + expression + " images")
    
    img_size = 48
    batch_size = 64
    
    datagen_train = ImageDataGenerator(horizontal_flip=True)
    
    train_generator = datagen_train.flow_from_directory(path+"train/",
                                                        target_size=(img_size,img_size),
                                                        color_mode="grayscale",
                                                        batch_size=batch_size,
                                                        class_mode='categorical',
                                                        shuffle=True)
    
    datagen_validation = ImageDataGenerator(horizontal_flip=True)
    validation_generator = datagen_validation.flow_from_directory(path+"test/",
                                                        target_size=(img_size,img_size),
                                                        color_mode="grayscale",
                                                        batch_size=batch_size,
                                                        class_mode='categorical',
                                                        shuffle=False)
    
    model = 0
    model_json_file = "./model.json"
    with open(model_json_file, "r") as json_file:
        loaded_model_json = json_file.read()
        model = model_from_json(loaded_model_json)                                                  
    opt = Adam(lr=0.0005)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    
    epochs = 25
    steps_per_epoch = train_generator.n//train_generator.batch_size
    validation_steps = validation_generator.n//validation_generator.batch_size
    
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1,
                                  patience=2, min_lr=0.00001, mode='auto')
    checkpoint = ModelCheckpoint("model_weights.h5", monitor='val_accuracy',
                                 save_weights_only=True, mode='max', verbose=1)
    #callbacks = [PlotLossesCallback(), checkpoint, reduce_lr]
    
    history = model.fit(
        x=train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=epochs,
        validation_data = validation_generator,
        validation_steps = validation_steps
    )
