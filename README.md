# Multi Terra

The tool to verify if your terraform/terragrunt code is synchronized with the state in the cloud.

What do we want to do? We want to run:

    terragrunt plan -lock=false

in multiple directories and verify if the output contains the following messages:

    Your infrastructure matches the configuration
    Objects have changed outside of Terraform
    Terraform will perform the following actions

## Install

Clone the repo:

    git clone git@github.com:gajdaw/multi-terra-python.git

Install dependencies:

    pip3 install -r requirements.txt

and create link to `mterra` file:

    cd ~/bin
    ln -s /path/to/the/repo/multi-terra-python/main.py mterra

I assume that `~/bin` directory is included in your `PATH`.

## Run

    mterra
    mterra find
    mterra run
