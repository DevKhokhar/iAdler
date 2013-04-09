from mail_insights.models import Annotation,TextProcessor
from mbox_processor.models import MailThread
from collections import defaultdict,OrderedDict
#from numpy import array

class UnigramDistribution():

    class Meta:
        app_label = 'mail_insights'

    @staticmethod
    def increment_distribution(distribution,key):
        distribution[key] += 1

    #@staticmethod
    #def get_weight(weighted_annotation,vector_candidates):
        #if(weighted_annotation.word in vector_candidates):
            #return weighted_annotation.tfidf()
        #else:
            #return 0

    @staticmethod
    def generate_tf(documents):
        tf = defaultdict(int)
        for document in documents:
            tokens = TextProcessor().extract_nouns(document)
            [UnigramDistribution.increment_distribution(tf,token) for token in tokens]
        return tf

    @staticmethod
    def generate_df(documents):
        df = defaultdict(int)
        for document in documents:
            tokens =  TextProcessor().extract_nouns(document)
            [UnigramDistribution.increment_distribution(df,token) for token in OrderedDict.fromkeys(tokens).keys()]
        return df

    @staticmethod
    def generate_tf_df_for_mail_threads():
        Annotation.objects.delete()       
        all_mails = reduce(lambda x,y: x+y,map(lambda x: x.mails,MailThread.objects()))
        documents = map(lambda x: x.subject + "\n" + x.body,all_mails)
        tf = UnigramDistribution.generate_tf(documents)
        df = UnigramDistribution.generate_df(documents)
        for token in tf.keys():
            annotation = Annotation(word=token,term_frequency=tf[token],document_frequency=df[token],word_type=Annotation.WORD_TYPE[0][0])
            annotation.save()

    @staticmethod
    def max_tfidf():
        max_tfidf = -1
        annotations = Annotation.objects()
        for annotation in annotations:
            tfidf = annotation.tfidf()
            max_tfidf = tfidf if max_tfidf < tfidf else max_tfidf
        return max_tfidf

    #@staticmethod
    #def generate_vector(text,corpus_tokens):
        #Assumption: the unigram distribution of annotations is modelled into VS. Space is defined by dimension number which is in the DB record
        #annotations = Annotation.objects.filter(word__in=corpus_tokens)
        #tokens = TextProcessor().tokenize(text)
        #vector_array = map(lambda annotation: UnigramDistribution.get_weight(annotation,tokens),annotations)
        #return array(vector_array)
