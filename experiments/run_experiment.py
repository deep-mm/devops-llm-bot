import pandas
import time
import github
import gpt
import Score

def run_experiment(csvFile):
    for i in range(0, len(csvFile)):
        repo_identifier = csvFile.iloc[i]['GitHub_Repo_Link'].split('github.com/')[1]
        print(repo_identifier)
        try:
            default_branch = github.get_default_branch(repo_identifier);
            repo_structure = github.get_repository_tree(repo_identifier, default_branch)
            dependencies = github.get_list_of_dependencies(repo_identifier)

            generated_workflow_file = gpt.generate_build_pipeline(repo_structure, dependencies, default_branch)

            csvFile.loc[i,'Generated_Build_Pipeline_File_Content'] = generated_workflow_file
            valid_syntax = True#github.check_yaml_syntax(generated_workflow_file);
            if not valid_syntax:
                csvFile.loc[i,'Syntax_Check'] = 'Invalid'
                continue

            csvFile.loc[i,'Syntax_Check'] = 'Valid'
            workflow_files = github.get_all_workflow_files(repo_identifier)

            build_file_content = ''
            build_file_devops_aware_score = 0
            # Loop through workflow files
            for workflow_file in workflow_files:
                workflow_file_content = github.get_workflow_file_content(repo_identifier, workflow_file, default_branch)
                devops_aware_score = Score.get_devops_aware_score(generated_workflow_file, workflow_file_content)
                if devops_aware_score > build_file_devops_aware_score:
                    build_file_devops_aware_score = devops_aware_score
                    build_file_content = workflow_file_content

            exact_match_score = Score.get_exact_match_score(generated_workflow_file, build_file_content)
            bleu_score = Score.get_bleu_score(generated_workflow_file, build_file_content)

            csvFile.loc[i,'GitHub_Build_Pipeline_File_Content'] = build_file_content
            csvFile.loc[i,'DevOps_Aware_Score'] = build_file_devops_aware_score
            csvFile.loc[i,'Exact_Match_Score'] = exact_match_score
            csvFile.loc[i,'BLEU_Score'] = bleu_score
            # Add delay to avoid rate limiting
            time.sleep(10)
        except Exception as e:
            print(e)
            continue

    csvFile.to_csv('dataset/output.csv', index=False)

# reading the CSV file
csvFile = pandas.read_csv('dataset/dataset_sample.csv')

# Pre-processing the CSV file
csvFile = csvFile[csvFile['GitHub_Repo_Link'].notna()]

csvFile

run_experiment(csvFile)