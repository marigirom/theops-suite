# Project 01 — Docker Stack Plan

## Overview

**Goal:** Package a small Python (FastAPI) API, a PostgreSQL 16 database, and an
Nginx reverse proxy into a production-style Docker Compose stack. By the end you
will be able to show:

- A multi-stage, non-root, health-checked container image
- A three-service Compose stack on a custom network with a named volume
- A working backup/restore flow
- A README with an architecture diagram and image-size comparison

**Branch:** `project/01-docker`
**Tag:** `v1.0.0-docker`
**Repo folder:** `01-docker-stack/`

---

## Prerequisites (check before writing a single file)

| Tool | Check command | Good output |
|---|---|---|
| Docker Engine | `docker version --format '{{.Server.Version}}'` | `29.x.x` |
| Compose plugin | `docker compose version` | `Docker Compose version v2.x.x` or `v5.x.x` |
| Git | `git --version` | `git version 2.x.x` |
| curl | `curl --version \| head -1` | `curl 8.x.x ...` |
| make | `make --version \| head -1` | `GNU Make 4.x` |

> If `make` is missing: `sudo apt install make`

---

## Repository Bootstrap (one-time, before any project folder)

This sub-task sets up the monorepo root that all seven projects will live in.
It is done **once** on `main` before you branch for Project 01.

### Sub-Task 0 — Bootstrap the monorepo

**Intent:** Create the GitHub repo, local clone, root-level `.gitignore` and
`README.md`, then push `main`. This is the shared foundation.

**Expected outcomes:**
- `git remote -v` shows `git@github.com:marigirom/theops-suite.git`
- `git log --oneline` shows one commit on `main`
- GitHub shows the repo with the root README

**Steps:**

0-A. [YOU DO] Create the GitHub repo
- Go to https://github.com/new
- Name: `theops-suite`, Public, **do not** initialise with a README (we do that locally)
- Click "Create repository"

0-B. [YOU DO] Generate and register an SSH key (skip if you already have one)
```bash
# Check for an existing key first
ls ~/.ssh/id_ed25519.pub
```
If that file doesn't exist:
```bash
ssh-keygen -t ed25519 -C "marigirom@theops-suite"
# Press Enter three times to accept defaults
cat ~/.ssh/id_ed25519.pub
```
Copy the output. On GitHub → Settings → SSH and GPG keys → New SSH key → paste it.

Verify:
```bash
ssh -T git@github.com
# Expected: Hi marigirom! You've successfully authenticated...
```

0-C. [YOU DO] Initialise the local repo
```bash
mkdir -p ~/Desktop/MyProjects/theops-suite
cd ~/Desktop/MyProjects/theops-suite
git init -b main
git remote add origin git@github.com:marigirom/theops-suite.git
```

0-D. [YOU DO] Create the root `.gitignore`
Create the file `~/Desktop/MyProjects/theops-suite/.gitignore` with this content:
```
# Environment and secrets
.env
*.env

# Terraform
*.tfstate
*.tfstate.*
.terraform/
*.plan

# Kubernetes
kubeconfig
*.kubeconfig

# VM disks
*.qcow2
*.vmdk
*.vdi

# Database dumps
*.sql
*.dump

# Python
__pycache__/
*.pyc
.venv/

# macOS
.DS_Store
```

0-E. [YOU DO] Create the root `README.md`
Create `~/Desktop/MyProjects/theops-suite/README.md` with just a skeleton:
```markdown
# TheOps Suite

A set of seven DevOps projects built locally with Docker, Kubernetes, Linux, KVM and Git.

| # | Project | Tools | Status |
|---|---------|-------|--------|
| 01 | Docker stack | Docker, Compose, Nginx, Postgres | 🚧 in progress |
| 02 | Kubernetes | minikube, kubectl | ⏳ pending |
| 03 | CI/CD | GitHub Actions, GHCR | ⏳ pending |
| 04 | Terraform | Terraform, local providers | ⏳ pending |
| 05 | Linux baseline | bash, systemd, SSH | ⏳ pending |
| 06 | Linux networking | nftables, namespaces, DNS | ⏳ pending |
| 07 | Virtualization | KVM, libvirt, cloud-init | ⏳ pending |
```

0-F. [YOU DO] First commit and push
```bash
git add .gitignore README.md
git commit -m "chore: initialise monorepo with root README and gitignore"
git push -u origin main
```

**Commit message:** `chore: initialise monorepo with root README and gitignore`

**Status:** [ ] pending

