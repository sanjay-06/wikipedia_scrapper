from core.scrap import Scrapper, Parser
import pickle5
import time

class Classifier:
    pipe = pickle5.load(open("./model/pipe", "rb"))
    pca = pickle5.load(open("./model/pca", "rb"))
    model = pickle5.load(open("./model/model", "rb"))

    @staticmethod
    def predict_class(link: str):
        page_html = Scrapper.load_page(link)
        page_text = [Parser.parse_html_text(page_html)]

        tfidf_text = Classifier.pipe.transform(page_text)
        pca_tfidf_text = Classifier.pca.transform(tfidf_text.toarray())

        output_class = Classifier.model.predict(pca_tfidf_text)
        return output_class
    
    @staticmethod
    def get_utilities(text_list, class_):
        print("Start of get_utilities")
        import time
        t = time.time()
        tfidf_text = Classifier.pipe.transform(text_list)
        print(f"After pipe: {time.time() - t}")
        pca_tfidf_text = Classifier.pca.transform(tfidf_text.toarray())
        print("After pca")

        index = list(Classifier.model.classes_).index(class_)

        print(f"Predicting probabilities for {len(pca_tfidf_text)} rows")
        t = time.time()
        probabilities = Classifier.model.predict_proba(pca_tfidf_text)
        print(f"Done: {time.time() - t}")

        return [probability[index] for probability in probabilities]




