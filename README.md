# Nagpur Sustainable Planner

Nagpur Sustainable Planner is a Python-based web application built with Streamlit for interactive urban planning and sustainable city analysis. It combines map visualization, planning logic, and machine learning-based modules to help explore land use and development scenarios in a simple, easy-to-use interface.

---

## Table of Contents

- Overview
- Features
- Tech Stack
- Project Structure
- Installation
- How to Run Locally
- Deployment
- How the App Works
- Input / Output Flow
- Modules in the Project
- Common Errors and Fixes
- Future Improvements
- Contributing
- License
- Author

---

## Overview

This project is designed to support sustainable planning workflows through:
- interactive map-based visualization,
- modular planning logic,
- data loading and preprocessing,
- model-based predictions,
- and a Streamlit front end for easy usage.

It is structured as a lightweight research and prototype application that can be expanded into a more advanced urban decision-support system.

---

## Features

- Interactive web interface using Streamlit
- Map visualization using Folium
- Integration with `streamlit-folium`
- Modular code structure
- Data loading and preprocessing support
- Planning and land-use related logic
- Machine learning workflow support
- Easy deployment on Streamlit Community Cloud

---

## Tech Stack

- Python
- Streamlit
- Folium
- streamlit-folium
- Pandas
- NumPy
- scikit-learn

---

## Project Structure

```bash
nagpur-sustainable-planner/
│
├── app.py
├── data_loader.py
├── map_generator.py
├── planner_logic.py
├── ml_model.py
├── ml_landuse.py
├── ml_infrastructure.py
├── train_models.py
│
├── components/
├── data/
├── models/
├── utils/
│
├── requirements.txt
├── packages.txt
├── README.md
└── LICENSE
