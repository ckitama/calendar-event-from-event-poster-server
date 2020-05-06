from textblob import TextBlob

from swagger_server.api import estnlp_api, genericnlp_api
# from swagger_server.api.estnlp_api import find_est_ner
# from swagger_server.api.genericnlp_api import find_generic_ner
from swagger_server.models import AutoNerResultDto


def find_auto_ner(text_fragments):
    text = " ".join(text_fragments)
    blob = TextBlob(text)
    language = blob.detect_language()
    print("detected language:", language)

    if language == "et":
        auto_ner_result_dto = map_result_from_estnlp_api(text_fragments)
    else:
        auto_ner_result_dto = map_result_from_genericnlp_api(text_fragments)

    return auto_ner_result_dto


def map_result_from_estnlp_api(text_fragments):
    est_ner_result_dto = estnlp_api.find_est_ner(text_fragments)
    to_dict = est_ner_result_dto.to_dict()
    auto_ner_result_dto = AutoNerResultDto().from_dict(to_dict)
    return auto_ner_result_dto


def map_result_from_genericnlp_api(text_fragments):
    generic_ner_result_dto = genericnlp_api.find_generic_ner(text_fragments)
    auto_ner_result_dto = map_generic_ner_result_dto_to_auto_ner_result_dto(generic_ner_result_dto)
    return auto_ner_result_dto


def map_generic_ner_result_dto_to_auto_ner_result_dto(generic_ner_result_dto):
    auto_ner_result_dto = AutoNerResultDto()

    auto_ner_result_dto.per = []
    if generic_ner_result_dto.person is not None:
        auto_ner_result_dto.per += generic_ner_result_dto.person
    if generic_ner_result_dto.event is not None:
        auto_ner_result_dto.per += generic_ner_result_dto.event
    if generic_ner_result_dto.product is not None:
        auto_ner_result_dto.per += generic_ner_result_dto.product
    if generic_ner_result_dto.work_of_art is not None:
        auto_ner_result_dto.per += generic_ner_result_dto.work_of_art
    if len(auto_ner_result_dto.per) == 0:
        auto_ner_result_dto.per = None

    auto_ner_result_dto.loc = []
    if generic_ner_result_dto.gpe is not None:
        auto_ner_result_dto.loc += generic_ner_result_dto.gpe
    if generic_ner_result_dto.loc is not None:
        auto_ner_result_dto.loc += generic_ner_result_dto.loc
    if len(auto_ner_result_dto.loc) == 0:
        auto_ner_result_dto.loc = None

    auto_ner_result_dto.org = []
    if generic_ner_result_dto.org is not None:
        auto_ner_result_dto.org += generic_ner_result_dto.org
    if generic_ner_result_dto.fac is not None:
        auto_ner_result_dto.org += generic_ner_result_dto.fac
    if generic_ner_result_dto.norp is not None:
        auto_ner_result_dto.org += generic_ner_result_dto.norp
    if len(auto_ner_result_dto.org) == 0:
        auto_ner_result_dto.org = None

    auto_ner_result_dto.start = generic_ner_result_dto.start
    auto_ner_result_dto.end = generic_ner_result_dto.end
    return auto_ner_result_dto


# print(find_auto_ner(["Concert in Dublin 17 March, Royal Festival Hall 6 p.m."]))
# print(find_generic_ner(["Concert in Dublin 17 March, Royal Festival Hall 6 p.m."]))

# print(find_est_ner(["ööbikuoru villas rouges 16. augustil 2020 kell 18.00 aan alte akustiline kontsert Sbiad teiega en hea"]))
# print(find_auto_ner(["ööbikuoru villas rouges 16. augustil 2020 kell 18.00 aan alte akustiline kontsert Sbiad teiega en hea"]))


