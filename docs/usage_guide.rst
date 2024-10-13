Usage Guide
===========

🌍 Project Overview
-------------------

**Moroccan Real Estate** is a data engineering project that integrates **Apache Airflow**, **Apache Spark**, and **Google Cloud Storage (GCS)** to handle and process datasets from the moroccan real estate market. We use automated workflows to scrape real estate data, transform it, and store it for further analysis.

---

🗂️ Project Folder Structure
---------------------------

The project is organized into the following folders:

.. code-block:: text

    MOROCCAN-REAL-ESTATE/
    │
    ├── src/                                     # Source code folder
    │   ├── dags/                                # 🚀 Airflow DAGs (workflow definitions)
    │   ├── jobs/                                # ⚡ Spark jobs
    │   ├── scraping/                            # 🕷️ Web scraping scripts
    │   └── modelling/                           # 🤖 Modelling scripts (machine learning, data science)
    │
    ├── terraform/                               # 🌍 Terraform configurations
    │
    ├── notebooks/                               # 📒 Jupyter notebooks for analysis and exploration
    │
    ├── noxfile.py                               # 🛠️ Nox sessions definition (for automation)
    │
    ├── project.toml                             # 📦 Project configuration
    │
    ├── tests/                                   # 🧪 Unit, Integration, and E2E tests
    │   ├── unit/                                # Unit tests
    │   ├── integration/                         # Integration tests
    │   └── e2e/                                 # End-to-end tests
    │
    ├── data/                                    # 📊 Local data storage (for small sample datasets)
    │
    ├── docs/                                    # 📚 Documentation (Sphinx-generated)
    │   ├── conf.py                              # Sphinx configuration
    │   └── index.rst                            # Main documentation page
    │
    └── README.md                                # 📖 Project documentation



---

⚙️ Automated CI and Documentation Building
------------------------------------------

We use **Nox** to automate various development tasks such as linting, formatting, type checking, testing, and building the documentation.

📦 How to Run Nox Sessions
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use Nox to streamline your development workflow by running sessions for common tasks.

1. **To run all predefined sessions** (lint, formatting, typing, test):

   .. code-block:: bash

      nox

2. **To run a specific session**, use the following command format:

   .. code-block:: bash

      nox -s <session_name>

   For example, to run the linting session only:

   .. code-block:: bash

      nox -s lint

🚀 Available Nox Sessions
~~~~~~~~~~~~~~~~~~~~~~~~~

- **lint**: Runs Ruff to check for linting issues.
- **formatting**: Runs Black and Isort to check code formatting.
   - **run**: Use this session to apply code formatting changes.
- **typing**: Runs MyPy for static type checking.
- **dev**: Sets up a development environment.
   - **windows**: Specify this option when working on Windows.
- **doc**: Builds documentation using Sphinx.
   - **i**: Build interactive documentation using Sphinx.
- **test**: Runs the test suite with Pytest and coverage.

💡 Running Nox Sessions with Arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To pass additional arguments to a session (e.g., specifying OS for the dev session):

.. code-block:: bash

   nox -s dev -- windows

(Example for running the `dev` session on Windows).
