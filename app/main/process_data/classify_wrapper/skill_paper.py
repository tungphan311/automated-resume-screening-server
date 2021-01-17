import spacy
from nltk import RegexpParser, tree
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
import itertools
from app.main.process_data.classifier.paper import Paper

GRAMMAR = r"""
DBW_CONCEPT: {<JJ.*>*<HYPH>*<JJ.*>*<HYPH>*<NN.*>*<HYPH>*<NN.*>+}
""" #good for syntactic
# DBW_CONCEPT: {<NN><$>}

class SkillPaper(Paper):
    """ 
    A simple subclass of Paper.
    Preprocess preprocess for extract skill-terms.
    """
    def set_paper(self, paper):
        """Function that initializes the paper variable in the class.

        Args:
            paper (either string or dictionary): The paper to analyse. It can be a full string in which the content
            is already merged or a dictionary  {"title": "","abstract": "","keywords": ""}.

        """
        self.title = None
        self.abstract = None
        self.keywords = None
        self._text = None
        self.semantic_chunks = None
        self.syntactic_chunks = None
        
        try:
            if isinstance(paper, dict):              
                for attr in self.text_attr:
                    try: 
                        setattr(self, attr, paper[attr])
                    except KeyError:
                        continue
                    
                self.treat_keywords()
                self.text()
                
            elif isinstance(paper, str):
                self._text = paper.strip()
            
            else:
                raise TypeError("Error: Unrecognised paper format")
                return
        
            self._text = '. '.join([s for s in self._text.split('\n') if s is not None or s != ""])
            self._text = self._text.replace('/', ', ')
            self.pre_process()
            
        except TypeError:
            pass

    def extraxt_syntactic_chuncks(self, document):
        """ Extract chunks of text from the paper, using stopwords and comma as delimiter.
        This modification will also remain some specified punction for programming languages.
        Returns:
            chunks (list): list of all chunks of text 
        """
        tokenizer = RegexpTokenizer(r'[\w\-\.+#]+|,')
        tokens = tokenizer.tokenize(document)
        filtered_words = [a for a in [w if w not in stopwords.words('english') and w != ',' else ':delimiter:' for w in tokens] if a != '']
        matrix_of_tokens = [list(g) for k,g in itertools.groupby(filtered_words,lambda x: x == ':delimiter:') if not k]
        return [" ".join(row).lower() for row in matrix_of_tokens]

    def extraxt_semantic_chuncks(self, pos_tags):
        """ Extract chunks of text from the paper taking advantage of the parts of speech previously extracted.
        It uses a grammar
        Returns:
            chunks (list): list of all chunks of text 
        """
        grammar_parser = RegexpParser(GRAMMAR)
        chunks = list()
        pos_tags_with_grammar = grammar_parser.parse(pos_tags)
        #print(pos_tags_with_grammar)
        for node in pos_tags_with_grammar:
            if isinstance(node, tree.Tree) and node.label() == 'DBW_CONCEPT': # if matches our grammar 
                chunk = ''
                for leaf in node.leaves():
                    concept_chunk = leaf[0]
                    concept_chunk = re.sub('[\=\,\…\’\'\“\”\"\/\‘\[\]\®\™\%]', ' ', concept_chunk)
                    concept_chunk = re.sub('\.$', '', concept_chunk)
                    concept_chunk = concept_chunk.lower().strip()
                    chunk += ' ' + concept_chunk
                chunk = re.sub('\.+', '.', chunk)
                chunk = re.sub('\s+', ' ', chunk)
                chunks.append(chunk)
        return chunks


    