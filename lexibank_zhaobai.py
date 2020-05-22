import attr
from pathlib import Path

from pylexibank import Concept, Language, FormSpec
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar

from clldutils.misc import slug


@attr.s
class CustomConcept(Concept):
    Chinese_Gloss = attr.ib(default=None)
    Number = attr.ib(default=None)


@attr.s
class CustomLanguage(Language):
    Latitude = 25.5844078
    Longitude = 100.3117 
    ChineseName = "趙莊白語"
    SubGroup = "Bai"
    Family = "Sino-Tibetan"
    DialectGroup = "Southern Bai"


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "zhaobai"
    concept_class = CustomConcept
    language_class = CustomLanguage
    form_spec = FormSpec(
            separators=';/,',
            )

    def cmd_makecldf(self, args):
        args.writer.add_sources()

        # TODO: add concepts with `add_concepts`
        args.writer.add_language(
                ID='ZhaozhuangBai',
                Glottocode='dali1242',
                Name='Zhaozhuang Bai')

        for concept in self.conceptlists[0].concepts.values():
            idx = concept.number + "_" + slug(concept.gloss)
            args.writer.add_concept(
                ID=idx,
                Name=concept.gloss,
                Chinese_Gloss=concept.attributes["chinese"],
                Number=concept.number,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
            )
            args.writer.add_forms_from_value(
                    Language_ID='ZhaozhuangBai',
                    Parameter_ID=idx,
                    Value=concept.attributes['form'],
                    Source="Zhao2006"
                    )

