# ------------------------------------------
# 
# Program created by Maksim Kumundzhiev
#
#
# email: kumundzhievmaxim@gmail.com
# github: https://github.com/KumundzhievMaxim
# -------------------------------------------

import sys
import numpy as np
from learning_functions.perform_learning import perform_learning
from keras_models.detection import detection_unet


model_params = {'kernel_size': (3, 3, 3),
                'filters': 16,
                'weights': np.array([0.1, 0.9]),
                'learning_rate': 0.001}

perform_learning(training_sample_dir=sys.argv[1],
                 val_sample_dir=sys.argv[2],
                 batch_size=16,
                 three_d=True,
                 sample_channels=1,
                 categorise=True,
                 output_classes=2,
                 model_func=detection_unet,
                 model_params=model_params,
                 epochs=50,
                 model_path=sys.argv[3],
                 checkpoint_path="checkpoints/detection_model/detection_model.{epoch:02d}.h5",
                 log_name="detection",
                 shuffle=True)