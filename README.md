# Secure account storage and Docker CI learning project

AI-assisted starter for guided learning. Run and inspect it yourself before claiming practice.
This project is a small in-memory CLI demonstration, not an API, website, or production identity service.

## Intended learning
- Goal 2: password storage, parameterised SQL, input validation and security tests.
- Goal 3: commits, a YAML workflow and automated verification.
- Goal 4: Docker image creation and execution on a GitHub-hosted Ubuntu runner.
- AWS deployment, certification, CD and ethics are not demonstrated by this program.

## Files
Upload accounts.py, test_accounts.py, demo.py, Dockerfile and README.md to a NEW repository root.
Create `.github/workflows/security-docker.yml` and paste the workflow template there.
Do not leave the template only in the root; it will not run there.

## Local commands (optional)
python3 -m unittest discover -v
python3 demo.py
docker build -t secure-account-demo .
docker run --rm --network none --read-only --cap-drop ALL --security-opt no-new-privileges secure-account-demo

## Security reasoning and limits
Password material is derived using PBKDF2-HMAC-SHA256 with 600,000 iterations and a random 16-byte salt.
Digests are compared using compare_digest. SQL values are bound with placeholders.
Tests check a specific injection payload; they do not prove the absence of all security flaws.
The database is temporary, in memory, and contains fictional test accounts only.
Missing-user and wrong-password timing differs. There is no rate limiting, MFA, transport security,
authorisation, session management or persistent secret management. Do not deploy as a real login service.
Password length bounds are exercise rules, not a claim of full standards compliance.
The container runs as a non-root user. Its test execution disables networking, drops capabilities
and uses a read-only filesystem. This is not a vulnerability scan or production hardening assessment.
A version tag is used for the base image; release pinning and image scanning remain future work.

## Evidence to retain AFTER your run
1. Repository root with source, tests and Dockerfile.
2. Workflow summary showing all steps succeeded.
3. Run security tests log: 10 tests and OK.
4. Build Docker image log: successful image creation.
5. Run tests inside Docker log: 10 tests and OK.
6. Run demonstration log: three True results.
Record your actual time and observations. A failed run is useful for troubleshooting, but must not
be represented as a successful run. Do not fabricate retrospective hours or dates.

## Reflection prompts
Explain in your own words: why use SQL placeholders; why salt a password;
how an image differs from a running container; what the CI log proves and what it does not.
You may use AI help, but describe that help and your own actions according to course rules.

## Primary references
https://docs.python.org/3/library/sqlite3.html
https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac
https://docs.python.org/3/library/hmac.html#hmac.compare_digest
https://docs.docker.com/build/concepts/dockerfile/
https://docs.github.com/en/actions/tutorials/build-and-test-code/python
