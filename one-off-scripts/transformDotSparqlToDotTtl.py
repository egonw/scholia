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
        ttl_file.write(f"q:{fn} a sh:SPARQLExecutable,\n")

        # Read the content of the .sparql file
        with open(i, 'r') as sparql_file:
            sparql_content = sparql_file.read()

        # Check for keywords and write corresponding content
        if "SELECT" in sparql_content.upper():
            ttl_file.write("  sh:SPARQLSelectExecutable,\n")
            ttl_file.write("  sh:select '''\n")
        elif "CONSTRUCT" in sparql_content.upper():
            ttl_file.write("  sh:SPARQLConstructExecutable,\n")
            ttl_file.write("  sh:construct '''\n")
        elif "ASK" in sparql_content.upper():
            ttl_file.write("  sh:SPARQLAskExecutable,\n")
            ttl_file.write("  sh:ask '''\n")
        else:
            ttl_file.write("  spex:describe '''\n")

        # Append sparql content to the .ttl file
        ttl_file.write(sparql_content)
        ttl_file.write("'''.\n")

    # Output the ttl filename
    print(ttl)
