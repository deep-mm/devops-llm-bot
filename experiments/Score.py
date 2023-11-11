from difflib import SequenceMatcher
from nltk.translate.bleu_score import sentence_bleu
import yaml

def get_exact_match_score (generated_workflow_file_content, actual_workflow_file_content):
    return SequenceMatcher(None, generated_workflow_file_content, actual_workflow_file_content).ratio()

def get_bleu_score (generated_workflow_file_content, actual_workflow_file_content):
    return sentence_bleu([generated_workflow_file_content], actual_workflow_file_content)

def get_devops_aware_score (generated_workflow_file_content, actual_workflow_file_content):
    actual = yaml.safe_load(actual_workflow_file_content)
    generated = yaml.safe_load(generated_workflow_file_content)

    actual_jobs = actual['jobs']
    generated_jobs = generated['jobs']

    actual_jobs_names = [job_name for job_name in actual_jobs.keys()]
    generated_jobs_names = [job_name for job_name in generated_jobs.keys()]

    # Get list of steps
    actual_steps = []
    for job_name in actual_jobs_names:
        actual_steps += actual_jobs[job_name]['steps']

    generated_steps = []
    for job_name in generated_jobs_names:
        generated_steps += generated_jobs[job_name]['steps']

    # Get list of actions
    actual_steps_updated = []

    # For each step in generated step list, find the corresponding step in actual step list by nearest bleu score of step name
    for generated_step in generated_steps:
        actual_step_updated = max(actual_steps, key=lambda actual_step: sentence_bleu([generated_step], actual_step))
        actual_steps_updated.append(actual_step_updated)

    # Compare the steps in actual and generated steps list
    score = 0
    for actual_step, generated_step in zip(actual_steps_updated, generated_steps):
        # Check if step dictionary contains uses key
        if 'uses' in actual_step.keys() and 'uses' in generated_step.keys():
            if get_exact_match_score(actual_step['uses'], generated_step['uses']) > 0.5:
                score += get_bleu_score(actual_step['uses'], generated_step['uses'])

        # Check if step dictionary contains run key
        elif 'run' in actual_step.keys() and 'run' in generated_step.keys():
            if get_exact_match_score(actual_step['run'], generated_step['run']) > 0.5:
                score += get_bleu_score(actual_step['run'], generated_step['run'])

        else:
            score += get_bleu_score(actual_step, generated_step)

    return score/len(actual_steps_updated)
        


