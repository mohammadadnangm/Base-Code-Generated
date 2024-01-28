import pandas as pd
import numpy as np
import random
import math
import ast

# Assuming the vehicle_data DataFrame is already loaded
vehicle_data = pd.read_csv('vehicle_data.csv')

# Get a list of unique cell IDs
unique_cell_ids = vehicle_data['cell_id'].unique()

# Select a random cell ID
random_cell_id = random.choice(unique_cell_ids)





# Storing in Blockchain
# Start
transaction_protocol = TA.initiate_transaction_protocol()

# While check
while transaction_protocol.has_transactions_to_check():
    # Format of the transaction
    transaction_format_is_valid = transaction_protocol.check_transaction_format()
    
    # History of the transaction
    transaction_history_is_valid = transaction_protocol.check_transaction_history()
    
    if transaction_format_is_valid and transaction_history_is_valid:
        # If(Endorsing policy is true)
        if transaction_protocol.endorsing_policy_is_true():
            # Submit and update ledger
            transaction_protocol.submit_and_update_ledger()
            
            # Create blocks→ Send message to TA
            blocks = transaction_protocol.create_blocks()
            TA.receive_message(blocks)
            
            # Group Leader updates the ledger
            group_leader.update_ledger()
        else:
            # Do not update the ledger
            pass
    else:
        # Drop the transaction
        transaction_protocol.drop_transaction()

# End

