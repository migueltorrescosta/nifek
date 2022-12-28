# Nifek

Personal project to support all the tools I wanted to have available, tailored for me :D
Based on https://djangocentral.com/building-a-blog-application-with-django/

# Todo

- Code
  - Add [testing suite](https://docs.djangoproject.com/en/4.1/topics/testing/overview/) to the pre-commit hooks.
- Apps
  - Mott: Mottery App.
  - Anki: Anki Like app.
  - MeBa: Diagram maker to increase our Mental Bandwith.
  - Ping: `Uptime Robot` like app.
  - Mova: Visually compare Monetary Values.
  - Paol: Create a Polling system that allows for multiple questions. On Visualization, allow for the viewing of Paretto Optimal only points.
  - Pink: Promise tracker for various events. Sends out a monthly email with the status updates of all subscribers of an event.
- `SEO` optimization
  - Add `sitemap.xml`,
  - Follow other [suggestions from janowski](https://www.janowski.dev/articles/seo-for-django-5-methods-to-improve-seo/)

# Development setup

- **Run:** `podman-compose up` Launches the server locally. You might need to access `127.0.0.1` rather than `0.0.0.0` due to the `ALLOWED_HOSTS` setting.

- **Deployment process:** Since the deployment to `dokku` and `github` is decoupled, we introduce the test running at a `pre-commit` stage, so that it is done before both the deployment to `Linode` and to `GitHub`.

```mermaid
  sequenceDiagram
    participant GitHub
    participant Developent Machine
    participant Linode Server
    Developent Machine->Developent Machine: Run Tests before any git push
    Note over Linode Server, GitHub: git push | git push origin
    Developent Machine->>GitHub: push
    Note over Linode Server, GitHub: git push dokku
    Developent Machine->>Linode Server: deploy
    Note over Linode Server, GitHub: git push all
    Developent Machine->>GitHub: push
    Developent Machine->>Linode Server: deploy
```

For a multi developer experience, we might want to use `GitHub Actions` as our `CI/CD` and deploy to `Linode` as the last step:

```mermaid
  sequenceDiagram
    participant Development Machine
    participant GitHub
    participant Linode Server
    Note over Development Machine, Linode Server: git push
    Development Machine->>GitHub: push & run tests
    GitHub->>Linode Server: deploy
```

# Production setup

- Linode Server `139.144.68.153` hosting with basic DNS
- Domain acquired from NameCheap
- Dokku Apps:
  - Django: `nifek-django-dokku-app`
  - Postgres: `nifek-postgres-dokku-db`
- [Let's Encrypt dokku plugin](https://github.com/dokku/dokku-letsencrypt) used for Managing SSL Certificates
- [Whitenoise](https://whitenoise.evans.io/en/stable/django.html): Responsible for staticfile serving, with caching and compression. Potentially look into
  - optimizing delivery times via CloudFlare or anothe CDN provider.
  - Removing the collectstatic from the predeploy script ( it shouldn't be needed anymore, we need to check that it doesn't destroy the admin panel css though )
- Email: noreplynifek@gmail.com . It was faster to use Google's provided email API than to setup an `SMTP Server`
- `SEO`: Optimized via the addition of title and per page description tags.

# Tech Stack

- Django: https://www.djangoproject.com/
- Magic Links: https://github.com/pyepye/django-magiclink
- Messages / Notifications: https://docs.djangoproject.com/en/4.1/ref/contrib/messages/
- Form rendering: https://django-crispy-forms.readthedocs.io/en/latest/
- Bootstrap: https://getbootstrap.com/docs/4.0/getting-started/introduction/
- Postgres: https://www.postgresql.org/about/

# Data Flows

## Auth

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
