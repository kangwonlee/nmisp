# workflows

* Github Workflows as a SubTree
* Would use `conda` to create a `test-environment`
* Based on https://github.com/kangwonlee/test_ipynb.git

## Example

1. Assume a repository does not have the `.github/workflow` folder yet.
1. Go to the local repository folder. Let's say this folder is `.`.
1. Prepare a `pytest` setup under `./tests/` folder.
1. Also under the `./tests/` folder, prepare `.yml` files of `test-environment` recipes.<br>
    For example, for python 3.7, please use filename of `environment.3.7.yml`.<br>
    In case of Anaconda 2019.07, `environment.2019.07.yml`.
1. `mkdir ./.github`
1. Add this repository as a subtree of the repository.<br>
    `git subtree add --prefix=./.github/workflows/ https://github.com/kangwonlee/workflows.git workflows/master --squash`
1. Make changes to files of `./.github/workflows/` as necessafy & commit.
1. Push to GitHub.

## To update the subtree

1. Make sure if the updated version of this `workflows` is suitable for your work.
1. `git subtree pull --prefix=./.github/workflows/ https://github.com/kangwonlee/workflows.git workflows/master --squash`

## To feedback

1. Please check https://github.com/kangwonlee/workflows/issues