---

## Day 1 — The Image

### Sub-Task 1 — Create the branch and project folder

**Intent:** Every project lives on its own branch. Creating the folder and branching
now means every commit for this project is isolated and reviewable as a PR.

**Expected outcomes:**
- `git branch` shows `project/01-docker` as current
- `01-docker-stack/` folder exists with the right subdirectory layout

**Steps:**

1-A. [YOU DO] Create the branch
```bash
cd ~/Desktop/MyProjects/theops-suite
git checkout -b project/01-docker
```

1-B. [YOU DO] Create the folder skeleton
```bash
mkdir -p 01-docker-stack/app
mkdir -p 01-docker-stack/nginx
mkdir -p 01-docker-stack/backups
```

**Commit message:** `chore(docker): scaffold 01-docker-stack folder structure`

**Status:** [ ] pending

---

### Sub-Task 2 — Write the FastAPI application

**Intent:** A minimal, self-contained Python API that exposes `/health` and
`/items`. It is small enough to understand completely and big enough to demonstrate
a real app talking to a database.

**Why FastAPI instead of Flask?** FastAPI ships its own ASGI server (uvicorn),
generates automatic docs at `/docs`, and validates request bodies with Pydantic —
all useful interview talking points. It is also the modern choice for new Python APIs.

**Expected outcomes:**
- `01-docker-stack/app/main.py` exists, under 60 lines
- `01-docker-stack/app/requirements.txt` exists with pinned versions
- Running the app manually with `uvicorn` returns `{"status":"ok"}` from `/health`

**Files to create:**

`01-docker-stack/app/requirements.txt` — pinned dependencies:
```
fastapi==0.115.0
uvicorn[standard]==0.30.6
sqlalchemy==2.0.36
psycopg2-binary==2.9.9
```

`01-docker-stack/app/main.py` — the application (Bob will draft this and explain
every line before you type it):

Key endpoints:
- `GET /health` → `{"status": "ok"}` — used by Docker's HEALTHCHECK and K8s probes
- `GET /items` → list of all rows from the `items` table
- `POST /items` → insert a row `{"name": "<string>"}`, return the created row

Database connection: read `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASS`
from environment variables. Use SQLAlchemy 2.x (the modern declarative style) for
the DB layer — it shows ORM knowledge without being verbose (adds about 15 lines).

> Bob will present the full drafted file with a line-by-line explanation as a
> separate chat message during the step-by-step walkthrough — not in this plan.

**Commit message:** `feat(docker): add FastAPI app with /health and /items endpoints`

**Status:** [ ] pending

---

### Sub-Task 3 — Write the multi-stage Dockerfile and .dockerignore

**Intent:** Demonstrate production-image best practices: build artefacts stay out
of the final image, the app runs as a non-root user, and Docker knows how to test
whether the container is alive.

**Expected outcomes:**
- `docker build -t theops-api:0.1.0 .` succeeds from `01-docker-stack/`
- `docker inspect --format '{{.State.Health.Status}}' api` returns `healthy`
- `docker exec api id` does **not** show `uid=0(root)`
- Image size is visibly smaller than a single-stage equivalent

**Key Dockerfile design decisions:**

| Decision | Why |
|---|---|
| Two stages: `builder` + `final` | Build tools (gcc, pip) stay out of the final image |
| `python:3.12-slim` as final base | Much smaller than `python:3.12`; no dev packages |
| Install into a venv in the builder | Copying the whole venv is cleaner than `pip install --target` |
| `adduser --disabled-password appuser` | Never run as root in a container |
| `HEALTHCHECK` on `/health` | Docker marks the container unhealthy automatically |
| `.dockerignore` | Keeps `__pycache__`, `.git`, `.env` out of the build context |

`01-docker-stack/.dockerignore` content:
```
.git
__pycache__
*.pyc
.env
backups/
*.md
```

> Bob will draft the full Dockerfile with a line-by-line explanation during the
> step-by-step walkthrough.

**Standalone verify commands (run from `01-docker-stack/`):**
```bash
docker build -t theops-api:0.1.0 .
docker run -d --name api -p 8000:8000 \
  -e DB_HOST=localhost -e DB_PORT=5432 \
  -e DB_NAME=appdb -e DB_USER=app -e DB_PASS=changeme \
  theops-api:0.1.0
# Wait ~5 seconds for the healthcheck interval
docker inspect --format '{{.State.Health.Status}}' api
docker exec api id
docker image ls theops-api
# /health will return ok; /items will fail (no DB yet) — that is expected here
curl -s localhost:8000/health
docker stop api && docker rm api
```

