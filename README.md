# [NiFeK](https://nifek.com)

![GitHub issues](https://img.shields.io/github/issues/migueltorrescosta/nifek)
![GitHub closed issues](https://img.shields.io/github/issues-closed/migueltorrescosta/nifek)
![GitHub pull requests](https://img.shields.io/github/issues-pr/migueltorrescosta/nifek)
![GitHub last commit](https://img.shields.io/github/last-commit/migueltorrescosta/nifek)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/m/migueltorrescosta/nifek/main)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/migueltorrescosta/nifek)
![GitHub repo size](https://img.shields.io/github/repo-size/migueltorrescosta/nifek)
![GitHub repo file count](https://img.shields.io/github/directory-file-count/migueltorrescosta/nifek)
![Lines of code](https://img.shields.io/tokei/lines/github/migueltorrescosta/nifek)

![Website](https://img.shields.io/website?down_color=red&down_message=offline&up_color=green&up_message=online&url=https%3A%2F%2Fnifek.com)
[![Known Vulnerabilities](https://snyk.io/test/github/migueltorrescosta/nifek/badge.svg)](https://snyk.io/test/github/migueltorrescosta/nifek)
![Security Headers](https://img.shields.io/security-headers?url=https%3A%2F%2Fnifek.com%3A443%2F)

[Personal project](https://nifek.com) to support all the tools I wanted to have available 🪞
Initial structure based on a template blog app https://djangocentral.com/building-a-blog-application-with-django/

# 📝 ToDo

## 💻 Project Quality

- Add Load Testing to the app, probably with [Locust](https://www.section.io/engineering-education/how-to-test-django-applications-with-locust/).
- Add [code coverage](https://adamj.eu/tech/2019/04/30/getting-a-django-application-to-100-percent-coverage/) as a GitHub Actions Artifact. [This approach](https://www.hacksoft.io/blog/github-actions-in-action-setting-up-django-and-postgres) seems promising. FOr the time we can manually run coverage, which lies at 93% 🥳
- For SEO Optimization add a `sitemap.xml` and follow the [suggestions from janowski](https://www.janowski.dev/articles/seo-for-django-5-methods-to-improve-seo/).

## 📱 New Apps

- **Mott:** Mottery App.
- **Diam:** Diagram maker to increase our Mental Bandwith.
- **Ping:** `Uptime Robot` like app.
- **Mony:** Visually compare Monetary Values.
- **Paol:** Create a Polling system that allows for multiple questions. On Visualization, allow for the viewing of Paretto Optimal only points.
- **Pink:** Promise tracker for various events. Sends out a monthly email with the status updates of all subscribers of an event.
- **Meas:** Implementation of the framework described on `How To Measure Anything`
- **Fute:** App to organize football matches easily (i.e. track who is coming on a first come basis / potentially other options )
- **XP:** App focused on which experiences to prioritize for your life ( Similar to a Recommendations for one time events, with Clustering analysis for suggestions ).

## ☎ Old Apps

- **Core:** Add user Profile Page!
- **Thes:** Allow users to tag/untag existing Thesis
- **Cram:** Reach out to Michael Nielsen for possible feedback,having read [his post](http://augmentingcognition.com/ltm.html)

# 📚 Tech Stack

- [Django](https://www.djangoproject.com/) as the core Framework.
- [Magic Links](https://github.com/pyepye/django-magiclink) to provide passwordless Authentication with email based Magic Links.
- [coverage](https://github.com/nedbat/coveragepy) provides us with accurate testing coverage reports
- [Messages / Notifications](https://docs.djangoproject.com/en/4.1/ref/contrib/messages/) For displaying relevant messages from the backend to the user.
- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) for Backend provided form rendering.
- [Bootstrap](https://getbootstrap.com/docs/4.0/getting-started/introduction/) for UI/UX.
- [Postgres](https://www.postgresql.org/about/) as a relational solution for our DB.
- [Dependabot](https://github.blog/2020-06-01-keep-all-your-packages-up-to-date-with-dependabot/) to avoid outdated/insecure dependencies.

# 🏌 Development setup

_Remark: Replace `podman-docker` commands with `docker-compose` depending on whether you use `podman` or `docker` as your `container` management solution._

## Build

`podman-compose build` to build the `web` and `db` apps ( Django and Postgres respectively ).

## Run

`podman-compose up` launches the server locally. The app should be available under `0.0.0.0:8000`. `127.0.0.1` does not work due to the chosen `ALLOWED_HOSTS` setting. On the web container run `django manage.py createsuperuser` to be able to do the first login as staff, and have the `admin` panel locally available. Emails are saved under the `sent_emails` folder for local development ( Needed for magiclinks )

## Tests

To run tests locally, `docker exec` into the running django container, and run `python manage.py test`. To also get coverage, run `make coverage` inside the container. This will generate an `htmlcov` folder which you can see in firefox. Due to containerization, you might need to change the `htmlcov` folder permissions via `sudo chown -R <username>` and `sudo chgrp -R <username>` before opening the `html` files with your browser. This can be done outside docker via the command `make perms`.

On the server, `dokku` takes care of running tests before deploying any image.

## Pre Commit Hooks

The current `.pre-commit-config.yaml` setup enforces `trailing-whitespace`, `detect-private-key`, `end-of-file-fixer`, `forbid-submodules`, `name-tests-test`, `pretty-format-json`, `requirements-txt-fixer`, `check-added-large-files`, `check-docstring-first` `check-json`, `check-merge-conflict`.

## Deploying changes

The deployment to `dokku` and `github` is decoupled.

- `git push` and `git push origin` send changes to GitHub only.
- `git push dokku` sends changes to `dokku` only.
- `git push all` sends changes to both. `dokku` runs tests pre-deployment, and rejects the changes if the tests fail 🦺

For a multi developer experience, we might want to use `GitHub Actions` as our `CI/CD` and deploy to `Linode` as the last step:

```mermaid
  sequenceDiagram
    participant Development Machine
    participant GitHub
    participant Linode Server
    Development Machine ->> Development Machine: pre-commit run
    Note over Development Machine, Linode Server: git push
    Development Machine->>GitHub: push & run tests
    GitHub->>Linode Server: deploy
```

# 👮‍♀️ Production Environment

## 🔑 Key Info

- Linode Server `139.144.68.153`, with basic DNS
- Domain acquired from https://namecheap.com
- Dokku Apps:
  - Django: `nifek-django-dokku-app`
  - Postgres: `nifek-postgres-dokku-db`

## 📃 SSL Certificate

Solved by [Let's Encrypt dokku plugin](https://github.com/dokku/dokku-letsencrypt).

## 📤 Static File Serving

Solved by [Whitenoise](https://whitenoise.evans.io/en/stable/django.html), which provides caching and compression out of the box. Loading times can be decreased by setting up CloudFlare or another CDN provider as the source of all StaticFiles.

## 📩 Email setup

Email: noreplynifek@gmail.com . It was faster to use Google's provided email API than to setup an `SMTP Server`

## 🚅 Parallelization

Useless at the moment as we're using a single CPU. Note that we can still benefit from concurrency: Long running threads should not block slower ones.

## 🌐 Web Insights

Look into [PageSpeed Insights](https://pagespeed.web.dev/report?url=https%3A%2F%2Fnifek.com%2F&form_factor=desktop) or Lighthouse ( available via Chrome's Dev Tools ). Some optimization via the addition of title and per page description tags has been done, and we score high on the mentioned tools. Nonetheless there's always room for improvement. 🦸‍♀️

# 🪄 Data Flows

## 🕵 Auth via MagicLinks

```mermaid
  sequenceDiagram
    participant email
    participant user
    participant browser
    participant django
    Note over email, django: Login Flow
    user->>browser: Login Button
    browser->>django: GET /accounts/login
    django->>browser: Login Form
    browser->>django: POST /auth/login ( with email )
    django->>email: Verification email with Magic Link
    email->>user: Get Magic Link
    user->>browser: Access authenticated resource
    Note over email, django: Logout Flow
    user->>browser: Logout Button
    browser->>django: /auth/logout
```

## 📷 Cram FlashCard process

[Anki](https://apps.ankiweb.net/) like app

- The Cards are shared per collection. We should email the Collection/Card owner when someone else changes a Card they use.
- On `process_revision`, if the revision is "Again", the `next_revision_timestamp` is chosen uniformly between `1` and `2` minutes from the current time, and increment `number_of_failed_revisions` by one. Otherwise we take the time since the `last_revision_timestamp`, multiply it by `max{ 2.5 - 0.2*number_of_failed_revisions, 1.3 }`, and add up to `5%` noise value to avoid deterministic review times and collision of card review times all simultaneously. In all cases the `previous_revision_timestamp` is set to the current time.

### 🪣 Model structure

```mermaid
classDiagram
    Collection <|-- Card : collection
    User <|-- Collection : owner
    User <|-- Card : owner
    User <|-- Collection : editors
    User <|-- Card : editors
    Card <|-- UserCardScore : card
    User <|-- UserCardScore : user

    class Card{
        -pk : Integer
        -concept : CharField 128
        -description : TextField
        -difficulty : Enum
     }

    class UserCardScore{
        -pk : Integer
        -previous_revision_timestamp: Datetime
        -next_revision_timestamp: Datetime
        -last_revision: Enum<Again, Hard, Normal, Easy>
        -number_of_failed_revisions: Integer
        -process_revision(revision)
     }

    class Collection{
        -pk : int
        -title : CharField 128
        -create_collection(title)
        -add_editor(user)
        -remove_editor(user)
    }

    class User{
        -pk : int
    }
```
