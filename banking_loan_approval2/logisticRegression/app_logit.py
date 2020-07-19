from certifai.model.sdk import SimpleModelWrapper
import pickle


def start():
    model_file = '../models/german_credit_logit.pkl'
    try:
        with open(model_file, 'rb') as f:
            saved = pickle.load(f)
            model = saved.get('model')
            encoder = saved.get('encoder', None)
    except FileNotFoundError as e:
        print(f"Model pkl file {model_file} does not exist - run ../train.py first")
        exit(1)

    app = SimpleModelWrapper(model=model, encoder=encoder)
    app.run()

if __name__ == '__main__':
    start()
