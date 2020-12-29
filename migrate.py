import requests
import os


def migrate_github_to_dagshub(
        dagshub_token,
        origin_url,
        dagshub_owner_name,
        dagshub_repo_name,
        dagshub_url="https://dagshub.com",
        is_org=False,
        is_mirror=False,
        is_private=False,
        github_user="",
        github_pass=""):
    """
    Migrates a repository from GitHub to DAGsHub
    :param dagshub_token: Required. An auth token for your DAGsHub account.
    Create one by going to https://dagshub.com/user/settings/tokens, and copy the hash you are given
    :param origin_url: Required. URL of the repo to be copied,
    for example https://github.com/DAGsHub/client.git
    :param dagshub_owner_name: Required. The owner name that you want to migrate the repo to.
    Can be an organization or a user name.
    :param dagshub_repo_name: Required. Name of the repository on DAGsHub
    :param dagshub_url: DAGsHub base URL. Defaults to https://DAGsHub.com
    :param is_org: Whether the owner is going to be an organization. Default False.
    :param is_mirror: Whether the repository is going to be a mirror. Default False.
    :param is_private: Whether the repository is going to be private. Default False.
    :param github_user: If the repository on GitHub is private, supply your GitHub user.
    :param github_pass: If the repository on GitHub is private, supply your GitHub password.
    :return: http response for the migration request (201 if successful)
    """
    api_url = os.path.join(dagshub_url, "api", "v1")
    if is_org:
        res = requests.get(os.path.join(api_url, "orgs", dagshub_owner_name)).json()
    else:
        res = requests.get(os.path.join(api_url, "users", dagshub_owner_name)).json()
    owner_id = res['id']
    auth_header = {"Authorization": "token " + dagshub_token}
    # Adding must have attributes to migrate request
    payload = {
        "clone_addr": origin_url,
        "user_id": owner_id,
        "repo_name": dagshub_repo_name,
        "mirror": is_mirror,
        "private": is_private
    }
    if github_user and github_pass:
        payload["auth_username"] = github_user
        payload["auth_password"] = github_pass
    res = requests.post(os.path.join(api_url, "repos", "migrate"), data=payload, headers=auth_header)
    return res
