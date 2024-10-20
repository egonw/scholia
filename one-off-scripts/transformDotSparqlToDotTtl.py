import os
import glob

# Path to sparql files
sparql_files_path = '../scholia/app/templates/*sparql'

# Get the list of .sparql files
sparql_files = glob.glob(sparql_files_path)

# Process each sparql file
for i in sparql_files:
    # Extract the filename (fn) and create .ttl filename
    fn = os.path.basename(i)[0:-7]  # extract name without extension
    ttl = i[0:-7] + ".ttl"  # create .ttl filename

    # Open .ttl file to write
    with open(ttl, 'w') as ttl_file:
        ttl_file.write("""@prefix q: <https://github.com/WDScholia/scholia/scholia/app/templates/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <https://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
""")
        ttl_file.write(f"q:{fn} a sh:SPARQLExecutable,\n")

        # Read the content of the .sparql file
        with open(i, 'r') as sparql_file:
            sparql_content = sparql_file.read()

        # Check for keywords and write corresponding content
        if "SELECT" in sparql_content.upper():
            ttl_file.write("  sh:SPARQLSelectExecutable;\n")
            ttl_file.write("  sh:select '''")
        elif "CONSTRUCT" in sparql_content.upper():
            ttl_file.write("  sh:SPARQLConstructExecutable;\n")
            ttl_file.write("  sh:construct '''")
        elif "ASK" in sparql_content.upper():
            ttl_file.write("  sh:SPARQLAskExecutable ;\n")
            ttl_file.write("  sh:ask '''")
        else:
            ttl_file.write("  spex:SPARQLDescribeExecutable ;\n")
            ttl_file.write("  spex:describe '''")

        # Append sparql content to the .ttl file
        ttl_file.write(sparql_content)
        ttl_file.write("''';\n")

        # Find a title
        lines = sparql_content.splitlines()
        for line in lines:
            if line.startswith("# title:"):
                ttl_file.write("  dcterms:title \"" + line[8:].strip() + "\" ;\n")

        # Add the license
        ttl_file.write("  dcterms:license <https://www.gnu.org/licenses/gpl-3.0> .\n")

    # Output the ttl filename
    print(ttl)
