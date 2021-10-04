# ansible_deploy_template
Basic ansible playbook to deploy a django website (with nginx and gunicorn) using ansible

In the process of working through Test-Driven-Development with Python, I was unable to successfully automate the deployment using Fabric as was suggested in the [book](https://www.obeythetestinggoat.com/book/chapter_automate_deployment_with_fabric.html). Ansible was suggested as an alternative in the appendices. 

This playbook does a lot of the steps outlined in the section of [chapter 10: Thinking about automation](https://www.obeythetestinggoat.com/book/chapter_making_deployment_production_ready.html#_thinking_about_automating). 

**Provisioning**
* Adds the deadsnakes repository 
* Installs nginx, git, python3.6, python3.6-venv
* Adds Nginx config for virtual host
* Adds Systemd job for Gunicorn (including unique SECRET_KEY)

**Deployment**
* Creates directory in ~/sites
* Pulls down source code
* Starts virtualenv in virtualenv
* pip install -r requirements.txt
* manage.py migrate for database
* collectstatic for static files
* Restarts Gunicorn job

At the current time it does not run the functional tests on the site

## Using the playbook

**BEFORE RUNNING THE PLAYBOOK**
* Install ansible
     * **NOTE** Ansible isn't currently support on windows. Can get around this by installing ubuntu terminal through WSL. The ubuntu website has a [walkthrough](https://ubuntu.com/tutorials/ubuntu-on-windows) of how to install
* Install django-environ
* Ensure Django settings file is set up for secure running on server
  * DEBUG, SECRET_KEY, and HOSTS should be got from .env file
  * [django-environ docs](https://django-environ.readthedocs.io/en/latest/)
* Update `site.yml` with 
  * WSGI_DIRECTORY: The directory name where the for the project wsgi.py file
  * REPO_URL: The URL for the git repo
  * REPO_BRANCH: The branch name of the git repo to be cloned
* Update `production` and `staging` files with your
  * Production and staging servers
  * For both servers also specify the ssh username that will be used to log in to your server

**RUNNING THE PLAYBOOK**
  * Navigate to the playbook folder in the ubuntu terminal
  * Run the playbook using `ansible-playbook site.yml -kK -i staging`
    * Change `staging` to `production` to deploy to production server
    * -kK asks for your ssh password & your sudo password when you run the playbook.
    * `ansible.cfg` sets the default server to staging if `-i <servers>` is not included
