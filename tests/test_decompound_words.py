from unittest import TestCase

from search_client.constants import DocumentTypes
from search_client.opensearch.indices.products import build_products_index_configuration
from search_client.opensearch.indices.legacy import create_open_search_index_configuration


class BaseDecompoundWordsTestCase(TestCase):
    """
    Github Actions does not support mounting docker volumes
    So it is impossible to mount a decompound dictionary and truly test this
    Instead we test that indices will get created correctly and composed word search should function
    """

    document_type = None

    def _test_decompound_word_multilingual_indices(self):
        dutch_index = create_open_search_index_configuration("nl", self.document_type, "dutch-decompound-words.txt")
        self.assertIn("dutch_dictionary_decompound", dutch_index["settings"]["analysis"]["analyzer"])
        decompound_analyser = dutch_index["settings"]["analysis"]["analyzer"]["dutch_dictionary_decompound"]
        self.assertEqual(decompound_analyser, {
            'type': 'custom',
            'tokenizer': 'standard',
            'filter': [
                'lowercase',
                'dutch_stop',
                'dutch_synonym',
                'dictionary_decompound'
            ]
        })
        self.assertIn("dictionary_decompound", dutch_index["settings"]["analysis"]["filter"])
        decompound_filter = dutch_index["settings"]["analysis"]["filter"]["dictionary_decompound"]
        self.assertEqual(decompound_filter, {
            "type": "dictionary_decompounder",
            "word_list_path": "dutch-decompound-words.txt",
            "updateable": True,
            "only_longest_match": True,
            "min_word_size": 8,
            "min_subword_size": 5
        })
        for text_field in ["title", "text", "description"]:
            self.assertEqual(dutch_index["mappings"]["properties"][text_field]['fields']['analyzed']["analyzer"],
                             "custom_dutch")
            self.assertEqual(dutch_index["mappings"]["properties"][text_field]['fields']['analyzed']["search_analyzer"],
                             "dutch_dictionary_decompound")

        english_index = create_open_search_index_configuration("en", self.document_type)
        self.assertNotIn("dutch_dictionary_decompound", english_index["settings"]["analysis"]["analyzer"])
        self.assertNotIn("dictionary_decompound", english_index["settings"]["analysis"]["filter"])
        for text_field in ["title", "text", "description"]:
            self.assertEqual(
                english_index["mappings"]["properties"][text_field]['fields']['analyzed']["analyzer"],
                "english"
            )
            self.assertEqual(
                english_index["mappings"]["properties"][text_field]['fields']['analyzed']["search_analyzer"],
                "english"
            )

    def _test_decompound_word(self):
        index = build_products_index_configuration(self.document_type, "dutch-decompound-words.txt")
        self.assertIn("dutch_dictionary_decompound", index["settings"]["analysis"]["analyzer"])
        decompound_analyser = index["settings"]["analysis"]["analyzer"]["dutch_dictionary_decompound"]
        self.assertEqual(decompound_analyser, {
            'type': 'custom',
            'tokenizer': 'standard',
            'filter': [
                'lowercase',
                'dutch_stop',
                'dutch_synonym',
                'dictionary_decompound'
            ]
        })
        self.assertIn("dictionary_decompound", index["settings"]["analysis"]["filter"])
        decompound_filter = index["settings"]["analysis"]["filter"]["dictionary_decompound"]
        self.assertEqual(decompound_filter, {
            "type": "dictionary_decompounder",
            "word_list_path": "dutch-decompound-words.txt",
            "updateable": True,
            "only_longest_match": True,
            "min_word_size": 8,
            "min_subword_size": 5

        })
        nl_texts = index["mappings"]["properties"]["texts"]["properties"]["nl"]["properties"]
        en_texts = index["mappings"]["properties"]["texts"]["properties"]["en"]["properties"]
        unk_texts = index["mappings"]["properties"]["texts"]["properties"]["unk"]["properties"]
        for text_field in ["titles", "subtitles", "descriptions", "contents", "transcriptions"]:
            self.assertEqual(nl_texts[text_field]["properties"]["text"]['fields']['analyzed']["analyzer"],
                             "custom_dutch")
            self.assertEqual(nl_texts[text_field]["properties"]["text"]['fields']['analyzed']["search_analyzer"],
                             "dutch_dictionary_decompound")
            self.assertEqual(
                en_texts[text_field]["properties"]["text"]['fields']['analyzed']["analyzer"],
                "english"
            )
            self.assertEqual(
                unk_texts[text_field]["properties"]["text"]['fields']['analyzed']["analyzer"],
                "standard"
            )


class TestLearningMaterialDecompoundWords(BaseDecompoundWordsTestCase):
    document_type = DocumentTypes.LEARNING_MATERIAL

    def test_decompound_word_multilingual_indices(self):
        self._test_decompound_word_multilingual_indices()

    def test_decompound_word(self):
        self._test_decompound_word()


class TestResearchProductDecompoundWords(BaseDecompoundWordsTestCase):
    document_type = DocumentTypes.RESEARCH_PRODUCT

    def test_decompound_word_multilingual_indices(self):
        self._test_decompound_word_multilingual_indices()

    def test_decompound_word(self):
        self._test_decompound_word()
