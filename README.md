# NyayaLens — Indian Court Document Analysis Application

AI-powered Indian court document intelligence and analysis platform.

## Modules

### PDF Upload, Validation, and Text Extraction (`nyayalens/`)
The standalone PDF processing module responsible for file validation, PyMuPDF-based text extraction, scanned PDF/OCR detection, and standard output contract generation.

- **Service Module**: [`nyayalens/services/pdf_service.py`](file:///nyayalens/services/pdf_service.py)
- **Validators**: [`nyayalens/utils/validators.py`](file:///nyayalens/utils/validators.py)
- **Automated Tests**: [`nyayalens/tests/test_pdf.py`](file:///nyayalens/tests/test_pdf.py)
- **Documentation**: Refer to [`nyayalens/README.md`](file:///nyayalens/README.md) for full module specifications, contract schema, and integration examples.

### Quick Start & Tests

```bash
# Install dependencies
pip install -r nyayalens/requirements.txt

# Run automated tests
pytest nyayalens/tests/test_pdf.py -v
```
