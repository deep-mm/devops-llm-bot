from difflib import SequenceMatcher
from nltk.translate.bleu_score import sentence_bleu
import extract_data
import yaml

def get_exact_match_score (generated_workflow_file_content, actual_workflow_file_content):
    return SequenceMatcher(None, generated_workflow_file_content, actual_workflow_file_content).ratio()

def get_bleu_score (generated_workflow_file_content, actual_workflow_file_content):
    return sentence_bleu([generated_workflow_file_content], actual_workflow_file_content)

def calc_step_score (generated_step, actual_step):
    # Check if step dictionary contains uses key
    if 'uses' in actual_step.keys() and 'uses' in generated_step.keys():
        return get_exact_match_score(actual_step['uses'], generated_step['uses'])
            
    # Check if step dictionary contains run key
    elif 'run' in actual_step.keys() and 'run' in generated_step.keys():
        return get_exact_match_score(actual_step['run'], generated_step['run'])
            
    else:
        return get_bleu_score(str(actual_step), str(generated_step))
    
def check_if_build_or_test_step (step, language):
    keywords = ['build', 'test']
    # Check if build or test keyword is present in name, run or uses key
    if 'run' in step.keys() and (extract_data.check_against_all_languages(step['run'])):
        return True
    elif 'uses' in step.keys() and any(keyword in step['uses'].lower() for keyword in keywords):
        return True
    elif 'name' in step.keys() and any(keyword in step['name'].lower() for keyword in keywords):
        return True
    else:
        return False

def get_devops_aware_score (generated_workflow_file_content, actual_workflow_file_content, language):
    actual = yaml.safe_load(actual_workflow_file_content)
    generated = yaml.safe_load(generated_workflow_file_content)

    actual_jobs = actual['jobs']
    generated_jobs = generated['jobs']

    actual_jobs_names = [job_name for job_name in actual_jobs.keys()]
    generated_jobs_names = [job_name for job_name in generated_jobs.keys()]

    # Get list of steps
    actual_steps = []
    for job_name in actual_jobs_names:
        # Check if job dictionary contains steps key
        if 'steps' in actual_jobs[job_name].keys():
            # Ensure that steps is a list and if not, convert it to a list
            if type(actual_jobs[job_name]['steps']) is not list:
                actual_jobs[job_name]['steps'] = [actual_jobs[job_name]['steps']]
            actual_steps += actual_jobs[job_name]['steps']

    generated_steps = []
    for job_name in generated_jobs_names:
        # Check if job dictionary contains steps key
        if 'steps' in generated_jobs[job_name].keys():
            # Ensure that steps is a list and if not, convert it to a list
            if type(generated_jobs[job_name]['steps']) is not list:
                generated_jobs[job_name]['steps'] = [generated_jobs[job_name]['steps']]
            generated_steps += generated_jobs[job_name]['steps']

    # Get list of actions
    matched_actual_steps = []
    score = 0

    # For each step in actual step list, find the steps with build or test keywords in it
    for actual_step in actual_steps:
        # Check equalIgnoreCase for build or test keywords
        if check_if_build_or_test_step(actual_step, language):
            matched_actual_steps.append(actual_step)
            score += max(calc_step_score(generated_step, actual_step) for generated_step in generated_steps)

    # return average score only if there are matched steps
    if len(matched_actual_steps) > 0:
        return score / len(matched_actual_steps)
    else:
        return 0
        