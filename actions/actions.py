# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import yaml
from typing import Any, Text, Dict, List
from os import path
from os.path import exists, isfile
from yaml.representer import SafeRepresenter

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


class folded_str(str): pass


class literal_str(str): pass


def change_style(style, representer):
    def new_representer(dumper, data):
        scalar = representer(dumper, data)
        scalar.style = style
        return scalar
    return new_representer


represent_folded_str = change_style('>', SafeRepresenter.represent_str)
represent_literal_str = change_style("|", SafeRepresenter.represent_str)

yaml.add_representer(folded_str, represent_folded_str)
yaml.add_representer(literal_str, represent_literal_str)


def add_example(filepath: str, new_example: str, intent_name: str = None):
    filepath, _ = path.splitext(filepath)

    if exists(filepath + '.yml'):
        filepath = filepath + '.yml'
    elif exists(filepath + '.yaml'):
        filepath = filepath + '.yaml'

    if not exists(filepath):
        raise Exception(f'Filepath {filepath} not exist')

    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)

    if intent_name is None and len(data['nlu']) != 1:
        raise Exception(f'File contains more than 1 intent. specify the intent_name parameter')

    for item in data['nlu']:
        item['examples'] = [example.strip('\n').strip() for example in item['examples'].split('- ') if example]

        if item['intent'] == intent_name or intent_name is None:
            item['examples'] = literal_str('- ' + '\n- '.join(item['examples']) + f'\n- {new_example}')

    with open(filepath, 'w') as f:
        yaml.dump(data, f, sort_keys=False, default_flow_style=False, Dumper=IndentDumper, allow_unicode=True)


class ActionGetConfidence(Action):
    def name(self) -> Text:
        return "action_get_confidence"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        confidence = round(tracker.latest_message['intent'].get('confidence') * 100, 2)

        dispatcher.utter_message(text=f'{confidence}%')

        return []


class ActionAddExample(Action):
    def name(self) -> Text:
        return "action_add_example"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_events = [event for event in tracker.events if event['event'] == 'user']

        new_examples = user_events[-3]['parse_data']['text']
        intent_name = user_events[-1]['parse_data']['text']

        filepath = f'data/nlu/{intent_name}'

        add_example(filepath, new_examples)

        dispatcher.utter_message(text=f'Example {new_examples} added to intent {intent_name} examples.')

        return []
