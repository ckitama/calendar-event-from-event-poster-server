from collections import defaultdict
from textblob import TextBlob
import en_core_web_sm

from swagger_server.api import estnlp_api
from swagger_server.models import GenericNerResultDto


def find_generic_ner(text_fragments):
    found_named_entities = defaultdict(list)

    nlp = en_core_web_sm.load()

    for text_fragment in text_fragments:
        blob = TextBlob(text_fragment)
        language = blob.detect_language()
        print("detected language:", language)
        try: # translate to english
            text_fragment = str(blob.translate(to='en'))
        except: # text already in english
            pass

        print("text_fragment for analysis:", text_fragment)

        doc = nlp(text_fragment)
        # print([(X.text, X.label_) for X in doc.ents])
        named_entity_pairs = [(X.text, X.label_) for X in doc.ents]
        for named_entity in named_entity_pairs:
            found_named_entities[named_entity[1].lower()].append(named_entity[0])

    try:
        # try translating to estonian
        joined_fragments = " ".join(text_fragments)
        blob = TextBlob(joined_fragments)
        text_fragments_in_estonian = str(blob.translate(to='et'))
        # get start and end time from estnlp_api
        start, end = estnlp_api.get_normalized_start_end(text_fragments_in_estonian)
        found_named_entities["start"] = start
        found_named_entities["end"] = end
    except:
        pass

    generic_ner_result_dto = GenericNerResultDto().from_dict(found_named_entities)
    return generic_ner_result_dto

# find_generic_ner(["ööbikuoru villas rouges 16. augustil 2020 kell 18.00 aan alte akustiline kontsert Sbiad teiega en hea"])
# find_generic_ner(["Concert in Dublin 17 March, Royal Festival Hall 6 p.m."])
# print(find_generic_ner(["Concert in Dublin 17 March, Royal Festival Hall 6 p.m."]))