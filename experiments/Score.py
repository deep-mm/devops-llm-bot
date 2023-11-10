from difflib import SequenceMatcher
from nltk.translate.bleu_score import sentence_bleu

def get_exact_match_score (generated_workflow_file_content, actual_workflow_file_content):
    return SequenceMatcher(None, generated_workflow_file_content, actual_workflow_file_content).ratio()

def get_bleu_score (generated_workflow_file_content, actual_workflow_file_content):
    return sentence_bleu([generated_workflow_file_content], actual_workflow_file_content)