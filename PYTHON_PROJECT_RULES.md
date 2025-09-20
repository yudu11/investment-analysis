# 📌 Python Project Structure Rules

## 🎯 Purpose  
This document defines the folder structure and coding rules for all Python projects in this repository.  
All contributors (including AI coding assistants) must follow these rules.  

---

## 📂 Folder Structure  

```
project_root/
│
├── src/                        # Main application code
│   └── package_name/           # Replace with project package/module name
│       ├── __init__.py
│       ├── main.py             # Entry point (if CLI/app)
│       ├── config/             # Configuration files / settings
│       ├── models/             # Data models (ORM, Pydantic, dataclasses)
│       ├── services/           # Business logic / service layer
│       ├── controllers/        # API routes / request handlers
│       ├── utils/              # Reusable utilities/helpers
│
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── conftest.py             # pytest fixtures
│
├── scripts/                    # CLI tools / one-off scripts
├── docs/                       # Documentation
│
├── .env.example                # Example env variables
├── requirements.txt            # Dependencies
├── pyproject.toml / setup.cfg  # Build/config
├── README.md                   # Overview
├── .gitignore
└── PYTHON_PROJECT_RULES.md     # This file
```

---

## ✅ Rules  

### General  
- All source code goes under `src/`.  
- Use a single top-level package name inside `src/`.  
- Do not place application code in the root.  
- Tests must mirror the `src/` structure.  

### Naming Conventions  
- **snake_case** → files, functions.  
- **PascalCase** → classes.  
- **UPPER_CASE** → constants.  
- **lowercase** → package/module names.  

### Separation of Concerns  
- `models/` → data structures (ORM entities, DTOs, Pydantic models).  
- `services/` → business logic.  
- `controllers/` → API routes, CLI handlers.  
- `utils/` → helpers, stateless utilities.  

### Config & Environment  
- All env vars loaded via `src/config/`.  
- Always provide `.env.example`.  
- Never commit real secrets.  

### Testing  
- Use **pytest**.  
- New code must include tests.  
- Minimum coverage: **80%**.  
- Mirror `src/` folder structure under `tests/`.  

### Documentation  
- Update `README.md` with new features.  
- Use module docstrings (PEP 257).  
- Comment complex logic.  

---

## 🚫 Forbidden  
- Hardcoding secrets.  
- Tests inside `src/`.  
- Circular imports.  
- Mixing responsibilities (e.g., DB logic in controllers).  

---

## 🧩 Deliverables  
Whenever new code is generated or modified:  
1. Place files in correct folder.  
2. Add/update tests.  
3. Update documentation.  
4. Ensure imports are **relative inside `src/`**.  

---

⚡ **Reminder:** Validate compliance before committing or opening a Pull Request.  
