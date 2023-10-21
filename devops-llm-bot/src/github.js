
const createIssueComment = async (context, body) => {
  const issueComment = context.issue({
    body,
  });
  return context.octokit.issues.createComment(issueComment);
}

const getDefaultBranch = async (context, owner, repo) => {
    const defaultBranch = await context.octokit.repos.get({
        owner,
        repo,
    });
    return defaultBranch.data.default_branch;
}

const createBranch = async (context, owner, repo, branch, default_branch) => {
    // Get current reference in Git
    const reference = await context.octokit.git.getRef({
      repo, // the repo
      owner, // the owner of the repo
      ref: "heads/" + default_branch,
    });
    
    // Create a branch
    return await context.octokit.git.createRef({
      repo,
      owner,
      ref: `refs/heads/${branch}`,
      sha: reference.data.object.sha, // accesses the sha from the heads/master reference we got
    });
}

const getRepositoryTree = async (context, owner, repo, branch) => {
    let repositoryTree = await context.octokit.git.getTree({
        repo,
        owner,
        tree_sha: "heads/" + branch,
    });

    return repositoryTree.data.tree.map((item) => item.path);
}

const getLanguages = async (context, owner, repo) => {
    const languages = await context.octokit.repos.listLanguages({
        repo,
        owner,
    });

    return Object.keys(languages.data);
}

const getDependencies = async (context, owner, repo) => {
  const url = `https://api.github.com/repos/${owner}/${repo}/dependency-graph/sbom`;

  try {
    const response = await context.octokit.request('GET ' + url, {
      headers: {
        Accept: 'application/vnd.github.v3+json',
      },
    });

    const sbom = response.data.sbom;
    if (sbom) {
      let packages = sbom.packages || [];

      packages = packages.filter((package) => {
        return package.downloadLocation == `git+https://github.com/${owner}/${repo}`;
      });

      const dependency_names = packages.map((package) => {
        return `${package.name}, version = ${package.versionInfo}`;
      });

      return dependency_names;
    } else {
      return [];
    }
  } catch (error) {
    return [];
  }
}

const getFileDetails = async (context, owner, repo, branch, file) => {
    const fileDetails = await context.octokit.repos.getContent({
        repo,
        owner,
        path: file,
        ref: branch,
    });
    return fileDetails;
}

const getPreviousConversations = async (context, owner, repo, issue_number) => {
    let comments = await context.octokit.issues.listComments({
        owner,
        repo,
        issue_number: issue_number,
    });

    comments = comments.data.filter((comment) => {
        return comment.user.type != "Bot";
    });

    comments = comments.map((item) => item.body);
    
    // Remove last comment
    comments.pop();

    // Reverse the comments to get the latest comment first
    comments.reverse();

    return comments;
}

module.exports = {
    createIssueComment,
    getDefaultBranch,
    createBranch,
    getLanguages,
    getRepositoryTree,
    getDependencies,
    getFileDetails,
    getPreviousConversations,
}