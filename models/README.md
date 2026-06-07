# Models Directory

This directory documents model artifacts and their lifecycle.

Current artifact:

- `pipeline_itsm.joblib`: scikit-learn pipeline used by the Streamlit app for category and priority prediction.

Recommended practices:

- regenerate the artifact after training logic changes;
- document the training dataset assumptions;
- avoid storing sensitive or customer-derived embeddings or model inputs.