**SCREENSHOT CHECKPOINT — image size**
- Capture: `docker image ls theops-api` with the size column visible
- Filename: `docs/screenshots/01-image-size.png`
- README section: "Image size comparison"

**Commit message:** `feat(docker): multi-stage Dockerfile with non-root user and healthcheck`

**Status:** [ ] pending

---

## Day 2 — The Stack

### Sub-Task 4 — Write compose.yaml and .env

**Intent:** Wire all three services together with a custom network, a named volume,
health-dependent startup order, and secrets kept out of the repo.

**Expected outcomes:**
- `docker compose up -d` starts all three services with no errors
- `docker compose ps` shows all three as `running (healthy)` or `running`
- Only port `8080` is reachable from the host (proxy only)
- Port `8000` is **not** reachable from the host (verify with `curl localhost:8000`)

**Services summary:**

| Service | Image | Published port | Key settings |
|---|---|---|---|
| `db` | `postgres:16` | none (internal only) | named volume `pgdata`, `pg_isready` healthcheck |
| `api` | built from `./` (the Dockerfile) | none (internal only) | `depends_on: db: condition: service_healthy` |
| `proxy` | `nginx:1.27-alpine` | `8080:80` | config from `./nginx/default.conf` |

**Network:** `appnet` (bridge driver). No service publishes directly to the host
except `proxy`.

**Secrets strategy:** `.env` holds real values, `.env.example` holds placeholders,
only `.env.example` is committed.

`.env.example` content:
```
POSTGRES_DB=appdb
POSTGRES_USER=app
POSTGRES_PASSWORD=changeme
DB_HOST=db
DB_PORT=5432
DB_NAME=appdb
DB_USER=app
DB_PASS=changeme
```

**Nginx config file** (`01-docker-stack/nginx/default.conf`):
Proxy all traffic on port 80 to `api:8000`. Bob will draft this with explanation.

> Bob will draft `compose.yaml`, `.env.example`, and `nginx/default.conf` with
> line-by-line explanations during the step-by-step walkthrough.

**Commit message:** `feat(docker): add compose.yaml with three-service stack and appnet`

**Status:** [ ] pending

---

### Sub-Task 5 — Write the Makefile

**Intent:** A Makefile turns long `docker compose` commands into short, memorable
targets. This is a common pattern on real teams.

**Expected outcomes:**
- `make up` starts the stack
- `make down` stops it without deleting the volume
- `make logs` streams combined logs
- `make backup` creates `backups/appdb.sql`
- `make restore` loads `backups/appdb.sql` back into the DB

**Targets:**

| Target | Command it runs |
|---|---|
| `up` | `docker compose up -d --build` |
| `down` | `docker compose down` |
| `logs` | `docker compose logs -f` |
| `backup` | `docker compose exec -T db pg_dump -U app appdb > backups/appdb.sql` |
| `restore` | `docker compose exec -T db psql -U app appdb < backups/appdb.sql` |

**Note on `-T`:** The `-T` flag disables pseudo-TTY allocation. Without it,
`pg_dump` output contains control characters that corrupt the SQL file.

> Bob will draft the Makefile with explanation during the walkthrough.

**Commit message:** `feat(docker): add Makefile with up/down/logs/backup/restore targets`

**Status:** [ ] pending

---

### Sub-Task 6 — Verify the full stack end-to-end

**Intent:** Prove every Definition of done item with observable output.

**Steps:**

6-A. [YOU DO] Start the stack
```bash
cd 01-docker-stack
cp .env.example .env
# Edit .env to set a real password if you like (optional for local dev)
make up
```
Expected: three containers start; `docker compose ps` shows all three running.

6-B. [YOU DO] Confirm only the proxy is reachable
```bash
curl -s localhost:8080/items      # should return []
curl -s localhost:8000/health     # should refuse connection (port not published)
```

6-C. [YOU DO] Insert data and confirm persistence
```bash
curl -s -X POST localhost:8080/items \
  -H "Content-Type: application/json" \
  -d '{"name": "test-item"}'
make down
make up
curl -s localhost:8080/items      # test-item should still be there
```

6-D. [YOU DO] Backup and restore
```bash
make backup                       # creates backups/appdb.sql
# Confirm the file exists:
ls -lh backups/appdb.sql
# Wipe the data:
curl -s localhost:8080/items      # note items count
# (manual: connect to DB and DELETE FROM items — Bob will show how)
make restore
curl -s localhost:8080/items      # items are back
```

