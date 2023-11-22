import pandas
import time
import github
import gpt
import Score
import sys
import asyncio

async def run_experiment_row(csvFile, i):
    repo_identifier = csvFile.iloc[i]['GitHub_Repo_Link'].split('github.com/')[1]
    print(repo_identifier)
    try:
        default_branch = github.get_default_branch(repo_identifier);
        repo_structure = github.get_repository_tree(repo_identifier, default_branch)
        recursive_repo_structure = github.get_recursive_repository_tree(repo_identifier, default_branch)
        dependencies = github.get_list_of_dependencies(repo_identifier)
        build_file_content = csvFile.iloc[i]['GitHub_Build_Pipeline_File_Content']
        repo_language = csvFile.iloc[i]['Language']

        generated_workflow_file = gpt.generate_build_pipeline(repo_structure, dependencies, default_branch, recursive_repo_structure)

        csvFile.loc[i,'Generated_Build_Pipeline_File_Content'] = generated_workflow_file
        valid_syntax = github.run_action_lint(generated_workflow_file);
        if not valid_syntax:
            csvFile.loc[i,'Syntax_Check'] = 'Invalid'
            return

        csvFile.loc[i,'Syntax_Check'] = 'Valid'
        
        exact_match_score = Score.get_exact_match_score(generated_workflow_file, build_file_content)
        bleu_score = Score.get_bleu_score(generated_workflow_file, build_file_content)
        devops_aware_score = Score.get_devops_aware_score(generated_workflow_file, build_file_content, repo_language)

        csvFile.loc[i,'Exact_Match_Score'] = exact_match_score
        csvFile.loc[i,'BLEU_Score'] = bleu_score
        csvFile.loc[i,'DevOps_Aware_Score'] = devops_aware_score
        # Add delay to avoid rate limiting
        #time.sleep(5)
    except Exception as e:
        print(e)
        csvFile.loc[i,'Syntax_Check'] = str(e)
        return

async def run_experiment(csvFile):
    tasks = [run_experiment_row(csvFile, row) for row in range(len(csvFile))]
    await asyncio.gather(*tasks)

print (sys.argv)
# reading the CSV file
csvFile = pandas.read_csv(f'dataset/{sys.argv[1]}.csv')

# Pre-processing the CSV file
csvFile = csvFile[csvFile['GitHub_Repo_Link'].notna()]

# Get first 20 rows
csvFile = csvFile.head(100)

# Explicitly specify dtypes to avoid pandas inferring dtypes
csvFile = csvFile.astype({'GitHub_Repo_Link': 'string', 'GitHub_Build_Pipeline_File_Content': 'string', 'Generated_Build_Pipeline_File_Content': 'string', 'Syntax_Check': 'string', 'Exact_Match_Score': 'float', 'BLEU_Score': 'float', 'DevOps_Aware_Score': 'float'})

# Start time
start_time = time.time()

asyncio.run(run_experiment(csvFile))

# End time
end_time = time.time()

# Print time taken
print(f"Time taken: {end_time - start_time}")

csvFile.to_csv('dataset/output.csv', index=False)