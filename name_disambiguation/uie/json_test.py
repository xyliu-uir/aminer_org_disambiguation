from paddlenlp import Taskflow
from pprint import pprint
import json

# en = "huazhong university of science and technology(huazhong university of science and technology,huazhong univ. of sci. and technol.),wuhan,china"
# schema = ["primary organization", "secondary organization", "tertiary organization", "city", "postal code", "country"]
# ie = Taskflow("information_extraction", schema=schema, model="uie-base-en")
# pprint(ie(en))

data = [{'city': [{'end': 134,
                   'probability': 0.9992363412030443,
                   'start': 129,
                   'text': 'wuhan'}],
         'country': [{'end': 140,
                      'probability': 0.9999805689651851,
                      'start': 135,
                      'text': 'china'}],
         'primary organization': [{'end': 91,
                                   'probability': 0.8742967328466733,
                                   'start': 46,
                                   'text': 'huazhong university of science and '
                                           'technology'},
                                  {'end': 45,
                                   'probability': 0.9770061605329516,
                                   'start': 0,
                                   'text': 'huazhong university of science and '
                                           'technology'}],
         'secondary organization': [{'end': 91,
                                     'probability': 0.8234314254530943,
                                     'start': 46,
                                     'text': 'huazhong university of science and '
                                             'technology'},
                                    {'end': 45,
                                     'probability': 0.9769097559485473,
                                     'start': 0,
                                     'text': 'huazhong university of science and '
                                             'technology'}],
         'tertiary organization': [{'end': 91,
                                    'probability': 0.8570237327323476,
                                    'start': 46,
                                    'text': 'huazhong university of science and '
                                            'technology'},
                                   {'end': 127,
                                    'probability': 0.5390083447290763,
                                    'start': 92,
                                    'text': 'huazhong univ. of sci. and technol.'},
                                   {'end': 45,
                                    'probability': 0.9827001968064124,
                                    'start': 0,
                                    'text': 'huazhong university of science and '
                                            'technology'}]}]


print(type(json.loads(data)))