6-E. [YOU DO] Inspect the network
```bash
docker network inspect theops-suite_appnet
# or: docker network ls and find the right name
```
All three containers must appear under "Containers".

**SCREENSHOT CHECKPOINT — stack running**
- Capture: `docker compose ps` with all three services showing
- Filename: `docs/screenshots/01-compose-ps.png`
- README section: "Running the stack"

**SCREENSHOT CHECKPOINT — proxy only**
- Capture: terminal showing `curl localhost:8080/items` succeeds AND
  `curl localhost:8000/health` fails (connection refused)
- Filename: `docs/screenshots/01-proxy-only.png`
- README section: "Security — only proxy exposed"

**SCREENSHOT CHECKPOINT — backup and restore**
- Capture: `make backup` output + `ls -lh backups/appdb.sql` + `make restore`
- Filename: `docs/screenshots/01-backup-restore.png`
- README section: "Backup and restore"

**Commit message:** `docs(docker): add evidence screenshots`

**Status:** [ ] pending

---

### Sub-Task 7 — Write the project README

**Intent:** Recruiters read the per-project README. It must tell a story:
what problem it solves, how it is built, how to run it, and what you learned.

**Expected outcomes:**
- `01-docker-stack/README.md` exists with all required sections
- An architecture diagram is included (ASCII or Mermaid)
- Image-size comparison table is present
- "How to run" section works in under 10 commands

**Required sections:**

1. What it is (two sentences max)
2. Architecture diagram — show the three services, the `appnet` network, the named
   volume, and which port is published
3. How to run (clone, copy .env, `make up`, `curl`)
4. Image size comparison — single-stage naive build vs. multi-stage build
   (the guide explicitly requires this)
5. Lessons learned (3–5 bullet points)
6. What I would do next (stretch goals from the guide)

> Bob will draft the README with explanation during the walkthrough.

**Commit message:** `docs(docker): add project README with architecture diagram`

**Status:** [ ] pending

---

### Sub-Task 8 — Git wrap-up: PR, merge, tag

**Intent:** Follow the minimal git workflow from the guide. The branch must be
merged via a PR, not a direct push to main.

**Steps:**

8-A. [YOU DO] Final commit check — before every commit Bob will remind you:
- No `.env` with real passwords
- No `backups/*.sql` files
- No `__pycache__` or `.pyc` files

8-B. [YOU DO] Push the branch
```bash
git push -u origin project/01-docker
```

8-C. [YOU DO] Open a Pull Request on GitHub
- Go to your repo → "Compare & pull request"
- Title: `feat(docker): Project 01 — containerized three-tier stack`
- Description: paste the Definition of done checklist with ticks

8-D. [YOU DO] Merge the PR on GitHub (Merge commit is fine for now — squash rebase
strategy is saved for Project 03)

8-E. [YOU DO] Pull main and tag
```bash
git checkout main
git pull origin main
git tag v1.0.0-docker
git push origin v1.0.0-docker
```

**Status:** [ ] pending

---

## Definition of Done (copied from the guide)

- [ ] Final image is slim and runs as non-root
- [ ] Only the proxy is reachable from the host
- [ ] Data survives `down` and `up`
- [ ] Backup script tested with a restore
- [ ] README includes an architecture diagram and the image-size comparison

---

## Stretch Goals (attempt after DoD is fully ticked)

- Scan the image with Trivy and record results in `docs/TROUBLESHOOTING.md`
- Add `read_only: true` to the api service plus a `tmpfs` for `/tmp`

---

## Notes / Deviations from the Guide

1. **FastAPI instead of Flask** — the guide says "Flask (or FastAPI)". FastAPI is
   chosen because it ships uvicorn, generates /docs automatically, and is the
   modern standard. If you want Flask instead, say so and the plan will adapt.

2. **`backups/` inside the repo but gitignored** — your choice from the
   prerequisite questions. The `.gitignore` already covers `*.sql`.

3. **`compose.yaml` not `docker-compose.yml`** — the guide uses `compose.yaml`
   which is the current Compose v2 convention. Both filenames work but `compose.yaml`
   is preferred.

4. **SQLAlchemy instead of plain psycopg2** — your choice from the confirmation
   questions. SQLAlchemy 2.x adds ~15 lines but demonstrates ORM knowledge and is
   directly reusable in Projects 02–04. The `psycopg2-binary` package is still
   needed as the underlying driver.
