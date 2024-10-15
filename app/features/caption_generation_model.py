import os
import tensorflow as tf
import pickle

class CaptionGenerationModel:
    def __init__(self):
        # Get the absolute path of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        encoder_dir = os.path.join(current_dir, '..', '..', 'models', 'encoder')
        decoder_dir = os.path.join(current_dir, '..', '..', 'models', 'decoder')
        tokenizer_dir = os.path.join(current_dir, '..', '..', 'models', 'tokenizer.pickle')

        self.encoder = tf.keras.models.load_model(encoder_dir)
        self.decoder = tf.keras.models.load_model(decoder_dir)
        # Load tokenizer
        with open(tokenizer_dir, 'rb') as handle:
            self.tokenizer = pickle.load(handle)

    def evaluate(self, input, max_length=10):
        hidden = tf.zeros((1, 512))
        features = self.encoder(tf.expand_dims(input, axis=1))
        dec_input = tf.expand_dims([self.tokenizer.word_index['startseq']], 0)
        result = []

        for i in range(max_length):
            predictions, hidden, _ = self.decoder(dec_input, features, hidden)
            predicted_id = tf.random.categorical(predictions, 1)[0][0].numpy()
            
            if self.tokenizer.index_word[predicted_id] == 'endseq':
                break
            else:
                result.append(self.tokenizer.index_word[predicted_id])
            dec_input = tf.expand_dims([predicted_id], 0)

        return ' '.join(result)