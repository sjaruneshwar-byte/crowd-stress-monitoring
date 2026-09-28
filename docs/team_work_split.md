# Team Work Allocation

## Member 1 — Frontend and dashboard
- Build the upload interface, monitoring cards, timeline visualization, and history table.
- Maintain `templates/index.html`, `static/style.css`, and `static/app.js`.
- Connect UI to `/api/analyze` and `/api/history`.
- Add frontend validation and responsive behavior.
- Submit feature branch `feature/dashboard` and a pull request.
- Provide dashboard screenshots and explain the UI in the viva.

## Member 2 — Detection and backend
- Maintain `detector.py` and collaborate on `app.py`.
- Explain and test HOG + SVM pedestrian detection.
- Evaluate detection quality on permitted test videos and document limitations.
- Validate uploads and API responses; add tests for detection behavior.
- Submit feature branch `feature/detection` and a pull request.
- Explain the algorithm and measured limitations in the viva.

## Member 3 — Database, integration, testing and documentation
- Maintain `database.py`, `tests/`, and `docs/`.
- Design the persistence model and test database behavior.
- Coordinate integration and regression testing.
- Maintain README, setup instructions, architecture diagram, issues and milestones.
- Submit feature branch `feature/integration` and a pull request.
- Coordinate GitHub screenshots, final demo, and merge-conflict exercise.

## Shared responsibilities
All members must:
- Clone and run the project locally.
- Make meaningful code commits under their own GitHub accounts.
- Review at least one teammate's pull request.
- Test the integrated `main` branch.
- Understand the complete system and the limits of the prototype.
