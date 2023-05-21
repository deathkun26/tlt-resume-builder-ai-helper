from model.Gramformer.gramformer import Gramformer

# 0 = detector, 1 = highlighter, 2 = corrector, 3 = all

class GrammarCorrect:
    def __init__(self):
        self.gf = Gramformer(models=1, use_gpu=False)

    def correct(self, sentences):
        outputs = []
        for sentence in sentences:
            res = self.gf.correct(sentence,  max_candidates=1)
            outputs += list(res)
        return outputs

# class GrammarCorrect:
#     def __init__(self):
#         print("!!! use fake gramformer !!!")
    
#     def correct(self, sentences):
#         return sentences