import nbformat as nbf
import argparse
from termcolor import colored

# +
# Flag if the notebook is corrupt
META_CORRUPT = False

# Cell output to tell the learners if the metadata is intact
WARNING = colored("**IMPORTANT: Missing grader metadata detected! It has now been added. Please close this notebook WITHOUT SAVING and re-open it from the classroom. If you see a pop-up asking to 'Reload' or 'Overwrite', please select 'Reload'.**", 'red')
SAFE = colored("Grader metadata detected! You can proceed with the lab!", 'green')

# String to search for in the cell 'tags' metadata
TAG = "graded"

# Strings in the cell indicating that a cell can be edited
EDITABLE_IDENTIFIERS = {"# START CODE HERE", "# You can change"}

# key to search for in the cell metadata 
DELETABLE_META = "deletable"

# Strings in the cell indicating that the cell is required by the grader
REQUIRED_IDENTIFIERS = ["Graded Cell", "# START CODE HERE", "grader-required-cell", "writefile"]
# -

parser = argparse.ArgumentParser(description='get filename')
parser.add_argument('--filename',
                    help='filename of the notebook to check')
args = parser.parse_args()

ntbk = nbf.read(f'./{args.filename}', nbf.NO_CONVERT)

for cell in ntbk.cells:
    
    # The loop will only check code cells
    if cell.cell_type == 'code':
        
        required_identifier_found =  any(required_check in cell.source for required_check in REQUIRED_IDENTIFIERS)
        
        # Only check the metadata if the cell is required by the grader
        if required_identifier_found:
            
            cell.metadata['tags'] = cell.get('metadata', {}).get('tags', [])

            if TAG not in cell.metadata.tags:
                
                # Flag notebook as corrupt and back up to a different file
                META_CORRUPT = True
                nbf.write(ntbk, f'corrupt_{args.filename}') if META_CORRUPT else None
                
                cell.metadata.tags.append(TAG)
        

            # Required cells should not be deletable. Add that metadata if it's missing.
            if DELETABLE_META not in cell.metadata:

                META_CORRUPT = True
                nbf.write(ntbk, f'corrupt_{args.filename}') if META_CORRUPT else None

                cell.metadata['deletable'] = False

                # Mark if cell should be editable (e.g. blank exercise)
                cell_editable = any(editable_check in cell.source for editable_check in EDITABLE_IDENTIFIERS)
                
                if not cell_editable:
                    cell.metadata['editable'] = False

# Save the new metadata into the current notebook if current version is corrupt
if META_CORRUPT:
    nbf.write(ntbk, f'{args.filename}')
    print(WARNING)

else:
    print(SAFE)
