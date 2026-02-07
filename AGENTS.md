# Repository Guidelines

## Standard Task Workflow

For tasks of implementing new features:

- Read PRD.md, Plan.md, Progress.md before coding.
- Summarize current project state before implementation.
- Carry out the implementation; build and test if possible.
- Update Progress.md after changes.
- Commit with a clear, concise message.

For tasks of bug fixing:

- Summarize the bug, reason, and solution before implementation.
- Carry out the implementation to fix the bug; build and test afterwards.
- Update Progress.md after changes.
- Commit with a clear, concise message.

For tasks of reboot from a new Codex session:

- Read PRD.md, Plan.md, Progress.md.
- Assume this is a continuation of an existing project.
- Summarize your understanding of the current state and propose the next concrete step without writing code yet.

## Project Structure & Module Organization
The repository is organized around three top-level folders:
- `src/` for application code (currently minimal; keep new modules here).
- `script/` for build and test scripts.
- `doc/` for documentation. Current planning docs live in `doc/v1.0/` (e.g., `PRD.md`, `Plan.md`, `Progress.md`).

Place new files in the most relevant folder and keep module groupings flat unless complexity warrants subfolders.

## Build, Test, and Development Commands
- `script/build.sh`: Build the project artifacts. Use this after making code changes.
- `script/test.sh`: Run the test suite. Use this before committing.

Example:
```bash
script/build.sh
script/test.sh
```

## Coding Style & Naming Conventions
- Follow the language and framework conventions already used in `src/`.
- Keep filenames descriptive and lowercase with hyphens if needed (e.g., `card-parser.js`, `image_loader.py`).
- Prefer small, focused modules and avoid deep nesting.

## Testing Guidelines
- Add tests when behavior changes or new logic is introduced.
- Keep tests close to the code they cover (e.g., `src/feature_x/feature_x.test.*`) if a test framework is introduced.
- Use `script/test.sh` as the canonical test command and document any new test runners there.

## Standard Task Workflow
- For new features or bug fixes, read `doc/v1.0/PRD.md`, `doc/v1.0/Plan.md`, and `doc/v1.0/Progress.md` first.
- Summarize the current state before implementing changes.
- Build and test when possible.
- Update `doc/v1.0/Progress.md` after changes.

## Commit & Pull Request Guidelines
- Current history uses short, imperative messages (e.g., `Initial commit`). Continue this style.
- If adding scope, keep it brief (e.g., `feat: add detector stub`).
- PRs should include a short summary and testing notes (e.g., `Tests: script/test.sh`).

## Security & Configuration Tips
- Do not commit secrets or personal credentials.
- Keep any local configuration out of the repo unless explicitly required.
