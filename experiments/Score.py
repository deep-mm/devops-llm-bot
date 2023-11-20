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
    # Check if build or test keyword is present in name, run or uses key
    if 'name' in step.keys() and ('build' in step['name'].lower() or 'test' in step['name'].lower()):
        return True
    elif 'run' in step.keys() and (extract_data.has_build_command(language, step['run'])):
        return True
    elif 'uses' in step.keys() and ('build' in step['uses'].lower() or 'test' in step['uses'].lower()):
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
            actual_steps += actual_jobs[job_name]['steps']

    generated_steps = []
    for job_name in generated_jobs_names:
        # Check if job dictionary contains steps key
        if 'steps' in generated_jobs[job_name].keys():
            generated_steps += generated_jobs[job_name]['steps']

    # Get list of actions
    matched_actual_steps = []
    matched_generated_steps = []
    matched_generated_steps_scores = []
    score = 0

    # For each step in actual step list, find the steps with build or test keywords in it
    for actual_step in actual_steps:
        # Check equalIgnoreCase for build or test keywords
        if check_if_build_or_test_step(actual_step, language):
            matched_actual_steps.append(actual_step)
            # Find the corresponding step in generated step list by max step score
            max_step_score = 0
            matched_generated_step = None
            for generated_step in generated_steps:
                step_score = calc_step_score(generated_step, actual_step)
                if step_score > max_step_score:
                    max_step_score = step_score
                    matched_generated_step = generated_step
            score += max_step_score
            # Check if matched_generated_step already exists in matched_generated_steps and if not add it
            if matched_generated_step not in matched_generated_steps:
                matched_generated_steps.append(matched_generated_step)
                matched_generated_steps_scores.append(max_step_score)
            else:
                index = matched_generated_steps.index(matched_generated_step)
                matched_generated_steps_scores[index] += max_step_score

    # Calculate score
    # for step_score in matched_generated_steps_scores:
    #     score += min(1, step_score)

    return score/len(matched_actual_steps)
        


