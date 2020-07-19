from certifai.model.sdk import SimpleModelWrapper, ComposedModelWrapper
import pickle
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def start():
    composed_app = ComposedModelWrapper(port=5111)
    apps = {}

    # Load each trained model, wrap it and add it to the composed app
    for model in ['dtree', 'logit', 'mlp', 'svm']:
        with open(f'{dir_path}/../models/german_credit_{model}.pkl', 'rb') as f:
            saved = pickle.load(f)
        app = SimpleModelWrapper(
            model=saved.get('model'),
            encoder=saved.get('encoder', None))
        # setup the predict endpoint route for each model
        composed_app.add_wrapped_model(f'/german_credit_{model}', app)

    composed_app.run()


if __name__ == '__main__':
    start()
