from Model import Model, train_models
import pickle
import numpy as np
import os, sys


class Predictor:
    def __init__(self, vetorice="tfidf"):
        self.traits = ["OPN", "CON", "EXT", "AGR", "NEU"]
        self.models = {}
        self.modelsreg = {}
        self.vetorice = vetorice
        self.load_models()
        self.dicname = {
            "sOPN": "Trait Score of Openness",
            "prob_cOPN": "Probability of trait of Openness",
            "cOPN": "Trait Category  of Openness",
            "sCON": "Trait Score of concienstiouness",
            "prob_cCON": "Probability of trait of concienstiouness",
            "cCON": "Trait Category  of Conscientiousness",
            "sEXT": "Trait Score of Extraversion",
            "prob_cEXT": "Probability of trait of Extraversion",
            "cEXT": "Trait Category  of Extraversion",
            "sAGR": "Score of Agreeableness",
            "prob_cAGR": "Probability of trait of Agreeableness",
            "cAGR": "Trait Category  of Agreeableness",
            "sNEU": "Trait Score of Neuroticism ",
            "prob_cNEU": "Probability of trait of Neuroticism",
            "cNEU": "Trait Category  of Neuroticism",
        }

    def load_models(self):
        r = ["categorical", "regression"]
        for trait in self.traits:
            with open(
                "models/{1}_categorical_model_{0}.pkl".format(self.vetorice, trait),
                "rb",
            ) as f:
                self.models[trait] = pickle.load(f)

    def predict(self, X, traits="All", predictions="All"):
        predictions = {}
        if traits == "All":
            for trait in self.traits:
                pkl_model = self.models[trait]

                trait_scores = pkl_model.predict(X, regression=True).reshape(1, -1)
                predictions["pred_s" + trait] = trait_scores.flatten()[0]

                trait_categories_probs = pkl_model.predict_proba(X)
                predictions["pred_prob_c" + trait] = trait_categories_probs[:, 1][0]

                trait_categories = pkl_model.predict(X, regression=False)
                predictions["pred_c" + trait] = str(trait_categories[0])

            result = self.print_Pred(predictions, X)
            # resultant = self.print_val(predictions, X)
            return result
            
    def predicts(self, X, traits="All", predictions="All"):
        predictions = {}
        if traits == "All":
            for trait in self.traits:
                pkl_model = self.models[trait]

                trait_scores = pkl_model.predict(X, regression=True).reshape(1, -1)
                predictions["pred_s" + trait] = trait_scores.flatten()[0]

                trait_categories_probs = pkl_model.predict_proba(X)
                predictions["pred_prob_c" + trait] = trait_categories_probs[:, 1][0]

                trait_categories = pkl_model.predict(X, regression=False)
                predictions["pred_c" + trait] = str(trait_categories[0])

            # result = self.print_Pred(predictions, X)
            resultant = self.print_val(predictions, X)

        return resultant

    def print_Pred(self, prediction, X):
        result = []
        result.append("Evaluated Text: " + X[0])
        ind = 0
        for t, v in prediction.items():
            s = t.split("_")
            try:
                k = s[1] + "_" + s[2]
            except:
                k = s[1]
            if ind % 3 == 0:
                print(s, "pip", t)
                text = "Prediction  " + str(self.dicname[k]) + " is -> :  " + str(v)
            print(text + ": \n" + "\n")
            result.append(text)
        return result
    
    def print_val(self, prediction, X):
        result = []
        print("Evaluated Text: " + X[0])
        ind = 0
        for t, v in prediction.items():
            s = t.split("_")
            try:
                k = s[1] + "_" + s[2]
            except:
                k = s[1]
            if ind % 3 == 0:
                print(s, "pip", t)
                text = str(v)
            print(text +  "\n")
            result.append(text)
        return result


if __name__ == "__main__":
    P = Predictor()
