import pymupdf


def extract_tables_from_pdf(filepath: str, output_file: str):
    doc = pymupdf.open(filepath)
    with open(output_file, "wb") as out:
        for page in doc:
            tf = page.find_tables(strategy="lines")
            if tf:
                for table in tf.tables:
                    pd_table = table.to_pandas()
                    out.write(pd_table.to_csv(index=False).encode("utf-8"))
                    out.write("\n\n".encode("utf-8"))
