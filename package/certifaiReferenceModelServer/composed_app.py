from certifai.model.sdk import SimpleModelWrapper, ComposedModelWrapper
import pickle
from pathlib import Path
from os import getenv
module_folder = Path(__file__).parent


def start():
    composed_app = ComposedModelWrapper(port= int(getenv('MODEL_PORT', 5111)))

    # Load each trained model, wrap it and add it to the composed app
    for model in ['dtree', 'logit', 'mlp', 'svm']:
        model_file = module_folder / f'models/german_credit_{model}.pkl'
        with open(model_file, 'rb') as f:
            saved = pickle.load(f)
        app = SimpleModelWrapper(
            model=saved.get('model'),
            encoder=saved.get('encoder', None))
        composed_app.add_wrapped_model(f'/german_credit_{model}', app)

    # TODO add others
    # TODO does this get too big by loading them all up front?

    composed_app.run()


if __name__ == '__main__':
    start()
