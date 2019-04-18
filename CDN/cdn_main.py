"""
CDN Main functionality

Contains code to
- process a training datasets
- train a model
- perform predictions

"""

# Imports
import tensorflow as tf
import pandas as pd
from CDN.model.architectures import architectures
from CDN.model.cdn import CDN

"""
PARAMETERS
"""
# ==========================================#

# Extract architectures
M256_HIDDEN_UNITS = architectures['m256'][0]
M512_HIDDEN_UNITS = architectures['m512'][0]
M1024_HIDDEN_UNITS = architectures['m1024'][0]
M256_DO_RATES = architectures['m256'][1]
M512_DO_RATES = architectures['m512'][1]
M1024_DO_RATES = architectures['m1024'][1]


# ==========================================#


def training(data_path, train_datasets, model_dir, batch_size, learning_rate, num_steps):
    """
    Perform training of three a CDN model ensemble consisting of three different models
    :param model_dir:
    :param batch_size:
    :param learning_rate:
    :param num_steps:
    :return:
    """

    # M256 model training
    print("Training M256 Model ...")
    tf.reset_default_graph()
    with tf.Session() as sess:
        cdn256 = CDN(sess=sess,
                     model_dir=model_dir+"/m256",
                     model_name='m256',
                     batch_size=batch_size,
                     learning_rate=learning_rate,
                     num_steps=num_steps)
        cdn256.hidden_units = M256_HIDDEN_UNITS
        cdn256.do_rates = M256_DO_RATES
        cdn256.train(input_path=data_path, train_datasets=train_datasets)

    # Training of mid model
    print("Training M512 Model ...")
    tf.reset_default_graph()
    with tf.Session() as sess:
        cdn512 = CDN(sess=sess,
                     model_dir=model_dir+"/m512",
                     model_name='m512',
                     batch_size=batch_size,
                     learning_rate=learning_rate,
                     num_steps=num_steps)
        cdn512.hidden_units = M512_HIDDEN_UNITS
        cdn512.do_rates = M512_DO_RATES
        cdn512.train(input_path=data_path, train_datasets=train_datasets)

    # Training of large model
    print("Training M1024 Model ...")
    tf.reset_default_graph()
    with tf.Session() as sess:
        cdn1024 = CDN(sess=sess,
                      model_dir=model_dir+"/m1024",
                      model_name='m1024',
                      batch_size=batch_size,
                      learning_rate=learning_rate,
                      num_steps=num_steps)
        cdn1024.hidden_units = M1024_HIDDEN_UNITS
        cdn1024.do_rates = M1024_DO_RATES
        cdn1024.train(input_path=data_path, train_datasets=train_datasets)


def prediction(model_dir, data_path, out_name):
    """
    Perform prediction using a trained CDN ensemble
    :return:
    """
    preds_256 = None
    preds_512 = None
    preds_1024 = None


    # Small model predictions
    tf.reset_default_graph()
    with tf.Session() as sess:
        cdn256 = CDN(sess=sess,
                     model_dir=model_dir + "/m256",
                     model_name='m256')
        cdn256.hidden_units = M256_HIDDEN_UNITS
        cdn256.do_rates = M256_DO_RATES

        # Predict ratios
        preds_256 = cdn256.predict(input_path=data_path,  out_name='cdn_predictions_m256.txt')


    # Mid model predictions
    tf.reset_default_graph()
    with tf.Session() as sess:
        cdn512 = CDN(sess=sess,
                     model_dir=model_dir+"/m512",
                     model_name='m512')
        cdn512.hidden_units = M512_HIDDEN_UNITS
        cdn512.do_rates = M512_DO_RATES

        # Predict ratios
        preds_512 = cdn512.predict(input_path=data_path, out_name='cdn_predictions_m512.txt')

    # Large model predictions
    tf.reset_default_graph()
    with tf.Session() as sess:
        cdn1024 = CDN(sess=sess,
                      model_dir=model_dir+"/m1024",
                      model_name='m1024')
        cdn1024.hidden_units = M1024_HIDDEN_UNITS
        cdn1024.do_rates = M1024_DO_RATES

        # Predict ratios
        preds_1024 = cdn1024.predict(input_path=data_path, out_name='cdn_predictions_m1024.txt')

    # Average predictions
    preds = (preds_256 + preds_512 + preds_1024) / 3
    preds.to_csv(out_name, sep="\t")

    return None


